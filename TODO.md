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

- [ ] The stored API token is read-scoped; writes need admin basic auth.
      Consider issuing a write-scoped token if API automation continues.

## Ongoing discipline

- Submodules pin a commit. After pushing a child repo, bump the pointer here:

      git -C <project> pull
      git add <project> && git commit -m "bump <project>"

- Unscrubbed pre-split history lives in a private archive repo, including the
  previous standalone self-healing repo on its own branch. Do not merge it back.
