from ncclient import manager
import xml.dom.minidom

# Function to change the router configuration
def write_config(device, config_filename):
    with open(config_filename, 'r') as file:
        config = file.read()

    with manager.connect(host=device["host"], port=device["port"],
                         username=device["username"], password=device["password"],
                         hostkey_verify=False, timeout=60) as m:
        # Execute NETCONF <edit-config> operation on the 'candidate' datastore
        netconf_response = m.edit_config(target="candidate", config=config)
        # Print the response from the device
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Function to commit the configuration
def commit_config(device):
    with manager.connect(host=device["host"], port=device["port"],
                         username=device["username"], password=device["password"],
                         hostkey_verify=False, timeout=60) as m:
        # Directly use commit RPC of ncclient
        commit_response = m.commit()
        print(xml.dom.minidom.parseString(commit_response.xml).toprettyxml())

# Router connection details for each device
devices = [
    {"host": "clab-eBGP-vMX-vmx01", "port": 830, "username": "admin", "password": "admin@123"},
    {"host": "clab-eBGP-vMX-vmx02", "port": 830, "username": "admin", "password": "admin@123"}
]

# Configuration file names for each device
config_files = ["router-config-01.xml", "router-config-02.xml"]

# Apply the configurations to each device using a for loop and then commit
for device, config_file in zip(devices, config_files):
    write_config(device, config_file)
    commit_config(device)
