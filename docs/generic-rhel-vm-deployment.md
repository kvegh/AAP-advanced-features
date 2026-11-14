# Generic RHEL VM deployment

Source version **0.0.4** provides the shared basic VM creator at
[`playbooks/deploy_generic_linux_vm.yml`](../playbooks/deploy_generic_linux_vm.yml).
Application code remains in its own project. The original Assistant creator
supplies the implementation being relocated; this source removes its dependency
on Assistant authentication files and its application-specific image cleanup.

## Scope and image selection

The intended target is one RHEL 9 x86_64 guest on an existing libvirt/KVM
hypervisor, using a standalone QCOW2 source with an operator-verified SHA256.
The source image is preserved. The guest disk uses the supported last-partition
GPT/XFS layout. Other guest storage layouts and non-KVM platforms are outside
this initial scope.

| Use | Image selected in protected configuration | Mode | Update policy |
| --- | --- | --- | --- |
| General RHEL VM | Original RHEL 9.8 KVM image | `generic_image: true` | Defaults to enabled |
| Sniper patch-test VM | Original RHEL 9.4 KVM image | `generic_image: true` | `update_packages: false` |
| AAP VM | Prepared image retaining its AAP installer bundle | `generic_image: false` | Explicit caller choice |

Image filenames are not inferred from the requested use. The protected
configuration supplies the exact path and checksum. Prepared mode preserves
existing accounts, login/sudo configuration, installer and application content;
both modes reset only the new clone's machine and SSH identity. Upstream mode
also creates its selected bootstrap account offline. Cloud-init package updates
and upgrades are disabled; Ansible alone applies the selected update policy.
When updates are disabled, the entire RHSM/package update role is skipped.

Zabbix is an appliance and remains on its existing separate image-cloning path.
Application installation, DNS/proxy/TLS publication, Satellite registration,
content configuration, snapshot/rollback and isolated recovery are not functions
of this creator.

## Inputs and prerequisites

Use the existing supported Core 2.20 EE and an inventory where the Ansible
pattern `hypervisor` selects exactly one host. A host named `hypervisor` or a
single-member group works; zero or multiple matches are refused before SSH.
Hypervisor connection settings must match the protected pin.
Existing privilege escalation and network access must already work; this source
does not install controller dependencies or change SSH trust settings.
For prepared images, omitting `guest_become_password` preserves the existing
Machine credential or inventory escalation setting. The creator does not infer
passwordless sudo or substitute the SSH password. An explicitly provided
separate password remains exact; upstream-image bootstrap still requires its
existing matching login/sudo password contract.

The hypervisor needs its maintained libvirt, QCOW2, libguestfs and cloud-init seed
tools. The guest needs Python, sudo and the documented GPT/XFS native utilities.
Network DHCP discovery and the selected bridge must be available. Updates also
require reachable RHEL repositories and existing protected RHSM registration
inputs when the image is unregistered. See the role documentation for details:
[`linux_vm`](../playbooks/roles/linux_vm/README.md),
[`linux_guest`](../playbooks/roles/linux_guest/README.md),
[`linux_root_growth`](../playbooks/roles/linux_root_growth/README.md) and
[`linux_updates`](../playbooks/roles/linux_updates/README.md).

The file bound by `generic_linux_vm_config_file` must be an absolute readable
regular file containing the Vault-encrypted `provisioning` mapping. The existing
`AC_AGENTS_ENVIRONMENT_VAULT_FILE` credential binding is also recognized.
There is no implicit lookup in a sibling secrets checkout. Attach the matching
existing Vault credential; do not put a password in launch variables or code.

| Input | Meaning |
| --- | --- |
| `provisioning.golden_image_path`, `source_image_sha256` | Exact source path and 64-character lowercase SHA256 |
| `provisioning.vm_name`, `vm_domain`, `vm_dir` | Default name, guest DNS domain and destination directory |
| `provisioning.vm_network`, `network_bridge` | Exact libvirt network and its expected bridge |
| `provisioning.hypervisor_pin` | Address, non-root user, port, machine ID and public SSH host keys |
| `provisioning.guest_ssh_user`, `guest_ssh_password` | Existing protected bootstrap access |
| `provisioning.guest_become_password` | Existing separate escalation password, when needed |
| `provisioning.rhsm_org`, `rhsm_activation_key` | Existing registration inputs when updates require registration |
| `provisioning.generic_image` | Boolean: true for an upstream image, false for a prepared image |
| `provisioning.update_packages` | Optional boolean, defaults to true |
| `vm_name`, `vm_hostname` | Optional VM-name and guest-hostname overrides |
| `vm_vcpus`, `vm_memory_mb`, `vm_disk_gb` | Resource overrides; defaults 2 CPU, 4096 MiB, protected disk size or 20 GiB |

An optional `linux_vm_upstream` mapping carries only the documented routing,
image, checksum, pin and update selections. Credential overrides are refused.
It exists for application resource owners to pass their selected fresh VM route.

For an independently verified existing allocation, the resource owner instead
supplies `linux_vm_existing_route` with exactly `vm_name`, `vm_dir`, `vm_domain`,
`vm_network`, `network_bridge` and `hypervisor_pin`, together with strict
`generic_linux_vm_create: false`. This route adds no image or credential values;
the mounted encrypted file may contain only the existing guest bootstrap access.
Both routing maps together, unexpected keys and existing-route input with
creation enabled are refused. Name, resources and target pin are checked on both
paths; image path and checksum are mandatory only for fresh creation.

All actual settings remain in protected CaC; the shared public source has no
environment defaults or private companion fallback.

## AAP integration and execution

