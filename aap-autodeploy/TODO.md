# AAP AutoDeploy TODOs

- [ ] Sanitize variable names across playbooks and vault — establish a consistent naming convention (e.g., decide on `vault_` prefix vs no prefix, `password` vs `passwd`, snake_case consistently)
- [ ] Clean up duplicate credentials (ids 9, 10 — empty "hypervisor cred" entries) in AAP UI
- [ ] Clean up temp host "golden-image-temp" (host 11) from AAP inventory
- [ ] Delete temp JT 29 ("TEMP - Configure AutoDeploy JTs") from AAP UI
- [ ] Destroy leftover test VMs: aap27-test-10 (192.168.42.177), aap27-test-11 (192.168.42.134)
- [ ] End-to-end test: run full sequence 01→02→03→04
