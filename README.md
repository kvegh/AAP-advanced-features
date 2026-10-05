# AAP Advanced Features

Demo and automation projects for Red Hat Ansible Automation Platform 2.7.

## Projects

| Directory | Description |
|---|---|
| `aap_autodeploy_configascode/` | Automated AAP test instance deployment pipeline: golden image clone, DNS/cert/nginx, AAP install, config-as-code. See [PLAN.md](aap_autodeploy_configascode/PLAN.md). |
| `AIOps_selfhealing_demo/` | AIOps self-healing demo: Zabbix alerts → EDA → Claude CLI → MCP → AAP remediation. |
| `automation-orchestrator/` | Automation Orchestrator deployment on OpenShift via OLM, with CloudNativePG and AAP OIDC/integration wiring. See [documentation.md](automation-orchestrator/documentation.md). |
| `ServiceNow-ITSM-Integration/` | ServiceNow ITSM integration playbooks (bootstrap pattern). |
| `config_exceptions_ng/` | Configuration drift detection and exception handling. |
| `intelligent-assistant/` | Intelligent Assistant / AI chatbot setup and issue tracking. |
| `collections/` | Vendored Ansible collections (`ansible.controller`, `ansible.eda`). |

## Config-as-Code

AAP configuration is captured as variable files for the `infra.aap_configuration` dispatch role. See [Configuration_as_Code.md](aap_autodeploy_configascode/Configuration_as_Code.md) for the CaC architecture, file layout, and variable naming.