The approved base-CaC integration adds a shared umbrella Project and a generic
RHEL deployment Job Template. Its minimal VM-only file credential contains the
encrypted settings file and uses the existing Vault password. It does not need
Assistant application authentication snapshots or a new secret store.
The shared Project, Job Template and credential type have been created and
read back, with their definitions captured in the existing private base CaC.
Repeat reconstruction from that capture and migration of existing callers remain
unfinished. The shared importer remains the only CaC import route.

The generic template must accept the caller's inventory, required credentials
and VM inputs, and execute the complete playbook. Leave job tags and skip-tags
empty. Partial provisioning and guest-only execution are rejected before remote
actions. Explicitly skipping `always` skips all work and produces no artifact.

For an authorized command-line execution using an already available compatible
runtime, supply an operator-owned inventory and protected configuration:

```sh
ansible-playbook -i inventory.yml playbooks/deploy_generic_linux_vm.yml \
  --vault-password-file /protected/existing-vault-password \
  -e generic_linux_vm_config_file=/protected/vm-settings.vault
```

AAP's five logical stages are resource reservation/image preparation, this
shared creator, registration plus infrastructure, AAP installation, and base
CaC. Its owner verifies an existing allocation before requesting the shared
creator's explicit no-creation path. The existing complete Assistant and
isolated recovery flows retain their current dependencies until their migration
is qualified.

## Results, repeat execution and failures

The full successful creation publishes `generic_linux_vm`, including verified
guest/native identity, resources, hostname, source hash and update outcome.
Do not treat a launch acknowledgement or partial task success as that result.

`generic_linux_vm_create: false` is a strict boolean. It validates inputs locally,
performs no hypervisor or guest action and publishes only
`generic_linux_vm_creation` with `skipped: true` and `created: false`.
It does not verify or adopt an existing VM. The resource owner must provide its
own independently verified existing-allocation result. A legacy owner must keep
an unknown original image checksum unknown rather than substituting today's hash.

Fresh creation refuses an existing domain or destination disk. It is not an
idempotent desired-state updater for existing VMs. After interruption or partial
failure, inspect the exact owned resources and last native job result before
another action. Do not relaunch blindly, overwrite a destination or remove a
partial guest automatically. Check mode stops after safe preflight before disk
creation; it does not prove customization, boot or guest access.

## Verification and acceptance status

The 0.0.4 source passed all 29 existing shared regression methods; the paired
AAP candidate passed seven affected methods and three actual producer/consumer
contract methods, for 39 distinct passing tests. Both entrypoint syntax checks
passed using actual Core **2.20.10** in the cached AAP 2.7 minimal EE:
`registry.redhat.io/ansible-automation-platform-27/ee-minimal-rhel9@sha256:aea45867ebbfcb57bba69b3b6e33542dbbe95f237dfdf35e8b68773b4f3268f8`.
Local image ID was
`6ac3ae57346f0900fab85077798225c3498793084662a3a9ee2a14dd5f0dc3a6`.
Strict production lint separately passed with ansible-lint **26.8.0** on the
development host's Core **2.16.19**. That lint result does not establish complete
target-Core compatibility or replace the actual Core 2.20 syntax/tests.
The first native AAP attempt stopped at local validation because the earlier
check required a group and rejected a valid named host. The correction uses the
same native host-pattern lookup as the play; it changes no inventory or SSH
policy. A subsequent native AAP job on exact source 0.0.3 completed fresh
creation with a verified-result artifact and reported package updates.
Independent post-job identity, RPM, storage and unrelated-resource checks plus
test cleanup remain unfinished. That job does not verify the later owner-route
repair, prepared-image deployment or no-update Sniper deployment from this source.

The 0.0.4 cross-project fixtures pass actual AAP owner output through the actual
shared entrypoint with only encrypted bootstrap settings. They preserve the
owner's null/unknown legacy image checksum, prove no SSH or image action for
false creation and reject malformed, mixed, credential-bearing and fresh routes
without image inputs. Full shared regression qualification took 142.115 seconds;
the seven existing AAP methods took 25.429 seconds. Independent bounded source
review found the owner-contract defect resolved, with no remaining concrete
finding in that delta. These are fixture and source checks, not live reuse proof.

Tests cover protected-file loading, routing/pin/hash/bridge failures, image-mode
behavior, explicit no-creation truthfulness, partial-tag refusal, existing-disk
preservation and root-growth behavior. Independent source re-review confirmed
the partial-tag safety repair. These tests use fixtures and do not create a VM.

Repeat the focused suite in an existing compatible environment with:

```sh
python3 -m unittest discover -s tests -p 'test_generic_linux_vm*.py'
ansible-playbook -i localhost, playbooks/deploy_generic_linux_vm.yml --syntax-check
ansible-lint --offline --profile production --strict playbooks/
```

Do not install or upgrade dependencies as part of those commands. Final AAP
acceptance, independent final guest/storage verification, test cleanup,
CaC reconstruction/repeat apply, full per-directive review and APME coverage
remain unfinished. Prepared-image and no-update live acceptance have not been
performed through this relocated source. No completed review report or functional
acceptance is claimed. Publication makes source available for the remaining integration and
AAP tests; it does not establish deployment or justify deleting an active caller.

The required AAP acceptance starts with an absent authorized test VM and uses
the shared Project/JT plus protected inputs. It must verify the selected image,
actual guest identity/access/resources/storage, update choice, final completion,
source-image preservation and preservation of unrelated guests. The Sniper
variant must preserve its unpatched baseline; prepared mode must retain the AAP
installer and original access behavior. Existing-owner reuse must create nothing
and pass the owner's independent checks. Keep those results separate from
focused fixture evidence and existing jobs run from Assistant source.
