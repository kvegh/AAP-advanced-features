# TODO — umbrella repo

Tasks for this repository itself: the submodule index, the shared root files,
and the documentation describing them. Per-project work belongs in each
project's own repo.

Open since the 2026-10-05 split of the predecessor monorepo into an umbrella
repo plus one repository per project, wired in as submodules.

## 0. Re-read and clarify the umbrella structure and documentation

The README no longer matches what the repo contains. Re-read both, decide what
this repo is *for*, then make the docs say that. Known discrepancies:

- [ ] **"This repo holds no project files" is false.** `README.md:6` says the
      umbrella holds only the index and submodule pointers. The root also
      carries `myvars`, `roi_demo.yml`, `ansible.cfg`, `inventory/` and
      `design_decisions_history.md`. Either the sentence is wrong or those
      files are in the wrong place — decide which.

- [ ] **`inventory/` is undocumented.** It holds `README.md` and a 41 KB
      `demo_network_inventory_vault.yml`. Not mentioned anywhere in the
      umbrella README, and its relationship to the planned CMDB work is
      unstated.

- [ ] **`roi_demo.yml` is an orphan playbook at the root.** No project owns it.
      Decide whether it moves into a submodule or is retired.

- [ ] **`collections/` is empty and untracked.** Leftover from the monorepo
      layout. Remove it or document why it must exist.

- [x] ~~**The Secrets section goes stale with the `myvars` move.**~~ Done
      2026-10-17 alongside task 1: the section now states that each project
      keeps its own vault file at its own repo root, and why.

- [ ] **`README.md:11-14` carries Windows release notes** — per-project status
      embedded in the umbrella index. Decide whether project status belongs
      here at all, or only in each project's own README.

## 1. Move `myvars` into `aap_autodeploy_configascode` — done 2026-10-17

The split broke the path: those playbooks loaded `../myvars`, which resolved to
the umbrella root when that was the AAP project. Once the repo itself became
the project root, `..` pointed outside it and the vault file was never found.
Nothing else referenced the file, so it moved rather than being copied, and the
seven load paths were rewritten.

Still unverified: no playbook has actually run against the new path — see
task 2.

## 2. Test-run every split repo

Nothing has been exercised since the split. Syntax checks pass; no playbook
has actually run.

## 3. Review vault files across all repos

They are no longer one shared file and their contents differ per project. Work
out which repo needs which keys. Note that a vault credential on a job template
only supplies the decryption password — not the file, and not the variables.

Two conventions are in use and should be reconciled:

- `aap_autodeploy_configascode` — a vault file named `myvars` at the repo root.
  As of 2026-10-17 it is the only repo using one.
- `automation-orchestrator`, `ServiceNow-ITSM-Integration` — `vars/vault.yml`
  with a committed `vars/vault.yml.example` alongside it.

A third approach exists and may be the better default: `AIOps_selfhealing_demo`
dropped its vault file entirely on 2026-10-09 (`ce4eced`) and now asserts the
environment-specific values from inventory, so the repo carries no secrets and
nothing to decrypt. Worth deciding whether that generalises before standardising
on a filename.

The README Secrets section currently states the root-level rule, which only
describes autodeploy. Update it once this is settled.

## 4. Submodule pointer hygiene

- [ ] `AIOps_selfhealing_demo` and `ServiceNow-ITSM-Integration` have both
      advanced past the pinned commit. Bump them.

- Ongoing: a submodule records a specific commit, so after pushing a child
  repo, bump the pointer here:

      git -C <project> pull
      git add <project> && git commit -m "bump <project>"

## 5. Retire superseded copies

- [ ] **Retire the old AAP project** that pointed at the predecessor monorepo
      for the autodeploy and orchestrator playbooks. Its job templates were
      re-pointed at the new per-repo projects, so it now has none attached.

- [ ] **`config_exceptions_ng` is duplicated** — this repo's copy and an older
      one inside the predecessor monorepo. Decide which is canonical and
      retire the other.

- [ ] **The predecessor monorepo holds superseded generations** of the deploy
      and self-healing playbooks. Decide whether to retire them.

- Unscrubbed pre-split history lives in a private archive repo, including the
  previous standalone self-healing repo on its own branch. Do not merge it back.

