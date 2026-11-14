# Shared RHEL VM deployment

Source version **0.0.2**. The canonical creator lives in
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

Focused tests, syntax and strict lint passed on Core 2.20.10. The relocated source
has not completed AAP end-to-end acceptance; caller migration remains unfinished.
See the [operator guide](docs/generic-rhel-vm-deployment.md) for inputs, safety,
verification and partial-failure handling. Existing consumers must qualify their
replacement before removing the Assistant copy.
