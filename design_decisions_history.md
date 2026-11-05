# Design decisions history

## Track the approved Windows demo policy and native Claude readiness — 2026-11-05

Umbrella implementation: `5fd3459`. AutoDeploy advances to `e0ebd1a`
(version 0.42.6, code implementation `276ad84`); Windows advances to `c06aa9e`
(version 1.0.12, code implementation `b0bf1af`). Every other project reference is
preserved.

The operator retained the Windows demo's HTTPS/NTLM certificate-validation
exception and skipped the additional predeployment inspection. The producer and
shared release transaction now record certificate validation truthfully as false;
authenticated Windows facts and native ownership checks remain required.
Fifty-one shared lifecycle/version checks and 141 Windows checks passed, along
with Windows syntax and scoped lint. Runtime import and functional testing are
still outstanding. The documented original AAP has a second interface on the
isolated Windows network; restoring that topology awaits the operator's decision.

The separately published native Claude installer passed its normal deployment,
actual-user binary checks and both private MCP diagnostics while preserving
existing client data. No model call or full isolation release occurred. These
results establish software readiness, not complete instance recovery. Source
references were verified over the existing SSH transport; no base image was
changed or rebuilt by this umbrella update.

## Track canonical Controller port validation — 2026-11-05

Umbrella implementation: `4545143`. AutoDeploy advances to `c1a7404`
(implementation `6de45e0`, version 0.42.3); Windows advances to `65b7024`
(implementation `12605b8`, version 1.0.10). Other project references remain
unchanged.

A real configuration continuation found the same SSH port serialized as text
by Controller while its independently registered pin held an integer. The
shared publisher now accepts only a valid integer or canonical positive ASCII
decimal text, then compares the exact port. It rejects booleans, floats, signs,
whitespace, leading zeroes, out-of-range values and different ports. Machine,
user, host-key, job, TLS and policy checks retain their existing behavior.

All 61 affected shared checks, the actual read-only planning replay, nine
Windows consumer tests and scoped production lint passed. The following live
Assistant continuation passed that guard and durably published only its
approved HTTPS bootstrap; software validation, full release and retirement are
still separate acceptance steps. Both consumers use the existing pinned role,
with existing credentials and port settings. Source references were verified
against their SSH remotes; whitespace checks passed.

## Reference the Windows baseline release hooks — 2026-11-05

Umbrella implementation: `3bcbf93`. Only the Windows project reference advances,
to `600bc64` (implementation `45f4692`, version 1.0.9). Its completed baseline
jobs now join authenticated Windows identity with exact native clone ownership
before invoking the existing shared release role in the same job. Partial or
check runs cannot release a guest.

The selected private configuration reuses existing credentials for the two
baseline jobs. Existing passwords, Vault identities, other Job Templates and
legacy targets remain unchanged. Native execution-environment checks verified
credential precedence, HTTPS/CA settings and both existing Vault keys without
network calls. All 136 tests, 35 playbook syntax checks and scoped production
lint passed. The reference was checked against the published SSH remote.

Actual Windows image inspection, certificate authentication, deployment and
teardown remain unverified. This umbrella change neither imports the selected
configuration nor launches a Windows job. The README preserves that acceptance
boundary; all other project references remain unchanged.

## Reference recovery lifecycle and use-case preparation — 2026-11-05

Umbrella implementation: `132df06`. Only the AutoDeploy, AIOps and Windows
references advance; other project references remain unchanged. The README
separates published implementation from outstanding live acceptance so the
recovery checkout records both the current code and its practical limits.

AutoDeploy `9ddb82f` includes shared typed guest release/retirement, AIOps
instance-settings preparation and the final normal-installation release hook.
The hook runs only after successful configuration, credential publication and
cleanup. Its implementation `75639c5` passed 75 regression/version checks and
production lint; a complete live AAP installation remains unverified.
A repeat import using the instance-settings preparation preserved existing
runtime ciphertext and event credentials.

AIOps `86d3cb5` provides the Claude installer with private Linux and Zabbix MCP
configuration. Windows `4754d98` includes the isolated test profile and guarded
directory/trust cleanup preparation. Their live functional tests and subsequent
decommissioning remain separate requirements. Referenced commits were verified
against the public repositories over the existing SSH transport; whitespace
checks passed. No VM or application job was launched by this umbrella update.

## Track bounded RHEL publications and configured stage surveys — 2026-11-04

The RHEL submodule now tracks `f57008d7b3de23696e58c44451cfe825ca13a894` (version 0.5.1).
Implementation `59e9e8c` adds optional issue-date caps and
verification in Library before exact Test promotion. Implementation
`17593e5` publishes the configured generic stage surveys.
The separate private companion stores whole-file encrypted AAP configuration;
public source retains automation and generic definitions.

Existing regression tests and eight new cutoff tests, seven syntax checks,
production lint and actual JT metadata/prerequisite readbacks passed. Live
patching validation remains separate. Unrelated submodule working changes
were preserved.

Umbrella implementation commit: `ea8732b458699f9989b22fadb3da716b6b988a4a`.

## Reference dynamic multiple-CVE survey input — 2026-11-04

Umbrella implementation: `50df934990518b26064550d707798d729fbab3e2`. The RHEL reference advances
to `384adc19520c18183baa218dea831c18282905f5`, including implementation
`01aa887` (version 0.4.0).

The user requested multiple CVEs in the JT survey and live Satellite mapping.
A required textarea accepts comma, space or newline separators. Each CVE is
resolved through live queries in the selected repositories, associations are
confirmed against full advisory details, and every requested CVE receives its
own installed-fix proof. Unknown IDs stop the run and shared RHSAs are deduplicated.
The public README catalog is never used for runtime resolution.

All 81 tests, seven syntax checks, production lint and legacy host-Python
grammar checks pass. Real Ansible fixture runs prove identical input follows
changed server metadata, and read-only live queries verified a two-CVE lookup
and rejection of an unmatched extra input. No actual preparation, Content View
update, patching, reboot or snapshot ran. Other references and changes remain
preserved.

## Reference the RHEL advisory and CVE catalog — 2026-11-04

Umbrella documentation implementation: `24a1f304299fd2926f14b38d5ced46d05483d022`.
The RHEL reference advances to `4d0c2cfdf73bebc128eef94cd848149edf054e63`,
including catalog documentation `8d4e255`. Runtime version remains 0.3.0.

