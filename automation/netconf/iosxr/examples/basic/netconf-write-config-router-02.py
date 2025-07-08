from ncclient import manager
import xmltodict
import xml.dom.minidom

# Router connection details
device = {
    "host": "clab-ebgp-c8k-cisco8201-2",
    "port": 830,
    "username": "cisco",
    "password": "cisco123"
}

# New hostname configuration
hostname_config = f'''
<config
	xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
	<routing-policy
		xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-policy-repository-cfg">
		<route-policies>
			<route-policy>
				<route-policy-name>ALLOW</route-policy-name>
				<rpl-route-policy>route-policy ALLOW
pass
end-policy
        </rpl-route-policy>
			</route-policy>
		</route-policies>
	</routing-policy>
	<bgp
		xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg">
		<instance>
			<instance-name>default</instance-name>
			<instance-as>
				<as>0</as>
				<four-byte-as>
					<as>65100</as>
					<bgp-running></bgp-running>
					<default-vrf>
						<global>
							<router-id>2.2.2.2</router-id>
							<global-afs>
								<global-af>
									<af-name>ipv4-unicast</af-name>
									<enable></enable>
									<sourced-networks>
										<sourced-network>
											<network-addr>203.0.113.0</network-addr>
											<network-prefix>24</network-prefix>
										</sourced-network>
									</sourced-networks>
								</global-af>
							</global-afs>
						</global>
						<bgp-entity>
							<neighbors>
								<neighbor>
									<neighbor-address>10.0.0.1</neighbor-address>
									<create></create>
									<remote-as>
										<as-xx>0</as-xx>
										<as-yy>65000</as-yy>
									</remote-as>
									<neighbor-afs>
										<neighbor-af>
											<af-name>ipv4-unicast</af-name>
											<activate></activate>
											<route-policy-in>ALLOW</route-policy-in>
											<route-policy-out>ALLOW</route-policy-out>
										</neighbor-af>
									</neighbor-afs>
								</neighbor>
							</neighbors>
						</bgp-entity>
					</default-vrf>
				</four-byte-as>
			</instance-as>
		</instance>
	</bgp>
	<interface-configurations
		xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
		<interface-configuration>
			<active>act</active>
			<interface-name>Loopback0</interface-name>
			<interface-virtual></interface-virtual>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
				<addresses>
					<primary>
						<address>10.2.2.2</address>
						<netmask>255.255.255.255</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
		<interface-configuration>
			<active>act</active>
			<interface-name>FourHundredGigE0/0/0/0</interface-name>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
				<addresses>
					<primary>
						<address>203.0.113.1</address>
						<netmask>255.255.255.0</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
		<interface-configuration>
			<active>act</active>
			<interface-name>FourHundredGigE0/0/0/1</interface-name>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
				<addresses>
					<primary>
						<address>10.0.0.2</address>
						<netmask>255.255.255.0</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
	</interface-configurations>
</config>
'''

# Function to change the hostname
def push_config(host, port, user, password, config):
    with manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False) as m:
        netconf_response = m.edit_config(target="candidate", config=config)
        m.commit()
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Change the hostname
push_config(device["host"], device["port"], device["username"], device["password"], hostname_config)