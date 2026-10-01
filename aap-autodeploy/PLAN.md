# AAP AutoDeploy Plan

## Context

We need a repeatable, fully automated way to deploy fresh AAP 2.7 instances for testing. Currently there is no automation for the AAP platform install itself — only VM provisioning (`deploy_vms.yml`) and post-install configuration (`aap_deploy/` playbooks) exist separately. This project bridges the gap: from golden image clone to a fully working AAP test instance, driven entirely by Ansible.

All playbooks and docs go in `AAP-advanced-features/aap-autodeploy/`. The VM deployment playbook stays in `automAIton`. No sensitive data (passwords, tokens, IPs, hostnames) in the repo — everything parameterized via vault.

---

## Architecture Overview

```
Golden Image (pre-updated RHEL 9.8 qcow2)
    |
    v
[1] Clone + resize disk + virt-install on hypervisor
    |
    v
[2] Prepare host: create aap_service user, SSH keys, subscribe, install prereqs
    |
    v
[3] Copy installer tarball from existing AAP, extract, template inventory, run installer
    |
    v
[4] Configure nginx reverse proxy on hypervisor for external access
```

---

## Deliverables

### Files in `AAP-advanced-features/aap-autodeploy/`

```
aap-autodeploy/
  deploy-test-aap.yml          # Main orchestration playbook (multi-play)
  templates/
    inventory.j2               # AAP installer inventory template
    nginx-aap-test.conf.j2     # nginx reverse proxy config for test instance
  vars/
    main.yml                   # Non-sensitive defaults (ports, sizing, paths)
  version-registry.yml         # Tracks AAP version -> VM name mapping
```

Secrets come from the shared `automAIton/myvars` vault (passed via `vault_file` variable). No separate vault in this directory.

### Changes to `automAIton/deploy_vms/deploy_vms.yml`

