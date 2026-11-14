# linux_vm

Create one guarded Linux QCOW2 clone on a libvirt/KVM hypervisor. The canonical
entrypoint is `playbooks/deploy_generic_linux_vm.yml`.

## Inputs

The existing encrypted file supplies `provisioning`: image path, destination
directory, VM domain/network/name and guest bootstrap SSH/become values. Resource
overrides remain `vm_name`, `vm_vcpus`, `vm_memory_mb` and `vm_disk_gb`.
`vm_hostname` selects a validated guest DNS hostname independently of the libvirt
VM name; it defaults to `vm_name.vm_domain`. Prepared AAP clones can therefore
retain their existing public FQDN. Verification checks the configured hostname
without requiring DNS publication, and artifacts retain that hostname.

Both image modes require an exact
`source_image_sha256`, `network_bridge` and the existing `hypervisor_pin`
(address, non-root user, port, machine ID and public host keys). An optional
`linux_vm_upstream` mapping can select the same non-credential routing fields;
it cannot replace bootstrap access. For an upstream KVM image, set `generic_image: true`; the new clone receives the
protected bootstrap account offline. For an installer-bearing prepared image,
set `generic_image: false`; the new clone retains its existing login, accounts,
installer bundle and application content. Both modes reset machine/SSH identity
and inject freshly generated public host identity without network access. The
optional historical `linux_vm_upstream` image-route mapping accepts either mode.
No assistant-specific installer or account cleanup is performed.

The operator-owned encrypted configuration selects the default original RHEL 9.8
KVM image. Sniper patch test clients explicitly select the RHEL 9.4 image and
`update_packages: false`. Other deployments default to package updates enabled;
`provisioning.update_packages` is an optional boolean. Cloud-init package updates
and upgrades are always disabled for fresh upstream clones so the Ansible update
stage alone applies that choice. AAP platform installation remains a separate
workflow and keeps its installer-bearing golden image.

## Safety and outcomes

The role refuses an existing domain or destination disk, requires a standalone
upstream image and verifies its expected hash before copying and customizing the
new clone. It verifies pinned hypervisor identity/network, bootstraps guest access
offline, creates fresh host keys and pins both SSH hops. Verification reports
identity, resources, source hash and whether Ansible completed updates.

Run the complete entrypoint without task tags or skip-tags. Partial provisioning
or guest-only execution is unsupported and rejected before managed-host work.
All plays share the always tag; explicitly skipping always skips every action
and produces no verification artifact. There is no domain-description resume or
existing-disk import path.

Creation remains fresh-only: an existing domain or disk is refused. A resource
owner must verify and reuse its existing VM without invoking creation; there is
no overwrite or implicit-adoption switch.

`generic_linux_vm_create` is a strict boolean, defaulting to true. Explicit false
validates the mounted configuration and requested routing locally, skips every
hypervisor/guest action and emits only `generic_linux_vm_creation` with
`skipped: true` and `created: false`. It emits no `generic_linux_vm` verification
artifact and establishes no existing-VM proof. The resource owner must validate
its previously owned result independently; a workflow may retain that owner's
prior artifact. False never adopts, overwrites, starts or verifies a VM.

This is normal deployment. It does not read recovery source credentials,
reconcile firewall/CaC policy, release isolation, install an application, or
register the guest to a Satellite. Existing isolated recovery remains with its
current owner. Creation is one-shot; investigate partial results before retrying.
Check mode stops before disk creation after safe preflight.

## Supporting tools

Existing libvirt and libguestfs CLI operations are retained from the maintained
creator: the current runtime uses their disk inspection, guarded offline QCOW2
customization, import and exact DHCP/native identity interfaces. This relocation
does not add a collection or tooling installation. Ansible's file/copy/stat,
assert, fact, connection and package modules handle the surrounding automation.

The small identity filter validates the pinned SSH keys, network XML and saved
native provenance used by those interfaces; it is not a transport or secret
store. Its historical `linux_vm_recovery_*` filter names are retained to limit
migration churn, while this entrypoint exclusively requests normal provenance.
The offline shell templates reset only the new clone's identity/access. The
root-growth role separately documents its GPT/XFS helper.

Dependencies must already exist on the authorized controller/hypervisor/guest.
Focused synthetic tests exercise the source interfaces and safety boundaries.
They do not establish final AAP end-to-end acceptance of the relocated source.
