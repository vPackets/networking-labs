import sys
import time
from ncclient import manager
from ncclient.xml_ import to_ele

def create_vrf_subint(netconf_config, ip, uname, pword):
    con = manager.connect(host=ip, port=830, username=uname, password=pword, hostkey_verify=False, device_params={'name':'iosxr'})
    con.edit_config(netconf_config, target = "candidate")
    con.commit()
    con.close_session()

def gen_xml(low, high):
    netconf_config = """
    <config>
     <interfaces xmlns="http://openconfig.net/yang/interfaces">
      <interface>
        <name>Bundle-Ether100</name>
        <config>
         <name>Bundle-Ether100</name>
         <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ieee8023adLag</type>
        </config>
        <subinterfaces>"""

    for id in range(low,high):
         netconf_config = netconf_config + f"""
         <subinterface>
          <index>{id}</index>
          <config>
           <index>{id}</index>
          </config>
          <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
           <addresses>
            <address>
             <ip>100.100.100.1</ip>
             <config>
              <ip>100.100.100.1</ip>
              <prefix-length>24</prefix-length>
             </config>
            </address>
           </addresses>
          </ipv4>
          <ipv6 xmlns="http://openconfig.net/yang/interfaces/ip">
           <addresses>
            <address>
             <ip>2001:100:100:100::1</ip>
             <config>
              <ip>2001:100:100:100::1</ip>
              <prefix-length>64</prefix-length>
             </config>
            </address>
           </addresses>
          </ipv6>
          <vlan xmlns="http://openconfig.net/yang/vlan">
           <match>
            <single-tagged>
             <config>
              <vlan-id>{id}</vlan-id>
              </config>
            </single-tagged>
           </match>
          </vlan>
         </subinterface>"""

    netconf_config = netconf_config + """
        </subinterfaces>
       </interface>
     </interfaces>
     <network-instances xmlns="http://openconfig.net/yang/network-instance">"""

    for id in range(low,high):
        netconf_config = netconf_config + f"""
        <network-instance>
         <name>DX-VRF-{id}</name>
         <config>
          <name>DX-VRF-{id}</name>
          <route-distinguisher>{id}:{id}</route-distinguisher>
          <enabled-address-families xmlns:idx="http://openconfig.net/yang/openconfig-types">idx:IPV4</enabled-address-families>
          <enabled-address-families xmlns:idx="http://openconfig.net/yang/openconfig-types">idx:IPV6</enabled-address-families>
         </config>
         <interfaces>
          <interface>
           <id>Bundle-Ether100.{id}</id>
           <config>
            <id>Bundle-Ether100.{id}</id>
             <interface>Bundle-Ether100</interface>
             <subinterface>{id}</subinterface>
           </config>
          </interface>
         </interfaces>
        </network-instance>"""

    netconf_config = netconf_config + """
     </network-instances>
    </config>"""


    return netconf_config


def rollback(ip, uname, pword):
    nc = manager.connect_ssh(host=ip, port='830', username=uname, password=pword, device_params={"name": "iosxr"}, manager_params={"timeout": 300})
    rpc = """
    <roll-back-configuration-last xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-cfgmgr-rollback-act">
     <count>1</count>
    </roll-back-configuration-last>
    """
    nc.dispatch(to_ele(rpc))


def test_netconf_over_time(ip, uname, pword, low, high):
    t = 1000
    netconf_config = gen_xml(low, high)
    while t > 0:
        diff = high - low
        print(f"### creating {diff} VRFs and subinterfaces ###")
        create_vrf_subint(netconf_config, ip, uname, pword)
        time.sleep(5)
        print(f"### removing {diff} VRFs and sub-interfaces ###")
        rollback(ip, uname, pword)
        time.sleep(5)
        t -= 1
    
test_netconf_over_time(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]) + 1)
