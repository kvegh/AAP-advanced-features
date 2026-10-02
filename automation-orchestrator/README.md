# Automation Orchestrator Deployment

Deploys Automation Orchestrator on OpenShift via OLM, with CloudNativePG for PostgreSQL and optional AAP integration.

## Prerequisites

- OpenShift 4.14+ with `redhat-operators` and `certified-operators` CatalogSources
- OCP cluster-admin credentials (provided at launch via job template survey)
- `ee-supported-rhel9` registered as an Execution Environment in AAP (includes all certified collections and the `kubernetes` Python library)

## Files

| File | Purpose |
|------|---------|
| `deploy-automation-orchestrator.yml` | Main playbook — operators, PG, CR, AAP integration |
| `cleanup-aap-orchestrator.yml` | Cleanup playbook — removes Orchestrator OAuth2 apps from AAP |
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

The vault only contains AAP credentials (`aap_gateway_url`, `aap_admin_username`, `aap_admin_password`). OCP credentials are provided at launch time via the job template survey — they are never stored in the vault.

Omit `aap_gateway_url` from the vault to skip AAP integration (Orchestrator deploys standalone).

**Note:** `aap_gateway_url` must be reachable from the OCP cluster — use the public URL (e.g., `https://aap.example.com`), not an internal hostname that the remote OCP pods cannot resolve.

### 3. Deploy Orchestrator

```bash
ansible-playbook deploy-automation-orchestrator.yml --ask-vault-pass \
  -e ocp_api_url=https://api.cluster.example.com:6443 \
  -e ocp_admin_password=<password>
```

The playbook automatically obtains an OCP API token at runtime using the OAuth `openshift-challenging-client` flow (with `X-CSRF-Token` header required by OCP 4.21+) — no manual `oc login` needed. The route hostname is derived from the API URL automatically.

To debug credential-related task failures, pass `secure_logging: false` as an extra var — this disables `no_log` on sensitive tasks so request/response bodies are visible in job output.

### Running as an AAP Job Template

1. **Project**: Create a project pointing at this repo. Enable `scm_update_on_launch: true` so the playbook always runs the latest version.
2. **Execution Environment**: Register `ee-supported-rhel9:latest` with pull policy `Never` (the image must already be in AAP's podman storage — see Step 1).
3. **Inventory**: Create an inventory with a single `localhost` host. Set `ansible_connection: local` as a host variable (the playbook also sets `connection: local`, so any inventory works).
4. **Job Template**: Create a job template using the project, EE, inventory, and `deploy-automation-orchestrator.yml` as the playbook.
5. **Vault Credential**: Attach an Ansible Vault credential to the job template (decrypts `vars/vault.yml` at runtime).
6. **Survey**: Enable a survey with two fields:
   - `ocp_api_url` (text) — the OCP API URL, e.g. `https://api.cluster-xyz.dyn.redhatworkshops.io:6443`
   - `ocp_admin_password` (password) — the OCP admin password (stored encrypted, shown as `$encrypted$`)
7. No custom credential types needed — AAP secrets live in the encrypted vault file, OCP credentials come from the survey.

### Cleanup between deployments

When tearing down an OCP cluster and redeploying to a new one, the Orchestrator `setup_aap_oidc` step will fail because the OAuth2 app ("Syntara") from the old cluster still exists on AAP. Run the cleanup job template first:

- **Playbook**: `cleanup-aap-orchestrator.yml`
- **What it does**: Finds and deletes all OAuth2 applications matching "syntara" or "orchestrator" from AAP Gateway
- **When to run**: Before deploying Orchestrator to a new OCP cluster, or after tearing down an old deployment

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
- AAP credentials: existence check via Orchestrator REST API before POST
- Identity provider and integration: existence checks before POST
- Operators: OLM Subscriptions and InstallPlans are idempotent

## Future improvements

- **Switch to `ee-minimal-rhel9` base image**: The current EE uses `ee-supported-rhel9` (~2.5GB) because AAP 2.7 gateway auth prevents `ansible-galaxy` from pulling collections from PAH during project sync. Once gateway-compatible galaxy credentials are sorted out, switch back to `ee-minimal-rhel9` (~500MB) and bake only `redhat.openshift` + `ansible.platform` via `dependencies.galaxy` in the EE definition, or rely on runtime collection install from PAH.
