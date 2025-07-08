# Basic script that pushes BGP configuration to 2 routers
# The router configuration files are read from the script and pushed to the devices.
# Each file is specific to a router and must be defined in the following script.
# a function is created to simplify the code


from ncclient import manager
import xml.dom.minidom

# Function to change the router configuration
def write_config(device, config_filename):
    # Read the configuration from the file
    with open(config_filename, 'r') as file:
        config = file.read()

    with manager.connect(host=device["host"], port=device["port"], username=device["username"], password=device["password"], hostkey_verify=False) as m:
        netconf_response = m.edit_config(target="candidate", config=config)
        m.commit()
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Router connection details for both routers
devices = [
    {
        "host": "clab-ebgp-c8k-cisco8201-1",
        "port": 830,
        "username": "cisco",
        "password": "cisco123"
    },
    {
        "host": "clab-ebgp-c8k-cisco8201-2",
        "port": 830,
        "username": "cisco",
        "password": "cisco123"
    }
]

# Apply the configurations to each device
write_config(devices[0], "router-config-01.xml")
write_config(devices[1], "router-config-02.xml")
