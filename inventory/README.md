# Demo network inventory

`demo_network_inventory_vault.yml` is an Ansible Vault-encrypted YAML record of
VM identities, guest interface names, MACs, network membership, addresses, DHCP
reservations, and pending assignments across the umbrella demo environment.
It is a reference data file, not an executable Ansible inventory or playbook.

Observed assignments and proposed Windows assignments are explicitly separated
by status fields. Unknown values remain null, with status fields distinguishing
unknown gateways from confirmed or desired absence of a gateway. Additional
addresses are retained pending review. Nothing in this file changes live networks.

View it using a password file stored outside Git:

```bash
ansible-vault view inventory/demo_network_inventory_vault.yml \
  --vault-password-file /secure/vault-password-file
```

Edit through `ansible-vault edit` with the same credential. Do not commit decrypted
copies, password files, or rendered tables containing environment values. The
record needs additional guest discovery and confirmation before all assignments
can be considered permanent. Update the record as reservations and fixed VM MACs
are applied.