The project README now contains fourteen public RHEL 7 advisory candidates
with issue dates, components, severity, CVEs and Red Hat advisory links.
It explains CVE resolution through Satellite, including a CVE that selects
two Python advisories, and RHSA input for selecting exactly one advisory.
The catalog also records how its earliest issue date determines the initial
cutoff. Only public advisory metadata is included; runtime behavior is unchanged.

Catalog completeness and CVE associations were reconciled against the captured
advisory metadata, the example lookup was verified with a read-only Satellite
query, and whitespace checks pass. No preparation or patching ran. Other project
references and working changes are preserved.

## Reference preparation before all selected security advisories — 2026-11-04

Umbrella implementation: `45093f2e4bb3c82dbf36fbcff7fdc0ecd712f9ec`. The RHEL source reference
advances to `9cb3d73592edc37463087430391eb48edebcf150`, including preparation
implementation `7a0a2fd` (version 0.3.0).

Preparation now derives a baseline cutoff before the earliest outstanding RHSA
on the explicit host pair, validates the selected repository metadata, and
publishes in Library before checking that the complete selected advisory set is
absent. Only then does it initialize Test/Prod and reassign the pair. Recovery
revalidates the recorded initial baseline, while established later versions are
preserved. This makes the full advisory set available for separate minor-update
demonstration stages without silently including the earliest fixes in baseline.

All 67 tests, including five simulated real Ansible prep runs, seven syntax
checks and production-profile lint pass. No remote preparation, content change,
host reassignment, patching or snapshot was executed. Other project references
and working changes are preserved.

## Reference the corrected RHEL advisory verification — 2026-11-04

Umbrella implementation: `177722711fc5dc9967bb94228dd56b01fa0085f8`. The RHEL reference advances
to `2dca2bdd381fca799fce14c7dc5962f98ffe19cc`, including epoch correction
`9199670f987932bcfec9179934da64625d3ec3e7` (version 0.2.2).

Advisory filenames omit epochs, so the project now resolves authoritative epochs
from exact packages in the selected repositories before native RPM comparison.
Missing or ambiguous metadata stops verification. Fifty-four tests, seven
syntax checks, production lint and direct read-only checks on the selected two
hosts pass. All fourteen inspected advisories remain outstanding; earlier
fixed results for nonzero-epoch packages were false positives.

No patching, reboot, Content View change or snapshot ran. Later AAP CaC and
live patching validation remain separate. Other project references and
working changes are preserved.

## Reference the verified AIOps deployment and repeat importer — 2026-11-04

Umbrella implementation `16216be` advances only the AIOps and AutoDeploy
references, retaining all other project references and working changes.
AIOps source `321341a` includes monitoring implementation `1172d8a` and its
deployment records; AutoDeploy source `295e5a3` records version 0.34.3 and
variable-preservation fix `8c0af1c`.

The normal monitoring job and independent readbacks passed. Both a controlled
fault and a real website button press produced successful automatic restore and
rearm. The scoped agent installation and passive ping passed separately. The
fixed normal configuration import also passed while preserving the running
website activation, Event Stream and existing template identities. Protected
resource and job evidence remains encrypted in the private companion repository.

These references make the tested deployment reproducible. Per-VM isolation
removal, copied testserver monitoring and model-directed remediation, the older
AutoDeploy template family and inventory naming remain separate unfinished work.
Private-only MCP exposure and the existing shared deployment playbook design are
retained.

## Validate the RHEL project using an existing Satellite EE — 2026-11-04

Umbrella implementation: `f0092187172315a4876d2af61723215fca8998be`. The RHEL reference advances to
`e27e14651560c4724f90ab688233bd7cf3aeb7ba`, including read-only diagnostic
`1c9c73e0b6c1e551abdfe37738a532873555419f` and existing-collection compatibility
fix `524f835` (version 0.2.1).

The user chose a trial with the existing EE, whose live diagnostic reported
Core 2.15.11, Python 3.9.19 and redhat.satellite 3.14.0 and read Satellite over
verified HTTPS with zero changes. The source now uses that collection's filter
argument and declares its version explicitly. The diagnostic also checks
module argument names, required module availability and all six stage syntaxes.
Forty-four offline tests, seven syntax checks and production-profile lint pass.

This records runtime inspection and compatibility work; actual Content View
publication, host reassignment, patching and reboots remain unrun. The separate
snapshot and rollback task stays on hold. All other project references and
working changes are preserved.

## Keep inventory examples separate from runnable RHEL stages — 2026-11-04

Umbrella implementation: `e67abab701fb0e0352c2a82917c21d9013ed290e`. The RHEL source pin advances
to `8ff8e509d845eda9db7ee77a28947b670af30495`, including inventory-format
fix `224a8b12c9ff9474567c3491b9439c8024237a40` (0.1.2).

AAP discovered the YAML inventory example as an extra playbook after source
synchronization. Its INI replacement keeps the project menu focused on the six
actual demonstration stages while preserving generic local inventory examples.
The playbooks, declared runtime collection, and later live-validation boundary
remain unchanged. Other project references and local working changes are
preserved.

## Separate RHEL source sync from runtime dependency installation — 2026-11-04

Umbrella implementation: `64b26b74564dcc508b44aca3127d8bc8834ef33d`. The project pin advances to
`5a01e8265986c29a3f9915dc9a01d460b98c7d31`, including source fix
`f528087bd55a7117eb2fee86860bb2888549ad9d` (0.1.1).

AAP also discovers a root requirements.yml during SCM updates. The collection
declaration now lives in dependencies/satellite.yml so runtime preparation is
intentional. The required certified collection and execution-environment
prerequisites are unchanged; no controller source settings or dependencies were
modified. Forty-two offline tests and production-profile lint pass. All other
project references and working changes remain preserved.

## Publish independently launched RHEL patching stages — 2026-11-04

Umbrella implementation: `976c50de2d522a6c3044e07e785b47174f9a7b51`. The RHEL-sniperpatching
submodule advances to `88425187e5ecbd83225a7aede03b8c3d403bf142`, including
implementation `ba33c694edd16334a29126b4684a4c3a2d26a624` (0.1.0).

The user requested gradual demonstration stages: isolated preparation, a genuine
minor Content View update, host patching with reboot and fix proof, full
publication, explicit production promotion and read-only checks. Production
receives the exact tested version. Supported Satellite operations use the
certified collection; incremental creation uses the documented API because the
collection does not expose it. All other submodule references are preserved.

