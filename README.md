# AAP Advanced Features

Demo and automation projects for Red Hat Ansible Automation Platform 2.7.

Each project is its own repository, linked here as a git submodule. This repo
holds no project files — only the index below and the submodule pointers.

Significant decisions and their implementation commits are summarized in
[design_decisions_history.md](design_decisions_history.md). Each changed project
maintains its own README and decision history alongside its implementation.
Umbrella planning lives in [TODO.md](TODO.md), including the pending definition
of shared agent development rules such as per-project versioning, and an
automation code review covering APME, CoP guidance, strict Ansible linting,
readability, reliable collections, Ansible use, MCP access, necessary verification
and opportunities to reduce runtime. Simplification and optimization must preserve
functionality.
It also tracks Git repository backups and restore testing as important future
recovery work.
The Windows project now records successful targeted application synchronization,
export, internal import, baseline installation and upgrades on both endnodes;
see its documentation for verification details. Fresh-environment workflow 1252
passed all 17 stages on 2026-10-07 after verified Windows-only teardown.
The Windows project also provides named monthly internal WSUS baselines,
reproducible Job Template configuration, installed-build assessment and managed
OS update/reboot automation. April 2026 content publication and its internal
approval cutoff have passed live validation. Server 2022 has now reached the
April OS build with no applicable approved updates or pending reboot; Server
2025 installation is still being verified.
Evaluation-image activation preparation and verified recovery with temporary
connectivity are documented, including restoration of client isolation.
The update template supports concurrent jobs with separate managed-host limits;
the Windows guide includes measured runtimes for its ten latest successful jobs.
Managed guests now default to 4 GiB RAM. Existing guests need a clean full VM
stop/start after patching to apply that persistent change. WSUS setup also
provides a focused repair for IIS MIME mappings required to serve UUP payloads.

## Projects

| Submodule | Repository | Description |
|---|---|---|
| `aap_autodeploy_configascode/` | [aap_autodeploy_configascode](https://github.com/kvegh/aap_autodeploy_configascode) | Automated AAP test instance deployment pipeline: golden image clone, DNS/cert/nginx, AAP install, config-as-code. |
| `AIOps_selfhealing_demo/` | [aiops-selfhealing-demo](https://github.com/kvegh/aiops-selfhealing-demo) | AIOps self-healing demo: Zabbix alerts → EDA → Claude CLI → MCP → AAP remediation. |
| `automation-orchestrator/` | [automation-orchestrator](https://github.com/kvegh/automation-orchestrator) | Automation Orchestrator deployment on OpenShift via OLM, with CloudNativePG and AAP OIDC/integration wiring. |
| `ServiceNow-ITSM-Integration/` | [ServiceNow-ITSM-Integration](https://github.com/kvegh/ServiceNow-ITSM-Integration) | ServiceNow ITSM demo plan for incident management, catalog fulfillment, and CMDB reconciliation; implementation pending. |
| `config_exceptions_ng/` | [config_exceptions_ng](https://github.com/kvegh/config_exceptions_ng) | Configuration drift detection and exception handling. |
| `intelligent-assistant/` | [intelligent-assistant](https://github.com/kvegh/intelligent-assistant) | Intelligent Assistant / AI chatbot setup and issue tracking. |
| `disconnected-windows-patching/` | [disconnected-windows-patching](https://github.com/kvegh/disconnected-windows-patching) | Windows OS and application patching with WSUS and Chocolatey/Nexus; named monthly internal baselines, verified offline transfer, managed OS install/reboot automation and application baseline-to-current upgrades. |
| `automation_portal_setup/` | [automation_portal_setup](https://github.com/kvegh/automation_portal_setup) | Ansible automation portal self-service catalog: RHEL appliance on KVM, deployed by cloud-init. |

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

AAP configuration is captured as variable files for the `infra.aap_configuration`
dispatch role. See
[Configuration_as_Code.md](https://github.com/kvegh/aap_autodeploy_configascode/blob/main/Configuration_as_Code.md)
for the CaC architecture, file layout, and variable naming.

The primary goal is a new AAP that can take over the production platform's
tasks, including deploying further AAP instances. A trusted seed starts with
independently supplied Git and Vault access. The encrypted base stores credential
inputs for a trusted replacement, while automatic credential and deployment-template
provisioning, complete production capture, functional verification and controlled
takeover remain planned. Demo-specific configuration stays separate from base.
Autodeploy also tracks automated MCP access and Vault-encrypted per-instance
connection values as future work. Persistent API tokens are created manually for
now; encrypted write-back and client trust setup remain unimplemented.

The four deployment stages completed on a fresh environment as individually
launched jobs on 2026-10-18, ending with subscription import and platform-only
base configuration. Stage 03 can resume monitoring an existing installer after
a Controller timeout without starting another installation. The separate AIOps
configuration import is now verified: all 29 expected objects exist, its projects
are synchronized, and both EDA activations are running. Automatic job handoff
and functional remediation tests remain planned.

Disconnected Windows has its own configuration import playbook and Job Template,
which load its encrypted private capture without launching the imported jobs or
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
A separate CaC import playbook and Job Template are
available with Git and Vault credentials attached. The configuration import
completed successfully: independent verification found all eight owned objects,
a synchronized project, and matching inventory, execution environment,
credential, label, survey, and extra-variable definitions. The imported deployment
and cleanup Job Templates have never run; OpenShift deployment and functional
validation remain pending.

The Assistant Team capture follows its current public code and external
encrypted configuration snapshots. Deployment and recovery definitions are
separate from optional authentication maintenance, which needs authorization
and CA trust for the target AAP. Its dedicated importer and import Job Template
are created, using the existing CaC Git-token credential type. The supplied
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

Existing playbooks keep runtime Vault files inside their project, because AAP
syncs each project separately and a path outside it is not resolvable. For
`aap_autodeploy_configascode` that file is `myvars`, supplying variables such
as `vault_domain`, `vault_ansible_user`, `vault_ansible_password` and
`vault_aap_install_user`. Where a value appears in documentation rather than
code, it is written as a placeholder such as `YOURDOMAIN.tld`.

AAP configuration captures for demos are maintained as fully Vault-encrypted
files in private secrets repositories. Plaintext working captures, ownership
inventories, and export output stay outside Git. Demo configuration is imported
separately after platform base setup; extracting configuration does not deploy it.
The deployment playbooks download private CaC ciphertext through authenticated
Git during execution, then decrypt it using the attached CaC Vault credential.
