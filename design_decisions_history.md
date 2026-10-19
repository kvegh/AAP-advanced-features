# Design decisions history

This retrospective records significant decisions from Git history and available
session requirements. Implementation details belong in the individual projects.

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
