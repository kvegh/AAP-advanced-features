# AAP Advanced Features

Demo and automation projects for Red Hat Ansible Automation Platform 2.7.

Each project is its own repository, linked here as a git submodule. This repo
holds no project files — only the index below and the submodule pointers.

## Projects

| Submodule | Repository | Description |
|---|---|---|
| `aap_autodeploy_configascode/` | [aap_autodeploy_configascode](https://github.com/kvegh/aap_autodeploy_configascode) | Automated AAP test instance deployment pipeline: golden image clone, DNS/cert/nginx, AAP install, config-as-code. |
| `AIOps_selfhealing_demo/` | [aiops-selfhealing-demo](https://github.com/kvegh/aiops-selfhealing-demo) | AIOps self-healing demo: Zabbix alerts → EDA → Claude CLI → MCP → AAP remediation. |
| `automation-orchestrator/` | [automation-orchestrator](https://github.com/kvegh/automation-orchestrator) | Automation Orchestrator deployment on OpenShift via OLM, with CloudNativePG and AAP OIDC/integration wiring. |
| `ServiceNow-ITSM-Integration/` | [ServiceNow-ITSM-Integration](https://github.com/kvegh/ServiceNow-ITSM-Integration) | ServiceNow ITSM integration playbooks (bootstrap pattern). |
| `config_exceptions_ng/` | [config_exceptions_ng](https://github.com/kvegh/config_exceptions_ng) | Configuration drift detection and exception handling. |
| `intelligent-assistant/` | [intelligent-assistant](https://github.com/kvegh/intelligent-assistant) | Intelligent Assistant / AI chatbot setup and issue tracking. |
| `disconnected-windows-patching/` | [disconnected-windows-patching](https://github.com/kvegh/disconnected-windows-patching) | AAP and WSUS demo for Windows patching in a simulated disconnected environment. |

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

## Secrets

No cleartext secrets in any repo. Sensitive values are ansible-vault encrypted
and committed — an AAP vault credential decrypts them at job runtime, so the
ciphertext has to be in the synced project.

Playbooks reference them as variables from `myvars` at this repo's root, e.g.
`vault_domain`, `vault_ansible_user`, `vault_ansible_password`,
`vault_aap_install_user`. Where a value appears in documentation rather than
code, it is written as a placeholder such as `YOURDOMAIN.tld`.
