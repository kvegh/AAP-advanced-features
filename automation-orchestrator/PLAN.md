# Automation Orchestrator Setup Plan

## Context

Automation Orchestrator needs to be deployed on a remote RHPDS OpenShift cluster (independent deployment model). AAP 2.7 runs on local VMs (containerized installer). The previous attempt in the AAP-advanced-features repo used a Helm-based approach for the wrong product (Automation Portal) and was deleted. This plan uses the correct OLM operator approach per the 2026.8 documentation.

The goal: a tested, documented, automated setup captured in the `AAP-advanced-features` git repo as a playbook.

---

## Architecture

```
 KVM host
   |
   +-- AAP VM (AAP 2.7 containerized) <--- Automation Gateway on port 443
   |
   +-- managed host VMs
   |
   +-- ...
   
 RHPDS OCP cluster (remote, AWS)
   |
   +-- automation-orchestrator namespace
         +-- Orchestrator Operator (OLM)
         +-- AutomationOrchestrator CR
         +-- PostgreSQL secrets (pointing to external PG or CloudNativePG)
```

Cross-cluster link: Orchestrator --> AAP Gateway on port 443 (HTTPS only, no inbound from AAP to OCP needed).

---

## Decisions (resolved)

1. **PostgreSQL**: CloudNativePG operator on OCP (fine for demo)
2. **Release channel**: `stable`
3. **S3 storage**: Skip for now
4. **LLM provider**: Defer to later
5. **Tooling**: Pure Ansible with `kubernetes.core` (via `ee-supported-rhel9`) -- no `oc` CLI dependency. Playbook must be runnable from AAP as a job template. Module defaults use `group/kubernetes.core.k8s`.
6. **Orchestrator configuration**: No certified Ansible collection exists for Orchestrator's own config (identity providers, integrations). The REST API is the only documented interface -- `ansible.builtin.uri` is the correct approach.
7. **Passwords**: Generated at runtime via `lookup('password', ...)`. Idempotent -- check if K8s secret exists first, only generate if missing. Passwords live only in OCP secrets, never in git.
8. **AAP credentials**: Automatic path via `setup_aap_oidc` — provides AAP admin credentials transiently (never stored by Orchestrator). The endpoint creates the OAuth2 application on AAP and configures the OIDC identity provider automatically. For the integration health-check credential, AAP admin creds are stored in the Orchestrator credential store (encrypted at rest).
9. **EE**: Stock `ee-supported-rhel9` used directly — includes all certified collections (`redhat.openshift`, `ansible.platform`) and the `kubernetes` Python library. No custom build needed. AAP 2.7 gateway auth prevents `ansible-galaxy` from pulling collections from PAH during project sync, so baking collections into the EE (via the supported image) is the current workaround.
10. **Disk**: AAP host has sufficient disk space. The `ee-supported-rhel9` image is ~2.5GB.
11. **Collection sync**: Not required — collections are included in `ee-supported-rhel9`. The `sync-collections.yml` playbook remains in the repo for reference if switching back to `ee-minimal-rhel9` in the future.
12. **Secrets handling**: Zero plaintext secrets in git. OCP token, AAP OAuth/service account creds, and route hostname stored in `vars/vault.yml` (ansible-vault encrypted, committed to repo). Decrypted at runtime by AAP Vault credential. PG and Orchestrator admin passwords generated at runtime, stored only in K8s secrets.
13. **Subscription**: No separate manifest needed. Orchestrator operator available via `redhat-operators` catalog (OCP pull secret on RHPDS covers it). AAP subscription includes Orchestrator entitlement.
14. **PostgreSQL**: CloudNativePG operator runs PG pods directly on OCP. No external DB. Fine for demo.
15. **AAP containerized EE storage**: AAP containerized uses a separate podman storage root (`~/aap/containers/storage`). Images built or pulled into the interactive user's storage are not visible to AAP's receptor. Use `podman save | podman --remote load` to copy images into AAP's service storage.

---

## Constraints (modus operandi)

