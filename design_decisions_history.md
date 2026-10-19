# Design decisions history

This retrospective records significant decisions from Git history and available
session requirements. Implementation details belong in the individual projects.

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
