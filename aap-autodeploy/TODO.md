# AAP AutoDeploy TODOs

- [ ] Sanitize variable names across playbooks and vault — establish a consistent naming convention (e.g., decide on `vault_` prefix vs no prefix, `password` vs `passwd`, snake_case consistently)
- [ ] Clean up duplicate credential (id 10, empty "hypervisor cred" without organization) created by MCP
- [ ] Clean up temp host "golden-image-temp" (host 11) from AAP inventory
- [ ] Remove `deploy-test-aap.yml` utility playbook after JT configuration is done
- [ ] End-to-end test: run full sequence 01→02→03→04
