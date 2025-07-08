
from ncclient import manager

# Connect to the network device using ncclient
with manager.connect(host="clab-eBGP-c8K-Cisco8201-1", port=830, username="cisco", password="cisco123", hostkey_verify=False) as nc_conn:
    # Retrieve the running configuration
    nc_config = nc_conn.get_config(source='running').data_xml
    # Print the configuration
    print(nc_config)



'''

Pretty config to test:

from ncclient import manager
import xml.dom.minidom

# Define the connection details in a dictionary
device = {
    "host": "clab-eBGP-c8K-Cisco8201-1",
    "port": 830,
    "username": "cisco",
    "password": "cisco123",
    "hostkey_verify": False
}

# Connect to the network device using ncclient
with manager.connect(**device) as nc_conn:
    # Retrieve the running configuration
    nc_config = nc_conn.get_config(source='running').data_xml
    
    # Parse and beautify the XML
    xml_pretty = xml.dom.minidom.parseString(nc_config)
    pretty_xml_as_string = xml_pretty.toprettyxml()
    
    # Print the formatted configuration
    print(pretty_xml_as_string)

    


'''