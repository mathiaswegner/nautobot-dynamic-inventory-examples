# Using Nautobot for dynamic inventory

## With Python

### Nautobot inventory

To connect to the Nautobot API, use the pynautobot.api() object and provide a URL and token.  The object endpoints are structured the same way that they are in the web UI.  From each endpoint, you can use get(), filter(), or all() to retrieve objects.  Get() is used to retrieve a single object, passing in an ID or keyword arguments that will narrow the results down to a single device (eg, the fully qualified name).  Filter() is used to retrieve a list of objects, passing in keyword arguments that will be used to filter the objects.  If multiple keywords are passed in, they will both be used (an AND search).  If a keyword is provided with a list value, they will both be used (an OR search).  All() retrieves all objects of that type.

### Network driver details

The function show_device_details prints information about a device.  This takes the Device object, creates a napalm connection to the device, runs a get_facts, and prints the results.  This is a simple example of how to get the necessary data from Nautobot to use Napalm to interact with a device.  The network_driver_mappings dict also provides driver mappings for ansible, netmiko, ntc_templates, pyats, pyntc, and scrapli.

## With Ansible

### Getting basic inventory

To use Nautobot as an Ansible inventory, simply install the nautobot collection:

`ansible-galaxy collection install networktocode.nautobot`

Then set up a config file.  The `nautobot_inventory.yaml` config file in this repository is a basic example.  It assumes that you are putting your Nautobot API token in an environment variable called NAUTOBOT_TOKEN.

The official documentation explains all of the configuration options.  Of particular interest are group_by, group, and query_filters.  Group_by is a list of Nautobot attributes which will be used to create inventory groups.  Group lets you create search based inventory groups using Jinja2 conditionals.  Query_filters is a list (used as a logical OR) of attribute: value pairs to limit the devices that are included in the inventory.

To use this inventory configuration, pass the config file as the inventory argument to an Ansible command.

### Getting attributes

To get attributes or related models that are not included in the basic inventory, the networktocode.nautobot.query_graphql task can be used to get exactly the values needed.  Set an ansible fact to be a graphql query that includes the data that you need, import the NAUTOBOT_TOKEN environment variable as an Ansible variable, and then use the networktocode.nautobot.query_graphql module to run the query.

## Official documentation

- Nautobot: <https://nautobot.readthedocs.io/>
- Pynautobot: <https://pynautobot.readthedocs.io/>
- Nautobot Ansible Collection: <https://nautobot-ansible.readthedocs.io/>
