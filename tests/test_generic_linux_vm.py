"""Exercise the canonical shared normal-image path without a hypervisor or network."""
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml
from ansible.errors import AnsibleFilterError
from ansible.parsing.vault import VaultLib, VaultSecret

ROOT = Path(__file__).resolve().parents[1]
ROLE = ROOT / 'playbooks/roles/linux_vm'
spec = importlib.util.spec_from_file_location('upstream_pin', ROOT / 'playbooks/filter_plugins/linux_vm_recovery.py')
identity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(identity)


def pin():
    return {'address': '192.0.2.10', 'user': 'fixture', 'port': 22,
            'machine_id': '1' * 32, 'host_keys': ['ssh-ed25519 AAAA']}


class NormalUpstreamTests(unittest.TestCase):
    def run_play(self, root, tasks, variables, *, check=False, roles=None):
        path = root / 'play.yml'
        path.write_text(yaml.safe_dump([{'name': 'Disposable upstream fixture', 'hosts': 'localhost',
            'connection': 'local', 'gather_facts': False, 'vars': variables, 'tasks': tasks}], sort_keys=False))
        env = dict(os.environ, ANSIBLE_NOCOLOR='1', ANSIBLE_HOME=str(root / 'home'),
            ANSIBLE_LOCAL_TEMP=str(root / 'local'), ANSIBLE_REMOTE_TEMP=str(root / 'remote'),
            ANSIBLE_FILTER_PLUGINS=str(ROOT / 'playbooks/filter_plugins'),
            ANSIBLE_ROLES_PATH=str(roles or ROOT / 'playbooks/roles'))
        args = [sys.executable, '-m', 'ansible.cli.playbook', '-i', 'localhost,', str(path)]
        if check:
            args.append('--check')
        return subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, timeout=90)

    def inputs(self, root):
        source = root / 'source.qcow2'
        source.write_bytes(b'unchanged synthetic image baseline')
        route = {'vm_name': 'fixture-v07', 'generic_image': True, 'update_packages': False,
            'golden_image_path': str(source), 'source_image_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'vm_dir': str(root / 'vms'), 'vm_domain': 'example.invalid', 'vm_network': 'normal',
            'network_bridge': 'fixture0', 'hypervisor_pin': pin()}
        provision = dict(route, guest_ssh_user='fixture', guest_ssh_password='synthetic-bootstrap-canary',
                         guest_become_password='synthetic-bootstrap-canary')
        variables = {'ansible_host': pin()['address'], 'linux_vm_upstream': route,
            'vm_name': route['vm_name'], 'linux_vm_deployment_name': route['vm_name'],
            '__linux_vm_environment': {'provisioning':deepcopy(provision)},
            'provisioning': provision, 'role_path': str(ROLE),
            'linux_vm_hostname': route['vm_name']+'.'+route['vm_domain']}
        return route, provision, variables

    def preflight(self, *, wrong_machine=False, wrong_hash=False, wrong_bridge=False, empty_route=False, missing_source=False):
        with tempfile.TemporaryDirectory(prefix='normal-image-preflight-') as tmp:
            root = Path(tmp)
            route, provision, variables = self.inputs(root)
            if wrong_hash:
                provision['source_image_sha256'] = route['source_image_sha256'] = '0' * 64
            if empty_route:
                variables['linux_vm_upstream']={}
            if missing_source:
                variables.pop('__linux_vm_environment')
            tasks = deepcopy(yaml.safe_load((ROLE / 'tasks/upstream-preflight.yml').read_text()))
            for task in tasks:
                if task['name'].startswith('Verify the actual'):
                    task['ansible.builtin.command']['argv'] = [sys.executable, '-c', "print('%s')" % ('2' * 32 if wrong_machine else '1' * 32)]
                if task['name'].startswith('Read the selected normal upstream network'):
                    xml = '<network><name>normal</name><bridge name="%s"/></network>' % ('other0' if wrong_bridge else 'fixture0')
                    task['ansible.builtin.command']['argv'] = [sys.executable, '-c', 'print(' + repr(xml) + ')']
            marker = root / 'passed'
            tasks.append({'name': 'First disposable storage boundary', 'ansible.builtin.file': {'path': str(marker), 'state': 'touch'}})
            result = self.run_play(root, tasks, variables)
            expected = not any((wrong_machine, wrong_hash, wrong_bridge, empty_route, missing_source))
            self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)
            self.assertEqual(marker.exists(), expected)
            self.assertEqual(Path(route['golden_image_path']).read_bytes(), b'unchanged synthetic image baseline')
            self.assertNotIn('synthetic-bootstrap-canary', result.stdout + result.stderr)

    def test_normal_preflight_accepts_only_exact_identity_source_hash_and_bridge(self):
        self.preflight()

    def test_missing_encrypted_namespace_cannot_select_normal_mode(self):
        self.preflight(missing_source=True)

    def test_wrong_machine_stops_before_storage(self):
        self.preflight(wrong_machine=True)

    def test_wrong_source_hash_stops_before_storage(self):
        self.preflight(wrong_hash=True)

    def test_wrong_network_bridge_stops_before_storage(self):
        self.preflight(wrong_bridge=True)

    def test_normal_publication_never_calls_recovery_release_and_cleans_public_trust(self):
        with tempfile.TemporaryDirectory(prefix='normal-image-publication-') as tmp:
            root = Path(tmp)
            _, _, variables = self.inputs(root)
            roles = root / 'roles'; poison = roles / 'linux_recovery_release/tasks'; poison.mkdir(parents=True)
            (poison/'main.yml').write_text('- name: Recovery role must never run for normal upstream mode\n  ansible.builtin.fail:\n    msg: Forbidden recovery policy call\n')
            trust = root / 'known_hosts'; trust.write_text('synthetic public key only'); trust.chmod(0o600)
            variables.update(deployment_vm_provenance={'vm_name': 'fixture-v07'}, deployment_vm_vcpus=2,
                deployment_vm_memory_mb=4096, deployment_vm_disk_gb=20, ansible_facts={'machine_id': '2'*32},
                deployment_vm_hypervisor_pin=pin(), deployment_vm_trust_file=str(trust))
            tasks = yaml.safe_load((ROOT/'playbooks/tasks/verified_generic_guest.yml').read_text())
            result = self.run_play(root, tasks, variables, roles=roles)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(trust.exists())
            self.assertNotIn('TASK [Recovery role must never', result.stdout)

    def test_normal_and_recovery_saved_provenance_cannot_be_interchanged(self):
        base={'schema_version':1,'deployment_type':'generic-upstream','vm_name':'fixture-v07','uuid':'fixture-uuid',
              'hypervisor_machine_id':'1'*32,'source_image_sha256':'a'*64,'host_keys':['ssh-ed25519 AAAA']}
        self.assertEqual(identity.saved_keys(base,'fixture-v07','fixture-uuid','1'*32,'a'*64,'generic-upstream'),['ssh-ed25519 AAAA'])
        with self.assertRaises(AnsibleFilterError):
            identity.saved_keys(base,'fixture-v07','fixture-uuid','1'*32,'a'*64)
        with self.assertRaises(AnsibleFilterError):
            identity.saved_keys(dict(base,deployment_type='generic-recovery'),'fixture-v07','fixture-uuid','1'*32,'a'*64,'generic-upstream')

    def test_copied_normal_clone_hash_must_match_before_customization(self):
        source=yaml.safe_load((ROLE/'tasks/main.yml').read_text())
        start=next(i for i,t in enumerate(source) if t['name']=='Hash the newly copied normal upstream clone before customization')
        checks=source[start:start+2]
        for changed in [False,True]:
            with self.subTest(changed=changed),tempfile.TemporaryDirectory(prefix='normal-clone-hash-') as tmp:
                root=Path(tmp)
                route,_,variables=self.inputs(root)
                clone=root/'clone.qcow2';clone.write_bytes(b'wrong-copy' if changed else Path(route['golden_image_path']).read_bytes())
                variables['linux_vm_deployment_disk']=str(clone)
                marker=root/'customization-boundary'
                tasks=checks+[{'name':'Disposable customization boundary','ansible.builtin.file':{'path':str(marker),'state':'touch'}}]
                result=self.run_play(root,tasks,variables)
                self.assertEqual(result.returncode==0,not changed,result.stdout+result.stderr)
                self.assertEqual(marker.exists(),not changed)
                self.assertTrue(clone.exists())

    def test_normal_check_mode_routes_around_recovery_policy_before_any_clone(self):
        with tempfile.TemporaryDirectory(prefix='normal-image-routing-') as tmp:
            root=Path(tmp)
            route,_,variables=self.inputs(root)
            variables.update(linux_vm_deployment_name=route['vm_name'],linux_vm_vcpus=2,
                linux_vm_memory_mb=4096,linux_vm_disk_gb=20,
                linux_vm_deployment_disk=str(root/'never-created.qcow2'))
            preflight=deepcopy(yaml.safe_load((ROLE/'tasks/upstream-preflight.yml').read_text()))
            for task in preflight:
                if task['name'].startswith('Verify the actual'):
                    task['ansible.builtin.command']['argv']=[sys.executable,'-c',"print('1'*32)"]
                if task['name'].startswith('Read the selected normal upstream network'):
                    task['ansible.builtin.command']['argv']=[sys.executable,'-c',"print('<network><name>normal</name><bridge name=\"fixture0\"/></network>')"]
            preflight_path=root/'upstream-preflight.yml';preflight_path.write_text(yaml.safe_dump(preflight,sort_keys=False))
            forbidden=root/'recovery-forbidden.yml'
            forbidden.write_text('- name: Recovery policy must not run in normal mode\n  ansible.builtin.fail:\n    msg: Forbidden recovery policy call\n')
            tasks=deepcopy(yaml.safe_load((ROLE/'tasks/main.yml').read_text()))
            for task in tasks:
                if task['name'].startswith('Verify a declared recovery hypervisor'):
                    task['ansible.builtin.include_tasks']['file']=str(forbidden)
                if task['name'].startswith('Verify a declared normal upstream'):
                    task['ansible.builtin.include_tasks']['file']=str(preflight_path)
                if task['name']=='Inspect existing VM names':
                    task['ansible.builtin.command']['argv']=[sys.executable,'-c',"print('unrelated-fixture')"]
                if task['name']=='Inspect golden image':
                    task['ansible.builtin.command']['argv']=[sys.executable,'-c',"print('{\"virtual-size\":1073741824}')"]
            result=self.run_play(root,tasks,variables,check=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertIn('Require the exact normal upstream network bridge',result.stdout)
            self.assertNotIn('TASK [Recovery policy must not',result.stdout)
            self.assertNotIn('TASK [Clone the golden image',result.stdout)
            self.assertFalse(Path(variables['linux_vm_deployment_disk']).exists())

    def test_existing_no_overwrite_guard_refuses_either_domain_or_disk_conflict(self):
        guard=next(t for t in yaml.safe_load((ROLE/'tasks/main.yml').read_text()) if t['name']=='Refuse to overwrite an existing VM or disk')
        for domain,disk in [(False,False),(True,False),(False,True)]:
            with self.subTest(domain=domain,disk=disk),tempfile.TemporaryDirectory(prefix='normal-image-conflict-') as tmp:
                root=Path(tmp)
                _,_,variables=self.inputs(root)
                variables.update(linux_vm_deployment_name='fixture-v07',__linux_vm_existing_vms={'stdout_lines':['fixture-v07'] if domain else []},__linux_vm_existing_disk={'stat':{'exists':disk}})
                marker=root/'clone-boundary'
                tasks=[guard,{'name':'Disposable clone boundary','ansible.builtin.file':{'path':str(marker),'state':'touch'}}]
                result=self.run_play(root,tasks,variables)
                self.assertEqual(result.returncode==0,not(domain or disk),result.stdout+result.stderr)
                self.assertEqual(marker.exists(),not(domain or disk))

    def test_protected_loader_preserves_credentials_and_has_no_sibling_fallback(self):
        for mode in ('explicit', 'environment', 'missing', 'route_updates', 'credential_override', 'recovery', 'priority_override'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix='shared-vm-config-') as tmp:
                root=Path(tmp)
                route,provision,variables=self.inputs(root)
                environment={'provisioning':provision, 'unrelated_application_secret':'do-not-bind-global-canary'}
                secret=VaultSecret(b'synthetic-key')
                ciphertext=root/'environment_vault.yml'
                ciphertext.write_bytes(VaultLib([('default',secret)]).encrypt(yaml.safe_dump(environment)))
                key=root/'key';key.write_text('synthetic-key');key.chmod(0o600)
                variables={'vm_name':route['vm_name']}
                env=dict(os.environ,ANSIBLE_NOCOLOR='1',ANSIBLE_HOME=str(root/'home'),ANSIBLE_LOCAL_TEMP=str(root/'local'),
                    ANSIBLE_REMOTE_TEMP=str(root/'remote'),ANSIBLE_ROLES_PATH=str(ROOT/'playbooks/roles'),
                    ANSIBLE_FILTER_PLUGINS=str(ROOT/'playbooks/filter_plugins'))
                env.pop('AC_AGENTS_ENVIRONMENT_VAULT_FILE',None)
                if mode=='environment':
                    env['AC_AGENTS_ENVIRONMENT_VAULT_FILE']=str(ciphertext)
                elif mode!='missing':
                    variables['generic_linux_vm_config_file']=str(ciphertext)
                if mode=='route_updates':
                    route['update_packages']=True
                    variables['linux_vm_upstream']=route
                if mode=='credential_override':
                    route['guest_ssh_password']='forbidden-override-canary'
                    variables['linux_vm_upstream']=route
                if mode=='recovery':
                    variables['linux_vm_recovery']={}
                if mode=='priority_override':
                    variables['provisioning']=dict(provision,guest_ssh_password='forbidden-override-canary')
                expected_success=mode in ('explicit','environment','route_updates')
                tasks=[{'name':'Run the actual canonical protected loader',
                    'ansible.builtin.import_tasks':str(ROOT/'playbooks/tasks/load_generic_linux_vm_config.yml')},
                    {'name':'Prove only provisioning is bound with the original bootstrap',
                    'no_log':True,'ansible.builtin.assert':{'that':[
                    "provisioning.guest_ssh_password == 'synthetic-bootstrap-canary'",
                    'unrelated_application_secret is not defined',
                    'provisioning.update_packages is boolean',
                    'provisioning.update_packages' if mode=='route_updates' else 'not provisioning.update_packages']}}]
                play=root/'load.yml';play.write_text(yaml.safe_dump([{'name':'Actual protected binding fixture','hosts':'localhost',
                    'connection':'local','gather_facts':False,'tasks':tasks}],sort_keys=False))
                inputs=root/'inputs.json';inputs.write_text(json.dumps(variables))
                result=subprocess.run([sys.executable,'-m','ansible.cli.playbook','-i','localhost,',str(play),
                    '-e','@'+str(inputs),'--vault-password-file',str(key)],env=env,cwd=ROOT,capture_output=True,text=True,timeout=90)
                self.assertEqual(result.returncode==0,expected_success,result.stdout+result.stderr)
                for secret_value in ('synthetic-bootstrap-canary','forbidden-override-canary','do-not-bind-global-canary'):
                    self.assertNotIn(secret_value,result.stdout+result.stderr)

    def test_canonical_update_selection_defaults_on_and_sniper_explicitly_off(self):
        entry=yaml.safe_load((ROOT/'playbooks/deploy_generic_linux_vm.yml').read_text())
        condition=next(role['when'] for play in entry for role in play.get('roles',[]) if isinstance(role,dict) and role['role']=='linux_updates')
        for policy,expected in ((None,True),(True,True),(False,False)):
            with self.subTest(policy=policy),tempfile.TemporaryDirectory(prefix='shared-vm-updates-') as tmp:
                root=Path(tmp);marker=root/'updates-selected'
                tasks=[{'name':'Actual canonical update selection','when':condition,
                    'ansible.builtin.copy':{'dest':str(marker),'content':'selected','mode':'0600'}}]
                provision={} if policy is None else {'update_packages':policy}
                result=self.run_play(root,tasks,{'provisioning':provision})
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertEqual(marker.exists(),expected)

    def test_upstream_bootstrap_stays_offline_and_cloud_init_never_updates(self):
        with tempfile.TemporaryDirectory(prefix='shared-vm-bootstrap-') as tmp:
            root=Path(tmp);_,_,variables=self.inputs(root)
            variables.pop('linux_vm_upstream')
            proof=root/'proof.json';stub=root/'customize.py'
            stub.write_text("import json,pathlib,sys,yaml\na=sys.argv[1:]\n"
                "assert '--no-network' in a\n"
                "assert a[a.index('--hostname')+1]=='aap27.v03.example.invalid'\n"
                "assert 'synthetic-bootstrap-canary' not in ' '.join(a)\n"
                "password=pathlib.Path(a[a.index('--password')+1].split(':',2)[2])\n"
                "assert password.read_text().strip()=='synthetic-bootstrap-canary'\n"
                "assert password.stat().st_mode & 511 == 384\n"
                "cfg=next(x.split(':',1)[0] for x in a if x.endswith(':/etc/cloud/cloud.cfg.d/99-automation-bootstrap.cfg'))\n"
                "data=yaml.safe_load(pathlib.Path(cfg).read_text())\n"
                "assert data['package_update'] is False and data['package_upgrade'] is False\n"
                "assert data['datasource_list']==['None']\n"
                "pathlib.Path("+repr(str(proof))+").write_text(json.dumps({'workspace':str(password.parent)}))\n")
            tasks=deepcopy(yaml.safe_load((ROLE/'tasks/generic-bootstrap.yml').read_text()))
            for task in tasks[1]['block']:
                if task['name'].startswith('Customize the new generic clone'):
                    task['ansible.builtin.command']['argv']=[sys.executable,str(stub)]+task['ansible.builtin.command']['argv'][1:]
            variables.update(linux_vm_deployment_name='fixture-v07',linux_vm_hostname='aap27.v03.example.invalid',linux_vm_deployment_disk=str(root/'clone.qcow2'))
            result=self.run_play(root,tasks,variables)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertFalse(Path(json.loads(proof.read_text())['workspace']).exists())
            self.assertNotIn('synthetic-bootstrap-canary',result.stdout+result.stderr)

    def test_generic_preflight_allows_controlled_updates_without_weakening_pins(self):
        for upstream in (True,False):
            with self.subTest(upstream=upstream), tempfile.TemporaryDirectory(prefix='shared-vm-updated-') as tmp:
                root=Path(tmp);_,provision,variables=self.inputs(root)
                variables.pop('linux_vm_upstream')
                provision['generic_image']=upstream
                provision['update_packages']=upstream
                if not upstream:
                    provision['guest_become_password']='synthetic-separate-sudo-canary'
                variables['__linux_vm_environment']['provisioning']=deepcopy(provision)
                tasks=deepcopy(yaml.safe_load((ROLE/'tasks/upstream-preflight.yml').read_text()))
                for task in tasks:
                    if task['name'].startswith('Verify the actual'):
                        task['ansible.builtin.command']['argv']=[sys.executable,'-c',"print('1'*32)"]
                    if task['name'].startswith('Read the selected normal upstream network'):
                        xml='<network><name>normal</name><bridge name="fixture0"/></network>'
                        task['ansible.builtin.command']['argv']=[sys.executable,'-c','print('+repr(xml)+')']
                result=self.run_play(root,tasks,variables)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertNotIn('synthetic-separate-sudo-canary',result.stdout+result.stderr)

    def test_prepared_image_preserves_installer_login_and_application_content(self):
        with tempfile.TemporaryDirectory(prefix='shared-vm-prepared-') as tmp:
            root=Path(tmp);_,_,variables=self.inputs(root)
            variables.pop('linux_vm_upstream')
            variables['provisioning']['generic_image']=False
            variables['__linux_vm_environment']['provisioning']['generic_image']=False
            installer=root/'installer-bundle';installer.write_text('keep-installer-canary')
            access=root/'existing-access';access.write_text('keep-existing-access-canary')
            proof=root/'proof.json';stub=root/'prepared-customize.py'
            stub.write_text("import json,pathlib,sys,yaml\na=sys.argv[1:]\n"
                "assert '--no-network' in a and '--password' not in a\n"
                "assert a[a.index('--hostname')+1]=='aap27.v03.example.invalid'\n"
                "assert 'synthetic-bootstrap-canary' not in ' '.join(a)\n"
                "identity=a[a.index('--run-command')+1]\n"
                "assert '/etc/machine-id' in identity and '/etc/ssh/ssh_host_' in identity\n"
                "assert all(x not in identity for x in ['useradd','userdel','/opt/sources','dnf ','subscription-manager'])\n"
                "uploads=[a[i+1] for i,x in enumerate(a) if x=='--upload']\n"
                "assert len([x for x in uploads if 'ssh_host_' in x])==6\n"
                "cfg=next(x.split(':',1)[0] for x in uploads if x.endswith(':/etc/cloud/cloud.cfg.d/99-automation-bootstrap.cfg'))\n"
                "data=yaml.safe_load(pathlib.Path(cfg).read_text())\n"
                "assert data['ssh_deletekeys'] is False and data['preserve_hostname'] is True\n"
                "assert data['package_update'] is False and data['package_upgrade'] is False\n"
                "assert 'ssh_pwauth' not in data and 'disable_root' not in data\n"
                "assert pathlib.Path("+repr(str(installer))+").read_text()=='keep-installer-canary'\n"
                "assert pathlib.Path("+repr(str(access))+").read_text()=='keep-existing-access-canary'\n"
                "pathlib.Path("+repr(str(proof))+").write_text(json.dumps({'workspace':str(pathlib.Path(cfg).parent)}))\n")
            tasks=deepcopy(yaml.safe_load((ROLE/'tasks/prepared-bootstrap.yml').read_text()))
            for task in tasks[1]['block']:
                if task['name'].startswith('Reset only the prepared clone identity'):
                    task['ansible.builtin.command']['argv']=[sys.executable,str(stub)]+task['ansible.builtin.command']['argv'][1:]
            variables.update(linux_vm_deployment_name='fixture-v07',linux_vm_hostname='aap27.v03.example.invalid',linux_vm_deployment_disk=str(root/'clone.qcow2'))
            result=self.run_play(root,tasks,variables)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertFalse(Path(json.loads(proof.read_text())['workspace']).exists())
            self.assertEqual(installer.read_text(),'keep-installer-canary')
            self.assertEqual(access.read_text(),'keep-existing-access-canary')
            self.assertNotIn('synthetic-bootstrap-canary',result.stdout+result.stderr)

    def test_shared_deployment_does_not_call_aap_api_or_recovery_workflow(self):
        forbidden={'ansible.builtin.uri','ansible.builtin.get_url','ansible.builtin.git'}
        seen=set()
        def visit(value):
            if isinstance(value,dict):
                seen.update(key for key in value if key.startswith('ansible.builtin.'))
                for item in value.values(): visit(item)
            elif isinstance(value,list):
                for item in value: visit(item)
        for file in (ROOT/'playbooks').rglob('*.yml'):
            visit(yaml.safe_load(file.read_text()))
        self.assertFalse(seen & forbidden)
        self.assertFalse((ROLE/'tasks/recovery-preflight.yml').exists())
        self.assertFalse((ROOT/'playbooks/roles/linux_recovery_release').exists())
        self.assertFalse((ROLE/'templates/clean_linux_clone.sh.j2').exists())


    def run_entrypoint_probe(self, root, *, create=False, hostname=None, invalid_route=False, missing_config=False, tags=None, skip_tags=None):
        route,provision,_=self.inputs(root)
        existing_disk=root/'vms'/('fixture-v07.disk.qcow2')
        existing_disk.parent.mkdir()
        existing_disk.write_bytes(b'existing-owned-disk-must-not-be-imported')
        marker=root/'ssh-transport-used'
        trap=root/'ssh-trap.py'
        trap.write_text('#!'+sys.executable+'\nimport pathlib,sys\npathlib.Path('+repr(str(marker))+").write_text('unexpected-remote-call')\nsys.exit(91)\n")
        trap.chmod(0o700)
        host={'ansible_host':pin()['address'],'ansible_connection':'ssh','ansible_user':'fixture',
              'ansible_ssh_executable':str(trap)}
        inventory=root/'inventory.yml'
        inventory.write_text(yaml.safe_dump({'all':{'children':{
            'hypervisor':{'hosts':{'fixture-hypervisor':host}},
            'provisioned_linux_guest':{'hosts':{'fixture-guest':dict(host,ansible_host='192.0.2.11')}}}}}))
        if invalid_route:
            provision['hypervisor_pin']=dict(pin(),address='192.0.2.99')
        vault_file=root/'environment_vault.yml'
        secret=VaultSecret(b'synthetic-key')
        vault_file.write_bytes(VaultLib([('default',secret)]).encrypt(yaml.safe_dump({'provisioning':provision})))
        key=root/'key';key.write_text('synthetic-key');key.chmod(0o600)
        variables={'vm_name':route['vm_name'],'generic_linux_vm_config_file':str(vault_file)}
        if create is not None: variables['generic_linux_vm_create']=create
        if hostname is not None: variables['vm_hostname']=hostname
        if missing_config:variables['generic_linux_vm_config_file']=str(root/'missing.vault')
        inputs=root/'inputs.json';inputs.write_text(json.dumps(variables))
        env=dict(os.environ,ANSIBLE_NOCOLOR='1',ANSIBLE_HOME=str(root/'home'),ANSIBLE_LOCAL_TEMP=str(root/'local'),
            ANSIBLE_REMOTE_TEMP=str(root/'remote'))
        env.pop('AC_AGENTS_ENVIRONMENT_VAULT_FILE',None)
        command=[sys.executable,'-m','ansible.cli.playbook','-i',str(inventory),
            str(ROOT/'playbooks/deploy_generic_linux_vm.yml'),'-e','@'+str(inputs),
            '--vault-password-file',str(key),'-v']
        if tags is not None: command.extend(['--tags',tags])
        if skip_tags is not None: command.extend(['--skip-tags',skip_tags])
        result=subprocess.run(command,env=env,cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertNotIn('synthetic-bootstrap-canary',result.stdout+result.stderr)
        self.assertEqual(Path(route['golden_image_path']).read_bytes(),b'unchanged synthetic image baseline')
        self.assertEqual(existing_disk.read_bytes(),b'existing-owned-disk-must-not-be-imported')
        return result,marker

    def test_explicit_no_creation_calls_neither_host_and_never_claims_verification(self):
        with tempfile.TemporaryDirectory(prefix='shared-vm-skip-') as tmp:
            result,marker=self.run_entrypoint_probe(Path(tmp),create=False,hostname='aap27.v03.example.invalid')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertFalse(marker.exists(),'No-creation must not invoke either managed-host SSH transport')
            self.assertIn('"generic_linux_vm_creation":',result.stdout)
            self.assertIn('"skipped": true',result.stdout)
            self.assertIn('"created": false',result.stdout)
            self.assertNotIn('"generic_linux_vm":',result.stdout)
            self.assertNotIn('"verified": true',result.stdout)
            self.assertNotIn('TASK [linux_vm :',result.stdout)
            self.assertNotIn('TASK [linux_guest :',result.stdout)

    def test_no_creation_still_rejects_invalid_boolean_hostname_and_protected_routing(self):
        for kwargs in ({'create':'false'},{'hostname':'invalid host'},{'invalid_route':True},{'missing_config':True}):
            with self.subTest(kwargs=kwargs),tempfile.TemporaryDirectory(prefix='shared-vm-invalid-skip-') as tmp:
                result,marker=self.run_entrypoint_probe(Path(tmp),**kwargs)
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertFalse(marker.exists())
                self.assertNotIn('"generic_linux_vm_creation":',result.stdout)
                self.assertNotIn('"verified": true',result.stdout)

    def test_creation_defaults_to_fresh_creator_rather_than_implicit_skip(self):
        with tempfile.TemporaryDirectory(prefix='shared-vm-default-create-') as tmp:
            result,marker=self.run_entrypoint_probe(Path(tmp),create=None)
            self.assertNotEqual(result.returncode,0)
            self.assertTrue(marker.exists(),'Default creation must reach the guarded managed-host preflight')
            self.assertNotIn('"generic_linux_vm_creation":',result.stdout)
            self.assertNotIn('"verified": true',result.stdout)

    def test_hostname_override_is_independent_of_domain_name_and_checked_exactly(self):
        verify=next(t for t in yaml.safe_load((ROOT/'playbooks/roles/linux_guest/tasks/main.yml').read_text())
                    if t['name']=='Verify Linux, hostname, and requested resources')
        expected='aap27.v03.example.invalid'
        import base64
        for static,short,success in ((expected,'aap27',True),('aap27.wrong.example.invalid','aap27',False),
                                     (expected,'fixture-v07',False)):
            with self.subTest(static=static,short=short),tempfile.TemporaryDirectory(prefix='shared-vm-hostname-') as tmp:
                root=Path(tmp)
                variables={'deployment_vm_name':'fixture-v07','deployment_vm_hostname':expected,
                    'deployment_vm_vcpus':2,'deployment_vm_memory_mb':4096,'linux_guest_crash_memory_mb':0,
                    'ansible_facts':{'system':'Linux','hostname':short,'processor_vcpus':2,'memtotal_mb':4000},
                    '__linux_guest_configured_hostname':{'content':base64.b64encode((static+'\n').encode()).decode()}}
                result=self.run_play(root,[verify],variables)
                self.assertEqual(result.returncode==0,success,result.stdout+result.stderr)


    def test_partial_tags_cannot_import_an_existing_disk_or_reach_either_host(self):
        for selection in ({'tags':'guest_config'},{'tags':'provision'},{'tags':'all,guest_config'},
                          {'skip_tags':'guest_config'},{'skip_tags':'provision'}):
            with self.subTest(selection=selection),tempfile.TemporaryDirectory(prefix='shared-vm-partial-tags-') as tmp:
                result,marker=self.run_entrypoint_probe(Path(tmp),create=True,**selection)
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('Run the whole shared deployment',result.stdout)
                self.assertFalse(marker.exists(),'Partial tags must be rejected before all managed-host actions')
                self.assertNotIn('TASK [linux_vm :',result.stdout)
                self.assertNotIn('TASK [linux_guest :',result.stdout)
                self.assertNotIn('"verified": true',result.stdout)

    def test_skipping_always_cannot_skip_the_guard_then_execute_managed_actions(self):
        with tempfile.TemporaryDirectory(prefix='shared-vm-skip-always-') as tmp:
            result,marker=self.run_entrypoint_probe(Path(tmp),create=True,skip_tags='always')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertFalse(marker.exists())
            self.assertNotIn('"generic_linux_vm":',result.stdout)
            self.assertNotIn('"generic_linux_vm_creation":',result.stdout)
            self.assertNotIn('"verified": true',result.stdout)


    def test_prepared_optional_become_preserves_omission_and_upstream_still_requires_it(self):
        input_tasks=yaml.safe_load((ROOT/'playbooks/tasks/linux_vm_upstream_inputs.yml').read_text())
        guard=yaml.safe_load((ROLE/'tasks/upstream-preflight.yml').read_text())[0]
        for mode in ('prepared_missing','prepared_explicit','upstream_missing'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory(prefix='shared-vm-optional-become-') as tmp:
                root=Path(tmp);route,provision,variables=self.inputs(root)
                upstream=mode=='upstream_missing'
                route['generic_image']=provision['generic_image']=upstream
                provision.pop('guest_become_password')
                if mode=='prepared_explicit':
                    provision['guest_become_password']='synthetic-prepared-sudo-canary'
                variables['__linux_vm_environment']['provisioning']=deepcopy(provision)
                marker=root/'validated'
                assertion="'guest_become_password' not in provisioning" if mode!='prepared_explicit' else (
                    "provisioning.guest_become_password == 'synthetic-prepared-sudo-canary'")
                tasks=deepcopy(input_tasks)+[deepcopy(guard),
                    {'name':'Prove protected optional escalation was not guessed','no_log':True,
                     'ansible.builtin.assert':{'that':[assertion]}},
                    {'name':'Disposable protected-input boundary',
                     'ansible.builtin.copy':{'dest':str(marker),'content':'passed','mode':'0600'}}]
                result=self.run_play(root,tasks,variables)
                self.assertEqual(result.returncode==0,not upstream,result.stdout+result.stderr)
                self.assertEqual(marker.exists(),not upstream)
                self.assertNotIn('synthetic-prepared-sudo-canary',result.stdout+result.stderr)
                self.assertNotIn('synthetic-bootstrap-canary',result.stdout+result.stderr)

    def test_prepared_add_host_omits_absent_become_and_preserves_existing_inventory_or_explicit_value(self):
        original=next(t for t in yaml.safe_load((ROLE/'tasks/main.yml').read_text())
                      if t['name']=='Add the new guest for connection verification')
        for mode in ('missing_new_host','missing_existing_inventory','explicit_separate'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory(prefix='shared-vm-become-binding-') as tmp:
                root=Path(tmp);route,provision,variables=self.inputs(root)
                provision['generic_image']=False
                provision.pop('guest_become_password')
                if mode=='explicit_separate':
                    provision['guest_become_password']='synthetic-explicit-sudo-canary'
                variables.update(linux_vm_disk_gb=20,linux_vm_vcpus=2,linux_vm_memory_mb=4096,
                    linux_vm_deployment_disk=str(root/'clone.qcow2'),__linux_vm_deployment_ip='192.0.2.11',
                    __linux_vm_domain_uuid={'stdout':'fixture-domain-uuid'},__linux_vm_deployment_bridge='fixture0',
                    __linux_vm_deployment_mac='52:54:00:00:00:11',
                    __linux_vm_public_host_keys=['ssh-ed25519 AAAA'],
                    __linux_vm_source_image={'stat':{'checksum':route['source_image_sha256']}})
                tasks=[]
                if mode!='missing_new_host':
                    tasks.append({'name':'Seed existing native inventory escalation','no_log':True,
                        'ansible.builtin.add_host':{'name':route['vm_name'],
                            'ansible_become_password':'synthetic-native-inventory-sudo-canary'}})
                bind=deepcopy(original);bind.update(no_log=True,register='__fixture_bound_guest')
                tasks.append(bind)
                if mode=='explicit_separate':
                    checks=[
                        "__fixture_bound_guest.add_host.host_vars.ansible_become_password == 'synthetic-explicit-sudo-canary'",
                        "hostvars['fixture-v07'].ansible_become_password == 'synthetic-explicit-sudo-canary'"]
                else:
                    checks=["'ansible_become_password' not in __fixture_bound_guest.add_host.host_vars"]
                    checks.append("'ansible_become_password' not in hostvars['fixture-v07']" if mode=='missing_new_host' else
                        "hostvars['fixture-v07'].ansible_become_password == 'synthetic-native-inventory-sudo-canary'")
                tasks.append({'name':'Prove actual add-host escalation binding is preserved','no_log':True,
                              'ansible.builtin.assert':{'that':checks}})
                result=self.run_play(root,tasks,variables)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                for canary in ('synthetic-explicit-sudo-canary','synthetic-native-inventory-sudo-canary',
                               'synthetic-bootstrap-canary'):
                    self.assertNotIn(canary,result.stdout+result.stderr)

if __name__=='__main__':
    unittest.main()
