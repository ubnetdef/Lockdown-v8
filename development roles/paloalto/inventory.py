#!/usr/bin/env python
import argparse

try:
    import json
except ImportError:
    import simplejson as json


class Inventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.enventory_generator()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()
        print(json.dumps(self.inventory))
        with open("temp", 'w') as f:
            f.write(json.dumps(self.inventory))


    def enventory_generator(self):
        inventory = {}
        _meta = {}
#####################################################################################################
        all = {}
        all_vars = {}
        all_vars['vcenter_hostname'] = 'cdr-vcenter.cse.buffalo.edu'
        all_vars['datastore'] = 'THE-VAULT'
        all_vars['datacenter'] = 'UBNetDef'
        all_vars['cluster'] = 'MAIN'
        all_vars['template'] = 'student_machine'
        all_vars['vm_name'] = 'student_vm'
        all_vars['vmnet'] = 'generic-net'
        all_vars['ip'] = '10.42.25.101'
        all_vars['netmask'] = '255.255.255.0'
        all_vars['gateway'] = '10.42.25.1'
        all_vars['pan_template'] = 'PaloAlto_SysSec_Class'
        all_vars['pan_default_ip'] = '192.168.1.1'
        all_vars['pan_username'] = 'admin'
        all_vars['pan_password'] = 'Change.me!'
        all_vars['pan_outside_ip'] = '192.168.8.101'
        all_vars['pan_final_management_ip'] = '192.168.8.131'
        all_vars['config_name'] = 'temp_xml_config.xml'
        all_vars['gretzky'] = '192.168.0.1'
        all_vars['dns_list'] = ['8.8.8.8', '8.8.4.4']
        #all_vars['ubit'] = Actual UBIT names spacified in Tower config

        all['vars'] = all_vars
        inventory['all'] = all
        return inventory
#####################################################################################################


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


