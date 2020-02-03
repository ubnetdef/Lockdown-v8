UB Lockdown v8
=========
This is a UB Lockdown v8 Deployment Repo. The whole deployment and VM configuration procedure is carried out by ansible.

Where to start?
=========
Main playbook: deploy.yaml

Requirements
------------
- python >=2.6
- pyshere
- pyVmomi
- Ansible 2.8

Role Variables
--------------
Variables are generated using dynamic inventory, please check out inventory.py
(Passwords and other sensitive information is passed thru a CLI, or a survey if you are using Ansible tower)

Deployment Procedure (You might have to zoom-in😅)
--------------
Consider an example of deploying a 4 team environment with following machines:
 - Router
 - Ubuntu (VM Group 1)
 - Windows 10 Pro (VM Group 2)
 - Windows Server (VM Group 3)
And Following Configurations:
 - Ubuntu is hosting a Web Server (Ex. WordPress)
 - Windows Server is hosting Active Directory
 - Windows 10 Pro is connected to the Active Directory
![Deployment Procedure](https://user-images.githubusercontent.com/35672535/73682204-e84e4c80-468d-11ea-96a0-fce0da6757c5.png)

Notes
--------------
This will make your life easy: https://wiki.ubnetdef.org/guides/lockdown_black_team

VM OVA(s) could be requested thru issues section of this repo. Generally we just install vmware tools and ssh/winrm depending on if it is Linux or Windows.

Some modules were imported from ansible 2.8 (as of 5/2/2019 Ansible 2.8 is still in development)

If you don't have problems with mass cloning and configuration in your vcenter, you can adjust role 'template_deployment' to make the deployment faster

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

As per https://github.com/PaloAltoNetworks/ansible-pan/pull/394 it is now possible to insert cmd commands in palo alto firewall
