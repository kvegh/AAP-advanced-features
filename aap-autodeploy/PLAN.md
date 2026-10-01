# AAP AutoDeploy Plan

## Context

We need a repeatable, fully automated way to deploy fresh AAP 2.7 instances for testing. Currently there is no automation for the AAP platform install itself — only VM provisioning (`deploy_vms.yml`) and post-install configuration (`aap_deploy/` playbooks) exist separately. This project bridges the gap: from golden image clone to a fully working AAP test instance, driven entirely by Ansible.

All playbooks and docs go in `AAP-advanced-features/aap-autodeploy/`. The VM deployment playbook stays in `automAIton`. No sensitive data (passwords, tokens, IPs, hostnames) in the repo — everything parameterized via vault.

---

## Architecture Overview

```
Golden Image (RHEL 9.8 qcow2 with aap_service user, installer pre-staged)
    |
    v
[1] Clone + resize disk + virt-customize hostname + virt-install on hypervisor
    |
    v
[2] Prepare host: grow filesystem, subscribe, install ansible-core, unsubscribe
    |
    v
[3] Customize inventory hostname, set bundle vars, run AAP installer
    |
    v
[4] Configure DNS + nginx reverse proxy on hypervisor for external access
```

---

## Deliverables

### Files in `AAP-advanced-features/aap-autodeploy/`

```
aap-autodeploy/
  deploy-test-aap.yml          # Main orchestration playbook (multi-play)
  templates/
    nginx-aap-test.conf.j2     # nginx reverse proxy config for test instance
  vars/
    main.yml                   # Non-sensitive defaults (ports, sizing, paths)
  version-registry.yml         # Tracks AAP version -> VM name mapping
myvars                         # Vault-encrypted secrets (repo root)
```

Inventory handling: copy from source AAP host, search-and-replace hostname. No template needed.

Secrets come from `myvars` in the repo root (vault-encrypted).

### Changes to `automAIton/deploy_vms/deploy_vms.yml`

Add `disk_size` variable support for `qemu-img resize` after copy (needed for AAP's 60G disk). Minimal change to existing playbook.

---

## Step-by-Step Design

### Step 1: VM Creation (Play 1 — targets: hypervisor)

Reuse the existing `deploy_vms.yml` with extended parameters:
- VM naming pattern: `aap{{ aap_version_short }}-{{ vm_suffix }}-{{ counter }}` (e.g., `aap27-test-1`)
- The same name is used as VM name, hostname, and DNS subdomain for consistency.
- `vcpus`: `4`
- `memory`: `20480` (20 GiB)
- `base_image`: path to golden image (not the raw RHEL base)
- `disk_size`: `60G` (new parameter — qemu-img resize after copy)

**Extend `deploy_vms.yml`**: Add a task between "Copy base image" and "Customize VM images" that runs `qemu-img resize` when `disk_size` is defined. One line addition; backwards compatible.

VM naming: `aapX-test-N` where X is the version and N is the counter (e.g., `aap27-test-1`).
Hostname: matches VM name (`aap27-test-1.supercorp.at`).

### Step 2: Host Preparation (Play 2 — targets: new VM via dynamic inventory)

After the VM boots and gets a DHCP IP:

1. **Wait for SSH** — `wait_for_connection`
2. **Grow the filesystem** — `growpart` + `xfs_growfs` to use the resized disk
3. **Subscribe to RHEL and enable AAP repo** — `redhat.rhel_system_roles.rhc` role with activation key (from vault)
4. **Install ansible-core** — `dnf install ansible-core`
5. **Unsubscribe from RHEL** — clean up subscription after install

The `aap_service` user, sudo, linger, SSH authorized_keys, and the AAP installer bundle are all pre-staged in the golden image.

### Step 3: AAP Installation (Play 3 — targets: new VM as aap_service)

The installer is already unpacked in the golden image at `/opt/sources/ansible-automation-platform-containerized-setup-bundle-2.7-8-x86_64/`.

1. **Customize the inventory** — search-and-replace hostname from source AAP FQDN to new VM's FQDN
2. **Set bundle install vars** — add `bundle_install=true` and `bundle_dir` to inventory
3. **Run the installer** — `command: ansible-playbook -i inventory ansible.containerized_installer.install`
   - This takes ~10-20 minutes
   - Runs as `aap_service` user (rootless podman)

### Step 4: Nginx Reverse Proxy (Play 4 — targets: hypervisor)

1. **Template nginx config** — server block for the test AAP
2. **Reload nginx** — `systemctl reload nginx`

**Domain approach — use a subdomain**, not a path:
- AAP's Envoy gateway expects to own the domain root; path-based routing breaks it
- New subdomain: matches VM name, e.g., `aap27-test-1.{{ domain }}`
- The Let's Encrypt cert would need a new SAN — or for test purposes, use nginx `proxy_ssl_verify off` to the backend's self-signed cert, and the frontend can share the existing wildcard or get a new cert
- Nginx reverse proxy is **required** — VMs are on an internal libvirt network, only the hypervisor has a public IP. External access requires nginx on the hypervisor forwarding to the VM, same as the existing AAP setup.

---

## Credential & Secret Handling

All secrets live in `myvars` (vault-encrypted, in the repo root). The playbook loads it via `vars_files: [../myvars]`.

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
aap_version_short: "27"   # used in naming: aap27-test-N
installer_extract_dir: "/opt/sources"

# AAP services config
redis_mode: standalone
hub_seed_collections: false
controller_percent_memory_capacity: 0.5

# Golden image
golden_image_path: "/opt/vms/goldimg-vm-1.disk.qcow2"

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
#     vm_name: "aap27-test-1"
#     deployed_date: "2026-10-01"
#     ip: "<assigned by DHCP>"
#     status: active
```

---

## Key Design Decisions

1. **KISS: Single playbook, multi-play** — not a role galaxy. One `deploy-test-aap.yml` with 4 plays. Post-install AAP configuration (projects, credentials, JTs) is handled separately.

2. **Bundle install, not online** — copy the existing 3.8G tarball rather than downloading from registry. Faster, no internet dependency, reproducible.

3. **Subdomain + nginx required for external access** — VMs are on internal libvirt network, only the hypervisor has a public IP. Nginx reverse proxy is mandatory, same as the existing AAP setup. Subdomain = VM name (e.g., `aap27-test-1`).

4. **Vault for ALL secrets** — passwords, registry creds, hostnames, IPs. The repo contains zero environment-specific values.

5. **Golden image as base** — pre-updated RHEL 9.8 with `aap_service` user (sudo, linger, hypervisor SSH key), and the AAP installer bundle unpacked under `/opt/sources/`. Subscribe only to enable AAP repo and install ansible-core, not for general updates.

6. **Extend deploy_vms.yml minimally** — add `disk_size` support (one task). Don't rewrite it.

7. **Installer pre-staged in golden image** — eliminates the slow SCP transfer step entirely. The unpacked bundle (~3.5 GiB) is baked into the golden image.

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
