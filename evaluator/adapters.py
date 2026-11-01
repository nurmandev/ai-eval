import json
import os
import urllib.error
import urllib.request

MAX_RESPONSE_BYTES = 2_000_000


class ProviderError(RuntimeError):
    pass


def _post_json(url, headers, payload, timeout):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise ProviderError("Provider response exceeded the 2 MB safety cap")
            data = json.loads(body.decode("utf-8"))
            return data
    except urllib.error.HTTPError as error:
        detail = error.read(4096).decode("utf-8", errors="replace")
        raise ProviderError(f"Provider returned HTTP {error.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise ProviderError(f"Provider request failed: {error}") from None


def generate(model, prompt, timeout=120):
    provider = model.get("provider")
    model_id = model.get("model_id")
    if not model_id:
        raise ProviderError("Model configuration requires a non-empty model_id")

    if provider == "openai":
        key = os.environ.get(model.get("api_key_env", "OPENAI_API_KEY"))
        if not key:
            raise ProviderError("Missing API credential for configured OpenAI model")
        payload = {
            "model": model_id,
            "input": prompt,
            "max_output_tokens": model.get("max_output_tokens", 8192),
        }
        if model.get("temperature", 0) is not None:
            payload["temperature"] = model.get("temperature", 0)
        data = _post_json(
            model.get("base_url", "https://api.openai.com/v1/responses"),
            {"Authorization": "Bearer " + key},
            payload,
            timeout,
        )
        text = "".join(
            item.get("text", "")
            for output in data.get("output", [])
            for item in output.get("content", [])
            if item.get("type") == "output_text"
        )
        return text, data.get("id"), data.get("usage")

    if provider == "anthropic":
        key = os.environ.get(model.get("api_key_env", "ANTHROPIC_API_KEY"))
        if not key:
            raise ProviderError("Missing API credential for configured Anthropic model")
        payload = {
            "model": model_id,
            "max_tokens": model.get("max_output_tokens", 8192),
            "messages": [{"role": "user", "content": prompt}],
        }
        if model.get("temperature", 0) is not None:
            payload["temperature"] = model.get("temperature", 0)
        data = _post_json(
            model.get("base_url", "https://api.anthropic.com/v1/messages"),
            {"x-api-key": key, "anthropic-version": "2023-06-01"},
            payload,
            timeout,
        )
        text = "".join(
            item.get("text", "") for item in data.get("content", []) if item.get("type") == "text"
        )
        return text, data.get("id"), data.get("usage")

    if provider == "google":
        key = os.environ.get(model.get("api_key_env", "GOOGLE_API_KEY"))
        if not key:
            raise ProviderError("Missing API credential for configured Google model")
        endpoint = model.get(
            "base_url",
            f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent",
        )
        generation_config = {
            "maxOutputTokens": model.get("max_output_tokens", 8192),
        }
        if model.get("temperature", 0) is not None:
            generation_config["temperature"] = model.get("temperature", 0)
        data = _post_json(
            endpoint,
            {"x-goog-api-key": key},
            {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": generation_config,
            },
            timeout,
        )
        candidates = data.get("candidates", [])
        text = "".join(
            part.get("text", "")
            for candidate in candidates
            for part in candidate.get("content", {}).get("parts", [])
        )
        return text, data.get("responseId"), data.get("usageMetadata")

    raise ProviderError(f"Unsupported provider: {provider!r}")
