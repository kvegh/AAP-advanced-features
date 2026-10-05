# Gemini API Compatibility: Model ID Prefix Mismatch with llama-stack

## Summary

When using Google Gemini as the LLM backend for the AAP Intelligent Assistant via the OpenAI-compatible endpoint, a model ID naming mismatch prevents the chatbot from finding the registered inference model. This is a Gemini-specific issue on top of the general installer bug documented in `installer-bug-chatbot-openai-model-not-registered.md` — fixing the installer bug alone is not sufficient for Gemini.

## Affected Configuration

- `lightspeed_chatbot_default_provider=openai`
- `lightspeed_chatbot_model_url=https://generativelanguage.googleapis.com/v1beta/openai/`
- Any Gemini model (e.g. `gemini-3.7-flash`, `gemini-2.5-pro`)

Standard OpenAI or Azure endpoints are **not affected** by this issue.

## Symptoms

After applying the workaround for the installer model registration bug, one of:

- **Startup failure**: The chatbot container crashes with:
  ```
  ValueError: Model <model_name> is not available from provider openai
  ```
  This occurs when `provider_model_id` does not match any ID in the Gemini API's `/models` list.

- **Model not found at query time**: The chatbot starts successfully, but queries return:
  ```json
  {
    "response": "Model not found",
    "cause": "Model with ID <model_name> does not exist"
  }
  ```
  This occurs when the `model_id` in the llama-stack config does not match the identifier that the lightspeed-core constructs when sending queries.

## Root Cause

Two interacting issues:

### 1. Gemini's `/models` endpoint returns IDs with a `models/` prefix

Standard OpenAI-compatible endpoints return model IDs like `gpt-4o`. The Gemini API returns them as `models/gemini-3.7-flash`:

```bash
curl -s "$OPENAI_BASE_URL/models" -H "Authorization: Bearer $API_KEY" | python3 -c "
import json, sys
for m in json.load(sys.stdin)['data']:
    print(m['id'])
"
# Output: models/gemini-3.7-flash, models/gemini-2.5-pro, ...
```

llama-stack's OpenAI provider validates models against this list during startup. If `provider_model_id` doesn't match an entry in the list, registration fails.

### 2. llama-stack constructs model identifiers from `provider_id/provider_model_id`

When registering a model with `provider_model_id: models/gemini-3.7-flash`, llama-stack constructs the internal identifier as `openai/models/gemini-3.7-flash`.

Meanwhile, the lightspeed-core (the `ansible-lightspeed` container) sends queries with `model: gemini-3.7-flash` and `provider: openai`. The chatbot constructs `openai/gemini-3.7-flash` for lookup — which does not match `openai/models/gemini-3.7-flash`.

### The mismatch chain

| Component | Model ID used | Source |
|---|---|---|
| Gemini API `/models` endpoint | `models/gemini-3.7-flash` | Gemini convention |
| llama-stack registered identifier | `openai/models/gemini-3.7-flash` | `provider_id` + `/` + `provider_model_id` |
| Lightspeed-core query request | `openai/gemini-3.7-flash` | `CHATBOT_DEFAULT_PROVIDER` + `/` + `lightspeed_chatbot_model_id` |

The lightspeed-core and llama-stack disagree on the model identifier because of the extra `models/` segment.

## Workaround

Two files need to be modified. Back up both originals first.

### Step 1 — Fix the chatbot llama-stack config

Edit `<lightspeed_data_dir>/etc/chatbot/ansible-chatbot-run.yaml`.

Add the inference model entry under `registered_resources.models` with the `models/` prefix in **both** `model_id` and `provider_model_id`:

```yaml
registered_resources:
  models:
    - metadata: {}
      model_id: openai/models/${env.INFERENCE_MODEL}
      provider_id: openai
      provider_model_id: models/${env.INFERENCE_MODEL}
      model_type: llm
    - metadata:
        embedding_dimension: 768
      model_id: sentence-transformers/all-mpnet-base-v2
      ...
```

