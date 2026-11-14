# Shared RHEL VM deployment

Source version **0.0.4**. The canonical creator lives in
[`playbooks/deploy_generic_linux_vm.yml`](playbooks/deploy_generic_linux_vm.yml).
Application submodules have independent versions and workflows.

| Caller | Selected image | Package updates |
| --- | --- | --- |
| General RHEL VM | Original Red Hat RHEL 9.8 KVM | Enabled by default |
| Sniper patch-test client | Original Red Hat RHEL 9.4 KVM | Explicitly disabled |
| AAP | Prepared image containing the AAP installer | Selected by AAP configuration |

The creator validates the protected target, original image checksum and network,
creates one fresh clone, verifies guest identity/access/resources, grows the
supported root filesystem and applies the selected update policy. It refuses an
existing destination. Run the whole playbook without tags or skip-tags.

Supply the encrypted VM configuration through the approved AAP file credential
and existing Vault credential. Image paths, checksums, host pins and access
values belong there. No application login snapshots are required.

AAP retains resource reservation before this creator and registration,
infrastructure, installation and base configuration afterward. Zabbix stays on
its existing appliance-cloning path. Satellite registration and patching are
separate from basic VM creation.

Existing AAP owners may supply a separate six-field route with strict
`generic_linux_vm_create: false`. That path validates locally, creates nothing
and supplies no new VM-verification or historical image-checksum claim.

A general-image AAP creation job passed on source 0.0.3. Independent final
verification and test cleanup remain unfinished; caller migration and complete
AAP acceptance are still pending. The 0.0.4 owner-route fix passed 39 tests
across the shared/AAP contract, both syntax checks and separate development-host
strict lint. Existing live callers have not adopted this repair.
See the [operator guide](docs/generic-rhel-vm-deployment.md) for inputs, safety,
verification and partial-failure handling. Existing consumers must qualify their
replacement before removing the Assistant copy.
