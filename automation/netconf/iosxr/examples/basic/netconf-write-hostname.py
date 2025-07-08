from ncclient import manager
import xmltodict
import xml.dom.minidom

# Router connection details
device = {
    "host": "clab-ebgp-c8k-cisco8201-1",
    "port": 830,
    "username": "cisco",
    "password": "cisco123"
}

# New hostname configuration
hostname_config = f'''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <host-names xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg">
        <host-name>{"Cisco8201-1"}</host-name>
    </host-names>
</config>
'''

# Function to change the hostname
def push_config(host, port, user, password, config):
    with manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False) as m:
        netconf_response = m.edit_config(target="candidate", config=config)
        m.commit()
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Change the hostname
push_config(device["host"], device["port"], device["username"], device["password"], hostname_config)