Forty-one offline tests, six syntax checks and production-profile lint pass.
Source validation and SCM synchronization do not establish live host patching
or restore readiness. AAP configuration-as-code integration remains later work.
The project README describes required runtime inputs and execution prerequisites.

## Verify monitoring and both private MCP integrations — 2026-11-03

Public AIOps implementations `ef7af00`, `06f64ba` and `ef45ec7` have now been
verified through their normal deployment jobs and independent read-only checks.
Monitoring DNS, trusted HTTPS, authentication, quarantine and proxy backend pass.
Both TRA MCP integrations reach their matching new targets while preserving
private configuration and existing client settings. The overview records this
actual state separately from website and remediation-loop work still pending.
No public MCP endpoint, new workflow or credential architecture is added.

## Describe the verified shared importer and automatic base access — 2026-11-03

Umbrella implementation `a5b56b1` advances AutoDeploy to `3a29555` and replaces
the outdated manual-token description. Normal base deployment publishes
per-instance API/MCP authentication and configures the selected AAP guest's
exact connection to its own hypervisor. Source implementations `931edb8` and
`3a29555` document the management automation and its validation.

The current shared importer has successfully restored AIOps, Assistant Team,
Windows Patching and Orchestrator configuration on a fresh test instance with
independent object and preservation checks. AutoDeploy's own import remains
pending the owner's choice about older jobs' hypervisor settings. AIOps
application data is held by its private companion; Linux MCP has passed an
actual read-only query. These results are distinguished from earlier importers
and from application jobs still requiring their own deployment checks.

Existing unrelated submodule working changes are preserved. No deployment,
new credential design or application workflow is introduced by this overview.

## Add RHEL-sniperpatching as a project submodule — 2026-11-03

Umbrella implementation: `eb4f7ebe02dbd135bb48eefa503adf443c006cc3`. Project initialization:
`a3c7cdfa6ae10c97f2b637c75f5a44193248e457`, with decision documentation in `28decaff64affcb4fc4c2f6c3116ddd894cce2ef`.

The user requested the public `RHEL-sniperpatching` repository as a submodule
of AAP Advanced Features. Its initial documentation provides the commit needed
for a pinned submodule reference, and the umbrella README lists the project.
The committed submodule URL uses HTTPS for public cloning and GitHub linking;
agent-side Git operations use SSH. Patching scope and implementation remain
undecided.

## Use one Git-token schema with a separate VM-state writer — 2026-11-03

Implementation `42bd149` and naming update `2f90107` align the AutoDeploy source
pin and overview with the approved writer change. The dedicated credential is
named `VM allocation git Pseudo CMDB writer` and uses the existing
`Cac_git_token_type`; repository read credentials keep their own read-only tokens.
Encrypted base and saved templates use the same name and `inputs.token` field.
The source derives the fixed repository URL from encrypted runtime configuration,
so extraction also attaches its existing environment Vault.

Controller refuses changing the type of credentials used by job history. The
owner approved creating a production replacement, updating active assignments,
verifying it and then deleting the retired credential; no job record is deleted.
The unused writer on the existing test controller changes type/name in place.
The source's 173-test suite and production lint pass; private comparisons preserve
reader values, literal templates and allocator state. The temporary Git/YAML
registry still has a separate backlog item for replacement by a real CMDB.

This retrospective records significant decisions from Git history and available
session requirements. Implementation details belong in the individual projects.

## Consolidate registry reads on existing repository credentials — 2026-11-03

Umbrella implementation `5e79976` advances AutoDeploy to `540594b` (0.28.9).
Source implementation `328c982` follows the owner's approval to reuse the
existing AutoDeploy secrets repository read credential for the registry.
The action binds its repository to encrypted runtime configuration and ignores
launch namespace overrides. Preparation retains the saved repository pair and
adds only the pinned Machine credential.

Companion implementation `e94e312` aligns five saved consumers, removes the
redundant reader credential/type from base provisioning and updates extraction
dependencies. The existing token read the actual registry ciphertext, and the
protected runtime URL matches that same repository. All 171 tests and production
lint pass. Writer inputs, token permissions and registry ciphertext are unchanged.

The owner separately requested a real CMDB instead of the temporary Git/YAML
registry. Beads `bead-wd-sc8` and the source work plan record that requirement;
selection and migration require an agreed design. No CMDB implementation or
allocation-writer change is part of this reader migration.

## Reuse one AutoDeploy CaC Vault for registry state — 2026-11-03

Umbrella implementation `4db042d` advances AutoDeploy to `cafcc98` (0.28.7).
Source implementation `eb6b214` follows the owner's instruction to reuse the
existing AutoDeploy secrets repository CaC Vault for registry encryption and
decryption. Preparation retains that saved Vault and adds only the registry
reader and pinned Machine; no distinct registry Vault is selected.

Companion implementation `79ff338` removes the redundant Vault from desired
bootstrap, selector associations and extraction dependencies. The existing
registry decrypts with the maintained shared password, so its ciphertext and
reservation history remain unchanged. Forty-nine focused checks, selector
syntax and production lint pass. This change does not delete credential objects,
rotate keys or alter either custom Git credential type. The five direct project
imports and their fixed `aap_cac_project_id` Extra Variables remain unchanged.

## Call one importer directly and name configuration deployments explicitly — 2026-11-03

Umbrella implementation `ca095d4` advances AutoDeploy to `e2d4360` (0.28.5).
Source implementation `b5fb34b` removes all five unused per-project wrappers;
the five Job Templates call `deploy-cac-project.yml` directly with their fixed
`aap_cac_project_id` in saved Extra Variables, as required by the owner.

The owner also requires the Deploy prefix. An existing application deployment
already uses an otherwise matching name, so the owner explicitly chose
`Deploy <Project Name> CaC` for all five configuration imports. Companion
implementation `35e3bc8` aligns the encrypted names, selector keys, survey title
and extraction references. The naming helper and public overview use the same
rule. Existing IDs, credentials, permissions, schedules and workflow links are
preserved. Twenty-four focused checks and importer/selector syntax checks pass.
No configuration import or application job is launched by this change.

## Share project imports and derive their Job Template names — 2026-11-03

Umbrella implementation `ba477f2` advances AutoDeploy to `ab805f0` (0.28.3).
Source implementation `305b0cd` replaces the five import engines with one
`deploy-cac-project.yml`; `3028df4` derives readable deployment template names
from project IDs, preserving word order and the AIOps/AAP acronyms. The previous
playbook filenames remain thin aliases. This keeps one implementation while
each project retains its own saved repository Git and Vault credentials.

