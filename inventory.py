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
        all_vars['datastore'] = 'cdr-backup'
        all_vars['datacenter'] = 'UBNetDef'
        all_vars['cluster'] = 'MAIN'
        all_vars['parent_folder'] = 'Competition'
        all_vars['WAN_start_address'] = '192.168.253.2'
        all_vars['pfsense_dns'] = all_vars['prefered_DNS']
        all_vars['Upstream_gateway_start_address'] = '192.168.253.1'
        all_vars['start_team'] = 14
        #todo Change number of teams
        all_vars['total_teams'] = 1
        all_vars['Lockdown_user_role'] = 'Lockdown blue team'
        all_vars['afinity_enable'] = True
        all_vars['pfsense_template'] = 'Router-v18'
        all_vars['cloud_folder'] = '{}_Cloud'.format(all_vars['parent_folder'])
        all_vars['domain'] = 'media.lockdown'
        all_vars['netbios'] = 'MEDIA'
        all_vars['WAN_Subnet'] = 29
        all_vars['IP_jump'] = 8
        all['vars'] = all_vars
        #####################################################################################################

        #####################################################################################################
        
        # LAN
        Ubuntu1 = ['10.X.1.10'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Ubuntu2 = ['10.X.1.40'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Ubuntu3 = ['10.X.1.90'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        CentOS = ['10.X.1.30'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Active_Directory = ['10.X.1.60'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Windows1 = ['10.X.1.70'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        Windows2 = ['10.X.1.80'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]

        # DMZ
        WEB = ['10.X.2.2'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        DB = ['10.X.2.3'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        FTP = ['10.X.2.4'.replace('X', str(i)) for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        DevServer = ['10.X.2.10'.replace('X', str(i))for i in range(
            all_vars['start_team'], all_vars['total_teams'] + all_vars['start_team'])]
        
        cloud = FTP + DB + WEB + DevServer

        for host_list in [
            Ubuntu1, Ubuntu2, Ubuntu3, CentOS, Active_Directory, Windows1, Windows2, WEB, DB, FTP, DevServer
        ]:
            for idx, host in enumerate(host_list):
                team_number = idx + all_vars['start_team']
                hostvars[host] = {}
                hostvars[host]['customization'] = {}
                hostvars[host]['timeout'] = 300
                network = {}

                #FIX THE AD DEPLOYMENT ROLES
                if host in Active_Directory:
                    hostvars[host]['domain_name'] = all_vars['domain']
                    hostvars[host]['netbios_name'] = all_vars['netbios']
                    hostvars[host]['ad_backuppass'] = 'Change.me!'
                    hostvars[host]['template'] = "v18-ADDS-New"
                    #hostvars[host]['template'] = "AD-Sucks"
                    hostvars[host]['AD_Name'] = 'AD'

                #if host in AliExpressWindows: #Formally RogueLinux, but now updated.
                #    #hostvars[host]['template'] = 'Desktop-Ubuntu-Rouge-18.04-v8'
                #    hostvars[host]['template'] = 'Knockoff95-v12'
                #    hostvars[host]['AD_Name'] = 'WeirdWindows'

                if host in Ubuntu1:
                    hostvars[host]['template'] = 'v18-UbuntuX'
                    hostvars[host]['AD_Name'] = 'Ubuntu1'

                if host in Ubuntu2:
                    hostvars[host]['template'] = 'v18-UbuntuX'
                    hostvars[host]['AD_Name'] = 'Ubuntu2'

                if host in Ubuntu3:
                    hostvars[host]['template'] = 'v18-UbuntuX'
                    hostvars[host]['AD_Name'] = 'Ubuntu3'

                #VASU PLEASE UPDATE THE DAMN CENTOS VM
                if host in CentOS:
                    hostvars[host]['template'] = 'v18-WebApp'
                    hostvars[host]['AD_Name'] = 'Winux'

                if host in Windows1:
                    hostvars[host]['template'] = 'V18-WindowsX-New'
                    hostvars[host]['AD_Name'] = 'Windows1'

                if host in Windows2:
                    hostvars[host]['template'] = 'V18-WindowsX-New'
                    hostvars[host]['AD_Name'] = 'Windows2'

                if host in FTP:
                    hostvars[host]['template'] = 'v18-Linux-FTP'
                    hostvars[host]['AD_Name'] = 'FTP'

                if host in DevServer:
                    hostvars[host]['template'] = 'v18-DevServer'
                    hostvars[host]['AD_Name'] = 'DevServer'

                if host in WEB:
                    hostvars[host]['template'] = 'v18-Backup'
                    hostvars[host]['AD_Name'] = 'WEB'
                    hostvars[host]['apache_mods_enabled'] = ['rewrite.load']

                if host in DB:
                    hostvars[host]['template'] = 'v18-UbuntuServer'
                    hostvars[host]['AD_Name'] = 'DATABASE'
                    hostvars[host]['mysql_users'] = []
                    hostvars[host]['mysql_users'].append({
                        'name': 'badmin',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'scam',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'magic',
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

                if host in Active_Directory:
                    hostvars[host]['ansible_user'] = 'Administrator'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['customization']['password'] = hostvars[host]['ansible_password']
                    hostvars[host]['timeout'] = 600

                if host in Windows1 + Windows2:
                    hostvars[host]['ansible_user'] = 'Admin'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['timeout'] = 600

                #DEFINE LINUX VMS HERE
                if host in Ubuntu1 + Ubuntu2 + Ubuntu3 + WEB + DB + DevServer + CentOS + FTP:
                    hostvars[host]['ansible_user'] = 'sysadmin'
                    hostvars[host]['ansible_password'] = 'changeme'
                    hostvars[host]['ansible_become_pass'] = hostvars[host]['ansible_password']
                    hostvars[host]['OS'] = 'Linux'

                if host in Windows1 + Windows2:
                    hostvars[host]['dns_domain_name'] = hostvars[
                        Active_Directory[idx]]['domain_name']
                    hostvars[host]['domain_admin_password'] = hostvars[
                        Active_Directory[idx]]['ansible_password']
                    hostvars[host]['domain_admin_user'] = hostvars[
                        Active_Directory[idx]]['ansible_user']
                
                #DEFINE WINDOWS VMS HERE
                if host in Active_Directory + Windows1 + Windows2:
                    hostvars[host]['ansible_connection'] = 'winrm'
                    hostvars[host]['ansible_winrm_transport'] = 'ntlm'
                    hostvars[host]['ansible_winrm_server_cert_validation'] = 'ignore'
                    hostvars[host]['ansible_port'] = 5985
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
        #AliExpressWindows_dict = {}
        Ubuntu1_dict = {}
        Ubuntu2_dict = {}
        Ubuntu3_dict = {}
        CentOS_dict = {}

        FTP_dict = {}
        WEB_dict = {}
        DB_dict = {}
        DevServer_dict = {}

        Active_Directory_dict["hosts"] = Active_Directory
        Windows1_dict["hosts"] = Windows1
        Windows2_dict["hosts"] = Windows2
        #AliExpressWindows_dict["hosts"] = AliExpressWindows
        Ubuntu1_dict["hosts"] = Ubuntu1
        Ubuntu2_dict["hosts"] = Ubuntu2
        Ubuntu3_dict["hosts"] = Ubuntu3
        CentOS_dict["hosts"] = CentOS

        FTP_dict["hosts"] = FTP
        WEB_dict["hosts"] = WEB
        DB_dict["hosts"] = DB
        DevServer_dict['hosts'] = DevServer
        #TODO: Potentially include palo Alto
        ################################################################################################
        
        #Comment/Uncomment here to include/exclude from deployment. Limit removal from top. Recall "Chesterton's Fence"

        inventory['all'] = all

        #inventory['Active_Directory'] = Active_Directory_dict
        #inventory['Windows1'] = Windows1_dict
        #inventory['Windows2'] = Windows2_dict
        #inventory['Ubuntu1'] = Ubuntu1_dict
        #inventory['Ubuntu2'] = Ubuntu2_dict
        #inventory['Ubuntu3'] = Ubuntu3_dict
        #inventory['WebApp'] = CentOS_dict

        #inventory['UbuntuFTP'] = FTP_dict
        #inventory['BackupServer'] = WEB_dict
        #inventory['DB'] = DB_dict
        inventory['DevServer'] = DevServer_dict

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
