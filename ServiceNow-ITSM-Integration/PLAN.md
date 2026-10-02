# ServiceNow ITSM Integration for AAP

## Context

The AIOps self-healing demo architecture diagram shows ITSM as a target of the Trusted Execution Layer, but no ITSM system is wired up yet. This project builds a ServiceNow integration demo in a new `ServiceNow-ITSM-Integration` subdir of the AAP-advanced-features repo, covering three use cases:

1. **UC1 — Service Catalog → Spoke → AAP:** ServiceNow catalog item triggers AAP job via Ansible Spoke, job processes the request and updates/closes the SNow ticket + CMDB
2. **UC2 — Zabbix → EDA → SNow incident:** Extends the existing AIOps self-healing demo — when Zabbix fires an event and EDA triggers remediation, Ansible also creates/updates/closes a ServiceNow incident
3. **UC3 — CMDB reconciliation:** Playbook that compares infrastructure reality against ServiceNow CMDB and flags/fixes discrepancies

Uses the certified `servicenow.itsm` collection throughout.

Reference repo: https://github.com/shadowman-lab/Ansible-SNOW

## Prerequisites to verify/complete

- [ ] **Sync `servicenow.itsm` to PAH** — not currently in the Private Automation Hub's rh-certified repo. Sync from console.redhat.com → Automation Hub → rh-certified content. Alternatively, add `collections/requirements.yml` to the project and configure the org's Galaxy credentials so AAP auto-installs at project sync.
- [ ] **Verify collection availability in EE** — check if `ee-supported-rhel9` ships `servicenow.itsm`. If not, either rely on project-level `collections/requirements.yml` or build a custom "ServiceNow EE".
- [ ] **ServiceNow instance** — Zurich release. Service account configured with "Web service access only" + `rest_api_explorer` role. Verify it's still active.
- [ ] **IntegrationHub subscription** — required for Ansible Spoke (UC1). Confirm it's available on the instance.

## Phase 0 — Foundation (AAP + repo setup)

### 0.1 Directory structure

```
ServiceNow-ITSM-Integration/
    PLAN.md
    README.md
    collections/requirements.yml          # servicenow.itsm, community.general
    vars/
        main.yml                          # non-sensitive config (SNow table names, field mappings)
        vault.yml.example                 # template: SN_HOST, SN_USERNAME, SN_PASSWORD
    playbooks/
        snow_create_incident.yml          # UC2: create incident
        snow_update_incident.yml          # UC2: update/close incident
        snow_catalog_fulfill.yml          # UC1: fulfill catalog request
        snow_cmdb_reconcile.yml           # UC3: CMDB vs reality
        snow_cmdb_update.yml              # shared: update a CI in CMDB
    roles/
        servicenow_credential/           # custom credential type setup (AAP-side)
        servicenow_incident/             # create/update/close incidents
        servicenow_cmdb/                 # CMDB operations
        servicenow_catalog/              # catalog RITM handling
    docs/
        00-prerequisites.md              # PAH sync, EE, SNow instance prep
        01-aap-setup.md                  # credential type, credential, project, JTs
        02-spoke-setup.md                # OAuth app in AAP, Spoke config in SNow
        03-uc1-service-catalog.md        # UC1 walkthrough
        04-uc2-incident-management.md    # UC2 walkthrough (AIOps extension)
        05-uc3-cmdb-reconciliation.md    # UC3 walkthrough
```

### 0.2 ServiceNow credential type in AAP

Custom credential type injecting `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` as env vars. The `servicenow.itsm` collection reads these automatically — zero credential references in playbooks.

**Input configuration:**
- `sn_host` (string, required) — ServiceNow instance URL
- `sn_username` (string, required)
- `sn_password` (string, secret, required)

**Injector configuration:**
- env: `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD`

### 0.3 ServiceNow credential

Create credential using the new type, populated with the SNow instance details.

### 0.4 Job templates

Create JTs for each playbook, all using:
- Project: "AAP Advanced Features"
- Credential: the new ServiceNow credential (+ machine cred where host access needed)
- EE: verify `ee-supported-rhel9` works; if not, create ServiceNow EE

## Phase 1 — UC2: Zabbix → EDA → SNow incident (extend AIOps demo)

Starting with UC2 because it extends the existing working demo — fastest path to visible results.

