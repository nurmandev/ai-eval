import json
import os
import resource
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path


class SandboxUnavailable(RuntimeError):
    pass


def extract_java_source(response):
    marker = "```"
    if marker not in response:
        return response.strip()
    blocks = response.split(marker)
    for block in blocks[1::2]:
        first_newline = block.find("\n")
        if first_newline < 0:
            continue
        language = block[:first_newline].strip().lower()
        if language in ("java", ""):
            return block[first_newline + 1 :].strip()
    raise ValueError("No Java source block found in model response")


def _limits(cpu_soft=4, cpu_hard=5, file_size_limit=64 * 1024 * 1024):
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_soft, cpu_hard))
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_size_limit, file_size_limit))
    resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))


def _sandbox_prefix():
    bwrap = shutil.which("bwrap")
    if not bwrap:
        raise SandboxUnavailable(
            "bubblewrap (bwrap) is required to run generated code with network disabled"
        )
    command = [
        bwrap,
        "--die-with-parent",
        "--unshare-net",
        "--unshare-pid",
        "--ro-bind",
        "/usr",
        "/usr",
    ]
    for path in ("/lib", "/lib64", "/etc"):
        if Path(path).exists():
            command.extend(["--ro-bind", path, path])
    command.extend(
        [
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--tmpfs",
            "/tmp",
        ]
    )
    return command


def _sandbox_command(classes_dir, java, measure_path):
    time_tool = shutil.which("time")
    command = _sandbox_prefix()
    command.extend(
        [
            "--ro-bind", str(classes_dir), "/classes",
            "--bind", str(measure_path), "/measurement",
            "--dir",
            "/work",
            "--chdir",
            "/work",
            "--",
        ]
    )
    if time_tool:
        command.extend([time_tool, "-f", "%M", "-o", "/measurement", "--"])
    command.extend(
        [
            java,
            "-Xms16m",
            "-Xmx128m",
            "-XX:MaxDirectMemorySize=16m",
            "-XX:ReservedCodeCacheSize=32m",
            "-XX:CompressedClassSpaceSize=32m",
            "-XX:ActiveProcessorCount=1",
            "-cp",
            "/classes",
            "Main",
        ]
    )
    return command


def run_java(source, test_cases, java="java", javac="javac", timeout_seconds=5):
    if os.name != "posix":
        raise SandboxUnavailable("The current Java sandbox is supported on POSIX systems only")

    results = []
    with tempfile.TemporaryDirectory(prefix="ai-eval-java-") as directory:
        root = Path(directory)
        if len(source.encode("utf-8")) > 256_000:
            return {
                "compiled": False,
                "compile_stderr": "Java source exceeded the 256 KB safety cap",
                "tests": [],
                "passed_weight": 0,
            }
        source_dir = root / "source"
        classes_dir = root / "classes"
        source_dir.mkdir()
        classes_dir.mkdir()
        source_file = source_dir / "Main.java"
        source_file.write_text(source, encoding="utf-8")
        compile_stdout_path = root / "compile.out"
        compile_stderr_path = root / "compile.err"
        compile_command = _sandbox_prefix()
        compile_command.extend(
            [
                "--ro-bind",
                str(source_dir),
                "/source",
                "--bind",
                str(classes_dir),
                "/classes",
                "--dir",
                "/work",
                "--chdir",
                "/work",
                "--",
                javac,
                "-J-Xmx256m",
                "-J-XX:ActiveProcessorCount=1",
                "--release",
                "17",
                "-encoding",
                "UTF-8",
                "-proc:none",
                "-classpath",
                "",
                "-d",
                "/classes",
                "/source/Main.java",
            ]
        )
        try:
            with compile_stdout_path.open("wb") as compile_stdout, compile_stderr_path.open(
                "wb"
            ) as compile_stderr:
                compiler = subprocess.Popen(
                    compile_command,
                    stdin=subprocess.DEVNULL,
                    stdout=compile_stdout,
                    stderr=compile_stderr,
                    preexec_fn=lambda: _limits(12, 13),
                    start_new_session=True,
                    env={
                        "PATH": "/usr/bin:/bin",
                        "HOME": "/tmp",
                        "LANG": "C.UTF-8",
                        "LC_ALL": "C.UTF-8",
                    },
                )
                try:
                    compile_exit_code = compiler.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    os.killpg(compiler.pid, signal.SIGKILL)
                    compiler.wait()
                    compile_exit_code = -signal.SIGKILL
        except OSError as error:
            return {
                "compiled": False,
                "compile_stderr": f"Compiler sandbox error: {error}",
                "tests": [],
                "passed_weight": 0,
            }
        compile_error_text = compile_stderr_path.read_text(
            encoding="utf-8", errors="replace"
        )[-8000:]
        if compile_exit_code != 0:
            if compile_exit_code == -signal.SIGKILL:
                compile_error_text = "Compilation timed out or exceeded its CPU limit"
            return {
                "compiled": False,
                "compile_stderr": compile_error_text,
                "tests": [],
                "passed_weight": 0,
            }

        for case in test_cases:
            if len(case["input"].encode("utf-8")) > 64 * 1024 * 1024:
                raise ValueError(f"Input for test {case['id']} exceeds the 64 MB safety cap")
            input_path = root / f"{case['id']}.in"
            output_path = root / f"{case['id']}.out"
            error_path = root / f"{case['id']}.err"
            usage_path = root / f"{case['id']}.usage"
            input_path.write_text(case["input"], encoding="utf-8")
            usage_path.touch()
            command = _sandbox_command(classes_dir, java, usage_path)
            started = time.monotonic()
            status = "runtime_error"
            actual = ""
            stderr = ""
            exit_code = None
            peak_rss_kb = None
            try:
                with (
                    input_path.open("rb") as stdin,
                    output_path.open("wb") as stdout,
                    error_path.open("wb") as stderr_file,
                ):
                    process = subprocess.Popen(
                        command,
                        stdin=stdin,
                        stdout=stdout,
                        stderr=stderr_file,
                        preexec_fn=_limits,
                        start_new_session=True,
                        env={
                            "PATH": "/usr/bin:/bin",
                            "HOME": "/tmp",
                            "LANG": "C.UTF-8",
                            "LC_ALL": "C.UTF-8",
                        },
                    )
                    try:
                        exit_code = process.wait(timeout=timeout_seconds)
                        status = "completed" if exit_code == 0 else "runtime_error"
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                        status = "timeout"
                actual = output_path.read_text(encoding="utf-8", errors="replace")
                stderr = error_path.read_text(encoding="utf-8", errors="replace")[-4000:]
                if usage_path.exists():
                    try:
                        peak_rss_kb = int(usage_path.read_text(encoding="ascii").strip())
                    except ValueError:
                        peak_rss_kb = None
                if status == "completed":
                    normalized_actual = "\n".join(line.rstrip() for line in actual.splitlines()).strip()
                    normalized_expected = "\n".join(
                        line.rstrip() for line in case["expected_output"].splitlines()
                    ).strip()
                    status = "passed" if normalized_actual == normalized_expected else "wrong_answer"
            except OSError as error:
                status = "sandbox_error"
                stderr = str(error)

            results.append(
                {
                    "test_id": case["id"],
                    "category": case["category"],
                    "status": status,
                    "weight": case["weight"],
                    "actual_output": actual[:4000],
                    "stderr": stderr,
                    "exit_code": exit_code,
                    "execution_time_ms": round((time.monotonic() - started) * 1000, 3),
                    "peak_rss_kb": peak_rss_kb,
                }
            )

    passed_weight = sum(case["weight"] for case in results if case["status"] == "passed")
    return {
        "compiled": True,
        "compile_stderr": compile_error_text,
        "tests": results,
        "passed_weight": passed_weight,
    }


