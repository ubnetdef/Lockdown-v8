import xml.etree.ElementTree as ET

import requests
from ansible.module_utils.basic import *
from bs4 import BeautifulSoup as BS


def main():
    fields = {
        "ip_address": {"default": '192.168.1.1', "type": "str"},
        "new_ip_address": {"required": True, "type": "str"},
        "username": {"default": 'admin', "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "config_name": {"required": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    r = requests.get("https://{}/api/?type=keygen&user={}&password={}".format(module.params['ip_address'], module.params['username'], module.params['password']), verify=False)
    soup = BS(r.text, "lxml")
    key = soup.find('key').text
    r = requests.get("https://{}/api/?type=export&category=configuration&key={}".format(module.params['ip_address'], key), verify=False)
    root = ET.fromstring(r.text)
    for device in root.findall('devices'):
        for entry in device:
            if entry.attrib.get('name') == 'localhost.localdomain':
                for deviceconfig in entry.findall('deviceconfig'):
                    for system in deviceconfig.findall('system'):
                        for ip_address in system.findall('ip-address'):
                            ip_address.text = module.params['new_ip_address']

    xmlstr = ET.tostring(root, encoding='unicode', method='xml') #encoding might be utf-8
    xmlstr.replace(' /', '/')
    with open(module.params['config_name'], 'w') as file:
        file.write(xmlstr)
    module.exit_json(changed=True)

# Start program
if __name__ == "__main__":
    main()