- **Pure Ansible only.** No `oc` CLI commands. No manual UI steps. No shell scripts.
- **Certified Red Hat collections only:** `redhat.openshift`, `ansible.platform`. No `kubernetes.core` directly.
- **Orchestrator REST API via `ansible.builtin.uri`** for post-deploy configuration (identity provider, integrations) — no certified collection exists for this.
- **No admin credentials handed to Orchestrator.** Manual OAuth path: create OAuth app + service account on AAP via `ansible.platform`, pass only client_id/secret to Orchestrator.
- **No plaintext secrets in git.** OCP and AAP credentials stored in `vars/vault.yml` (ansible-vault encrypted). Decrypted at runtime by AAP Vault credential. PG and Orchestrator admin passwords generated at runtime.
- **EE: stock `ee-supported-rhel9`** — includes all certified collections and `kubernetes` Python library. No custom build needed. Future improvement: switch to `ee-minimal-rhel9` once gateway-compatible galaxy credentials work.
- **Idempotent.** Re-running the playbook must not break an existing deployment (check-before-create pattern for secrets, operators, CRs).

---

## Steps

### Step 1: Register EE in AAP

Register `ee-supported-rhel9` as an Execution Environment in AAP (pull: never). Ensure the image exists in AAP's service podman storage — use `podman save | podman --remote load` if needed.

### Step 2: Prerequisites

- All credentials stored in `vars/vault.yml` (ansible-vault encrypted): OCP API URL/token, AAP Gateway URL/credentials, Orchestrator route hostname
- AAP Vault credential attached to job template for decryption at runtime
- Playbook uses `redhat.openshift.k8s` and `redhat.openshift.k8s_info` -- no `oc` CLI needed
- Authentication via `redhat.openshift.openshift_auth` or API token variable
- Preflight: verify OCP version >= 4.14 and OLM catalog via `k8s_info`

### Step 3: Create namespace and secrets

Create namespace via `redhat.openshift.k8s`.

For each secret: check if it already exists via `k8s_info`. If not, generate a random password with `lookup('password', '/dev/null length=32 chars=ascii_letters,digits')` and create the secret. If it exists, skip (idempotent).

Secrets needed:

```yaml
# orchestrator-pg-credentials
apiVersion: v1
kind: Secret
metadata:
  name: orchestrator-pg-credentials
  namespace: automation-orchestrator
type: Opaque
stringData:
  database: "orchestrator"
  username: "orchestrator_user"
  password: "{{ generated_at_runtime }}"

---
# temporal-pg-credentials
apiVersion: v1
kind: Secret
metadata:
  name: temporal-pg-credentials
  namespace: automation-orchestrator
type: Opaque
stringData:
  database: "temporal"
  username: "temporal_user"
  password: "{{ generated_at_runtime }}"
```

Admin password secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: orchestrator-admin-password
  namespace: automation-orchestrator
type: Opaque
stringData:
  password: "{{ generated_at_runtime }}"
```

### Step 4: Install the operator via OLM

```yaml
# OperatorGroup (AllNamespaces scope -- required)
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: automation-orchestrator-operator
  namespace: automation-orchestrator
spec: {}

---
# Subscription
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: automation-orchestrator-operator
  namespace: automation-orchestrator
spec:
  channel: stable  # or early-access
  name: automation-orchestrator-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Manual
```

- Apply via `redhat.openshift.k8s`
- Find and approve InstallPlan via `k8s_info` + `k8s` patch
- Wait for operator CSV to reach Succeeded phase via `k8s_info` with `wait_condition`

### Step 5: Provision PostgreSQL via CloudNativePG (runs on OCP)

- Install CloudNativePG operator (Namespace, OperatorGroup, Subscription from `certified-operators`)
- Wait for CloudNativePG operator ready
- Create Cluster CR with 3 databases (orchestrator, temporal, temporal_visibility)
- Operator auto-generates credential secrets

### Step 6: Create AutomationOrchestrator CR

```yaml
apiVersion: aap.ansible.com/v1alpha1
kind: AutomationOrchestrator
metadata:
  name: orchestrator
  namespace: automation-orchestrator
spec:
  postgres:
    host: "<pg-host>"
    port: 5432
    sslMode: require  # or verify-ca/verify-full
    backendDatabase:
      secretRef:
        name: orchestrator-pg-credentials
    temporalDatabase:
      secretRef:
        name: temporal-pg-credentials
  ingress:
    host: "<orchestrator-route-hostname>"
  secrets:
    initialAdminPasswordSecretRef:
      name: orchestrator-admin-password
