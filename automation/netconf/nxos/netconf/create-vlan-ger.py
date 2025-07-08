
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
    add_vlan = """
    <config>
      <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <bd-items>
          <bd-items>
            <BD-list>
              <fabEncap>vlan-250</fabEncap>
              <name>inband_mmt</name>
            </BD-list>
          </bd-items>
        </bd-items>
      </System>
    </config>
    """


    with manager.connect(host=device["address"],
                         port=device["netconf_port"],
                         username=device["username"],
                         password=device["password"],
                         hostkey_verify=False) as m:

        # create vlan with edit_config
        netconf_response = m.edit_config(target="running", config=add_vlan)
        print(netconf_response)

        netconf_response =m.commit()
        print(netconf_response)



if __name__ == '__main__':
    sys.exit(main())