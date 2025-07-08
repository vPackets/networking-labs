from ncclient import manager
from xml.dom.minidom import parseString

device = {
    "address": "198.18.128.3",
    "netconf_port": 830,
    "username": "netconf",
    "password": "C1sco12345!"
}

def main():
    with manager.connect(
        host=device["address"],
        port=device["netconf_port"],
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
    ) as m:
        
        filter_xml = """
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"/>
        """
        
        response = m.get_config(source="running", filter=("subtree", filter_xml))
        
        # Prettify
        raw_xml = response.xml
        parsed = parseString(raw_xml)
        pretty_xml = parsed.toprettyxml(indent="  ")
        
        print(pretty_xml)
    
    with open("get-running-config.xml", "w") as f:
        f.write(pretty_xml)



if __name__ == '__main__':
    main()