### What changes

1. **New playbook `snow_create_incident.yml`** — called from the existing AIOps remediation workflow. Creates a ServiceNow incident with:
   - Short description from Zabbix alert name
   - Description with host, alert details, timestamps
   - Caller: service account
   - Impact/urgency based on Zabbix severity
   - `set_stats` to pass `ticket_number` and `incident_sys_id` downstream

2. **New playbook `snow_update_incident.yml`** — called after remediation completes. Updates the incident:
   - If remediation succeeded: resolve with work notes describing what was done
   - If remediation failed/escalated: add work notes, leave open, bump priority

3. **Wire into AIOps workflow** — the existing EDA-triggered flow gets two new nodes:
   - Node at start: create incident (runs parallel to or before remediation)
   - Node at end: update/close incident based on remediation outcome

4. **CMDB update** — after successful remediation, update the CI record with current state

### Role: `servicenow_incident`

Dispatch on variable (`servicenow_action: create|update|close|find`):
- `create`: `servicenow.itsm.incident` with state=new
- `update`: add work notes, change state
- `close`: set state=resolved, close_code, close_notes
- `find`: `servicenow.itsm.incident_info` by number or sys_id

Reference: `Ansible-SNOW/roles/servicenow_ticket/` — adapt the dispatch pattern, drop custom fields specific to the reference instance.

## Phase 2 — UC1: Service Catalog → Spoke → AAP

### ServiceNow side (manual steps, documented in docs/02 and 03)

1. **OAuth application in AAP** — create via AAP admin UI. Note: AAP 2.5+ auto-applies an API Script that causes 401s with Spoke; it must be deleted.
2. **Ansible Spoke setup** — install from ServiceNow Store (requires IntegrationHub). Configure:
   - Connection credential with AAP OAuth client ID/secret
   - Connection alias pointing to AAP controller URL (must use `/controller/v2` endpoint path for AAP 2.5+)
   - Test connection
3. **Service Catalog item** — create a sample catalog item (e.g., "Request Linux Server"). Variables: hostname, OS, environment, owner.
4. **Flow Designer flow** — trigger on catalog item request, call Ansible Spoke action "Launch Job Template", pass variables as extra_vars.

### AAP side (automated via playbooks)

1. **Playbook `snow_catalog_fulfill.yml`** — receives extra_vars from Spoke (or webhook):
   - Reads request parameters
   - Does the provisioning work (or simulates it for demo)
   - Updates the RITM in ServiceNow (state=closed_complete)
   - Creates/updates CMDB CI record

### Role: `servicenow_catalog`

- Retrieve RITM details by sys_id
- Resolve variable mappings
- Close RITM with fulfillment notes

## Phase 3 — UC3: CMDB Reconciliation

### Playbook `snow_cmdb_reconcile.yml`

1. Gather facts from managed hosts (hostname, OS, IP, memory, CPUs)
2. Query ServiceNow CMDB for matching CIs (`servicenow.itsm.configuration_item_info`)
3. Compare gathered facts vs CMDB records
4. Report discrepancies
5. Optionally update CMDB to match reality (`servicenow.itsm.configuration_item`)

### Role: `servicenow_cmdb`

- `query`: find CI by name/IP/sys_id
- `update`: update CI fields (ip_address, os, host_name, fqdn, state)
- `create`: create new CI if host exists in inventory but not in CMDB
- `reconcile`: compare and report/fix

## Implementation order

1. **Phase 0** — repo structure, credential type, credential, collections (foundation)
2. **Phase 1 UC2** — incident management (extends AIOps demo, fastest visible value)
3. **Phase 2 UC1** — catalog/Spoke (requires manual SNow-side setup, document the steps)
4. **Phase 3 UC3** — CMDB reconciliation (most standalone, can be done last)

## Verification

- **UC2:** Trigger a Zabbix alert → verify EDA fires → verify incident appears in ServiceNow → verify incident updates/closes after remediation
- **UC1:** Order a catalog item in ServiceNow → verify AAP job launches → verify RITM closes in ServiceNow
- **UC3:** Run reconciliation playbook → verify discrepancy report → verify CMDB updates
- **Credential injection:** Run a simple test playbook that does `servicenow.itsm.incident_info` to confirm the credential type works