Add `disk_size` variable support for `qemu-img resize` after copy (needed for AAP's 60G disk). Minimal change to existing playbook.

---

## Step-by-Step Design

### Step 1: VM Creation (Play 1 — targets: hypervisor)

Reuse the existing `deploy_vms.yml` with extended parameters:
- `projectname`: `aap-v{{ aap_version_short }}` (e.g., `aap-v27`)
- `sequence`: `1`
- **Note**: `deploy_vms.yml` creates names as `{{ projectname }}-vm-{{ item }}`, producing `aap-v27-vm-1`. To get the desired `aap-v27-testvm` naming, we'll modify the naming pattern in `deploy_vms.yml` to use a configurable suffix (default `vm`) so we can pass `suffix: testvm`.
- `vcpus`: `4`
- `memory`: `20480` (20 GiB)
- `base_image`: path to golden image (not the raw RHEL base)
- `disk_size`: `60G` (new parameter — qemu-img resize after copy)

**Extend `deploy_vms.yml`**: Add a task between "Copy base image" and "Customize VM images" that runs `qemu-img resize` when `disk_size` is defined. One line addition; backwards compatible.

VM naming: `aap-vX-testvm` where X is the version (e.g., `aap-v27-testvm`).
Hostname: matches VM name.

### Step 2: Host Preparation (Play 2 — targets: new VM via dynamic inventory)

After the VM boots and gets a DHCP IP, we need to:

1. **Discover the VM's IP** — `virsh net-dhcp-leases internal` on hypervisor, register the IP
2. **Add to in-memory inventory** — `add_host` with the discovered IP
3. **Wait for SSH** — `wait_for_connection`
4. **Create `aap_service` user** — with sudo NOPASSWD, home dir, SSH key
5. **Subscribe to RHEL** — `community.general.redhat_subscription` with activation key (from vault)
6. **Enable AAP repo** — `ansible-automation-platform-2.7-for-rhel-9-x86_64-rpms`
7. **Install ansible-core** — `dnf install ansible-core`
8. **Grow the filesystem** — `growpart` + `xfs_growfs` to use the resized disk
9. **Configure `loginctl enable-linger`** for the aap_service user (required for rootless podman)

### Step 3: AAP Installation (Play 3 — targets: new VM as aap_service)

1. **Copy installer tarball** — SCP from the existing AAP host (`/opt/sources/*.tar.gz`) directly to the new VM. The tarball is 3.8 GiB. Both hosts are on the internal network. Run `scp` on the existing AAP host targeting the new VM's IP.
2. **Extract tarball** — `unarchive` on the new VM
3. **Template the inventory** — `template` module with `inventory.j2`
   - All host groups point to the new VM's hostname
   - `ansible_connection=local`
   - All passwords from vault variables
   - Registry credentials from vault
   - `bundle_install=true`, `bundle_dir` pointing to extracted bundle
   - MCP enabled with `mcp_allow_write_operations=true`
4. **Run the installer** — `command: ansible-playbook -i inventory ansible.containerized_installer.install`
   - This takes ~10-20 minutes
   - Runs as `aap_service` user (rootless podman)

### Step 4: Nginx Reverse Proxy (Play 4 — targets: hypervisor)

1. **Template nginx config** — server block for the test AAP
2. **Reload nginx** — `systemctl reload nginx`

**Domain approach — use a subdomain**, not a path:
- AAP's Envoy gateway expects to own the domain root; path-based routing breaks it
- New subdomain: parameterized, e.g., `{{ aap_test_subdomain }}.{{ domain }}`
- The Let's Encrypt cert would need a new SAN — or for test purposes, use nginx `proxy_ssl_verify off` to the backend's self-signed cert, and the frontend can share the existing wildcard or get a new cert
- Nginx reverse proxy is **required** — VMs are on an internal libvirt network, only the hypervisor has a public IP. External access requires nginx on the hypervisor forwarding to the VM, same as the existing AAP setup.

---

## Credential & Secret Handling

All secrets live in `automAIton/myvars` (shared vault). The playbook loads it via `vars_files: ["{{ vault_file }}"]`.

**Required variables in myvars** (same names as the current AAP inventory):

| Variable | Purpose |
|---|---|
| `registry_username` | Red Hat registry service account |
| `registry_password` | Registry service account token |
| `postgresql_admin_password` | PostgreSQL admin password |
| `gateway_admin_password` | Gateway admin password |
| `gateway_pg_password` | Gateway PostgreSQL password |
| `controller_admin_password` | Controller admin password |
| `controller_pg_password` | Controller PostgreSQL password |
| `hub_admin_password` | Hub admin password |
| `hub_pg_password` | Hub PostgreSQL password |
| `eda_admin_password` | EDA admin password |
| `eda_pg_password` | EDA PostgreSQL password |
| `automationmetrics_pg_password` | Metrics PostgreSQL password |
| `automationmetrics_controller_read_pg_password` | Metrics controller read PG password |
| `rhsm_activation_key` | RHEL subscription activation key |
| `rhsm_org_id` | RHEL subscription org ID |
| `godaddy_api_token` | GoDaddy API token for DNS records |
| `domain` | Domain name |
| `public_ip` | Hypervisor's public IP |
| `ssh_pubkey_path` | Path to SSH public key on hypervisor |
| `installer_path` | Path to installer tarball on source AAP |
| `source_aap_host` | SSH alias for existing AAP host |

### `main.yml` (committed — non-sensitive defaults)

```yaml
# VM sizing
aap_vcpus: 4
aap_memory_mb: 20480
aap_disk_size: "60G"

# AAP installer
aap_version: "2.7-8"
aap_version_short: "v27"
installer_extract_dir: "/opt/sources"

# AAP services config
redis_mode: standalone
hub_seed_collections: false
controller_percent_memory_capacity: 0.5

# Golden image
golden_image_path: "/opt/images/rhel-9.8-updated-golden.qcow2"

# Network
vm_network: "internal"
vm_dir: "/opt/vms"

# MCP
mcp_allow_write_operations: true
```

---

## Version Registry (`version-registry.yml`)

```yaml
# Tracks deployed AAP test instances
# Updated manually or by the playbook after successful deployment
deployments: []
# Example entry:
#   - version: "2.7-8"
#     vm_name: "aap-v27-testvm"
#     deployed_date: "2026-10-01"
#     ip: "<assigned by DHCP>"
#     status: active
```

---

## Key Design Decisions

1. **KISS: Single playbook, multi-play** — not a role galaxy. One `deploy-test-aap.yml` with 4 plays. Post-install AAP configuration (projects, credentials, JTs) is handled separately.

2. **Bundle install, not online** — copy the existing 3.8G tarball rather than downloading from registry. Faster, no internet dependency, reproducible.

3. **Subdomain + nginx required for external access** — VMs are on internal libvirt network, only the hypervisor has a public IP. Nginx reverse proxy is mandatory, same as the existing AAP setup.

4. **Vault for ALL secrets** — passwords, registry creds, hostnames, IPs. The repo contains zero environment-specific values.

5. **Golden image as base** — skip RHEL update on every deploy. Subscribe only to enable AAP repo, not for general updates.

6. **Extend deploy_vms.yml minimally** — add `disk_size` support (one task). Don't rewrite it.

7. **Installer copy via SCP from the existing AAP host** — direct SCP from the existing AAP host to the new VM over the internal network.

8. **Filesystem grow after clone** — golden image is small (~10G), resize to 60G at clone time, grow XFS on first boot.

---

## Verification

1. **VM boots**: `virsh list` on hypervisor shows new VM running
2. **SSH works**: `ansible -m ping` against new VM succeeds
3. **AAP accessible**: `curl -k https://<new-ip>` returns the AAP login page
4. **API works**: `curl -k -u admin:<password> https://<new-ip>/api/controller/v2/ping/` returns 200
5. **MCP works**: `curl -k -X POST https://<new-ip>:8448/mcp` returns 405 (TLS works, POST expected)
6. **Post-install objects**: Job templates, credentials, projects exist in the new AAP

---

## Decisions Made

1. **No subscription manifest needed** — Red Hat defaults to SCA (Simple Content Access). The containerized installer pulls images using a registry service account (username/token in vault), not a manifest file.

2. **Full stack** — deploy all components (Gateway, Controller, EDA, Hub, MCP, Metrics) to match the production setup and support AIOps demo testing.

3. **Subdomain over path** — AAP's Envoy proxy owns the domain root, so path-based routing (`/test-vX`) won't work. Use a parameterized subdomain instead.

---

## Resolved

- **Subscription for AAP repo**: Subscribe using activation key + org ID from vault (`rhsm_activation_key`, `rhsm_org_id`), enable AAP repo, install ansible-core, then unsubscribe after install completes.
