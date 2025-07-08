from ncclient import manager

# Nexus 9000 NETCONF connection info
HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

# Module name based on your discovery: Cisco-NX-OS-device
MODULE_NAME = "Cisco-NX-OS-device"

def pull_yang_schema():
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
        print(f"📥 Fetching YANG model: {MODULE_NAME}")
        schema = m.get_schema(MODULE_NAME)
        
        # Write to a text file
        with open(f"{MODULE_NAME}.txt", "w") as f:
            f.write(schema.data)
        print(f"✅ Schema written to {MODULE_NAME}.txt")

if __name__ == "__main__":
    pull_yang_schema()