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
        #todo Change number of teams
        all_vars['total_teams'] = 15
        all_vars['Lockdown_user_role'] = 'Lockdown blue team'
        all_vars['afinity_enable'] = True
        all_vars['pfsense_template'] = 'Router-v8'
        all_vars['cloud_folder'] = '{}_Cloud'.format(all_vars['parent_folder'])
        all_vars['domain'] = 'vinny.lockdown'
        all_vars['netbios'] = 'WINGS'
        all_vars['WAN_Subnet'] = 29
        all_vars['IP_jump'] = 8
        all['vars'] = all_vars
        #####################################################################################################

        #####################################################################################################
        
        # LAN
        AliExpressWindows = ['10.X.1.10'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Ubuntu = ['10.X.1.40'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Ubuntu2 = ['10.X.1.50'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        CentOS = ['10.X.1.30'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Active_Directory = ['10.X.1.60'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Windows1 = ['10.X.1.70'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Windows2 = ['10.X.1.80'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]

        # DMZ
        WEB = ['10.X.2.2'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        DB = ['10.X.2.3'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        FTP = ['10.X.2.4'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        API = ['10.X.2.10'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        
        cloud = FTP + DB + WEB + API

        for host_list in [
                AliExpressWindows, Ubuntu, Ubuntu2, CentOS, Active_Directory, Windows1, Windows2, WEB, DB, FTP, API
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

                if host in AliExpressWindows: #Formally RogueLinux, but now updated.
                    #hostvars[host]['template'] = 'Desktop-Ubuntu-Rouge-18.04-v8'
                    hostvars[host]['template'] = 'AliExpressWindows'
                    hostvars[host]['AD_Name'] = 'WeirdWindows'

                if host in Ubuntu:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'Ubuntu1'

                if host in Ubuntu2:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'Ubuntu2'

                #VASU PLEASE UPDATE THE DAMN CENTOS VM
                if host in CentOS:
                    hostvars[host]['template'] = 'Desktop-Centos-07-v8'
                    hostvars[host]['AD_Name'] = 'CentOS'

                if host in Windows1:
                    hostvars[host]['template'] = 'Lockdown-Windows10-v12'
                    hostvars[host]['AD_Name'] = 'Windows1'

                if host in Windows2:
                    hostvars[host]['template'] = 'Lockdown-Windows10-v12'
                    hostvars[host]['AD_Name'] = 'Windows2'

                if host in FTP:
                    hostvars[host]['template'] = 'Windows-Server-FTP-v8'
                    hostvars[host]['AD_Name'] = 'FTP'

                if host in API:
                    hostvars[host]['template'] = 'BlakeWeb-API'
                    hostvars[host]['AD_Name'] = 'API'

                if host in WEB:
                    hostvars[host]['template'] = 'BlakeWeb-Site'
                    hostvars[host]['AD_Name'] = 'WEB'
                    hostvars[host]['apache_mods_enabled'] = ['rewrite.load']

                if host in DB:
                    hostvars[host]['template'] = 'Server-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'DATABASE'
                    hostvars[host]['mysql_users'] = []
                    hostvars[host]['mysql_users'].append({
                        'name': 'badmin',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'wings',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'pizza',
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
                        'name': 'data',
                        'collation': 'utf8_general_ci',
                        'encoding': 'utf8',
                        'replicate': 0
                    })

                if host in Active_Directory + FTP:
                    hostvars[host]['ansible_user'] = 'Administrator'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['customization']['password'] = hostvars[host]['ansible_password']
                    hostvars[host]['timeout'] = 600

                if host in Windows1 + Windows2:
                    hostvars[host]['ansible_user'] = 'Admin'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['timeout'] = 600

                if host in AliExpressWindows + Ubuntu + WEB + DB + API + CentOS:
                    hostvars[host]['ansible_user'] = 'sysadmin'
                    hostvars[host]['ansible_password'] = 'changeme'
                    hostvars[host]['ansible_become_pass'] = hostvars[host]['ansible_password']
                    hostvars[host]['OS'] = 'Linux'

                if host in Windows1 + Windows2 + FTP:
                    hostvars[host]['dns_domain_name'] = hostvars[
                        Active_Directory[idx]]['domain_name']
                    hostvars[host]['domain_admin_password'] = hostvars[
                        Active_Directory[idx]]['ansible_password']
                    hostvars[host]['domain_admin_user'] = hostvars[
                        Active_Directory[idx]]['ansible_user']

                if host in Active_Directory + FTP + Windows1 + Windows2:
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


        Active_Directory_dict = {}
        Windows1_dict = {}
        Windows2_dict = {}
        AliExpressWindows_dict = {}
        Ubuntu_dict = {}
        Ubuntu2_dict = {}
        CentOS_dict = {}

        FTP_dict = {}
        WEB_dict = {}
        DB_dict = {}
        API_dict = {}

        Active_Directory_dict["hosts"] = Active_Directory
        Windows1_dict["hosts"] = Windows1
        Windows2_dict["hosts"] = Windows2
        AliExpressWindows_dict["hosts"] = AliExpressWindows
        Ubuntu_dict["hosts"] = Ubuntu
        Ubuntu2_dict["hosts"] = Ubuntu2
        #CentOS_dict["hosts"] = CentOS

        FTP_dict["hosts"] = FTP
        WEB_dict["hosts"] = WEB
        DB_dict["hosts"] = DB
        API_dict['hosts'] = API
        #TODO: Potentially include palo Alto
        ################################################################################################
        
        #Comment/Uncomment here to include/exclude from deployment. Limit removal from top. Recall "Chesterton's Fence"

        inventory['all'] = all

        inventory['Active_Directory'] = Active_Directory_dict
        inventory['Windows1'] = Windows1_dict
        inventory['Windows2'] = Windows2_dict
        inventory['AliExpressWindows'] = AliExpressWindows_dict
        inventory['Ubuntu'] = Ubuntu_dict
        inventory['Ubuntu2'] = Ubuntu2_dict
        #inventory['CentOs'] = CentOS_dict

        inventory['FTP'] = FTP_dict
        inventory['WEB'] = WEB_dict
        inventory['DB'] = DB_dict
        inventory['WebAPI'] = API_dict

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
