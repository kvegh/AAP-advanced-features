# AAP Intelligent Assistant Setup — Reproducibility Guide

## Goal

Deploy the Automation Intelligent Assistant (Ansible Lightspeed chatbot) on an existing containerized AAP 2.7 installation, using Google Gemini as the LLM backend via the OpenAI-compatible endpoint.

## Architecture

- **AAP**: Containerized (Podman) on VM at <AAP_HOST_IP> (<AAP_HOSTNAME>), growth topology (all-in-one)
- **LLM**: Gemini 3.7 Flash via Google's Gemini API OpenAI-compatible endpoint
- **Automation Orchestrator**: Separate product, runs on RHPDS OCP cluster (not covered here)

## LLM Provider Decision

**Target:** Vertex AI OpenAI-compatible endpoint (`aiplatform.googleapis.com`).

**Problem:** Vertex AI only supports OAuth2 tokens that expire after 1 hour. No static API key option exists. A long-running service like the Intelligent Assistant would need a systemd timer refreshing tokens every 50 minutes — unacceptable complexity for a demo.

**Solution:** Google's Gemini API (`generativelanguage.googleapis.com`) accepts a static GCP API key that never expires. It serves the same Gemini models (including 3.7 Flash), on the same GCP project (`<YOUR_GCP_PROJECT_ID>`), **billed to the same account** as the Vertex AI approach would have been. The only difference is the hostname in the URL. The OpenAI-compatible endpoint format is identical.

**Note:** The upstream `ansible-chatbot-stack` code has native Vertex AI support via `VERTEX_AI_CREDENTIALS` env var with automatic token refresh, but the AAP containerized installer does not expose this. If Red Hat adds installer support for Vertex AI credentials in the future, the Vertex approach becomes viable without workarounds.

**Alternatives:** Any LLM with an OpenAI-compatible endpoint and function calling support can be used — including locally hosted models (e.g. via vLLM or Red Hat AI Inference Server). Just set the appropriate `model_url`, `model_api_key`, and `model_id`.

## Step 1 — GCP Setup

### Verify Gemini API is enabled

```bash
gcloud services list --enabled --project=<YOUR_GCP_PROJECT_ID> | grep generativelanguage
```

If not listed, enable it:

```bash
gcloud services enable generativelanguage.googleapis.com --project=<YOUR_GCP_PROJECT_ID>
```

### Create an API key restricted to Gemini API

```bash
gcloud services api-keys create \
    --display-name="Lightspeed Chatbot" \
    --api-target=service=generativelanguage.googleapis.com \
    --project=<YOUR_GCP_PROJECT_ID>
```

The output contains `keyString` — this is your API key. Save it.

### Test the endpoint

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <YOUR_GEMINI_API_KEY>" \
    -d '{"model":"gemini-3.7-flash","messages":[{"role":"user","content":"say hi"}]}' \
    | python3 -m json.tool
```

You should get a valid chat completion response.

## Step 2 — AAP Inventory Changes

SSH to the AAP host and edit the inventory file used for the initial installation (e.g. `inventory-growth`).

### Add the Lightspeed host group (before `[all:vars]`)

```ini
[ansiblelightspeed]
<AAP_HOSTNAME>
```

Use the same hostname as your other inventory groups.

### Add variables under `[all:vars]`

```ini
# Red Hat Ansible Lightspeed base
lightspeed_admin_password=<set your own>
lightspeed_pg_host=<AAP_HOSTNAME>
lightspeed_pg_password=<set your own>

# Automation intelligent assistant (chatbot)
lightspeed_chatbot_model_url=https://generativelanguage.googleapis.com/v1beta/openai/
lightspeed_chatbot_model_api_key=<YOUR_GEMINI_API_KEY>
lightspeed_chatbot_model_id=gemini-3.7-flash
lightspeed_chatbot_default_provider=openai

# MCP server integration (lets the chatbot interact with AAP)
lightspeed_mcp_controller_enabled=true
lightspeed_mcp_lightspeed_enabled=true
```

**Notes:**
- `lightspeed_admin_password` is internal to the Lightspeed service, does not need to match any existing AAP password.
- `lightspeed_chatbot_default_provider=openai` — the Gemini API is OpenAI-compatible, so we use the `openai` provider type.
- MCP integration enables the chatbot to query and interact with the AAP controller.

## Step 3 — Run the Installer

From the installer directory on the AAP host:

```bash
ansible-playbook -i inventory-growth ansible.containerized_installer.install
```

Add `-K` if a become password is required, `-v` for verbosity.

This will:
- Create a `lightspeed` PostgreSQL database
- Pull and start Lightspeed Podman containers
- Register Lightspeed with the platform gateway
- Configure MCP integration

## Step 4 — Verify

1. Log in to `https://<AAP_HOSTNAME>`
2. Look for the chat bubble icon in the top right corner of the taskbar
3. Click it — the Intelligent Assistant should open with a welcome message