def load_test_cases(path):
    manifest_path = Path(path)
    cases = json.loads(manifest_path.read_text(encoding="utf-8"))
    for case in cases:
        generator = case.pop("generator", None)
        if generator:
            kind = generator.get("kind")
            if kind == "alternating":
                n = int(generator["n"])
                if n < 1 or n > 200_000 or n % 2:
                    raise ValueError("alternating stress generator requires even N in [2, 200000]")
                values = [generator["positive"], generator["negative"]] * (n // 2)
                case["input"] = (
                    f"{n} {generator['k']}\n"
                    + " ".join(map(str, values))
                    + "\n"
                )
            elif kind == "idempotency_unique_max":
                account_count = request_count = 200_000
                input_lines = [
                    f"{account_count} {request_count} 1000000000000000000",
                    "a0 1000000000000000",
                    *(f"a{i} 0" for i in range(1, account_count)),
                    *(
                        f"{i} c k{i} a0 a1 1"
                        for i in range(request_count)
                    ),
                ]
                output_lines = ["SUCCESS"] * request_count + [""]
                output_lines.extend(
                    (
                        f"a0 {1_000_000_000_000_000 - request_count}",
                        f"a1 {request_count}",
                        *(f"a{i} 0" for i in range(2, account_count)),
                    )
                )
                case["input"] = "\n".join(input_lines) + "\n"
                case["expected_output"] = "\n".join(output_lines) + "\n"
            elif kind == "idempotency_reuse_max":
                request_count = 200_000
                input_lines = [
                    f"2 {request_count} 1",
                    f"a {request_count}",
                    "b 0",
                    *(
                        f"{i // 2} c repeated a b 1"
                        for i in range(request_count)
                    ),
                ]
                output_lines = [
                    "SUCCESS" if i % 2 == 0 else "REPLAY_SUCCESS"
                    for i in range(request_count)
                ]
                output_lines.extend(["", f"a {request_count // 2}", f"b {request_count // 2}"])
                case["input"] = "\n".join(input_lines) + "\n"
                case["expected_output"] = "\n".join(output_lines) + "\n"
            else:
                raise ValueError(f"Unsupported input generator: {kind}")
        base_dir = manifest_path.parent
        if "input_file" in case:
            case["input"] = (base_dir / case.pop("input_file")).read_text(encoding="utf-8")
        if "expected_output_file" in case:
            case["expected_output"] = (
                (base_dir / case.pop("expected_output_file")).read_text(encoding="utf-8")
            )
    if not cases or sum(case["weight"] for case in cases) != 100:
        raise ValueError("Test case weights must be nonempty and sum to 100")
    required = {"id", "category", "input", "expected_output", "weight"}
    for case in cases:
        if not required.issubset(case):
            raise ValueError(f"Malformed test case: {case}")
    return cases
