PYTHON ?= python3

.PHONY: setup validate test pilot evaluate report package clean

setup:
	$(PYTHON) --version
	java -version
	javac -version
	@command -v bwrap >/dev/null || (echo "bubblewrap (bwrap) is required for isolated generated-code execution" >&2; exit 1)
	@echo "No third-party Python packages are required."

validate:
	$(PYTHON) evaluator/main.py validate

test:
	$(PYTHON) -m unittest discover -s validation/reference-validation -v
	cd evaluator && $(PYTHON) -m unittest -v

pilot:
	$(PYTHON) evaluator/main.py evaluate --runs 1

evaluate:
	$(PYTHON) evaluator/main.py evaluate

report:
	$(PYTHON) evaluator/main.py report

package: report
	bash scripts/package-submission.sh

clean:
	find . -type f \( -name '*.class' -o -name '*.pyc' \) -delete