This ensures:
- `provider_model_id` matches the Gemini API's `/models` list → startup validation passes
- `model_id` matches the identifier llama-stack constructs → internal consistency

### Step 2 — Fix the lightspeed-core model ID

Edit `<lightspeed_data_dir>/etc/lightspeed_settings.py`.

Append the `ANSIBLE_AI_MODEL_MESH_CONFIG` override so the lightspeed-core sends `models/<model_name>` instead of just `<model_name>`:

```python
ANSIBLE_AI_MODEL_MESH_CONFIG = "{'ModelPipelineChatBot': {'provider': 'http', 'config': {'inference_url': 'https://<AAP_HOSTNAME>:8449', 'model_id': 'models/<MODEL_ID>', 'enable_health_check': True, 'mcp_servers': [{'name': 'mcp::aap-controller', 'type': 'controller'}, {'name': 'mcp::aap-lightspeed', 'type': 'lightspeed'}]}}, 'ModelPipelineStreamingChatBot': {'provider': 'http', 'config': {'inference_url': 'https://<AAP_HOSTNAME>:8449', 'model_id': 'models/<MODEL_ID>', 'enable_health_check': True, 'mcp_servers': [{'name': 'mcp::aap-controller', 'type': 'controller'}, {'name': 'mcp::aap-lightspeed', 'type': 'lightspeed'}]}}}"
```

Replace `<AAP_HOSTNAME>` with your AAP host and `<MODEL_ID>` with your Gemini model name (e.g. `gemini-3.7-flash`).

This overrides the `ANSIBLE_AI_MODEL_MESH_CONFIG` environment variable that was baked into the container at install time. The settings file is bind-mounted so edits take effect on restart.

### Step 3 — Restart both services

```bash
systemctl --user restart ansible-lightspeed-chatbot.service ansible-lightspeed.service
```

The chatbot takes approximately 60 seconds to fully initialize (loading providers, embedding models, vector DB).

### Step 4 — Verify

Check the chatbot container logs for successful startup:

```bash
podman logs --tail 5 ansible-lightspeed-chatbot
# Should show: "Application startup complete."
# Should NOT show: "Application startup failed."
```

Verify the model is registered with the correct identifier:

```bash
CHATBOT_KEY=$(podman exec ansible-lightspeed-chatbot printenv CHATBOT_API_KEY)
podman exec ansible-lightspeed-chatbot curl -sk \
    -H "Authorization: Bearer $CHATBOT_KEY" \
    https://localhost:8449/v1/models | python3 -c "
import json, sys
for m in json.load(sys.stdin).get('models', []):
    if 'gemini' in m['identifier']:
        print(m['identifier'], '-', m.get('provider_resource_id'))
"
# Should show: openai/models/gemini-3.7-flash - models/gemini-3.7-flash
```

## Why This Only Affects Gemini

Standard OpenAI-compatible endpoints (OpenAI, Azure, vLLM, Red Hat AI Inference Server) return model IDs without a `models/` prefix. Their `/models` list contains bare names like `gpt-4o` or `meta-llama/Llama-3.1-8B-Instruct`. For these endpoints, the workaround in the general installer bug document (setting `provider_model_id: ${env.INFERENCE_MODEL}`) is sufficient — this Gemini-specific fix is not needed.

The Gemini API's OpenAI-compatible endpoint is functional but not fully spec-aligned: it adds a `models/` prefix to all model IDs in the `/models` response, diverging from the convention that other OpenAI-compatible endpoints follow.

## Known Remaining Issue

After applying both workarounds, the Gemini 3.7 Flash model may return HTTP 400 errors on queries that involve tool/function calling:

```
Function call is missing a thought_signature in functionCall parts.
```

This is a Gemini API requirement for models with thinking capabilities — Gemini expects `thought_signature` to be echoed back when forwarding tool call results. The llama-stack OpenAI adapter does not currently handle this. This is a separate llama-stack/Gemini compatibility issue unrelated to model registration.

Queries that do not trigger tool calls (e.g. simple knowledge questions answered from RAG only) may work. The `no_tools: true` flag can be used to bypass tool calling entirely.
