from ncclient import manager
from lxml import etree
import xml.dom.minidom

device = {
    "address": "198.18.128.3",
    "netconf_port": 830,
    "username": "netconf",
    "password": "C1sco12345!"
}

filter_ethernet116 = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
      <phys-items>
        <PhysIf-list>
          <id>Ethernet1/16</id>
        </PhysIf-list>
      </phys-items>
    </intf-items>
  </System>
</filter>
"""

with manager.connect(host=device["address"],
                     port=device["netconf_port"],
                     username=device["username"],
                     password=device["password"],
                     hostkey_verify=False) as m:

    response = m.get_config(
        source="running",
        filter=("subtree", etree.fromstring(filter_ethernet116))  # <= parse as XML
    )

    xml_response = xml.dom.minidom.parseString(response.xml)
    pretty_xml = xml_response.toprettyxml(indent="  ")
    print(pretty_xml)