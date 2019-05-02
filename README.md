Lockdown v6 Deplotment
=========
This is a Lockdown v6 Deployment Repo. The whole deployment and VM configuration procedure is carried out by ansible.

Where to start?
=========
Main playbook: deploy.yaml

Requirements
------------
- python >=2.6
- pyshere
- pyVmomi

Role Variables
--------------
Variables are generated using dynamic inventory, please check out inventory.py
(Passwords and other sensitive information is passed thru a CLI, or a survey if you are using Ansible tower)

Notes
--------------
Vm OVA(s) could be requested thru issues section of this repo. Generally we just install vmware tools and ssh/winrm depending on if it is Linux or Windows.


Some Useful Links
------------------
https://docs.ansible.com/ansible/latest/modules/vmware_guest_module.html

https://docs.ansible.com/ansible/latest/modules/vsphere_guest_module.html //DEPRICATED

https://docs.ansible.com/ansible/latest/modules/vmware_local_role_manager_module.html

https://docs.ansible.com/ansible/devel/modules/vmware_object_role_permission_module.html

https://docs.ansible.com/ansible/latest/modules/vcenter_folder_module.html

https://docs.ansible.com/ansible/2.7/user_guide/playbooks_filters_ipaddr.html#ip-math

https://docs.ansible.com/ansible/latest/modules/vmware_guest_powerstate_module.html

https://docs.ansible.com/ansible/latest/modules/vmware_vm_shell_module.html

https://paloaltonetworks.github.io/ansible-pan/
