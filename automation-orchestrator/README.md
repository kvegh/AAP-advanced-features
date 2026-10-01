# Automation Orchestrator Deployment

Deploys Automation Orchestrator on OpenShift via OLM, with CloudNativePG for PostgreSQL and optional AAP integration.

## Prerequisites

- OpenShift 4.14+ with `redhat-operators` and `certified-operators` CatalogSources
- OCP service account token with cluster-admin (or namespace-admin on target namespaces)
- `ee-supported-rhel9` registered as an Execution Environment in AAP (includes all certified collections and the `kubernetes` Python library)

## Files

| File | Purpose |
|------|---------|
| `deploy-automation-orchestrator.yml` | Main playbook — operators, PG, CR, AAP integration |
| `vars/main.yml` | Default variables |
| `vars/vault.yml.example` | Template for secrets (copy to `vault.yml`, encrypt) |
| `collections/requirements.yml` | Documents required collections (informational, not used at runtime) |
| `execution-environment/execution-environment.yml` | EE base image reference |

## Usage

### 1. Register the EE in AAP

No custom build needed. The stock `ee-supported-rhel9` image includes all required certified collections (`redhat.openshift`, `ansible.platform`) and the `kubernetes` Python library.

In AAP, create an Execution Environment pointing at:
```
registry.redhat.io/ansible-automation-platform-27/ee-supported-rhel9:latest
```

**AAP containerized note:** The image must exist in AAP's service podman storage (`~/aap/containers/storage`), not the interactive user's storage. If the image is only in interactive storage, copy it:
```bash
podman save registry.redhat.io/.../ee-supported-rhel9:latest | podman --remote load
```

### 2. Create the vault file

```bash
cp vars/vault.yml.example vars/vault.yml
# Edit vars/vault.yml with your actual values
ansible-vault encrypt vars/vault.yml
```

Omit `aap_gateway_url` from the vault to skip AAP integration (Orchestrator deploys standalone).

### 3. Deploy Orchestrator

```bash
ansible-playbook deploy-automation-orchestrator.yml --ask-vault-pass
```

The playbook loads `vars/vault.yml` automatically via `vars_files`.

### Running as an AAP Job Template

1. Create the project pointing at this repo
2. Create the job template using the `ee-supported-rhel9` EE and `deploy-automation-orchestrator.yml`
3. Attach the Vault credential to the job template (decrypts `vars/vault.yml` at runtime)
4. No custom credential types needed — all secrets live in the encrypted vault file

## What it does

1. Validates OCP version and CatalogSources
2. Installs CloudNativePG operator (Manual approval) in `cnpg-system`
3. Creates PG secrets (generates passwords on first run, reads existing on re-run)
4. Creates CloudNativePG Cluster with `orchestrator` and `temporal` databases
5. Installs Orchestrator operator (Manual approval) in `automation-orchestrator`
6. Creates AutomationOrchestrator CR pointing at CloudNativePG
7. (Optional) Configures OIDC identity provider and AAP integration via Orchestrator REST API

## Idempotency

- Secrets: check-before-create pattern — passwords generated only on first run
- OAuth credentials: stored in K8s secret `orchestrator-aap-credentials` for re-runs
- Identity provider and integration: existence checks before POST
- Operators: OLM Subscriptions and InstallPlans are idempotent

## Future improvements

- **Switch to `ee-minimal-rhel9` base image**: The current EE uses `ee-supported-rhel9` (~2.5GB) because AAP 2.7 gateway auth prevents `ansible-galaxy` from pulling collections from PAH during project sync. Once gateway-compatible galaxy credentials are sorted out, switch back to `ee-minimal-rhel9` (~500MB) and bake only `redhat.openshift` + `ansible.platform` via `dependencies.galaxy` in the EE definition, or rely on runtime collection install from PAH.