Each fixed project ID determines its private `<project-id>-secrets` repository
and `vaults/cac/<project-id>-cac-vault.yml`. All five encrypted companion captures
are migrated, including their metadata, extraction references and documentation.
Central implementation `0c3e1e0` aligns the final template names, selector keys,
inventory references and protected-debug descriptions. Original secret values,
all 43 literal template markers and unrelated encrypted files are preserved.
Companion correction `322e86a` also matches the destination-host survey help
text to production exactly, preserving all other configuration values.

The destination inventory host and a native AAP API credential are selected at
launch. Its verified HTTPS origin must match the stored `ansible_fqdn`; source
execution environments call the destination API directly. Project imports and
prerequisite preparation no longer read installer passwords over SSH. Existing
and self destinations are supported by the standalone importer; the optional
multi-project selector retains its separate fresh-target preparation checks.
No destination API credential is provisioned by this refactor.

Generic resource handling creates group skeletons before memberships, preserves
masked service credentials and existing activation states, and creates new
activations disabled. The full implementation suite passes 170 tests; focused
naming, extraction, real TLS and Ansible rendering checks cover the final
references. Actual cached collection versions match the tested modules.
Independent production readback preserves all 124 template IDs and all 37
credentials. The seven intended template configuration updates and final five
name changes preserve grants, schedules and all 76 workflow nodes.

No use-case import, application job, VM operation, production SSL change or
credential rotation is performed. The owner explicitly deferred review of the
existing custom allocation/registry credential types until after this work;
that discussion is tracked separately as `bead-wd-72f.6`.

## Analyse consolidation before replacing use-case importers — 2026-11-03

Umbrella update `1937e69` publishes the recommendation from AutoDeploy analysis
`96ce498`, documented in `5e4293a` (0.26.3). All five CaC importers share the same
basic mechanism. Their resource schemas, names and ordinary validation should
be data for one generic playbook. Existing Event Stream and workflow support
removes reasons for duplicate API passes. Pinned EDA project field omissions and
asynchronous inventory group ordering need reusable resource-level handling.

Durable target service credentials require explicit lifecycle handling or
equivalent prepared inputs. Content/server preparation and the selector's child
job orchestration remain distinct from configuration import. One shared playbook
does not decide how AAP binds repository and destination credentials before
launch; that contract remains open under `bead-wd-72f`.

The analysis checked source references, vendor role/module behavior and an
illustrative schema. A zero-API synthetic probe found a local EDA activation
compatibility issue, tracked in `bead-wd-72f.4`; no production behavior was
attested or changed. The proposal does not require a new planner and distinguishes
disabled schedule definitions from enabling automated execution. Only
documentation and version metadata changed; no import or deployment job ran.

## Give each CaC repository its own credential pair — 2026-11-03

Umbrella implementation `8ea60c1` advances AutoDeploy to `8865506` and documents
the repository-specific read-token and CaC Vault pairs. Source implementation
`7e5f672` provisions all five pairs through encrypted bootstrap inputs; companion
capture `4ab587f`, documented in `3dc217a`, updates template bindings, source pins
and extraction ownership references. Each importer receives its repository's
pair. Runtime environment and instance-registry credentials retain their roles.

The owner authorized changes on production and the existing fresh test instance.
Existing readers were renamed in place; the base Vault was retained and four
repository Vault entries were added on each controller. Independent readback
verified all 124 production templates, the fourteen affected assignments, both
controllers' named pairs and unchanged unrelated configuration. Existing access
boundaries and secret inputs are preserved. Protected before/after evidence is
stored in the encrypted companion migration record. A tracked-file scan covering
decrypted configuration found no active old-name references; historical evidence
remains factual. Paired-bootstrap fixtures, selector checks and the corrected
example validate the source changes without a deployment or use-case import.

Destination API credential selection and inventory-based launcher replacement
remain pending under `bead-wd-72f`. Future extractor credential routing before
repository rekeying is tracked in `bead-wd-72f.2`.

## Store AAP API DNS names in inventory — 2026-11-03

Umbrella update `5ae7136` advances AutoDeploy to `81c7a2b` and documents the
explicit `ansible_fqdn` contract. Companion implementation `720710d`, documented
in `e143ebf`, saves the same metadata in the encrypted shared inventory capture.
The owner confirmed the numbered instance was an example; only the existing
verified AAP inventory entry was updated. Live readback and a decrypted capture
comparison confirm preservation of other variables, groups and literal tags.

The intended lookup uses the launch-time instance name and its stored DNS name
to form a verified HTTPS origin. Credential selection and replacement launcher
implementation remain deferred under Beads `bead-wd-72f`. No use-case job ran,
and this umbrella update changes only AutoDeploy's submodule pointer.

## Implement placement and future TLS before deciding use-case credentials — 2026-11-03

AutoDeploy implementation `aaafed2`, documented in `ada63ca`, adds the inventory
placement contract and future upstream certificate verification. Companion
capture `e3a171b` preserves the shared inventory's existing variables and groups
while adding per-hypervisor VM placement. The target instance remains a required
launch-time input. This umbrella update advances only the AutoDeploy submodule.

The owner retained public API access for the UI, declined API delegation and
prohibited production SSL changes. Existing deployments remain unchanged. Real
TLS refusal cases, Ansible publication/rollback and nginx syntax checks validate
the future code; no new VM or use-case deployment was run. Credential management
is deliberately deferred in Beads `bead-wd-72f`, before workflow replacement.

## Review the number of Job Templates across projects — 2026-11-03

Planning update: `57412d1`; authoritative task: Beads `bead-wd-1kf`.

After the production label audit, the owner considered the number of Job
Templates excessive and requested a review in the umbrella overview. The README
and planning overview now reference a review of purpose, usage, duplication and
consolidation opportunities across projects. Recommendations must preserve
required functionality, workflow dependencies, access boundaries, recovery paths
and useful independently rerunnable stages. The review remains open; this
planning update changes no deployed templates or project implementations.

## Create a dedicated repository for agent-generated code review rules

Implementation commit: `330b0a6`.

The repository owner requested `Agent_generated_code_review` as another
independent repository and submodule, with its README reserved for rules for
reviewing AI agent-generated Ansible code. Keeping the guidance separate allows
it to evolve independently of the reviewed projects. The rules will be
formulated after repository creation; this change does not introduce review
tooling or modify any demo implementation.

The new repository matches the public umbrella's visibility. Its committed
submodule URL uses HTTPS for GitHub linking, while local Git access uses SSH.

