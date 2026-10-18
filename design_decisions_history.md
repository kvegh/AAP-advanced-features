# Design decisions history

This retrospective records significant decisions from Git history and available
session requirements. Implementation details belong in the individual projects.

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
