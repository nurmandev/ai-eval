# Model Configuration

Edit [model-config.json](model-config.json) with exact model IDs that are currently available from the chosen provider. The checked-in configuration is intentionally empty; no model names or run results are fabricated.

Supported providers are `openai`, `anthropic`, and `google`, using the corresponding environment variable names in the root `.env.example`. The adapters use official provider HTTPS APIs and Python's standard library. If a provider changes its API, update and test its adapter before running an experiment.

Each entry requires a unique filesystem-safe `name`, provider, exact `model_id`, and may set `temperature`, `max_output_tokens`, `api_key_env`, or a provider-specific `base_url`. Use `temperature: null` if the chosen model/API does not accept a temperature parameter. Keep keys out of this JSON file.

Before a benchmark run, verify the model ID, model snapshot/date, allowed generation settings, provider terms, and current pricing manually; record evidence in run metadata. A missing credential is an explicit setup error, not a model score.