```

- Apply via `redhat.openshift.k8s`
- Wait for Ready=True via `k8s_info` with retries
- Retrieve route and admin password via `k8s_info`, display with `debug`

### Step 7: Verify deployment

- Playbook outputs: Orchestrator route URL, admin credentials
- Manual verification: access UI, log in

### Step 8: Create OAuth app and service account on AAP (no admin handover)

Using `ansible.platform` certified collection (not handing admin credentials to Orchestrator):

1. Create a dedicated OAuth2 application on AAP Gateway:
   - Grant type: `authorization-code`
   - Redirect URI: `https://<orchestrator-route>/api/v1/auth/oidc/callback`
   - Record `client_id` and `client_secret`
2. Create a dedicated service account user on AAP for job dispatch (limited permissions, not admin)
3. Assign the service account only the roles needed for launching job templates

### Step 9: Authenticate to Orchestrator API

- Use `ansible.builtin.uri` to POST `/api/v1/auth/login` with admin credentials
- Retrieve JWT access token for subsequent API calls

### Step 10: Add AAP as identity provider (manual OAuth path)

- Use `ansible.builtin.uri` to call the Orchestrator REST API to add AAP as an OIDC identity provider
- Provide: AAP Gateway URL as issuer, `client_id` and `client_secret` from Step 7
- Orchestrator never receives AAP admin credentials

### Step 11: Add AAP integration (for job dispatch)

- Use `ansible.builtin.uri` to call the Orchestrator REST API to create an AAP integration
- Provide: AAP Gateway URL, service account credentials from Step 7 (not admin)
- Test connection via API

---

## Ansible Playbook Design

Target directory: `automation-orchestrator/`

### Files to create

```
automation-orchestrator/
  PLAN.md                               # This plan document
  deploy-automation-orchestrator.yml    # Main playbook (inline k8s definitions, no templates)
  sync-collections.yml                  # Reference: sync collections to PAH (not needed with ee-supported)
  collections/
    requirements.yml                    # Documents required collections (informational only)
  vars/
    main.yml                            # Non-secret variables (namespace, channel, PG config)
    vault.yml                           # Encrypted secrets (OCP token, AAP creds, route host)
    vault.yml.example                   # Template showing required var names (no values)
  execution-environment/
    execution-environment.yml           # EE base image reference (ee-supported-rhel9)
  README.md                             # Setup docs
```

No Jinja templates needed -- `redhat.openshift.k8s` takes inline `definition:` dicts directly, which is cleaner and keeps everything in one playbook file.

Passwords for PG and Orchestrator admin are generated at runtime and stored in K8s secrets only. `vars/vault.yml` (ansible-vault encrypted) holds OCP credentials, AAP admin credentials, and the Orchestrator route hostname. Decrypted at runtime by AAP Vault credential.

### Playbook structure

The playbook runs against `localhost` and uses `redhat.openshift` certified collection for OCP resources, `ansible.platform` for AAP Gateway resources, and `ansible.builtin.uri` for Orchestrator REST API. No `oc` CLI. Authentication via `host` (API URL) + `api_key` (token) variables, or kubeconfig file.

1. **Preflight** -- `k8s_info` to verify OCP version, OLM catalog source
2. **CloudNativePG operator** -- Namespace, OperatorGroup, Subscription, approve InstallPlan, wait for CSV
3. **CloudNativePG Cluster** -- Create Cluster CR with 3 databases on OCP, wait for ready
4. **Orchestrator namespace + secrets** -- Namespace, generate passwords (idempotent), create PG credential secrets and admin password secret
5. **Orchestrator operator** -- OperatorGroup, Subscription, approve InstallPlan, wait for CSV
6. **AutomationOrchestrator CR** -- apply CR, wait for Ready condition
7. **AAP OAuth + service account** -- `ansible.platform` to create OAuth2 app (redirect URI pointing to Orchestrator) and limited-privilege service account on AAP
8. **Configure Orchestrator** -- `uri` to authenticate to Orchestrator API, add AAP as OIDC identity provider (with client_id/secret from step 7), add AAP integration (with service account from step 7)
9. **Output** -- retrieve Route URL and admin password, display

### Collections needed (included in ee-supported-rhel9)

- `redhat.openshift` (certified -- k8s, k8s_info, openshift_auth for OCP resources)
- `ansible.platform` (certified -- OAuth2 app, users, roles on AAP Gateway)
- `ansible.builtin` (uri module for Orchestrator REST API -- built-in, no install needed)

All collections are included in the stock `ee-supported-rhel9` image. No PAH sync or runtime install needed.

### EE: stock ee-supported-rhel9

```yaml
# execution-environment.yml
version: 3
images:
  base_image:
    name: registry.redhat.io/ansible-automation-platform-27/ee-supported-rhel9:latest
```