## Complete the fresh Windows end-to-end test and post-run verification

Umbrella update: `fb41bad`, tracking Windows through `6c23d61`. Workflow ordering
and metadata-only teardown checks were implemented in `07e1200`; application
reboot completion and standalone assessment configuration were fixed in `95e29f1`.
The operator authorized destruction only of the four Windows demo clones and
their owned disks. A preservation baseline and independent verification proved
the other seven VM definitions/states and both base images unchanged before
and after the complete rebuild.

Fresh workflow 2303 passed all 21 stages in 3h48m50s, including evaluation
activation, both repository pipelines, the internal April ceiling, independent
managed OS patch jobs and application baseline-to-current deployment. Actual
Controller timestamps verify both imports converged before the ceiling and both
patch jobs completed before baseline applications. Both endnodes were created
with 4096 MiB, verified in libvirt and Windows. The fresh Server 2025 clone
activated from an initially unlicensed state and returned to its original
topology, closing the previous live-validation gap.

Follow-up inspection found missing credentials on the standalone assessment
template and a later Server 2025 reboot marker. Preserve the successful workflow,
repair the reproducible template configuration and shared application reboot
checks, then rerun only the affected stages. Corrected upgrade job 2346 passed
with one changed task, the required Server 2025 reboot. Final assessment 2349
confirmed both April builds and no pending reboot; Check job 2351 found zero
applicable updates on Server 2025 after that restart. Five additional tests
cover seven reboot-control scenarios, including clean skips and uncleared-marker
failure. Detailed stage timings and original/follow-up evidence are recorded in
the Windows test report. Only the Windows gitlink and umbrella documentation
change here.

## Complete Windows patching and verify per-clone activation automation

Umbrella update: `e98d98a`, tracking Windows documentation through `70ec181`.
The per-clone activation implementation `88b307b` and review fixes `f198c25`,
`62d501e`, `a99cf7a` add a separate deployment stage after Windows basics and
before repository preparation. Use existing encrypted credentials and approved
temporary connectivity while preserving permanent adapters and verifying the
original topology after cleanup. Licensed clones remain read-only. Inventory
selection accepts the actual host alias; libvirt comparison excludes generated
network port/bridge metadata while retaining network identity and other guards.

Native Ansible controller configuration created the activation template and
workflow handoff. Check job 2283 and normal job 2286 passed on all four existing
licensed clones with zero changes; twenty regression tests cover guard and
cleanup cases. Fresh unlicensed activation still needs a controlled full
deployment to prove it end to end. The earlier successful complete workflow
predates the new activation stage.

Both Windows endnodes now meet their April OS and .NET baselines with no
applicable updates or pending reboot. Both run with the requested 4 GiB memory,
applied through clean full VM restarts at safe servicing boundaries. Record
the download repair separately from actual update installation: Server 2025's
successful 1h38m52s job includes earlier HTTP retries. Detailed results, actual
restart counts and application-feed audits are in the Windows project. Only
that submodule and umbrella documentation are changed here.

## Increase Windows memory and repair modern WSUS payload delivery

Umbrella update: `d4fc3dc`. Windows changes: `7e206ce` raises managed-guest
memory to 4 GiB and documents a full clean VM stop/start for existing guests;
`f9883a8` adds the inherited IIS MSU/WIM mappings required by Microsoft for UUP.
Windows decision documentation is captured through `c6bb296`, including the
requested review of Microsoft reboot guidance.

The operator authorized restarting the complete VMs to apply memory changes.
Wait for each client's active servicing to finish before shutting it down.
Server 2022 reached the April baseline, passed its empty-update and reboot
checks, then restarted with 4 GiB confirmed by libvirt and Windows. Server 2025
was still downloading when the missing MIME mappings were diagnosed: the
exact payload existed with its expected length but IIS returned HTTP 404.
Apply the focused setup tag through the existing Job Template and verify HTTP
delivery and actual client progress separately. These findings do not establish
RAM as the cause of every long job.

## Recover evaluation activation and enable independent Windows patch jobs

Umbrella update: `3bc2044`. Windows fixes: `a47bd1c` for remote-compatible reboot
assessment, `ce142d4` for native action argument types and exact filtering, and
`476f4e8` for simultaneous host-limited jobs and measured runtime analysis.
Windows decision documentation is captured through `bb215c5`.

The operator authorized temporary connectivity for the existing Server 2025
evaluation. Windows activated automatically with 180 days remaining; removal
of the live-only adapter restored isolation, with internal WSUS policies still
correct. Subsequent live patch attempts exposed a remote-restricted WUA interface
and native-module argument/filter compatibility issues. Focused fixes preserve
existing access controls, exact observed updates and license guards. Eight
Python checks and fifty-one PowerShell assertions on each repository server
passed after the fixes.

The operator selected separate Job Template instances per managed host for
concurrent patching. The playbook retains sequential client processing within
each launch. Each limit also includes the internal WSUS group for shared
read-only readiness checks; managed targets must remain disjoint. Controller
settings and a targeted launch were independently verified through MCP. Client
installation is in progress and final build/reboot verification remains pending.

The ten most recent successful Windows jobs were analyzed from their AAP event
timings. Long synchronization, transfer and combined verification/import phases
dominate the historical sample; timings predate removal of redundant hashes.
The guide separates measured facts from resource hypotheses and records startup
costs without assigning an unsupported cause. Only the Windows submodule and
its umbrella documentation change here.

## Review automation for simplicity while preserving functionality

Planning updates: `b8b0bab`, `cd51d12` and `bb13308`.

The operator expanded the umbrella code review TODO to cover Ansible and its
supporting languages. Requested review criteria include APME, applicable CoP
guidance, readability, suitable certified collections, Ansible wherever possible
and minimal supporting code. Agent operations should prefer available MCP tools,
with a reason recorded for necessary direct API access.

The operator also requested strict Ansible linting across all Ansible content.
The review must fix findings and keep rule exclusions minimal, with each
exception explicitly justified. This records the review requirement; it does
not claim existing content has passed linting.

The review must also question overengineering, unnecessary steps and excessive
verification. Cleanup and simplification must preserve required functionality,
verified through focused checks. The operator also requested checking speed
optimization potential: use timings to identify slow steps and repeated work,
and prefer simple improvements that preserve functionality. These updates record
review work; they do not change project implementations or deployed systems.

## Publish monthly internal Windows baselines and guarded client patching

