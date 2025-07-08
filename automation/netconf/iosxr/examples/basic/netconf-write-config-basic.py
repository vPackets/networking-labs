# Basic script that pushes BGP configuration to 2 routers
# Each configuration is embedeed into a router_configs dictionnary
# a function is created to simplify the code


from ncclient import manager
import xml.dom.minidom

# Router connection details for both routers
devices = [
    {
        "host": "clab-ebgp-c8k-cisco8201-1",
        "port": 830,
        "username": "cisco",
        "password": "cisco123"
    },
    {
        "host": "clab-ebgp-c8k-cisco8201-2",
        "port": 830,
        "username": "cisco",
        "password": "cisco123"
    }
]

# New hostname configurations for both routers
router_configs = [
    
    # Configuration for the first router
    '''<config 
	xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
    xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
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
					<as>65000</as>
					<bgp-running></bgp-running>
					<default-vrf>
						<global>
							<router-id>1.1.1.1</router-id>
							<global-afs>
								<global-af>
									<af-name>ipv4-unicast</af-name>
									<enable></enable>
									<sourced-networks>
										<sourced-network>
											<network-addr>192.0.2.0</network-addr>
											<network-prefix>24</network-prefix>
										</sourced-network>
									</sourced-networks>
								</global-af>
							</global-afs>
						</global>
						<bgp-entity>
							<neighbors>
								<neighbor>
									<neighbor-address>10.0.0.2</neighbor-address>
									<create></create>
									<remote-as>
										<as-xx>0</as-xx>
										<as-yy>65100</as-yy>
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
						<address>10.1.1.1</address>
						<netmask>255.255.255.255</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
		<interface-configuration>
            <shutdown xc:operation="remove"/>
			<active>act</active>
			<interface-name>FourHundredGigE0/0/0/0</interface-name>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
				<addresses>
					<primary>
						<address>192.0.2.1</address>
						<netmask>255.255.255.0</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
		<interface-configuration>
            <shutdown xc:operation="remove"/>
			<active>act</active>
			<interface-name>FourHundredGigE0/0/0/1</interface-name>
			<ipv4-network
				xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
				<addresses>
					<primary>
						<address>10.0.0.1</address>
						<netmask>255.255.255.0</netmask>
					</primary>
				</addresses>
			</ipv4-network>
		</interface-configuration>
	</interface-configurations>
</config>''', 




    # Configuration for the second router
    '''<config
	xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
    xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
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
            <shutdown xc:operation="remove"/>
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
            <shutdown xc:operation="remove"/>
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
'''   # Configuration for the second router
]

# Function to change the configuration
def write_config(device, config):
    with manager.connect(host=device["host"], port=device["port"], username=device["username"], password=device["password"], hostkey_verify=False) as m:
        netconf_response = m.edit_config(target="candidate", config=config)
        m.commit()
        print(xml.dom.minidom.parseString(netconf_response.xml).toprettyxml())

# Apply the configurations to each device
for device, config in zip(devices, router_configs):
    write_config(device, config)
