from ncclient import manager
import xml.dom.minidom
import time
import schedule
import logging
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup logging
log_file = '/home/netadmin/code/vrf/vrf_creation.log'
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Generate the VRF configurations
def generate_vrf_config(vrf_id, vlan_id):
    vrf_name = f"CUSTOMER_{vrf_id:04d}_VLAN_{vlan_id}"
    return f"""
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <vrfs xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-infra-rsi-cfg">
            <vrf>
                <vrf-name>{vrf_name}</vrf-name>
                <create></create>
                <bgp-global xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg">
                    <route-distinguisher>
                        <type>as</type>
                        <as-xx>0</as-xx>
                        <as>65000</as>
                        <as-index>{vlan_id}</as-index>
                    </route-distinguisher>
                </bgp-global>
                <afs>
                    <af>
                        <af-name>ipv4</af-name>
                        <saf-name>unicast</saf-name>
                        <topology-name>default</topology-name>
                        <create></create>
                        <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg">
                            <import-route-targets>
                                <route-targets>
                                    <route-target>
                                        <type>as</type>
                                        <as-or-four-byte-as>
                                            <as-xx>0</as-xx>
                                            <as>65000</as>
                                            <as-index>{vlan_id}</as-index>
                                            <stitching-rt>0</stitching-rt>
                                        </as-or-four-byte-as>
                                    </route-target>
                                </route-targets>
                            </import-route-targets>
                            <export-route-targets>
                                <route-targets>
                                    <route-target>
                                        <type>as</type>
                                        <as-or-four-byte-as>
                                            <as-xx>0</as-xx>
                                            <as>65000</as>
                                            <as-index>{vlan_id}</as-index>
                                            <stitching-rt>0</stitching-rt>
                                        </as-or-four-byte-as>
                                    </route-target>
                                </route-targets>
                            </export-route-targets>
                        </bgp>
                    </af>
                </afs>
            </vrf>
        </vrfs>
        <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg">
            <instance>
                <instance-name>default</instance-name>
                <instance-as>
                    <as>0</as>
                    <four-byte-as>
                        <as>65000</as>
                        <bgp-running></bgp-running>
                        <vrfs>
                            <vrf>
                                <vrf-name>{vrf_name}</vrf-name>
                                <vrf-global>
                                    <exists></exists>
                                    <route-distinguisher>
                                        <type>as</type>
                                        <as-xx>0</as-xx>
                                        <as>65000</as>
                                        <as-index>{vlan_id}</as-index>
                                    </route-distinguisher>
                                    <multi-path-as-path-ignore-onwards></multi-path-as-path-ignore-onwards>
                                    <vrf-global-afs>
                                        <vrf-global-af>
                                            <af-name>ipv4-unicast</af-name>
                                            <enable></enable>
                                            <label-mode>
                                                <label-allocation-mode>per-vrf</label-allocation-mode>
                                                <allocate-secondary-label>false</allocate-secondary-label>
                                            </label-mode>
                                            <ebgp>
                                                <paths-value>16</paths-value>
                                                <selective>false</selective>
                                            </ebgp>
                                            <connected-routes/>
                                        </vrf-global-af>
                                    </vrf-global-afs>
                                </vrf-global>
                                <vrf-neighbors>
                                    <vrf-neighbor>
                                        <neighbor-address>192.168.1.2</neighbor-address>
                                        <create></create>
                                        <remote-as>
                                            <as-xx>0</as-xx>
                                            <as-yy>65100</as-yy>
                                        </remote-as>
                                        <bfd-enable-modes>default</bfd-enable-modes>
                                        <vrf-neighbor-afs>
                                            <vrf-neighbor-af>
                                                <af-name>ipv4-unicast</af-name>
                                                <activate></activate>
                                                <send-community-ebgp>true</send-community-ebgp>
                                                <route-policy-in>AWS_DX_CUSTOMER</route-policy-in>
                                                <route-policy-out>AWS_DX_CUSTOMER</route-policy-out>
                                                <soft-reconfiguration>
                                                    <inbound-soft>true</inbound-soft>
                                                    <soft-always>true</soft-always>
                                                    <rpki-options>rpki-default-option</rpki-options>
                                                </soft-reconfiguration>
                                            </vrf-neighbor-af>
                                        </vrf-neighbor-afs>
                                    </vrf-neighbor>
                                </vrf-neighbors>
                            </vrf>
                        </vrfs>
                    </four-byte-as>
                </instance-as>
            </instance>
        </bgp>
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
            <interface-configuration>
                <active>act</active>
                <interface-name>Bundle-Ether2000.{vlan_id}</interface-name>
                <interface-mode-non-physical>default</interface-mode-non-physical>
                <description>*** To Customer CE Vlan {vlan_id} ***</description>
                <vrf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-infra-rsi-cfg">{vrf_name}</vrf>
                <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
                    <addresses>
                        <primary>
                            <address>192.168.1.1</address>
                            <netmask>255.255.255.252</netmask>
                        </primary>
                    </addresses>
                </ipv4-network>
                <vlan-sub-configuration xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2-eth-infra-cfg">
                    <vlan-identifier>
                        <vlan-type>vlan-type-dot1q</vlan-type>
                        <first-tag>{vlan_id}</first-tag>
                    </vlan-identifier>
                </vlan-sub-configuration>
            </interface-configuration>
        </interface-configurations>
    </config>
    """

# InfluxDB client setup
influxdb_token = "C1sco12345!"
influxdb_org = "lab"
influxdb_bucket = "vrf"
influxdb_url = "http://198.18.140.3:8086"

client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)
buckets_api = client.buckets_api()

# Check if the bucket exists, if not create it
def ensure_bucket_exists(bucket_name):
    buckets = buckets_api.find_buckets().buckets
    if not any(bucket.name == bucket_name for bucket in buckets):
        buckets_api.create_bucket(bucket_name=bucket_name, org_id=client.org_id)

ensure_bucket_exists(influxdb_bucket)

# Function to push configuration to the device
def push_config(device, config):
    with manager.connect(
        host=device["host"],
        port=device["port"],
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
    ) as m:
        netconf_response = m.edit_config(target="candidate", config=config)
        m.commit()
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Function to create VRF and update InfluxDB
def create_vrf(device, vrf_id):
    vlan_id = 1000 + vrf_id
    config = generate_vrf_config(vrf_id, vlan_id)
    
    try:
        push_config(device, config)
        logging.info(f"VRF {vrf_id} Created on {datetime.now().strftime('%d-%m-%Y')} at {datetime.now().strftime('%H:%M:%S')}, number of VRFs processed: {vrf_id}")
        
        point = Point("vrf_creation")\
            .tag("vrf_id", vrf_id)\
            .tag("vlan_id", vlan_id)\
            .field("status", "created")\
            .time(time.time_ns(), WritePrecision.NS)
        write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
    except Exception as e:
        logging.error(f"Failed to create VRF {vrf_id}: {e}")

# Device connection details
device = {
    "host": "198.18.128.7",
    "port": 830,
    "username": "admin",
    "password": "C1sco12345"
}

# Scheduling VRF creation every 5 minutes
vrf_counter = 0

def job():
    global vrf_counter
    if vrf_counter < 1000:
        create_vrf(device, vrf_counter + 1)
        vrf_counter += 1
    else:
        print("All VRFs created")
        logging.info("All VRFs created")
        return schedule.CancelJob

schedule.every(5).minutes.do(job)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
