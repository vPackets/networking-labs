from ncclient import manager

HOST = "198.18.128.3"
PORT = 830
USERNAME = "netconf"
PASSWORD = "C1sco12345!"

def show_capabilities():
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
        print("=== NETCONF Capabilities ===")
        for cap in m.server_capabilities:
            print(cap)

if __name__ == "__main__":
    show_capabilities()