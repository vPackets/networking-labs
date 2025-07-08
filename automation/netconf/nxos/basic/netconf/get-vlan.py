from ncclient import manager
from xml.dom.minidom import parseString

HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

filter = """
<filter>
  <System xmlns="http://cisco.com/ns/yang/Cisco-NX-OS-device">
    <vlan-items/>
  </System>
</filter>
"""

with manager.connect(
    host=HOST, port=PORT, username=USERNAME, password=PASSWORD,
    hostkey_verify=False, device_params={"name": "nexus"},
    allow_agent=False, look_for_keys=False
) as m:
    print("Pulling VLAN configuration from the switch...")
    response = m.get(filter=filter)
    xml_str = parseString(response.xml).toprettyxml()
    with open("vlan_readback.xml", "w") as f:
        f.write(xml_str)

    print("✅ VLAN configuration saved to vlan_readback.xml")