Umbrella update: `858ccb7`. Windows implementations: `eae5cbd` for named monthly
ceilings, `5e401ac` for managed update/reboot cycles, `63f4f1f` for removing
repeated payload hashes and `257f5bf` for internal-only policy reconciliation.
Evaluation prerequisites and subsequent client-source checks: `8f8539f`, with
decision documentation `abbafcc`.

The operator requested reproducible Ansible playbooks and Job Templates for a
named 2026 monthly cutoff on internal WSUS, followed by client installation of
the currently served baseline through any required reboots. Native Ansible
handles orchestration, installation and rebooting; WSUS API operations and
read-only guarded update searches use PowerShell through Ansible. External WSUS
retains newer content. Existing verified content skips external preparation and
transfer, and payload hashing stays at transfer boundaries instead of repeating
during policy checks.

Live publication verified the internal April 2026 ceiling and ready content.
The client Check run stopped on an unreachable Server 2025 endnode. A later
read-only WinRM audit confirmed both clients' internal WSUS settings and traced
Server 2025 shutdowns to expired evaluation activation grace. Activation and
network changes were not performed. Full client Check completion and actual OS
installation remain unverified. This umbrella update advances only the Windows
submodule reference and its documentation.

## Track recoverable MCP access for each deployed platform

Autodeploy planning: `e1aaed8` (0.10.4).

The operator requested future per-instance MCP token creation and recoverable
Vault-encrypted connection values in the private base repository. That work needs
a separately scoped Git write credential and protected client-side configuration
with CA trust. Existing import access remains read-only. Token creation is manual
for now; no persistent token provisioning, encrypted write-back or client trust
automation is implemented by this planning change. The umbrella advances only
the Autodeploy reference and related documentation.

## Verify Assistant Team configuration import and shared base prerequisites

Autodeploy documentation: `2858b56` (0.10.3), following verified administrator
password rollout documentation `b80a1f0` (0.10.2). Encrypted configuration fixes:
Assistant Team `094ee7f`, documented by `634f3ca`; shared base `63f08ff`.

The requested Assistant Team import succeeded after omitting empty credential
names from public code projects and making the generated platform CA available
to project-update execution environments. The remote Podman runtime resolves
volume sources on the host, so shared base declares the installer's host trust
directory as a read-only mount while preserving existing mounts and certificate
verification. The pinned certified collection was curated through local PAH and
the existing execution image was verified in the Controller runtime store.

Base job 2137 applied the trust setting, both project sync retries succeeded, and
import job 2139 restored 21 ordinary objects and six templates. Independent
trusted-TLS comparison passed 396 checks. Temporary tokens and workspaces were
removed. The earlier administrator-password rollout and configured-login rerun
also succeeded, with the installer inventory aligned. Runtime VM, recovery,
provider and optional maintenance automation remain separate and were not run.

The operator also requested a TODO for complete Intelligent Assistant/Lightspeed
CaC capture and independent rebuild, including service/installer settings, vaulted
credentials and passwords, and Gateway OAuth configuration. This is planning only.

## Define production replacement and encrypted seed credentials

Autodeploy: `c51aede` (0.10.1), including administrator-password implementation
`1216f38` and the existing-token importer correction `1926669`.

The operator clarified that the goal is an AAP capable of assuming production
tasks and deploying further AAP instances. A trusted seed needs independent
initial Git and Vault access. The operator requested encrypted copies of those
credential inputs in base for provisioning a trusted replacement. Actual target
credential and deployment-template restoration remains unimplemented; the plan
now tracks those gaps, complete production capture, job handoff, functional
tests and controlled takeover. Separate use-case ownership is preserved.

The Assistant Team importer and import template are prepared, with the provided
token encrypted and attached using the existing Git-token type. Token validity
does not establish private-repository permission: access verification still
fails. No import was launched. The initial administrator-password rollout also
stopped before target changes; its base Git credential was repaired, but live
password verification remains pending. This documentation does not resume
stopped jobs or establish takeover readiness.

## Verify Orchestrator configuration import

Import implementation: Autodeploy `bf12d01` and `de5b54c`, verified from
`d64e336` (0.8.3). Encrypted configuration: private capture `0fd3b53`.

The requested configuration import completed successfully. Independent read-only
API verification checked all eight owned objects against the encrypted intended
configuration, including project synchronization, inventory and execution
environment references, credential and label attachments, surveys, and extra
variables. Comparison accounts for Ansible rendering export wrappers and the
local Python interpreter variable. All 147 checks passed; TLS verification was
enabled and the temporary read-only token was revoked. The registry password
is present and API-masked; its exact value cannot be read back for comparison.

The imported deployment and cleanup templates have no job runs. This confirms
configuration delivery; OpenShift runtime deployment and functional testing
remain separate work. Verification output stays outside Git.

## Align Orchestrator and refresh Assistant Team configuration captures

Autodeploy documentation: `d64e336` (0.8.3). Private capture implementations:
Orchestrator `0fd3b53`; Assistant Team `2c3a825`, with history `fbd7afd`.

The operator selected `Orchestrator EE` consistently across its definition and
references. Assistant Team now follows current public code and external encrypted
configuration credentials. Its six deployment/recovery templates are separate
from optional authentication maintenance requiring authorization for the target
AAP. Existing encrypted authentication/configuration files were preserved.

Native export, owned references, strict rendering, missing-input guards and
private Vault round trips passed. The capture records PAH and image prerequisites;
its importer and target preparation remain outstanding. No configuration import,
runtime automation or provider authentication refresh was launched. This update
tracks only the Autodeploy submodule and related documentation.

## Roll out PAH base sources and prepare the Orchestrator import

Autodeploy implementations: `5fc2c98`, `40906b1`, `bf12d01`, and `de5b54c`;
verified rollout documentation: `0777bec` (0.8.2). Encrypted base update: private
configuration commit `82643da`.

The base rollout succeeded with protected logging after correcting an API
summary-field assumption and omitting upstream authentication fields until a
Red Hat token is supplied. Independent checks verified ordered local PAH sources,
unchanged collection versions, no collection sync, persistent read-token reuse,
and temporary-token cleanup. Direct public Galaxy is no longer an organization
source. This completes base repository setup, while collection preparation
remains a use-case task.

The user separately requested an Orchestrator CaC import playbook and Job
Template. The entry point loads its existing encrypted capture, checks readiness,
and imports definitions without launching deployment or cleanup. Tests and
syntax passed, the managing AAP project synchronized, and the new template's
Git and Vault attachments were verified. Its last job remains empty; neither
configuration import nor OpenShift runtime deployment was launched.

