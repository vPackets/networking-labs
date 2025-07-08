from ncclient import manager
import xml.dom.minidom

# Function to change the router configuration
def write_config(device, config_filename):
    # Read the configuration from the file
    with open(config_filename, 'r') as file:
        config = file.read()

    # Print the configuration (request XML) that will be sent to the device
    print("\n" + "="*40 + "\nRequest XML:\n" + "="*40)
    print(xml.dom.minidom.parseString(config).toprettyxml())

    with manager.connect(
        host=device["host"], 
        port=device["port"], 
        username=device["username"], 
        password=device["password"], 
        hostkey_verify=False
    ) as m:
        netconf_response = m.edit_config(target="candidate", config=config)

        # Print the response from the device
        print("\n" + "="*40 + "\nResponse XML:\n" + "="*40)
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

        m.commit()

# Router connection details
devices = [
    {"host": "198.18.128.7", "port": 830, "username": "admin", "password": "C1sco12345"},
]

# Configuration file names
config_files = ["cisco-8000-config-vrf.xml"]

# Apply the configurations to each device using a for loop
for device, config_file in zip(devices, config_files):
    write_config(device, config_file)
