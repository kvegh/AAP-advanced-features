# Automation Orchestrator Deployment

Deploys Automation Orchestrator on OpenShift via OLM, with CloudNativePG for PostgreSQL and optional AAP integration.

## Prerequisites

- OpenShift 4.14+ with `redhat-operators` and `certified-operators` CatalogSources
- OCP service account token with cluster-admin (or namespace-admin on target namespaces)
- Custom EE with `python3-kubernetes` and `python3-openshift` (see `execution-environment/`)
- Collections `redhat.openshift` and `ansible.platform` synced to PAH (see `sync-collections.yml`)

## Files

| File | Purpose |
|------|---------|
| `deploy-automation-orchestrator.yml` | Main playbook — operators, PG, CR, AAP integration |
| `sync-collections.yml` | Pre-flight — sync required collections to PAH |
| `vars/main.yml` | Default variables |
| `vars/vault.yml.example` | Template for secrets (copy to `vault.yml`, encrypt) |
| `collections/requirements.yml` | Runtime collection dependencies |
| `execution-environment/execution-environment.yml` | Custom EE build spec |

## Usage

### 1. Build the custom EE (on the build host, not the AAP VM)

```bash
ansible-builder build \
    -f execution-environment/execution-environment.yml \
    -t orchestrator-ee:latest
```

Push to PAH container registry, then register in AAP as an Execution Environment.

### 2. Sync collections to PAH

Run on the default EE (which already has `ansible.platform`):

```bash
ansible-playbook sync-collections.yml \
    -e aap_gateway_url=https://aap.example.com \
    -e aap_admin_username=admin \
    -e aap_admin_password=changeme
```

### 3. Deploy Orchestrator

```bash
ansible-playbook deploy-automation-orchestrator.yml \
    -e ocp_api_url=https://api.cluster.example.com:6443 \
    -e ocp_api_token=sha256~xxxx \
    -e orchestrator_route_host=orchestrator.apps.cluster.example.com \
    -e aap_gateway_url=https://aap.example.com \
    -e aap_admin_username=admin \
    -e aap_admin_password=changeme
```

Or with vault:

```bash
cp vars/vault.yml.example vars/vault.yml
ansible-vault encrypt vars/vault.yml
ansible-playbook deploy-automation-orchestrator.yml -e @vars/vault.yml --ask-vault-pass
```

Omit `aap_gateway_url` to skip AAP integration (Orchestrator deploys standalone).

### Running as an AAP Job Template

1. Create an OCP credential type injecting `ocp_api_url` and `ocp_api_token` as extra vars
2. Create the project pointing at this repo
3. Create the job template using the custom EE, `deploy-automation-orchestrator.yml`, and the OCP credential
4. Add AAP admin credentials as a second credential (or as survey variables)

## What it does

1. Validates OCP version and CatalogSources
2. Installs CloudNativePG operator (Manual approval) in `cnpg-system`
3. Creates PG secrets (generates passwords on first run, reads existing on re-run)
4. Creates CloudNativePG Cluster with `orchestrator` and `temporal` databases
5. Installs Orchestrator operator (Manual approval) in `automation-orchestrator`
6. Creates AutomationOrchestrator CR pointing at CloudNativePG
7. (Optional) Creates OAuth2 app and service account on AAP Gateway
8. (Optional) Configures OIDC identity provider and AAP integration via Orchestrator REST API

## Idempotency

- Secrets: check-before-create pattern — passwords generated only on first run
- OAuth credentials: stored in K8s secret `orchestrator-aap-credentials` for re-runs
- Identity provider and integration: existence checks before POST
- Operators: OLM Subscriptions and InstallPlans are idempotent