## Define PAH responsibilities and verify Windows configuration import

Autodeploy implementation: `d2e6988`; decision documentation: `66152f6` (0.6.5).

Base owns PAH repository and Controller content-source setup without collection
synchronization. Each use case declares its collection needs. A complete
step-by-step CaC guide and the remaining PAH setup are explicit project TODOs.
Bootstrap Git credentials must be available before downloading a private vault;
they are distinct from the target AAP's project Source Control credentials.

With repository access supplied, the Windows import completed after a retry.
Independent API verification found all 35 expected objects, the 17-node/16-link
workflow, and the expected group memberships. No imported Windows automation
ran. A regression reproduces the clean-target parent/child group race; the
importer now creates all groups before linking them. That ordering fix has
offline validation, while the successful live import used the preceding source.
The target's default public Galaxy attachment still needs replacing as part
of PAH base setup. Only the Autodeploy submodule reference changes here.

## Plan recoverable backups of public and private Git repositories

Planning update: `841fc29`.

The user requested Git backups as important, non-urgent recovery work. TODO
task 11 now includes automatic backups of the umbrella, project repositories,
and private secrets repositories, preserving complete history and all refs
outside the primary Git host. Backup verification and restore tests are part
of the requirement so that a successful copy alone does not imply recoverability.
Access credentials and Vault decryption material remain encrypted and separate
from repository backups. This records future work; no backup implementation or
schedule was created.

## Deploy each demo's AAP configuration separately with explicit target inputs

Autodeploy implementations: `a64e16c`, `a84bf09`, and `5ccb0ca`; referenced source
documentation: `feab2eb`. Orchestrator implementation: `e3d32ba`; decision history:
`69fe8fa`. Private capture updates: `d8c6aa1` for Orchestrator and `9d35857` for
Windows.

The AIOps import needed an explicit exclusion for the CoP Event Stream role,
whose item schema differs from the dedicated module definitions. Its corrected
import succeeded; independent API checks verified all 29 expected objects and
both activations running. This verifies configuration import, with functional
remediation tests still separate.

The user then authorized Windows configuration import after its missing machine
password was validated and saved in its encrypted capture. A dedicated playbook
and Job Template load only that private capture, reject job-launch and schedule
definitions, protect credential inputs during diagnostics, and clean temporary
access afterward. Each private repository requires its own allowed read access;
sanitized Git error categories make access failures visible without logging
secrets. Importing definitions does not launch their Windows automation.

The user also requested portable Orchestrator target inputs and cleanup. Source
playbooks no longer load the old AAP vault implicitly; source template surveys
and encrypted definitions now accept the intended target explicitly. Cleanup
uses exact requested application names and a temporary Gateway token. The now
unused playbook Vault attachment was removed from those two templates, retaining
the shared credential for its other users. No Orchestrator deployment or cleanup
was run. Only the Autodeploy and Orchestrator submodule references change here.

## Recover installer monitoring before configuring the new platform

Autodeploy implementation: `64aec45`; verified-deployment documentation:
`94705fa` (source version `0.5.10`).

A Controller timeout stopped monitoring while the remote installer was still
running. Starting another installer would have risked overlap, so Stage 03 now
accepts the original async job identifier and observes it without host preparation,
inventory edits, or another installer launch. The template time budget allows
for host preparation as well as the installer's own async limit.

Live recovery confirmed the original installer's successful exit and Controller
health. Stage 04 then imported the subscription and applied only the platform
organization and setting, with token and workspace cleanup verified. All four
stages have therefore been verified as individually launched jobs; automatic
handoff remains planned, and no use-case deployment was launched. This umbrella
update changes only the Autodeploy reference and related documentation.

## Keep deployment fixes and encrypted demo captures independently reviewable

Umbrella update: `e9ce160`; Autodeploy implementations: `97e3236`, `33f2575`,
and `91b5fc6` (included through its `85b6cb0` reference).

The Autodeploy reference now includes the declared DNS lookup collection,
AIOps Event Stream-before-activation ordering, and a consistent CoP credential
schema. Private configuration captures remain separate from reusable playbooks.
The user requested additional private encrypted captures for Orchestrator,
disconnected Windows, and Assistant Team. Plaintext captures, export output,
and ownership inventories stay outside Git; capture work does not authorize
deployment of those demos.

Source validation is documented in the individual project. The DNS retry passed;
the fresh AAP installation and platform-only configuration are tracked separately
from the unlaunched AIOps entry point. No unrelated submodule references changed.

## Review Ansible readability and collection suitability together

Planning update: `ea6953788ee24baead8ae251a6cb22e99257634c`.

The user expanded the existing readability review to cover all Ansible playbook
content, including roles and included tasks, and to consider reliable collection
modules and roles where appropriate. TODO task 10 now asks reviewers to prefer
certified, validated, or maintained community collections while checking their
maintenance, version compatibility, dependencies, PAH availability, and actual
behavior. Collection use alone does not justify a replacement; improvements and
validation remain owned by each project. This records future review work and
does not claim that the content review has already been performed.

## Track independent Autodeploy versions and shared agent rules

Autodeploy implementation: `f3efca9`; decision-history follow-up: `423bda5`.

The user adopted per-commit versioning for the Autodeploy project alone and
requested its `0.0.1` release. Feature commits increment minor and reset patch;
other commits, including documentation, increment patch. The project provides
generic empty CaC templates separately from its encrypted environment
configuration. The subsequent documentation commit advances its branch version
to `0.0.2` while the published source baseline remains tagged `v0.0.1`.

The user also requested a future umbrella task to define general development
rules for agents, using versioning as an example. TODO task 7 tracks that work;
it does not impose a shared version number or new rules on other projects.

## Separate projects and reproducible references

Commits `69b1fb0`, `ce277b1`, `708f380`, `c1d89db`, `a740487` and `2321b60`
converted projects to submodules, allowing independent histories while keeping
explicit versions in the umbrella repository. `9831b6b` documented this layout.
`7a74751` retained HTTPS URLs for anonymous cloning and GitHub linking; agent-side
Git operations use SSH, while AAP source synchronization uses HTTPS.

## Encrypted runtime configuration

`0655913` made encrypted configuration available to AAP at runtime without
committing plaintext secrets. `a9c30e9` added an encrypted network inventory and
a central inventory/CMDB follow-up, so environment-specific addressing remains
protected while a more durable source of truth is considered.

