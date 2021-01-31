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
        all_vars['parent_folder'] = 'Competition'
        all_vars['WAN_start_address'] = '192.168.253.2'
        all_vars['pfsense_dns'] = all_vars['prefered_DNS']
        all_vars['Upstream_gateway_start_address'] = '192.168.253.1'
        all_vars['start_team'] = 1
        all_vars['total_teams'] = 5
        all_vars['Lockdown_user_role'] = 'Lockdown'
        all_vars['afinity_enable'] = True
        all_vars['pfsense_template'] = 'Router-v8'
        all_vars['cloud_folder'] = '{}_Cloud'.format(all_vars['parent_folder'])
        all_vars['domain'] = 'reallife.lockdown'
        all_vars['netbios'] = 'VIRUS'
        all_vars['WAN_Subnet'] = 29
        all_vars['IP_jump'] = 8
        all['vars'] = all_vars
        #####################################################################################################

        #####################################################################################################
        Active_Directory = ['10.X.1.60'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Windows_10 = ['10.X.1.70'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Windows_Core = ['10.X.1.50'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Rouge_Windows = ['10.X.1.10'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        CentOS = ['10.X.1.30'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Ubuntu = ['10.X.1.40'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        FTP = ['10.X.2.4'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        WEB = ['10.X.2.2'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        DB = ['10.X.2.3'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        IOT = ['10.X.2.10'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        GitLab = ['10.X.2.5'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Traveler = ["192.168.253.{}".format(str((i-1)*all_vars['IP_jump']+3)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        PaloAlto = ['13.33.33.X'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]

        cloud = WEB + DB + FTP + IOT + GitLab + PaloAlto
        for host_list in [
                Active_Directory, Rouge_Windows, CentOS,
                Ubuntu, Windows_10, Windows_Core,
                WEB, DB, FTP, IOT, GitLab, Traveler, PaloAlto
        ]:
            for idx, host in enumerate(host_list):
                team_number = idx + all_vars['start_team']
                hostvars[host] = {}
                hostvars[host]['customization'] = {}
                hostvars[host]['timeout'] = 300
                network = {}

                if host in Active_Directory:
                    hostvars[host]['domain_name'] = all_vars['domain']
                    hostvars[host]['netbios_name'] = all_vars['netbios']
                    hostvars[host]['ad_backuppass'] = 'Change.me!'
                    hostvars[host]['template'] = "Server-Windows-2019-v8"
                    hostvars[host]['AD_Name'] = 'AD'

                if host in Rouge_Windows:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-Rouge-18.04-v8'
                    hostvars[host]['AD_Name'] = 'Rouge_Windows'

                if host in CentOS:
                    hostvars[host]['template'] = 'Desktop-Centos-07-v8'
                    hostvars[host]['AD_Name'] = 'CentOS'

                if host in Ubuntu:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'Ubuntu'

                if host in Traveler:
                    hostvars[host]['template'] = 'AWX-Desktop-LUbuntu-16.04'
                    hostvars[host]['AD_Name'] = 'Traveler'

                if host in PaloAlto:
                    hostvars[host]['template'] = 'AWX-Palo-Alto'
                    hostvars[host]['AD_Name'] = 'PaloAlto'
                    hostvars[host]['skip_deployment_check'] = 'True'

                if host in Windows_10:
                    hostvars[host]['template'] = 'Desktop-Windows-10-v8'
                    hostvars[host]['AD_Name'] = 'Windows10'

                if host in Windows_Core:
                    hostvars[host]['template'] = 'Server-Windows-Core-2019-v8'
                    hostvars[host]['AD_Name'] = 'WindowsCore'

                if host in FTP:
                    hostvars[host]['template'] = 'Windows-Server-FTP-v8'
                    hostvars[host]['AD_Name'] = 'FTP'

                if host in IOT:
                    hostvars[host]['template'] = 'Server-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'IoT'

                if host in GitLab:
                    hostvars[host]['template'] = 'Git-Server-Centos-7-v8'
                    hostvars[host]['AD_Name'] = 'GitLab'
                    hostvars[host][
                        'gitlab_external_url'] = "http://gitlab.{}".format(all_vars['domain'])

                if host in WEB:
                    hostvars[host]['template'] = 'Server-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'WEB'
                    hostvars[host]['magento_host'] = "http://10.{}.2.2/".format(team_number)
                    hostvars[host]['magento_db_host'] = "10.{}.2.3".format(team_number)
                    hostvars[host]['apache_mods_enabled'] = ['rewrite.load']

                if host in DB:
                    hostvars[host]['template'] = 'Server-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'DATABASE'
                    hostvars[host]['mysql_users'] = []
                    hostvars[host]['mysql_users'].append({
                        'name': 'magento',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'admin',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_databases'] = []
                    hostvars[host]['mysql_databases'].append({
                        'name': 'magento',
                        'collation': 'utf8_general_ci',
                        'encoding': 'utf8',
                        'replicate': 0
                    })

                if host in Active_Directory + FTP + Windows_Core:
                    hostvars[host]['ansible_user'] = 'Administrator'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['customization']['password'] = hostvars[host]['ansible_password']
                    hostvars[host]['timeout'] = 600

                if host in Windows_10:
                    hostvars[host]['ansible_user'] = 'Admin'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['timeout'] = 600

                if host in Rouge_Windows + CentOS + Ubuntu + WEB + DB + IOT + GitLab + Traveler:
                    hostvars[host]['ansible_user'] = 'sysadmin'
                    hostvars[host]['ansible_password'] = 'changeme'
                    hostvars[host]['ansible_become_pass'] = hostvars[host]['ansible_password']
                    hostvars[host]['OS'] = 'Linux'

                if host in FTP + Windows_10 + Windows_Core:
                    hostvars[host]['dns_domain_name'] = hostvars[
                        Active_Directory[idx]]['domain_name']
                    hostvars[host]['domain_admin_password'] = hostvars[
                        Active_Directory[idx]]['ansible_password']
                    hostvars[host]['domain_admin_user'] = hostvars[
                        Active_Directory[idx]]['ansible_user']

                if host in Active_Directory + FTP + Windows_10 + Windows_Core:
                    hostvars[host]['ansible_connection'] = 'winrm'
                    hostvars[host]['ansible_winrm_server_cert_validation'] = 'ignore'
                    hostvars[host]['OS'] = 'Windows'

                if host not in Active_Directory:
                    hostvars[host]['customization']['dns_servers'] = [Active_Directory[idx], all_vars['prefered_DNS']]
                    network['dns_servers'] = [Active_Directory[idx], all_vars['prefered_DNS']]
                else:
                    hostvars[host]['customization']['dns_servers'] = [all_vars['prefered_DNS']]
                    network['dns_servers'] = [all_vars['prefered_DNS']]

                if host in cloud:
                    hostvars[host]['folder'] = 'Lockdown/{}/{}'.format(
                        all_vars['parent_folder'], all_vars['cloud_folder'])
                else:
                    hostvars[host]['folder'] = 'Lockdown/{}/Team{:02d}'.format(
                        all_vars['parent_folder'], team_number)


                def networking (ip):
                    network['name'] = "team{}-net".format(team_number)
                    network['ip'] = ip
                    network['netmask'] = '255.255.255.0'
                    network['gateway'] = "10.{}.{}.1".format(team_number, host.split('.')[2])
                    network['start_connected'] = True
                    return network
                hostvars[host]['networks'] = [networking(host)]
                hostvars[host]['team_number'] = team_number
                hostvars[host]['customization']['hostname'] = hostvars[host]['AD_Name']

                if host in Traveler:
                    hostvars[host]['networks'][0]['netmask'] = '255.255.255.248'
                    hostvars[host]['networks'][0]['gateway'] = "192.168.253.{}".format(str((team_number-1)*all_vars['IP_jump']+1))

                if host in PaloAlto:
                    hostvars[host]['networks'] = []
                    for net_instance in ['13.33.33.37', '13.33.33.37', '13.33.33.37', '13.33.33.37']:
                        hostvars[host]['networks'].append(networking(net_instance))


        AD = {}
        AD['hosts'] = Active_Directory
        Linux_A = {}
        Linux_A['hosts'] = Rouge_Windows
        Linux_B = {}
        Linux_B['hosts'] = CentOS
        Linux_C = {}
        Linux_C['hosts'] = Ubuntu
        Windows_A = {}
        Windows_A['hosts'] = Windows_10
        Windows_B = {}
        Windows_B['hosts'] = Windows_Core
        WEB_Servers = {}
        WEB_Servers['hosts'] = WEB
        DB_Servers = {}
        DB_Servers['hosts'] = DB
        FTP_Servers = {}
        FTP_Servers['hosts'] = FTP
        IoT = {}
        IoT['hosts'] = IOT
        GIT_Servers = {}
        GIT_Servers['hosts'] = GitLab
        Traveler_box = {}
        Traveler_box['hosts'] = Traveler
        PaloAlto_box = {}
        PaloAlto_box['hosts'] = PaloAlto

        #TODO: Potentially include palo Alto
        ################################################################################################
        inventory['all'] = all
        inventory['AD'] = AD
        inventory['Rouge_Windows'] = Linux_A
        #inventory['CentOS'] = Linux_B
        inventory['Ubuntu'] = Linux_C
        inventory['Windows_10'] = Windows_A
        #inventory['Windows_Core'] = Windows_B
        inventory['WEB'] = WEB_Servers
        inventory['DB'] = DB_Servers
        #inventory['GIT'] = GIT_Servers
        inventory['FTP'] = FTP_Servers
        inventory['IOT'] = IoT
        #inventory['Traveler'] = Traveler_box
        #inventory['PaloAlto'] = PaloAlto_box

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