## 6. End-to-end tests for every project — later

Not near-term. A standing, re-runnable suite that exercises every project in
this umbrella, so at any point we can confirm they all still work.

Distinct from task 2: that one asks "has this ever run since the split?" and is
answered once. This is the regression suite that keeps answering it — most
valuable when a demo is imminent and nobody remembers what last touched what.

Shape to work out when we get there:

- [ ] Each project declares how it is exercised and what counts as a pass.
      Some can run unattended; others cannot without a target environment.
- [ ] Decide what each test needs and whether it is disposable. The autodeploy
      pipeline can build and destroy a throwaway AAP, so it can host tests for
      the projects that configure AAP — an obvious self-hosting opportunity.
- [ ] Classify by external dependency, since these will not all be satisfiable
      at once: OpenShift cluster (orchestrator), ServiceNow dev instance,
      Windows endnodes and WSUS/Nexus, Zabbix and EDA. Note which ones hold
      time-limited credentials that expire between runs.
- [ ] Decide where the suite runs — an AAP workflow spanning the per-repo job
      templates is the natural fit, versus external CI.
- [ ] Decide how results are reported and where a failure is recorded.

Blocked on task 2: there is no point automating a run of something that has
never completed manually.

## 7. Define shared development rules for agents

- [ ] Define general development rules that agents can follow across the
      umbrella projects, with explicit project-specific exceptions where needed.
      Include per-project versioning, release publication, documentation and
      decision-history updates, meaningful validation, and secret protection.
      Use the newly adopted Autodeploy version policy as one concrete example:
      each project owns its version; feature commits increment minor and reset
      patch; other commits, including documentation, increment patch; published
      releases require an annotated tag and matching GitHub release.
- [ ] Decide where the shared rules live and how each project's `AGENTS.md`
      references them. Keep Vault password files outside Git. Document agreed
      rules before applying them to other projects; their versions stay independent.

## 8. Recreate the development workspace automatically — later

- [ ] Automate rebuilding this agent development workspace on a fresh host:
      directory layout, repository checkouts and submodules, required tools,
      agent working rules, and configured integrations such as AAP MCP access.
- [ ] Separate reusable bootstrap definitions from environment-specific inputs.
      Keep sensitive inputs Vault-encrypted when stored in Git, and supply Vault
      password files such as `vpf` outside Git.
- [ ] Verify reconstruction on a clean host, including the required tools and
      integration access. Document any operator authentication steps that remain.

Deferred work: capture the requirement now; implement it later.

## 9. Create a credential rotation mechanism — later

- [ ] Design a mechanism to rotate credentials across the umbrella projects.
      Identify credential owners, dependent systems, and rotation triggers.
- [ ] Define how replacement credentials are propagated and verified before
      retiring the old ones, including recovery if an update fails. Keep secrets
      protected throughout rotation.

Deferred work: define the scope and procedure before implementing rotation.

## 10. Review all playbooks for readability and clarity

- [ ] Review all playbooks across the umbrella projects for readability and
      clarity, including task names, variable names, structure, and explanations
      of intent. Record any needed improvements in the owning project's TODO.

---

# Tracked here for now — belongs in a project repo

Carried over from the pre-split TODO. These are not umbrella tasks; relocating
them is itself a task.

- [ ] **Relocate the items below** into the repo that owns each, then delete
      this section.

## → `ServiceNow-ITSM-Integration`

- [ ] **`collections/requirements.yml` will break project sync.** At a repo
      root AAP runs `ansible-galaxy install` against it, and `community.zabbix`
      is neither in the execution image nor on the configured galaxy server.
      Same failure the orchestrator repo hit. Either sync the collection to
      private automation hub, or move the file off the magic path as was done
      there.

## → platform / infrastructure (no repo yet — decide on a home)

- [ ] Projects are only needed for repos AAP actually runs playbooks from.
      `ServiceNow-ITSM-Integration` (no playbooks yet), `config_exceptions_ng`
      (no job template) and `intelligent-assistant` (docs only) have none.

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

## → central CMDB and inventory source

Related to the undocumented `inventory/` directory in task 0.

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
