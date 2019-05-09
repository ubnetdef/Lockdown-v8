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
        "vm_name": {"default": True, "type": "str"}
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
    dev_changes = []
    for dev in vm.config.hardware.device:
        if not isinstance(dev, vim.vm.device.VirtualEthernetCard):
            continue

        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = dev
        virtual_nic_spec.device.key = dev.key
        virtual_nic_spec.device.macAddress = dev.macAddress
        virtual_nic_spec.device.backing = dev.backing
        virtual_nic_spec.device.wakeOnLanEnabled = dev.wakeOnLanEnabled

        # Connect things, if needed
        connectable = dev.connectable
        changed = False
        if not dev.connectable.startConnected:
            connectable.startConnected = True
            changed = True

        if not dev.connectable.connected and dev.connectable.status == 'ok':
            connectable.connected = True
            changed = True

        virtual_nic_spec.device.connectable = connectable

        if changed:
            dev_changes.append(virtual_nic_spec)

        if not dev_changes:
            continue

    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    vm.ReconfigVM_Task(spec=spec)

    module.exit_json(changed=True)


# Start program
if __name__ == '__main__':
    main()
