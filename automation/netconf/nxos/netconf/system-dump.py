from ncclient import manager
from xml.dom.minidom import parseString

HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

filter = """
<filter>
  <System xmlns="http://cisco.com/ns/yang/Cisco-NX-OS-device"/>
</filter>
"""

with manager.connect(
    host=HOST, port=PORT, username=USERNAME, password=PASSWORD,
    hostkey_verify=False, device_params={"name": "nexus"},
    allow_agent=False, look_for_keys=False
) as m:
    print("Getting System subtree...")
    response = m.get(filter=filter)
    xml_str = parseString(response.xml).toprettyxml()
    with open("system_dump.xml", "w") as f:
        f.write(xml_str)

    print("✅ System data saved to system_dump.xml")