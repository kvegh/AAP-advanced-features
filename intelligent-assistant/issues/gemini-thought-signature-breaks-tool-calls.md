# Gemini 3.x Models: thought_signature Breaks Tool/Function Calling in Intelligent Assistant

## Summary

All current Gemini 3.x models require a `thought_signature` field to be echoed back when returning function call results. The llama-stack OpenAI adapter used by the AAP Intelligent Assistant does not handle this field. As a result, any query that triggers MCP tool usage (e.g. "show me the latest job") fails with a 400 error, while plain RAG/documentation queries work fine.

Google has deprecated all Gemini 2.5 models (which did not require thought signatures), so there is currently no Gemini model available via the Gemini API that supports tool calling through llama-stack.

## Affected Configuration

- Any Gemini 3.x model used via the OpenAI-compatible endpoint (`generativelanguage.googleapis.com`)
- `lightspeed_chatbot_default_provider=openai`
- AAP 2.7 containerized deployment

## Symptoms

- Plain questions answered via RAG/knowledge_search work correctly.
- Any query that triggers MCP tool calls (job status, inventory lookups, etc.) fails with:
  ```
  Error code: 400 - Function call is missing a thought_signature in functionCall parts.
  This is required for tools to work correctly. Please refer to
  https://ai.google.dev/gemini-api/docs/thought-signatures for more details.
  ```
- The chatbot container logs show `500` on `/v1/query` and the full traceback ends with:
  ```
  RuntimeError: OpenAI response failed: Error code: 400 - [{'error': {'code': 400,
  'message': 'Function call is missing a thought_signature in functionCall parts...'}}]
  ```

## Root Cause

Gemini 3.x models include thinking capabilities. When the model returns a function/tool call, the response includes a `thought_signature` field. The Gemini API requires this field to be included in the subsequent request that provides the function result. This is a round-trip protocol requirement documented at https://ai.google.dev/gemini-api/docs/thought-signatures.

llama-stack's OpenAI provider adapter (`remote::openai`) does not preserve or forward the `thought_signature` field when relaying tool call results back to the API. The field is silently dropped, causing the Gemini API to reject the follow-up request.

This is a **llama-stack limitation**, not an AAP bug. It affects any llama-stack deployment using Gemini 3.x models with tool calling.

## Models Tested

| Model | RAG queries | Tool calls (MCP) | Status |
|---|---|---|---|
| `gemini-3.7-flash` | Works | Fails (thought_signature) | Available |
| `gemini-3.1-pro-preview` | Works | Fails (thought_signature) | Available |
| `gemini-2.5-pro` | N/A | N/A | Deprecated (404) |
| `gemini-2.5-flash` | N/A | N/A | Deprecated (404) |

All available 3.x models are expected to have the same issue.

## Workaround: Switch to a Non-Gemini Model

Since no current Gemini model works for tool calling through llama-stack, the workaround is to switch to a different LLM provider that uses standard OpenAI-compatible function calling without thought signatures. Options include:

- **vLLM** with an open model (e.g. Llama, Mistral)
- **Red Hat AI Inference Server** (RHAIS)
- **Azure OpenAI** with GPT models
- **Any OpenAI-compatible endpoint** that supports function calling

### How to Switch Models

Two files on the AAP host need to be changed (both are bind-mounted into containers):

#### 1. Chatbot llama-stack config

File: `<lightspeed_data_dir>/etc/chatbot/ansible-chatbot-run.yaml`

Change the inference model entry under `registered_resources.models`:

```yaml
registered_resources:
  models:
    - metadata: {}
      model_id: <provider>/<model_name_from_api>
      provider_id: <provider>
      provider_model_id: <model_name_from_api>
      model_type: llm
```

- `<provider>` matches `lightspeed_chatbot_default_provider` (e.g. `openai`)
- `<model_name_from_api>` is the model ID as returned by the provider's `/models` endpoint

If using the Gemini API, model IDs have a `models/` prefix (e.g. `models/gemini-3.7-flash`). Standard OpenAI endpoints use bare names (e.g. `gpt-4o`). See `gemini-api-model-id-mismatch.md` for details.

#### 2. Lightspeed-core settings

File: `<lightspeed_data_dir>/etc/lightspeed_settings.py`

Append or update the `ANSIBLE_AI_MODEL_MESH_CONFIG` override. The `model_id` value must match the `<model_name_from_api>` used in step 1:

```python
ANSIBLE_AI_MODEL_MESH_CONFIG = "{'ModelPipelineChatBot': {'provider': 'http', 'config': {'inference_url': 'https://<AAP_HOSTNAME>:8449', 'model_id': '<model_name_from_api>', 'enable_health_check': True, 'mcp_servers': [{'name': 'mcp::aap-controller', 'type': 'controller'}, {'name': 'mcp::aap-lightspeed', 'type': 'lightspeed'}]}}, 'ModelPipelineStreamingChatBot': {'provider': 'http', 'config': {'inference_url': 'https://<AAP_HOSTNAME>:8449', 'model_id': '<model_name_from_api>', 'enable_health_check': True, 'mcp_servers': [{'name': 'mcp::aap-controller', 'type': 'controller'}, {'name': 'mcp::aap-lightspeed', 'type': 'lightspeed'}]}}}"
```

If switching to a completely different LLM endpoint, also update:
- `lightspeed_chatbot_model_url` in the installer inventory
- `lightspeed_chatbot_model_api_key` in the installer inventory
- Re-run the installer, or manually update the chatbot container's environment variables

#### 3. Restart both services

```bash
systemctl --user restart ansible-lightspeed-chatbot.service ansible-lightspeed.service
```

The chatbot takes approximately 60 seconds to fully initialize.

#### 4. Verify

Check for successful startup:

```bash
podman logs --tail 5 ansible-lightspeed-chatbot
# Should show: "Application startup complete."
```

Test a tool-calling query in the UI (e.g. "what is the status of the latest job") to confirm MCP tools work.

## Permanent Fix

This requires llama-stack to support Gemini's thought_signature protocol in its OpenAI provider adapter. Specifically, the adapter must:

1. Preserve the `thought_signature` field from the model's function call response
2. Include it in the subsequent request that provides the function result

Until this is implemented upstream, Gemini 3.x models cannot be used for tool-calling workflows through llama-stack.
