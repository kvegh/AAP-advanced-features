# AAP Advanced Features

Demo and automation projects for Red Hat Ansible Automation Platform 2.7.

Each project is its own repository, linked here as a git submodule. This repo
holds no playbooks or project data — only the index below, the submodule
pointers, and umbrella-level planning and decision records.

Significant decisions and their implementation commits are summarized in
[design_decisions_history.md](design_decisions_history.md). Each changed project
maintains its own README and decision history alongside its implementation.
Beads tracks active work; the existing [TODO.md](TODO.md) overview includes the pending definition
of shared agent development rules such as per-project versioning, and an
automation code review covering APME, CoP guidance, strict Ansible linting,
readability, reliable collections, Ansible use, MCP access, necessary verification
and opportunities to reduce runtime. Simplification and optimization must preserve
functionality.
It also tracks Git repository backups and restore testing as important future
recovery work.

The [agreed recovery and deployment targets](aap_autodeploy_configascode/docs/recovery-and-use-case-targets.md)
describe external-AAP recovery, independent versioned environments, retained
older templates, self/remote CaC installation and use-case runtime destinations.
Current tasks are listed in [AutoDeploy's backlog](aap_autodeploy_configascode/TODO.md)
and [Hactar's backlog](https://github.com/kvegh/hactarconfig/blob/main/TODO.md).
The [Hactar recovery proof](https://github.com/kvegh/hactarconfig/blob/main/docs/recovery-proof.md)
defines the full acceptance checks; agreed targets and successful CaC imports
do not establish that the complete recovery cycle has passed.

The current delivery focus is a repeatable demonstration: deploy through the
existing jobs, demonstrate visible behavior, reset owned resources, and fix any
failed automation step before repeating the sequence. Keep intended-resource and
production safeguards; avoid adding generic recovery layers or duplicating run
history in the operator instructions. OpenShift runtime verification is deferred.

The current AutoDeploy reference includes the concise demo guide, shared
release/retirement helpers, selected private AAP MCP issuer trust and explicit
target prompts for the three later infrastructure stages. Its public overview
includes the closed agent-remediation acceptance, deferred independent CloudCLI
CaC work and current integration inputs;
full records remain in the separate encrypted Hactar checkpoint. This reference
uses AutoDeploy source 0.48.7, including the guest SSH connection correction.
The Windows reference includes the baseline, approved evaluation activation,
five-guest reset and final AAP-interface cleanup sequence. All five guest creation
stages, AD, evaluation activation, WSUS, exact April OS builds and the complete
application baseline-to-upgrade chain passed. The approved repository firewall
rule was applied and tested; it is no longer an unanswered prerequisite. The
current Windows reference is source 1.1.11, including the Python 3.9 file-check
correction. Final teardown passed: all five Windows guests and their owned
resources were removed, with unrelated guests and golden images preserved.
This repaired, staged reset does not establish fresh unattended provisioning.
The Assistant software validation and normal retirement passed.

Command Center is registered below at published source 0.34.0, including the
approval-button sizing and SSH-tunnel origin fixes. The existing installation's
backend HTTPS and strict nginx trust passed verification; the operator confirmed
both external and localhost access work. Its shared CaC importer and target
prerequisites are prepared. The separate AAP-driven test deployment still waits
for the initial-password and mandatory first-login password-change feature.

The AIOps reference adds bounded agent repair and native recovery checks. Normal
Claude installation verified private AAP MCP with trusted application-scoped TLS
and checked the Linux and Zabbix MCP connections. The controlled service-outage
rehearsal then passed: a real monitoring event reached EDA, one bounded agent
invocation launched one saved repair, and native service/fresh recovery checks
passed. The scoped agent and website activations remain running. This tests a
stopped service, not package removal or complete independent successor recovery.
The existing production AIOps project is deliberately pinned to its previously tested
commit so the new demo code can advance without changing that older runner.
Shared desired configuration for new demo instances continues to use `main`.

The Windows demo retains its approved HTTPS/NTLM certificate-validation
exception, recorded as false. Authenticated Windows facts, exact clone ownership
and the pinned test hypervisor remain required. Its infrastructure job owns the
selected AAP's additional isolated NIC and persistent RHEL connection; CaC import
remains API-only. Production access and private MCP boundaries remain protected.

The number of AAP Job Templates across projects needs review: identify obsolete
or duplicate entries and opportunities to consolidate them while preserving
required functionality and useful independent stages. This pending review is
tracked as Beads `bead-wd-1kf`; see
[the umbrella overview](TODO.md#12-review-the-number-of-aap-job-templates).

The Windows project now records successful targeted application synchronization,
export, internal import, baseline installation and upgrades on both endnodes;
see its documentation for verification details. Fresh-environment workflow 1252
passed all 17 stages on 2026-10-07 after verified Windows-only teardown.
Fresh workflow 2303 subsequently passed the expanded 21-stage end-to-end test
in 3h48m50s, finishing on 2026-10-21 at 01:01 UTC. It joins both content imports,
applies the internal April ceiling, patches the two endnodes independently, and
then deploys baseline and upgraded applications. Preservation checks before and
after rebuilding confirmed seven unrelated VM definitions/states and both base
images unchanged.
The Windows project also provides named monthly internal WSUS baselines,
reproducible Job Template configuration, installed-build assessment and managed
OS update/reboot automation. April 2026 content publication and its internal
approval cutoff have passed live validation. Both Server 2022 and Server 2025
have reached their April OS and .NET baselines with no applicable approved
updates or pending reboot. Per-clone evaluation activation is implemented as a
deployment stage after Windows basics: it preserves permanent adapters, uses
approved temporary connectivity where needed, and verifies restoration of the
original topology. Code, encrypted inputs and reproducible AAP configuration
are documented in the Windows project.
The activation Check and normal licensed skip path passed on the existing clones.
The fresh test also verified activation of an initially unlicensed Server 2025
clone and restoration of its original topology. Application completion now checks
installer reboot signals and Windows servicing markers before reporting success;
the standalone assessment template receives the correct existing credentials.
The update template supports concurrent jobs with separate managed-host limits;
the Windows guide records historical runtimes and all fresh-test stage timings.
Managed guests default to 4 GiB RAM, and both fresh endnodes were created with
that allocation, verified in libvirt and Windows. WSUS setup also
provides a focused repair for IIS MIME mappings required to serve UUP payloads.

## Projects

| Submodule | Repository | Description |
|---|---|---|
| `Agent_generated_code_review/` | [Agent_generated_code_review](https://github.com/kvegh/Agent_generated_code_review) | Dedicated home for review rules for AI agent-generated Ansible code; rules to be formulated. |
| `aap_autodeploy_configascode/` | [aap_autodeploy_configascode](https://github.com/kvegh/aap_autodeploy_configascode) | Automated AAP test instance deployment pipeline: golden image clone, DNS/cert/nginx, AAP install, config-as-code. |
| `AIOps_selfhealing_demo/` | [aiops-selfhealing-demo](https://github.com/kvegh/aiops-selfhealing-demo) | AIOps self-healing demo: Zabbix alerts → EDA → Claude CLI → MCP → AAP remediation, with environment-selectable website checks. |
| `automation-orchestrator/` | [automation-orchestrator](https://github.com/kvegh/automation-orchestrator) | Automation Orchestrator deployment on OpenShift via OLM, with CloudNativePG and AAP OIDC/integration wiring. |
| `ServiceNow-ITSM-Integration/` | [ServiceNow-ITSM-Integration](https://github.com/kvegh/ServiceNow-ITSM-Integration) | ServiceNow ITSM demo plan for incident management, catalog fulfillment, and CMDB reconciliation; implementation pending. |
| `config_exceptions_ng/` | [config_exceptions_ng](https://github.com/kvegh/config_exceptions_ng) | Configuration drift detection and exception handling. |
| `intelligent-assistant/` | [intelligent-assistant](https://github.com/kvegh/intelligent-assistant) | Intelligent Assistant / AI chatbot setup and issue tracking. |
| `disconnected-windows-patching/` | [disconnected-windows-patching](https://github.com/kvegh/disconnected-windows-patching) | Windows OS and application patching with WSUS and Chocolatey/Nexus; named monthly internal baselines, verified offline transfer, managed OS install/reboot automation and application baseline-to-current upgrades. |
| `automation_portal_setup/` | [automation_portal_setup](https://github.com/kvegh/automation_portal_setup) | Ansible automation portal self-service catalog: RHEL appliance on KVM, deployed by cloud-init. |
| `Automation_Dashboard/` | [Automation_Dashboard](https://github.com/kvegh/Automation_Dashboard) | Usage statistics and ROI reporting for AAP: simulated maintenance jobs that generate realistic runtimes for Automation Analytics. |
| `CMDB-for-AAP/` | [CMDB-for-AAP](https://github.com/kvegh/CMDB-for-AAP) | Authoritative host record for the demo estate, with git, ServiceNow and fact-generated flavours. |
| `RHEL-sniperpatching/` | [RHEL-sniperpatching](https://github.com/kvegh/RHEL-sniperpatching) | Staged RHEL patching by one RHSA or multiple CVEs with live Satellite lookup, automatic baseline cutoffs, verified date-bounded repository publications, generic stage surveys and authoritative RPM proof; complete single-RHSA/cutoff/full Test/Prod cycle and receiving-AAP import/runtime verified. |
| `command-center-ng/` | [command-center-ng](https://github.com/kvegh/command-center-ng) | Local agent command center with a RHEL 9 installer and AAP deployment playbook; its encrypted private CaC companion uses the shared AutoDeploy importer. |

## Cloning

Submodule directories are empty after a plain `git clone`. To get everything:

    git clone --recurse-submodules https://github.com/kvegh/AAP-advanced-features.git

For an existing clone:

    git submodule update --init --recursive

To pull the latest commit of every project:

    git submodule update --remote

A submodule records a specific commit, so after updating a project you commit
the new pointer here:

    git -C <project> pull
    git add <project> && git commit -m "bump <project>"

## Config-as-Code

Use-case deployment keeps the target instance name as a launch-time input.
AAP inventory hosts store their explicit API `ansible_fqdn`;
shared VM groups carry `hypervisor_host`. Future AutoDeploy installations verify
the nginx upstream certificate before publishing the API. Existing production
SSL is unchanged.

Each reviewed private CaC repository has separate credentials named
`<repo-name> CaC repo read token` and `<repo-name> CaC vault cred`. Encrypted base
bootstrap provisions these pairs, and each importer uses its repository's pair.
The original five bootstrap pairs remain required; supply both optional RHEL
entries together.
The reusable `Cac_git_token_type` injects `CAC_GIT_TOKEN` for the private
configuration fetch; it is separate from playbook SCM checkout and destination
AAP API authentication.
See the AutoDeploy [credential overview](aap_autodeploy_configascode/README.md).
The AutoDeploy repository's CaC Vault credential also encrypts and decrypts its
shared instance registry; no separate registry Vault credential is required.
Its existing repository read token reads that registry too. The redundant
registry-reader credential/type is no longer provisioned or used by the jobs.
The `VM allocation git Pseudo CMDB writer` credential uses the existing `Cac_git_token_type` with its
own write token; repository readers retain their separate read-only tokens.
The writer token is stored as `inputs.token` in its encrypted shared-base
credential entry. Allocation and extraction derive the repository URL from
encrypted runtime configuration and use the existing environment Vault.
Existing controllers require credential migration before using this updated
code. A writer with job history needs an approved replacement. The owner chose
`VM allocation git Pseudo CMDB writer` and deletion of the retired credential
after verification. An unused writer can change type in place.
Replacing this temporary Git/YAML registry with a real CMDB is tracked as
Beads `bead-wd-sc8`; product selection and migration require an agreed design.

The six project deployment Job Templates share
[`deploy-cac-project.yml`](aap_autodeploy_configascode/deploy-cac-project.yml).
Each template fixes its project ID and repository Git/Vault credentials. The
playbook derives `<project-id>-secrets` and
`vaults/cac/<project-id>-cac-vault.yml` from that ID; the platform base capture
remains separate. The existing templates keep their IDs and workflow links.
Each template stores `aap_cac_project_id` in Extra Variables and calls the shared
playbook directly. The unused per-project wrappers have been removed.

| Project ID | Deployment Job Template |
|---|---|
| `aiops-selfhealing-demo` | Deploy AIOps Selfhealing Demo CaC |
| `disconnected-windows-patching` | Deploy Disconnected Windows Patching CaC |
| `automation-orchestrator` | Deploy Automation Orchestrator CaC |
| `assistant-team` | Deploy Assistant Team CaC |
| `aap_autodeploy_configascode` | Deploy AAP Autodeploy Configascode CaC |
| `RHEL-sniperpatching` | Deploy RHEL Sniperpatching CaC |

The RHEL first interval has verified its cutoff baseline, single-advisory minor,
targeted Test/Prod patches and exact tested-minor reuse. The date-bounded
publication preserves that fix and excludes the next RHSA. Configuration import
and the receiving-runtime diagnostic also passed. The first cutoff has no
additional eligible package upgrade; both full host updates completed as verified
already-current runs.


At launch, select the destination inventory host. The saved **AAP API/MCP Auth
Token Store** supplies that instance's bearer token and matches its HTTPS
endpoint to the host's `ansible_fqdn`. The playbook verifies the certificate and
authenticates directly from the source execution environment; missing or
mismatched access stops before configuration changes. Repository access and
destination API access remain separate credentials. An instance can also target
itself through its own verified API. See
[instance token storage](aap_autodeploy_configascode/docs/instance-token-store.md)
for the encrypted records and token selection.

Project captures declare their resource lists and any required service
credentials. Imports update definitions without launching jobs; new EDA
activations are disabled and existing activation states are preserved. The
multi-project selector remains separate orchestration. See the
[consolidation analysis](aap_autodeploy_configascode/docs/deployment-consolidation-analysis.md)
for the reasons for sharing the implementation. Source validation and template
installation do not establish a successful use-case import; deployment results
are documented separately.

AAP configuration is captured as variable files for the `infra.aap_configuration`
dispatch role. See
[Configuration_as_Code.md](https://github.com/kvegh/aap_autodeploy_configascode/blob/main/Configuration_as_Code.md)
for the CaC architecture, file layout, and variable naming.

The primary goal is a new AAP that can take over the production platform's
tasks, including deploying further AAP instances. A trusted seed starts with
independently supplied Git and Vault access. The encrypted base provisions
credentials for a trusted replacement; the selected project imports create their
deployment templates. Complete production capture, functional verification and
controlled takeover remain separate work. Demo-specific configuration stays
separate from base.
Normal base deployment now creates and publishes each new instance's API/MCP
token in encrypted per-instance configuration. The selected instance name
determines its trusted API URL and token for the shared importer. The normal
base job also configures the selected AAP guest's exact SSH connection to its
own hypervisor, with persistent firewall rules and identity checks.

The shared importer has now successfully applied all five supported captures:
AIOps, Assistant Team, Disconnected Windows Patching, Automation Orchestrator and
AutoDeploy configuration to a
new test instance. Their objects, credentials and relationships were checked
independently, preserving earlier imports. The four older AAP deployment stages
stay on production and are excluded from future CaC installations. Future
environments use the newer four-stage templates, which still need verification
against both their source AAP's own hypervisor and a selected remote hypervisor.
The original production hypervisor is excluded from that versioned test chain.
The future bundle also excludes the old destroy template, workflow, provisioning
inventory and original Machine key, without deleting existing production objects.
Its normal import added fourteen templates and retained all fifty-five existing
templates, with credential and resource bindings independently checked. Importing
configuration does not run the imported application jobs or prove a new-VM cycle.
The receiving AAP also completed its normal self-target selector, including the
existing prerequisite and AutoDeploy import jobs, with trusted API access.

For AIOps, both new MCP installations have passed real read-only queries against
their matching testserver and monitoring instance. Website, monitoring and MCP
settings and guest ownership live in its private companion repository rather than AutoDeploy's
AAP configuration. Zabbix deployment, quarantine, DNS and trusted HTTPS also
passed independent verification. Website deployment and its restore/rearm
loop were verified separately from the configuration import: normal deployment
and both a controlled fault and a real website button press completed automatic
restore and rearm. The scoped agent deployment and a passive ping from the new
monitoring VM also passed. The normal monitoring deployment now enables the
selected testserver's Linux and ICMP checks, with fresh data, while disabling
irrelevant inherited Apache checks in place. The selected model-directed repair
also passed its controlled service-outage rehearsal with native recovery proof.
Its reviewed scoped activation is enabled; a tested problem-only event guard
rejects recovery and unknown events. MCP remains private and uses the existing
on-demand stdio transport.

Repeat imports also preserve serialized activation variables, including their
original formatting. The corrected import was verified while the website
activation stayed running, preserving existing template identities and the
selected Event Stream. Real definition changes still follow the native API's
update rules.

The results below describe earlier deployments using the former per-project
importers. Current shared-importer results are described above.

The four deployment stages completed on a fresh environment as individually
launched jobs on 2026-10-18, ending with subscription import and platform-only
base configuration. Stage 03 can resume monitoring an existing installer after
a Controller timeout without starting another installation. The separate AIOps
configuration import is now verified: all 29 expected objects exist, its projects
are synchronized, and both EDA activations are running. Automatic job handoff
and functional remediation tests remain planned.

Disconnected Windows has its own Job Template using the shared configuration
import playbook. It loads its encrypted private capture without launching imported jobs or
workflow. The Git credential must have read access to each selected private
configuration repository. Import diagnostics report fixed failure categories
without exposing tokens or raw Git errors. See the Autodeploy README for current
live verification results.

The Windows configuration import is now verified: all 35 expected objects exist,
including 18 Job Templates and a workflow with 17 nodes and 16 links. None of the
imported automation has run. Autodeploy now creates group skeletons before their
memberships to avoid a dependency race on clean targets. Base PAH repository and
Controller-source setup is now deployed and independently verified: certified,
validated, and community sources replace direct public Galaxy access, existing
read tokens are preserved, and no collection content was synchronized. Each use
case must declare and prepare its own collection requirements. The Autodeploy
plan includes a TODO for a complete step-by-step CaC guide.

Orchestrator deployment and cleanup now accept an explicit AAP target and runtime
credentials instead of loading the original AAP connection vault. Their surveys
match those inputs. Cleanup uses a temporary Gateway token and exact application
names; its token is revoked afterward. The encrypted Orchestrator capture is
aligned with that contract and consistently uses `Orchestrator EE` for its
execution environment definition, project default, and Job Templates.
A dedicated CaC Job Template uses the shared import playbook with its repository's
Git and Vault credentials attached. The earlier configuration import
completed successfully: independent verification found all eight owned objects,
a synchronized project, and matching inventory, execution environment,
credential, label, survey, and extra-variable definitions. The imported deployment
and cleanup Job Templates have never run; OpenShift deployment and functional
validation remain pending.

The Assistant Team capture follows its current public code and external
encrypted configuration snapshots. Deployment and recovery definitions are
separate from optional authentication maintenance, which needs authorization
and CA trust for the target AAP. Its dedicated Job Template uses the shared
importer and existing CaC Git-token credential type. The supplied
repository token is stored encrypted and attached to that template. Private Git
access, the pinned certified PAH collection and the cached execution image are
verified. The import restored all 21 ordinary objects and six templates;
independent comparison passed 396 checks. Imported runtime automation and optional
authentication maintenance have not run. Base now mounts its generated CA trust
read-only into project-update execution environments, preserving certificate
verification for local PAH downloads.

Administrator-password management is verified in base. The configured password
works after rollout, the installer inventory stays aligned, and a repeat run
authenticates directly with that password without installer bootstrap. Temporary
configuration tokens and workspaces were removed after both successful jobs.

The Autodeploy TODO now also tracks complete Intelligent Assistant/Lightspeed
capture, including service setup, vaulted credentials and passwords, Gateway
OAuth configuration and independent rebuild verification.

## Secrets

No cleartext secrets in any repo. Sensitive values are ansible-vault encrypted
and committed; an attached AAP Vault credential decrypts them at job runtime.

AutoDeploy still loads its encrypted runtime `myvars` from its code checkout,
including variables such as `vault_domain`, `vault_ansible_user`,
`vault_ansible_password` and `vault_aap_install_user`. AIOps and Assistant Team
keep their current runtime configuration in their separate private companion
repositories and supply encrypted settings or configuration files to the job.
Each project documents its delivery mechanism and required Vault credential;
independent AAP project checkouts do not share filesystem paths. Plaintext
examples use placeholders such as `YOURDOMAIN.tld`.

AAP configuration captures for demos are maintained as fully Vault-encrypted
files in private secrets repositories. Plaintext working captures, ownership
inventories, and export output stay outside Git. Demo configuration is imported
separately after platform base setup; extracting configuration does not deploy it.
The deployment playbooks download private CaC ciphertext through authenticated
Git during execution, then decrypt it using the attached CaC Vault credential.