No custom build needed. The image includes all certified collections and the `kubernetes` Python library (29.0.0). See README.md "Future improvements" for the plan to switch to `ee-minimal-rhel9`.

---

## Verification

1. Playbook outputs pod status, CR conditions, route URL, admin password
2. Access Orchestrator UI via route URL
3. Log in as admin
4. Verify "Log in with AAP" button appears (identity provider configured)
5. Log in via AAP SSO -- verify it works
6. Verify AAP integration shows healthy in Orchestrator UI
7. Create a test workflow with a Job Execution node pointing at an AAP job template

---

## Orchestrator REST API Reference (reverse-engineered)

The Orchestrator REST API is underdocumented. The official docs show UI field labels but not the actual JSON body structure. The API uses Pydantic v2 with `extra="forbid"` — any unknown field is rejected. The correct schemas were discovered by reading the source inside the Orchestrator backend pod (`/opt/app-root/src/src/syntara/`).

### Authentication

```
POST /api/v1/auth/login
Body: {"username": "admin", "password": "..."}
Response: {"access_token": "..."}
```

All subsequent requests need `Authorization: Bearer <token>` header.

### Identity Provider — automatic AAP setup

```
POST /api/v1/identity_providers/setup_aap_oidc
Body:
  aap_url: string (required)
  organization: string (default: "Default")
  admin_username: string (mutually exclusive with personal_access_token)
  admin_password: string (required with admin_username)
  personal_access_token: string (alternative to username/password)
  insecure_skip_tls_verify: bool (default: false)
Response: 201 — IdentityProviderRead
```

Creates an OAuth2 application on AAP and configures the OIDC identity provider in Orchestrator in one shot. Admin credentials are used transiently, never stored.

Source: `syntara/identity_providers/models/aap_setup.py` → `AAPOIDCSetupRequest`

### Identity Provider — manual

```
POST /api/v1/identity_providers
Body:
  name: string (required)
  configuration:
    provider_type: "oidc"
    issuer_url: string
    client_id: string
    client_secret: string
    redirect_uri: string
    idp_type: "aap" | "generic"
    disable_tls_verify: bool
    scopes: string
    auto_discovery: bool
    allow_all_authenticated: bool
    aap_role_mapping_enabled: bool
    enable_rp_initiated_logout: bool
Response: 201
```

List response uses `resources` array (not `results`).

### Credentials

```
POST /api/v1/credentials
Body:
  name: string (required)
  credential_type_id: UUID (required)
  project_id: UUID (required)
  inputs: object (required — fields depend on credential type)
Response: 201

Built-in credential types:
  - "Ansible Automation Platform" — inputs: {username, password} or {oauth_token}
  - "LLM Provider" — inputs: {api_key}
  - "HTTP Bearer Token" — inputs: {token}
  - "HTTP Basic Auth" — inputs: {username, password}
```

### Integrations

```
POST /api/v1/integrations
Body:
  name: string (required)
  integration_type: "ansible_automation_platform" | "llm_provider" | "mcp_server" (required)
  management_credential_id: UUID (required for AAP and LLM, optional for MCP)
  configuration:
    integration_type: string (must match top-level, acts as discriminator)
    base_url: string
    insecure_skip_tls_verify: bool
    allow_http: bool
    ca_certificate: string | null
  description: string | null
  enabled: bool (default: true)
  scope: "global" | "project" (default: "global")
  labels: object
  discovered_tools: list (MCP only)
  discovered_models: list (LLM only)
Response: 201

Extra fields cause: "Extra inputs are not permitted" (Pydantic extra="forbid")
Missing credential causes: "INTEGRATION_CREDENTIAL_REQUIRED"
```

Source: `syntara/integrations/models/integration.py` → `IntegrationCreate`

### Key gotchas

- All POST bodies use **nested `configuration` wrapper** — the docs show fields flat but the API nests them
- The credential field is `management_credential_id` (not `credential_id`, `health_check_credential_id`, or `connection_credential_id` — all of which the docs imply)
- List responses use `resources` as the array key (not `results`)
- The `integration_type` field must appear **both** at top level and inside `configuration` (discriminated union)

---

## What the playbook does NOT automate

- RHPDS OCP cluster provisioning (done separately)
- LLM provider integration (deferred to later)
- Pulling `ee-supported-rhel9` and loading it into AAP's podman storage (documented in README)
