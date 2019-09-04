#!/usr/bin/env python
import argparse
import os
import sys

try:
    import json
except ImportError:
    import simplejson as json


class Inventory(object):
############################################################################
################# DON'T CHANGE THIS ########################################
############################################################################
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        if self.args.list:
            self.inventory = self.inventory_generator()
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        else:
            self.inventory = self.empty_inventory()
        print(json.dumps(self.inventory))
        with open("temp", 'w') as f:
            f.write(json.dumps(self.inventory))


############################################################################
################# DON'T CHANGE THIS ########################################
############################################################################

    def inventory_generator(self):

        inventory = {}
        _meta = {}
        hostvars = {}
        #####################################################################################################
        all = {}
        all_vars = {}
        all_vars['prefered_DNS'] = '8.8.8.8'
        all_vars['vcenter_hostname'] = 'cdr-vcenter.cse.buffalo.edu'
        all_vars['datastore'] = 'THE-VAULT'
        all_vars['datacenter'] = 'UBNetDef'
        all_vars['cluster'] = 'MAIN'
        all_vars['parent_folder'] = 'Internal-v0'
        all_vars['WAN_start_address'] = '192.168.253.2'
        all_vars['pfsense_dns'] = all_vars['prefered_DNS']
        all_vars['Upstream_gateway_start_address'] = '192.168.253.1'
        all_vars['start_team'] = 1
        all_vars['total_teams'] = 2
        all_vars['afinity_enable'] = True
        all_vars['pfsense_template'] = 'Router-Internal-v0'
        all_vars['cloud_folder'] = '{}_Cloud'.format(all_vars['parent_folder'])
        all_vars['domain'] = 'star.wars'
        all_vars['netbios'] = 'STARWARS'
        all['vars'] = all_vars
        #####################################################################################################

        #####################################################################################################
        Active_Directory = ['10.X.1.60'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        Linux_clients_A = ['10.X.1.10'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        Linux_clients_B = ['10.X.1.20'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        Linux_clients_C = ['10.X.1.30'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        Windows_clients_A = ['10.X.1.40'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        Windows_clients_B = ['10.X.1.50'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        WEB = ['10.X.2.2'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        DB = ['10.X.2.3'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        FTP = ['10.X.2.4'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        GitLab = ['10.X.2.5'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams'] + 1)]
        cloud = WEB + DB + FTP + GitLab
        for host_list in [
                Active_Directory, Linux_clients_A, Linux_clients_B,
                Linux_clients_C, Windows_clients_A, Windows_clients_B,
                WEB, DB, FTP, GitLab
        ]:
            for idx, host in enumerate(host_list):
                team_number = idx + all_vars['start_team']
                hostvars[host] = {}
                hostvars[host]['customization'] = {}
                network = {}

                if host in Active_Directory:
                    hostvars[host]['domain_name'] = all_vars['domain']
                    hostvars[host]['netbios_name'] = all_vars['netbios']
                    hostvars[host]['ad_backuppass'] = 'Change.me!'
                    hostvars[host]['template'] = "Windows-Server-AD-Internal-v0"
                    hostvars[host]['AD_Name'] = 'AD'

                if host in Linux_clients_A:
                    hostvars[host]['template'] = 'Desktop-XUbuntu-16.04-Internal-v0'
                    hostvars[host]['AD_Name'] = 'Linux-A'

                if host in Linux_clients_B:
                    hostvars[host]['template'] = 'Desktop-CentOS-7-Internal-v0'
                    hostvars[host]['AD_Name'] = 'Linux-B'

                if host in Linux_clients_C:
                    hostvars[host]['template'] = 'Desktop-LUbuntu-16.04-Internal-v0'
                    hostvars[host]['AD_Name'] = 'Linux-C'

                if host in Windows_clients_A:
                    hostvars[host]['template'] = 'Desktop-Windows-10-Internal-v0'
                    hostvars[host]['AD_Name'] = 'Windows-A'

                if host in Windows_clients_B:
                    hostvars[host]['template'] = 'Desktop-Windows-7-Internal-v0'
                    hostvars[host]['AD_Name'] = 'Windows-B'

                if host in FTP:
                    hostvars[host]['template'] = 'Windows-Server-FTP-Internal-v0'
                    hostvars[host]['AD_Name'] = 'FTP'

                if host in GitLab:
                    hostvars[host]['template'] = 'Server-CentOS-7-GIT-Internal-v0'
                    hostvars[host]['AD_Name'] = 'GitLab'
                    hostvars[host][
                        'gitlab_external_url'] = "http://gitlab.{}".format(all_vars['domain'])

                if host in WEB:
                    hostvars[host]['template'] = 'Server-Ubuntu-16.04-Internal-v0'
                    hostvars[host]['AD_Name'] = 'WEB'
                    hostvars[host]['magento_host'] = "http://10.{}.2.2/".format(team_number)
                    hostvars[host]['magento_db_host'] = "10.{}.2.3".format(team_number)
                    hostvars[host]['apache_mods_enabled'] = ['rewrite.load']

                if host in DB:
                    hostvars[host]['template'] = 'Server-Ubuntu-16.04-Internal-v0'
                    hostvars[host]['AD_Name'] = 'DATABASE'
                    hostvars[host]['mysql_users'] = []
                    hostvars[host]['mysql_users'].append({
                        'name':
                        'magento',
                        'host':
                        '%',
                        'password':
                        'changeme',
                        'priv':
                        '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name':
                        'admin',
                        'host':
                        '%',
                        'password':
                        'changeme',
                        'priv':
                        '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_databases'] = []
                    hostvars[host]['mysql_databases'].append({
                        'name': 'magento',
                        'collation': 'utf8_general_ci',
                        'encoding': 'utf8',
                        'replicate': 0
                    })

                if host in Active_Directory + FTP:
                    hostvars[host]['ansible_user'] = 'Administrator'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['customization']['password'] = hostvars[
                        host]['ansible_password']

                if host in Windows_clients_A + Windows_clients_B:
                    hostvars[host]['ansible_user'] = 'Admin'
                    hostvars[host]['ansible_password'] = 'Change.me!'

                if host in WEB + DB:
                    hostvars[host]['ansible_python_interpreter'] = '/usr/bin/python3'

                if host in Linux_clients_A + Linux_clients_B + Linux_clients_C + GitLab + WEB + DB:
                    hostvars[host]['ansible_user'] = 'sysadmin'
                    hostvars[host]['ansible_password'] = 'changeme'

                if host in Linux_clients_A + Linux_clients_B + Linux_clients_C + GitLab + WEB + DB:
                    hostvars[host]['ansible_become_pass'] = hostvars[host]['ansible_password']
                    hostvars[host]['OS'] = 'Linux'

                if host in FTP + Windows_clients_A + Windows_clients_B:
                    hostvars[host]['dns_domain_name'] = hostvars[
                        Active_Directory[idx]]['domain_name']
                    hostvars[host]['domain_admin_password'] = hostvars[
                        Active_Directory[idx]]['ansible_password']
                    hostvars[host]['domain_admin_user'] = hostvars[
                        Active_Directory[idx]]['ansible_user']

                if host in Active_Directory + FTP + Windows_clients_A + Windows_clients_B:
                    hostvars[host]['ansible_connection'] = 'winrm'
                    hostvars[host]['ansible_winrm_server_cert_validation'] = 'ignore'
                    hostvars[host]['OS'] = 'Windows'

                if host not in Active_Directory:
                    hostvars[host]['customization']['dns_servers'] = [Active_Directory[idx]]
                    network['dns_servers'] = Active_Directory[idx]
                else:
                    hostvars[host]['customization']['dns_servers'] = [all_vars['prefered_DNS']]
                    network['dns_servers'] = all_vars['prefered_DNS']

                if host in cloud:
                    hostvars[host]['folder'] = 'Lockdown/{}/{}'.format(
                        all_vars['parent_folder'], all_vars['cloud_folder'])
                else:
                    hostvars[host]['folder'] = 'Lockdown/{}/Team{:02d}'.format(
                        all_vars['parent_folder'], team_number)

                network['name'] = "team{}-net".format(team_number)
                network['ip'] = host
                network['netmask'] = '255.255.255.0'
                network['gateway'] = "10.{}.{}.1".format(
                    team_number,
                    host.split('.')[2])
                network['start_connected'] = True
                hostvars[host]['networks'] = [network]
                hostvars[host]['team_number'] = team_number
                hostvars[host]['team_number'] = team_number
                # hostvars[host]['customization']['existing_vm'] = True
                hostvars[host]['networks'] = [network]
                hostvars[host]['customization']['hostname'] = hostvars[host]['AD_Name']

        AD = {}
        AD['hosts'] = Active_Directory
        Linux_A = {}
        Linux_A['hosts'] = Linux_clients_A
        Linux_B = {}
        Linux_B['hosts'] = Linux_clients_B
        Linux_C = {}
        Linux_C['hosts'] = Linux_clients_C
        Windows_A = {}
        Windows_A['hosts'] = Windows_clients_A
        Windows_B = {}
        Windows_B['hosts'] = Windows_clients_B
        WEB_Servers = {}
        WEB_Servers['hosts'] = WEB
        DB_Servers = {}
        DB_Servers['hosts'] = DB
        FTP_Servers = {}
        FTP_Servers['hosts'] = FTP
        GIT_Servers = {}
        GIT_Servers['hosts'] = GitLab

        ################################################################################################
        inventory['all'] = all
        inventory['AD'] = AD
        inventory['Linux-A'] = Linux_A
        inventory['Linux-B'] = Linux_B
        inventory['Linux-C'] = Linux_C
        inventory['Windows-A'] = Windows_A
        inventory['Windows-B'] = Windows_B
        inventory['WEB'] = WEB_Servers
        inventory['DB'] = DB_Servers
        inventory['FTP'] = FTP_Servers
        inventory['GIT'] = GIT_Servers

        #################################################################################################

        _meta['hostvars'] = hostvars
        inventory['_meta'] = _meta

        return inventory

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}
    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()

Inventory()
