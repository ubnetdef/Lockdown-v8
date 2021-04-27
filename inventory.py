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
        all_vars['total_teams'] = 13
        all_vars['Lockdown_user_role'] = 'Lockdown blue team'
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
        Nurse_Station_A = ['10.X.1.80'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Nurse_Station_B = ['10.X.1.90'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Doctor_Station = ['10.X.1.70'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Secretary_Station = ['10.X.1.100'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        IT_Station = ['10.X.1.10'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Ubuntu = ['10.X.1.40'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        FTP = ['10.X.2.4'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        WEB = ['10.X.2.2'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        DB = ['10.X.2.3'.replace('X', str(i)) for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]    
        IOT = ['10.X.2.10'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Calendar_System = ['10.X.2.12'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        Patient_Notes = ['10.X.2.14'.replace('X', str(i))for i in range(all_vars['start_team'], all_vars['total_teams']  + all_vars['start_team'])]
        cloud = FTP + WEB + DB + IOT + Calendar_System + Patient_Notes
        for host_list in [
                Active_Directory, Nurse_Station_A, Nurse_Station_B, 
                Doctor_Station, Secretary_Station, 
                IT_Station, Ubuntu, FTP, WEB, DB, IOT, 
                Calendar_System, Patient_Notes
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

                if host in IT_Station:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-Rouge-18.04-v8'
                    hostvars[host]['AD_Name'] = 'IT_Station'

                if host in Ubuntu:
                    hostvars[host]['template'] = 'Desktop-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'Ubuntu'

                if host in Nurse_Station_A:
                    hostvars[host]['template'] = 'Lockdown-v10-Windows-Template'
                    hostvars[host]['AD_Name'] = 'Nurse_A'

                if host in Nurse_Station_B:
                    hostvars[host]['template'] = 'Lockdown-v10-Windows-Template'
                    hostvars[host]['AD_Name'] = 'Nurse_B'

                if host in Doctor_Station:
                    hostvars[host]['template'] = 'Lockdown-v10-Windows-Template'
                    hostvars[host]['AD_Name'] = 'Doctor'

                if host in Secretary_Station:
                    hostvars[host]['template'] = 'Lockdown-v10-Windows-Template'
                    hostvars[host]['AD_Name'] = 'Secretary'

                if host in FTP:
                    hostvars[host]['template'] = 'Windows-Server-FTP-v8'
                    hostvars[host]['AD_Name'] = 'FTP'

                if host in IOT:
                    hostvars[host]['template'] = 'FinalIoTSystem'
                    hostvars[host]['AD_Name'] = 'IoT'

                if host in WEB:
                    hostvars[host]['template'] = 'FinalHTTP'
                    hostvars[host]['AD_Name'] = 'WEB'
                    hostvars[host]['apache_mods_enabled'] = ['rewrite.load']

                if host in Calendar_System:
                    hostvars[host]['template'] = 'FinalCalDav'
                    hostvars[host]['AD_Name'] = 'CalDav'

                if host in Patient_Notes:
                    hostvars[host]['template'] = 'FinalNotes'
                    hostvars[host]['AD_Name'] = 'Notes'

                if host in DB:
                    hostvars[host]['template'] = 'Server-Ubuntu-18.04-v8'
                    hostvars[host]['AD_Name'] = 'DATABASE'
                    hostvars[host]['mysql_users'] = []
                    hostvars[host]['mysql_users'].append({
                        'name': 'virus',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'flu',
                        'host': '%',
                        'password': 'changeme',
                        'priv': '*.*:ALL,GRANT'
                    })
                    hostvars[host]['mysql_users'].append({
                        'name': 'COWID',
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

                if host in Active_Directory + FTP:
                    hostvars[host]['ansible_user'] = 'Administrator'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['customization']['password'] = hostvars[host]['ansible_password']
                    hostvars[host]['timeout'] = 600

                if host in Nurse_Station_A + Nurse_Station_B + Doctor_Station + Secretary_Station:
                    hostvars[host]['ansible_user'] = 'Admin'
                    hostvars[host]['ansible_password'] = 'Change.me!'
                    hostvars[host]['timeout'] = 600

                if host in IT_Station + Ubuntu + WEB + DB + IOT + Calendar_System + Patient_Notes:
                    hostvars[host]['ansible_user'] = 'sysadmin'
                    hostvars[host]['ansible_password'] = 'changeme'
                    hostvars[host]['ansible_become_pass'] = hostvars[host]['ansible_password']
                    hostvars[host]['OS'] = 'Linux'

                if host in Nurse_Station_A + Nurse_Station_B + Doctor_Station + Secretary_Station + FTP:
                    hostvars[host]['dns_domain_name'] = hostvars[
                        Active_Directory[idx]]['domain_name']
                    hostvars[host]['domain_admin_password'] = hostvars[
                        Active_Directory[idx]]['ansible_password']
                    hostvars[host]['domain_admin_user'] = hostvars[
                        Active_Directory[idx]]['ansible_user']

                if host in Active_Directory + FTP + Nurse_Station_A + Nurse_Station_B + Doctor_Station + Secretary_Station + FTP:
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
        Nurse_Station_A_dict = {}
        Nurse_Station_B_dict = {}
        Doctor_Station_dict = {}
        Secretary_Station_dict = {}
        IT_Station_dict = {}
        Ubuntu_dict = {}
        FTP_dict = {}
        WEB_dict = {}
        DB_dict = {}
        IOT_dict = {}
        Calendar_System_dict = {}
        Patient_Notes_dict = {}
        Active_Directory_dict["hosts"] = Active_Directory
        Nurse_Station_A_dict["hosts"] = Nurse_Station_A
        Nurse_Station_B_dict["hosts"] = Nurse_Station_B
        Doctor_Station_dict["hosts"] = Doctor_Station
        Secretary_Station_dict["hosts"] = Secretary_Station
        IT_Station_dict["hosts"] = IT_Station
        Ubuntu_dict["hosts"] = Ubuntu
        FTP_dict["hosts"] = FTP
        WEB_dict["hosts"] = WEB
        DB_dict["hosts"] = DB
        IOT_dict["hosts"] = IOT
        Calendar_System_dict["hosts"] = Calendar_System
        Patient_Notes_dict["hosts"] = Patient_Notes

        #TODO: Potentially include palo Alto
        ################################################################################################
        inventory['all'] = all

        #inventory['Active_Directory'] = Active_Directory_dict
        inventory['Nurse_Station_A'] = Nurse_Station_A_dict
        inventory['Nurse_Station_B'] = Nurse_Station_B_dict
        inventory['Doctor_Station'] = Doctor_Station_dict
        inventory['Secretary_Station'] = Secretary_Station_dict
        #inventory['IT_Station'] = IT_Station_dict
        #inventory['Ubuntu'] = Ubuntu_dict
        #inventory['FTP'] = FTP_dict
        #inventory['WEB'] = WEB_dict
        #inventory['DB'] = DB_dict
        #inventory['IOT'] = IOT_dict
        #inventory['Calendar_System'] = Calendar_System_dict
        #inventory['Patient_Notes'] = Patient_Notes_dict

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
