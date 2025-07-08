from ncclient import manager

HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

def fetch_netconf_capabilities():
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
        with open("netconf_capabilities.txt", "w") as f:
            f.write("=== NETCONF Capabilities ===\n")
            for cap in m.server_capabilities:
                f.write(cap + "\n")

if __name__ == "__main__":
    fetch_netconf_capabilities()