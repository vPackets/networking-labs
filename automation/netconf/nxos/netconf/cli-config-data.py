from ncclient import manager
import xml.dom.minidom

HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

vlan_config = """
<config>
  <cli-config-data xmlns="http://cisco.com/ns/yang/cisco-nx-os-cli">
    <cmd>vlan 1000</cmd>
    <cmd>name NETCONF_VLAN1000</cmd>
  </cli-config-data>
</config>
"""

with manager.connect(
    host=HOST, port=PORT, username=USERNAME, password=PASSWORD,
    hostkey_verify=False, device_params={"name": "nexus"},
    allow_agent=False, look_for_keys=False
) as m:
    print("Pushing VLAN 1000 config using CLI-based NETCONF...")
    response = m.edit_config(target="running", config=vlan_config)
    formatted_output = xml.dom.minidom.parseString(response.xml).toprettyxml()

    with open("vlan_cli_push_result.xml", "w") as f:
        f.write(formatted_output)

    print("✅ Response saved to vlan_cli_push_result.xml")