## Modular disconnected Windows demo

`e9b63cd` introduced the Windows project. `4d0c32d` tracked separate Windows
basics, WSUS and Chocolatey setup stages for independent execution and recovery.
`c8bf8cf` added parallel service setup after preparation and explicit WSUS
synchronization/export/import. `9beea27` tracked the equivalent application
content pipeline and baseline-to-current upgrades.

## Guarded lifecycle and focused recovery

`0112532` tracked Windows-only clone destruction guards. `9344954` added
independent teardown verification and a reliable scheduled network launcher.
`06e3d83` tracked bounded WinRM reconnection during network changes. These
decisions support repeated demo deployment while protecting unrelated VMs.

## Approved repository onboarding

`13dc9e8` tracked version-scoped, idempotent Nexus EULA acceptance after explicit
approval. The Windows project's decision history records the implementation
commits and subsequent validation fixes in greater detail.

The updated Windows reference includes `95cbd03` for Windows package-array
validation and `cb629a0` for the verified application pipeline and retrospective
history. Targeted recovery retained the successful VM and WSUS stages while
verifying both internal release feeds and endnode upgrades.

`06474a4` records the subsequent successful fresh-environment workflow 1252,
which verified all 17 stages together after guarded Windows-only teardown and
preservation checks. No design change was needed for that complete rerun.

## Snow demo plan review

Commit `6509b3020c06d040a35fe3d0bb91d44a4daa6b4d` updates the Snow submodule reference to `f27d3d6`
and describes its current planning status in the project index. The referenced
project incorporates the user's approved corrections for repeatable setup,
persistent incident correlation, verified integration permissions, Spoke setup
feasibility, and standalone project dependencies. Its own decision history records
the review rationale and plan-update commit `8feca9e`.

The umbrella update was prepared in an isolated checkout with submodules left
uninitialized, preserving the other project's concurrent working copies and
their recorded references.

## Publish the AIOps hostname revision on main — 2026-10-30

The user prefers main and approved completing the website-hostname revision
there. The submodule now points to source commit `094d427`, which includes
implementation `89e113f` and the verified Vault-association rollout record.
The project index describes the environment-selectable website checks. Other
submodule references were left untouched; their working copies were already
modified by separate work.

Three local source tests pass. The existing restore and rearm templates received
their existing project Vault credential before main was advanced, with machine
credentials preserved and API readback verified. No lifecycle job was launched.
The original hostname feature branch is merged and removed, so its completed
progress is available through main.

Submodule-reference and README implementation commit: `c58b1d5`.

## Link durable task records and clarify deployment destinations

The operator requires tasks and decisions to remain available from Git after
reinstalling the original host. Implementation `f77b43b` links the current
AutoDeploy task/decision/restart documents and Hactar recovery records, preserving
unrelated submodule changes. The AutoDeploy reference includes the public task
overview and encrypted full-record export tooling.

The overview now describes instance-selected API/MCP authentication, retaining
the older four production stages while excluding them from future installations,
and verifying newer stages against their own or selected remote hypervisors.
It distinguishes current private runtime Vault locations from AutoDeploy's
existing encrypted runtime file. CaC installation and actual use-case behavior
remain separately verified; these documentation changes authorize no live rebuild
or original-host modification. Relative links, privacy patterns and diff checks
passed.

## Verify the selected guest release through normal automation

The AutoDeploy reference advances to `d5ddc2a`, including shared verifier fix
`d2d7254` and normal source job 3282 acceptance. Assistant revision `6098490`
ran the configuration-only path without provisioning or package updates.
Independent live/saved-policy, guest-connectivity and VM/service preservation
checks passed; production access remained blocked. The three encrypted captures
and source inventory match the intended transition, with tokens, allocation
history and existing literal template tags preserved. Hactar evidence update
`9d7e835` also refreshes the full encrypted task recovery copy.

This verifies the generic deployment hook for the selected guest. Other guest
restrictions and complete recovery/version-to-version acceptance remain open.
The four older production stage templates and the older destroy template were
preserved; unrelated working submodule changes remain separate.

## Verify portable AutoDeploy configuration and monitoring — 2026-11-04

The AutoDeploy reference advances to `ce2ab03`, documenting implementation
`a522e7b`, native-rule/group correction `1e89880` and trusted self-targeting fix
`2ef4d42`. Normal remote imports installed fourteen templates while preserving
fifty-five existing templates. The receiving AAP then completed selector 84,
prerequisite job 86 and importer 88 on `8c5a05c`, preserving all sixty-nine
template IDs and bindings. The older production-only family remains on its
original controller and outside future bundles. A complete successor VM cycle
and independent recovery remain separate acceptance requirements.

The AIOps reference advances to `55bf093`. Normal monitoring jobs enabled the
selected minimal guest's Linux/ICMP checks, with fresh data, and disabled copied
Apache checks in place. Problem guard `ba7785d` rejects recovery and unknown
events. General AI repair remains disabled pending the concrete private-runtime
prerequisites in `bead-wd-72f.33`; website recovery stays active and verified.

The inventory display rename preserves physical VM, DNS, allocation and token
identities. Its normal AIOps refresh retained runtime ciphertext and activation
state. Future shared-capture cleanup removes fourteen project-runtime fields;
older live production consumers still retain their required variables. Hactar
publication `26ea548` preserves the exact verified permissions, independent
deployment evidence and full encrypted task recovery records. Unrelated working
submodule references are preserved.

## 2026-11-05 — Track verified RHEL patching and configuration deployment

The umbrella now tracks RHEL `9383e56bef6b8c3366077f357f8a5b7bec5f8838` (0.5.6) and
AutoDeploy `0442d43c2790ec5f8b51868334b5c4999f540637` (0.44.2). Other project references are preserved.

The first RHSA interval verified baseline exclusion, one-advisory minor updates,
native RPM fix checks on Test and Prod, and reuse of the exact tested minor.
The midpoint cutoff was published and verified before Test promotion, preserving
the earlier fix and excluding the next RHSA. No automatic midpoint calculation
is claimed. The RHEL CaC import, seven-template readback and receiving-runtime
diagnostic also passed through the shared importer and protected companion.
The original five bootstrap pairs remain required; RHEL inputs are optional
together. No additional package upgrade is available in the first interval,
so handling that full-host no-update case remains a separate decision.

Umbrella implementation commit: `3e0fc2a4ab7e93b0b3e8c9faa3f0a0f38ff58c55`.
