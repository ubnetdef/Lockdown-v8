#!/usr/bin/python

import atexit
import ssl

from ansible.module_utils.basic import *
from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim


def get_obj(content, vimtype, name):

    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def main():

    fields = {
        "vcenter_ip": {"required": True, "type": "str"},
        "vcenter_password": {"required": True, "type": "str", "no_log": True},
        "vcenter_user": {"required": True, "type": "str"},
        "vm_name": {"default": True, "type": "str"},
        "isDHCP": {"default": False, "type": "bool"},
        "vm_ip": {"required": True, "type": "str"},
        "subnet": {"required": True, "type": "str"},
        "gateway": {"required": True, "type": "str"},
        "dns": {"required": True, "type": "list"},
        "domain": {"required": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)

    context = ssl._create_unverified_context()
    si = None
    try:
        print("Trying to connect to VCENTER SERVER . . .")
        si = connect.Connect(module.params['vcenter_ip'], 443, module.params['vcenter_user'], module.params['vcenter_password'],
                             sslContext=context)
    except IOError as e:
        pass
        atexit.register(Disconnect, si)

    print("Connected to VCENTER SERVER !")

    content = si.RetrieveContent()

    # vm_name = args.vm
    vm_name = module.params['vm_name']
    vm = get_obj(content, [vim.VirtualMachine], vm_name)

    if vm.runtime.powerState != 'poweredOff':
        print("WARNING:: Power off your VM before reconfigure")
        sys.exit()

    adaptermap = vim.vm.customization.AdapterMapping()
    globalip = vim.vm.customization.GlobalIPSettings()
    adaptermap.adapter = vim.vm.customization.IPSettings()

    isDHDCP = module.params['isDHCP']
    if not isDHDCP:
        """Static IP Configuration"""
        adaptermap.adapter.ip = vim.vm.customization.FixedIp()
        adaptermap.adapter.ip.ipAddress = module.params['vm_ip']
        adaptermap.adapter.subnetMask = module.params['subnet']
        adaptermap.adapter.gateway = module.params['gateway']
        globalip.dnsServerList = module.params['dns']

    else:
        """DHCP Configuration"""
        adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()

    adaptermap.adapter.dnsDomain = module.params['domain']

    globalip = vim.vm.customization.GlobalIPSettings()

    # For Linux . For windows follow sysprep
    ident = vim.vm.customization.LinuxPrep(domain=module.params['domain'],
                                           hostName=vim.vm.customization.FixedName(name=vm_name))

    customspec = vim.vm.customization.Specification()
    # For only one adapter
    customspec.identity = ident
    customspec.nicSettingMap = [adaptermap]
    customspec.globalIPSettings = globalip

    # Configuring network for a single NIC
    # For multipple NIC configuration contact me.

    print("Reconfiguring VM Networks . . .")


    vm.Customize(spec=customspec)

    module.exit_json(changed=True)


# Start program
if __name__ == '__main__':
    main()
