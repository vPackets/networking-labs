from ncclient import manager
import xml.dom.minidom

# Function to change the router configuration
def write_config(device, config_filename):
    # Read the configuration from the file
    with open(config_filename, 'r') as file:
        config = file.read()

    # Connect to the device with an increased timeout (e.g., 60 seconds)
    with manager.connect(host=device["host"], port=device["port"], 
                         username=device["username"], password=device["password"], 
                         hostkey_verify=False, timeout=60) as m:
        # Execute NETCONF <edit-config> operation on the 'running' datastore
        netconf_response = m.edit_config(target="running", config=config)
        # Print the response from the device
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Router connection details for each device
devices = [
    {"host": "clab-eBGP-ceos-ceos1", "port": 830, "username": "admin", "password": "admin"},
    {"host": "clab-eBGP-ceos-ceos2", "port": 830, "username": "admin", "password": "admin"}
]

# Configuration file names for each device
config_files = ["router-config-01.xml", "router-config-02.xml"]

# Apply the configurations to each device using a for loop
for device, config_file in zip(devices, config_files):
    write_config(device, config_file)
