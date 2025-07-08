from ncclient import manager
from xml.dom.minidom import parseString

# Nexus 9K device connection details
HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

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

    print("📥 Fetching full <running> configuration via NETCONF...")
    
    # Run get-config without filter (as long as your device allows it)
    response = m.get_config(source="running")

    # Format and pretty-print the XML
    pretty_xml = parseString(response.xml).toprettyxml()

    # Save to file
    with open("running_config.xml", "w") as f:
        f.write(pretty_xml)

    print("✅ Config saved to running_config.xml")