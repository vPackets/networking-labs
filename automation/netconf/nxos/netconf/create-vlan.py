from ncclient import manager
import xml.dom.minidom

# Nexus 9K device connection details
HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

# VLAN configuration using the working bd-items structure
vlan_config = """
<config>
  <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <bd-items>
      <bd-items>
        <BD-list>
          <fabEncap>vlan-220</fabEncap>
          <name>inband_mdt</name>
        </BD-list>
      </bd-items>
    </bd-items>
  </System>
</config>
"""

with manager.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    hostkey_verify=False,
    device_params={"name": "nexus"},
    allow_agent=False,
    look_for_keys=False
) as m:

    print("🔧 Pushing VLAN 250 config via NETCONF...")
    result = m.edit_config(target="running", config=vlan_config)

    # Optional: commit, only if using <candidate>
    # m.commit()

    # Format and save the response
    formatted_output = xml.dom.minidom.parseString(result.xml).toprettyxml()

    with open("vlan_push_result.xml", "w") as f:
        f.write(formatted_output)

    print("✅ Response written to vlan_push_result.xml")