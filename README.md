# Using Nautobot for dynamic inventory

## With Python

The script imports the necessary modules: argparse, sys, napalm, pynautobot, and getpass.

### Nautobot inventory

To connect to the Nautobot API, use the pynautobot.api() object and provide a URL and token.  The object endpoints are structured the same way that they are in the web UI.  From each endpoint, you can use get(), filter(), or all() to retrieve objects.  Get() is used to retrieve a single object, passing in an ID or keyword arguments that will narrow the results down to a single device (eg, the fully qualified name).  Filter() is used to retrieve a list of objects, passing in keyword arguments that will be used to filter the objects.  If multiple keywords are passed in, they will both be used (an AND search).  If a keyword is provided with a list value, they will both be used (an OR search).  All() retrieves all objects of that type.

### Network driver details

The function show_device_details prints information about a device.  This takes the Device object, creates a napalm connection to the device, runs a get_facts, and prints the results.  This is a simple example of how to get the necessary data from Nautobot to use Napalm to interact with a device.  The network_driver_mappings dict also provides driver mappings for ansible, netmiko, ntc_templates, pyats, pyntc, and scrapli.

## With Ansible

### Getting inventory

### Getting attributes

## Official documentation

- Nautobot: <https://nautobot.readthedocs.io/>
- Pynautobot: <https://pynautobot.readthedocs.io/>
- Nautobot Ansible Collection: <https://nautobot-ansible.readthedocs.io/>
