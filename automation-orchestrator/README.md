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

### 2. Obtain OCP API token

The vault requires an OCP API token (`ocp_api_token`). Two ways to get it:

**Option A — via `oc`:**
```bash
oc login https://api.cluster.example.com:6443 -u admin -p <password>
oc whoami -t
```

**Option B — via curl (no `oc` needed, works for RHPDS):**
```bash
curl -sk -X POST \
  "https://oauth-openshift.apps.<cluster>/oauth/authorize?response_type=token&client_id=openshift-challenging-client" \
  --user "admin:<password>" -D - -o /dev/null 2>&1 | grep -oP 'access_token=\K[^&]+'
```

### 3. Create the vault file

```bash
cp vars/vault.yml.example vars/vault.yml
# Edit vars/vault.yml with your actual values
ansible-vault encrypt vars/vault.yml
```

Omit `aap_gateway_url` from the vault to skip AAP integration (Orchestrator deploys standalone).

**Note:** `aap_gateway_url` must be reachable from the OCP cluster — use the public URL (e.g., `https://aap.example.com`), not an internal hostname that the remote OCP pods cannot resolve.

### 4. Deploy Orchestrator

```bash
ansible-playbook deploy-automation-orchestrator.yml --ask-vault-pass
```

The playbook loads `vars/vault.yml` automatically via `vars_files`.

### Running as an AAP Job Template

1. **Project**: Create a project pointing at this repo. Enable `scm_update_on_launch: true` so the playbook always runs the latest version.
2. **Execution Environment**: Register `ee-supported-rhel9:latest` with pull policy `Never` (the image must already be in AAP's podman storage — see Step 1).
3. **Inventory**: Create an inventory with a single `localhost` host. Set `ansible_connection: local` as a host variable (the playbook also sets `connection: local`, so any inventory works).
4. **Job Template**: Create a job template using the project, EE, inventory, and `deploy-automation-orchestrator.yml` as the playbook.
5. **Vault Credential**: Attach an Ansible Vault credential to the job template (decrypts `vars/vault.yml` at runtime).
6. No custom credential types needed — all secrets live in the encrypted vault file.

## What it does

1. Validates OCP version and CatalogSources
2. Installs CloudNativePG operator (Manual approval) in `cnpg-system`
3. Creates PG secrets (generates passwords on first run, reads existing on re-run)
4. Creates CloudNativePG Cluster with `orchestrator`, `temporal`, and `temporal_visibility` databases
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
