from ncclient import manager
import sys
from lxml import etree

device = {
    "address": "198.18.128.3",
    "netconf_port": 830,
    "username": "netconf",
    "password": "C1sco12345!"
}

def main():
    interface = "Ethernet1/3"   
    macsec_key = "MyNewSecretKey123"  

    macsec_config = f"""
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
          <phys-items>
            <PhysIf-list>
              <id>{interface}</id>
              <macsec-items>
                <CfgSharedSecret-items>
                  <secret>{macsec_key}</secret>
                </CfgSharedSecret-items>
              </macsec-items>
            </PhysIf-list>
          </phys-items>
        </intf-items>
      </System>
    </config>
    """

    with manager.connect(
        host=device["address"],
        port=device["netconf_port"],
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
    ) as m:

        # push macsec config
        netconf_response = m.edit_config(target="running", config=macsec_config)
        print(netconf_response)

        # optional: commit if needed (depends if device requires commit)
        try:
            netconf_response = m.commit()
            print(netconf_response)
        except Exception as e:
            print("Commit not supported or not needed:", str(e))

if __name__ == '__main__':
    sys.exit(main())