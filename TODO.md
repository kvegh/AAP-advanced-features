# TODO

Open items after the 2026-10-05 split of this monorepo into an umbrella repo
plus one repository per project, wired in as submodules.

## Blocking a clean demo run

- [ ] **Test-run every split repo.** Nothing has been exercised since the split.
      Syntax checks pass; no playbook has actually run.

- [ ] **Move `myvars` into `aap_autodeploy_configascode`.** Its playbooks load
      `../myvars`, which resolved to the umbrella root when that was the AAP
      project. Now the repo itself is the project root, so `..` points outside
      the project and the vault file is not found. Only this repo uses it, so
      it is a move, not a copy:

          git mv myvars aap_autodeploy_configascode/myvars
          ../myvars     → myvars      # 01-vm-setup, 02-infra-config,
                                      # 03-aap-install (×3), 04-aap-config,
                                      # destroy-test-aap
          ../../myvars  → ../myvars   # utils/tag_jts.yml

- [ ] **Review vault files across all repos.** They are no longer one shared
      file and their contents differ per project. Work out which repo needs
      which keys. Note a vault credential on a job template only supplies the
      decryption password — not the file, and not the variables.

- [ ] **`AIOps_selfhealing_demo` has no `playbooks/myvars`.** Only
      `myvars.example` is committed, so `deploy_zabbix_agent.yml` cannot run
      from this repo. Currently dormant: the job template that deploys agents
      runs a different copy from another project.

## Before adding more AAP projects

- [ ] **`ServiceNow-ITSM-Integration/collections/requirements.yml` will break
      project sync.** At a repo root AAP runs `ansible-galaxy install` against
      it, and `community.zabbix` is neither in the execution image nor on the
      configured galaxy server. Same failure the orchestrator repo hit. Either
      sync the collection to private automation hub, or move the file off the
      magic path as was done there.

- [ ] Projects are only needed for repos AAP actually runs playbooks from.
      `ServiceNow-ITSM-Integration` (no playbooks yet), `config_exceptions_ng`
      (no job template) and `intelligent-assistant` (docs only) have none.

## Cleanup

- [ ] **Retire the old AAP project** that pointed at this repo for the
      autodeploy and orchestrator playbooks. Its job templates were re-pointed
      at the new per-repo projects, so it now has none attached.

- [ ] **`config_exceptions_ng` is duplicated** — this repo's copy and an older
      one inside the predecessor monorepo. Decide which is canonical and
      retire the other.

- [ ] **Predecessor monorepo holds superseded generations** of the deploy and
      self-healing playbooks. Decide whether to retire them.

## Authentication investigation

- [ ] **Verify MCP port 8448 is inaccessible externally.** On 2026-10-06,
      `https://aap.supercorp.at:8448/mcp` responded to an internal MCP request
      with HTTP 401. Standard HTTPS port 443 served HTML and rejected the MCP
      POST, so no MCP exposure was found there. Only 443 is intended to be
      exposed externally; confirm firewall/proxy rules and test 8448 from an
      external network. Internal hostname reachability does not establish
      Internet exposure. If unintended exposure is found, restrict it while
      preserving intended private MCP access.

- [ ] **Understand the MCP-to-AAP authentication boundary.** On 2026-10-06,
      the bearer token configured for the `aap-mcp` connection was also accepted
      directly by the AAP controller API for reads and writes (project #34 and
      job template #35). This contradicts the earlier assumption that the
      stored API token was read-scoped; verify whether that note referred to
      a different token. Do not record token values in investigation output.
      Inspect the MCP server implementation and deployment configuration to
      establish whether it forwards the client's token, uses a separate AAP
      credential, or shares authentication with AAP. Identify the token issuer,
      associated identity, scope, expiry, and intended audiences. Explain why
      direct API access succeeds and whether MCP-only client authentication is
      intended. Document the actual authentication flow and any changes needed
      to enforce the intended boundary; do not rotate credentials or change
      access controls as part of discovery without explicit authorization.

## Project synchronization performance

- [ ] **Reduce collection installation delays during project synchronization.**
      Windows demo retries on 2026-10-06 repeatedly ran collection installation
      from `collections/requirements.yml`. One project update took about 48
      seconds, followed by an execution-node content sync lasting over 100
      seconds. Measure Git fetch, Galaxy installation, queueing, and content
      transfer separately to identify the actual bottleneck.
      Investigate a nonzero project cache timeout, disabling update-on-launch
      with explicit synchronization after pushes, and baking pinned collections
      into execution environments. Also investigate whether collection downloads
      can be avoided or limited during project sync without losing required
      dependencies. Check controller-wide versus per-project settings before
      changing them, and preserve reliable use of the intended Git revision.

## Ongoing discipline

- Submodules pin a commit. After pushing a child repo, bump the pointer here:

      git -C <project> pull
      git add <project> && git commit -m "bump <project>"

- Unscrubbed pre-split history lives in a private archive repo, including the
  previous standalone self-healing repo on its own branch. Do not merge it back.

## Central CMDB and inventory source

- [ ] Put a central CMDB/inventory source in place, either dynamically discovered
      or statically maintained. Define the authoritative source for VM identities,
      hostnames, roles, lifecycle, hypervisors, NIC MACs/names, networks, addresses,
      and AAP connection settings.
- [ ] Distinguish permanent infrastructure with stable assignments from ephemeral
      test deployments. Discover or register new deployments and retire their
      records when removed; ephemeral VMs do not require permanent IP reservations.
- [ ] Decide how AAP inventory, VM deployment inputs, and network configuration
      consume this source. The vaulted network YAML is an initial reference record,
      not yet a live CMDB or automated inventory integration.
- [ ] Keep sensitive/environment-specific values Vault-encrypted or in a protected
      external system; never commit plaintext credentials or infrastructure mappings.
