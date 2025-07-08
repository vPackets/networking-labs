from ncclient import manager
import xml.dom.minidom

def get_running_config(host, port, username, password):
    with manager.connect(
        host=host, port=port, username=username, password=password, 
        hostkey_verify=False, device_params={'name': 'csr'}
    ) as m:
        # Get running config
        running_config = m.get_config(source='running').xml
        return running_config

# Router connection details
router = {
    "host": "clab-eBGP-CSR-csr2",
    "port": 830,
    "username": "admin",
    "password": "admin"
}

# Retrieve the running configuration
running_config = get_running_config(**router)

# Pretty print the running configuration
print(xml.dom.minidom.parseString(running_config).toprettyxml())