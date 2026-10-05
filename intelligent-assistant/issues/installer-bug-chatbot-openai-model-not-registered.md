# AAP 2.7 Installer Bug: Inference Model Not Registered for non-RHOAI Providers

## Summary

The AAP 2.7 containerized installer fails to register the inference model in the llama-stack configuration when `lightspeed_chatbot_default_provider` is set to `openai` or `azure`. Only the `rhoai` provider gets a model registered. This causes the chatbot to return "Model not found" errors on every query, despite all containers running and the gateway reporting the Lightspeed service as healthy.

## Affected Version

- AAP containerized installer bundle 2.7-8
- `ansible.containerized_installer` collection shipped with the above

## Symptoms

- The chat bubble appears in the AAP UI (may require a hard browser refresh after initial install).
- The Lightspeed gateway status shows `status: good`.
- All four Lightspeed containers are running (`ansible-lightspeed`, `ansible-lightspeed-chatbot`, `ansible-lightspeed-mcp-controller`, `ansible-lightspeed-mcp-lightspeed`).
- The chatbot returns no answers. The RAG search API returns:
  ```json
  {
    "response": "Model not found",
    "cause": "Model with ID <model_id> does not exist"
  }
  ```
- The chatbot container logs show `404` responses on `/v1/query` and `/v1/streaming_query` endpoints.
- Container environment variables (`INFERENCE_MODEL`, `OPENAI_BASE_URL`, `OPENAI_API_KEY`) are all correctly set.

## Root Cause

The installer role template at:

```
roles/ansiblelightspeed/templates/ansible-chatbot-run.yaml.j2
```

wraps the inference model registration in a `rhoai`-only conditional:

```jinja2
registered_resources:
  models:
{% if lightspeed_chatbot_default_provider == "rhoai" %}
    - metadata: {}
      model_id: {{ lightspeed_chatbot_default_provider }}/${env.INFERENCE_MODEL}
      provider_id: {{ lightspeed_chatbot_default_provider }}
      provider_model_id: null
{% endif %}
    - metadata:
        embedding_dimension: 768
      model_id: sentence-transformers/all-mpnet-base-v2
      ...
```

When `lightspeed_chatbot_default_provider` is `openai` or `azure`, the inference model entry is completely skipped. The llama-stack configuration contains only the embedding model, and all inference requests fail with "Model not found".

## Expected Behavior

The template should register the inference model for all supported providers. The `rhoai`-only conditional should be removed. For the `openai` and `azure` providers, `provider_model_id` should be explicitly set (the `null` fallback only works for `rhoai` because its provider does not validate models against an API endpoint list):

```jinja2
registered_resources:
  models:
    - metadata: {}
      model_id: {{ lightspeed_chatbot_default_provider }}/${env.INFERENCE_MODEL}
      provider_id: {{ lightspeed_chatbot_default_provider }}
{% if lightspeed_chatbot_default_provider == "rhoai" %}
      provider_model_id: null
{% else %}
      provider_model_id: ${env.INFERENCE_MODEL}
{% endif %}
      model_type: llm
    - metadata:
        embedding_dimension: 768
      model_id: sentence-transformers/all-mpnet-base-v2
      ...
```

Note: The `openai` provider type (`remote::openai`) validates the model against the provider's `/models` endpoint during startup. When `provider_model_id` is `null`, llama-stack falls back to using `model_id` (which includes the provider prefix, e.g. `openai/gpt-4o`) for validation, causing a mismatch against the API's model list (which returns just `gpt-4o`). Setting `provider_model_id` explicitly avoids this.

## Workaround

**Step 1** — Back up the original config:

```bash
cp <lightspeed_data_dir>/etc/chatbot/ansible-chatbot-run.yaml ~/ansible-chatbot-run.yaml.backup
```

**Step 2** — Edit the bind-mounted config file on the AAP host:

```
<lightspeed_data_dir>/etc/chatbot/ansible-chatbot-run.yaml
```

Add the inference model entry under `registered_resources.models`, **before** the existing embedding model entry:

```yaml
registered_resources:
  models:
    - metadata: {}
      model_id: openai/${env.INFERENCE_MODEL}
      provider_id: openai
      provider_model_id: ${env.INFERENCE_MODEL}
      model_type: llm
    - metadata:
        embedding_dimension: 768
      model_id: sentence-transformers/all-mpnet-base-v2
      ...
```

Replace `openai` with `azure` if using the Azure provider.

The `provider_model_id` must match the model ID as returned by your LLM provider's `/models` endpoint. For standard OpenAI and Azure endpoints, this is the bare model name (e.g. `gpt-4o`). For non-standard endpoints (e.g. Google Gemini), see the separate Gemini compatibility document.

**Step 3** — Restart the chatbot:

```bash
systemctl --user restart ansible-lightspeed-chatbot.service
```

**Do not re-run the installer** after applying the workaround — the buggy template will overwrite the fix.

## Diagnosis Path

1. Gateway status API (`/api/gateway/v1/status/`) shows Lightspeed as healthy — this is misleading; the gateway only checks service registration, not model availability.
2. Chatbot container logs show `404` on `/v1/query` and `/v1/streaming_query` — these are the symptom.
3. Container environment variables are all correctly set — the installer handles those properly regardless of provider.
4. The llama-stack config (`ansible-chatbot-run.yaml`) under `registered_resources.models` lists only the embedding model — this is the root cause.
5. The installer template (`ansible-chatbot-run.yaml.j2`) wraps the inference model registration in a `rhoai`-only conditional — this is the bug.
