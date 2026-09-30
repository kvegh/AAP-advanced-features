# Automation Orchestrator Deployment

Deploys Automation Orchestrator on OpenShift via OLM, with CloudNativePG for PostgreSQL and optional AAP integration.

## Prerequisites

- OpenShift 4.14+ with `redhat-operators` and `certified-operators` CatalogSources
- OCP service account token with cluster-admin (or namespace-admin on target namespaces)
- Custom EE with `kubernetes` and `openshift` Python packages (see `execution-environment/`)
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

Run on the default EE (which already has `ansible.platform`). Reads AAP credentials from the vault:

```bash
ansible-playbook sync-collections.yml --ask-vault-pass
```

### 3. Create the vault file

```bash
cp vars/vault.yml.example vars/vault.yml
# Edit vars/vault.yml with your actual values
ansible-vault encrypt vars/vault.yml
```

Omit `aap_gateway_url` from the vault to skip AAP integration (Orchestrator deploys standalone).

### 4. Deploy Orchestrator

```bash
ansible-playbook deploy-automation-orchestrator.yml --ask-vault-pass
```

The playbook loads `vars/vault.yml` automatically via `vars_files`.

### Running as an AAP Job Template

1. Create the project pointing at this repo
2. Create the job template using the Orchestrator EE and `deploy-automation-orchestrator.yml`
3. Attach the Vault credential to the job template (decrypts `vars/vault.yml` at runtime)
4. No custom credential types needed — all secrets live in the encrypted vault file

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
