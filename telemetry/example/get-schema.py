from ncclient import manager
import re
from subprocess import Popen, PIPE, STDOUT

# Establish a connection
xr = manager.connect(host='198.18.128.7', port=830, username='admin', password='C1sco12345',
                     allow_agent=False,
                     look_for_keys=False,
                     hostkey_verify=False,
                     unknown_host_cb=True)

# Get schema
oc = xr.get_schema('Cisco-IOS-XR-telemetry-model-driven-cfg')

# Initialize Popen with pyang command
p = Popen(['pyang', '-f', 'tree'], stdout=PIPE, stdin=PIPE, stderr=PIPE)

# Communicate with subprocess, ensure input is encoded to bytes
output, err = p.communicate(input=oc.data.encode())

# Print the output, decode from bytes to string
print(output.decode())


"""

module: Cisco-IOS-XR-telemetry-model-driven-cfg
  x--rw telemetry-model-driven
     +--rw sensor-groups
     |  +--rw sensor-group* [sensor-group-identifier]
     |     +--rw sensor-paths
     |     |  +--rw sensor-path* [telemetry-sensor-path]
     |     |     +--rw telemetry-sensor-path    string
     |     +--rw sensor-group-identifier    xr:Cisco-ios-xr-string
     +--rw subscriptions
     |  +--rw subscription* [subscription-identifier]
     |     +--rw sensor-profiles
     |     |  +--rw sensor-profile* [sensorgroupid]
     |     |     +--rw strict-timer?         empty
     |     |     +--rw sample-interval?      uint32
     |     |     +--rw mode?                 Subscription-mode
     |     |     +--rw heartbeat-always?     empty
     |     |     +--rw heartbeat-interval?   uint32
     |     |     +--rw sensorgroupid         xr:Cisco-ios-xr-string
     |     +--rw destination-profiles
     |     |  +--rw destination-profile* [destination-id]
     |     |     +--rw destination-id    xr:Cisco-ios-xr-string
     |     +--rw source-qos-marking?        Mdt-dscp-value
     |     +--rw source-interface?          xr:Interface-name
     |     +--rw subscription-identifier    xr:Cisco-ios-xr-string
     +--rw gnmi
     |  +--rw bundling!
     |  |  +--rw enable?   empty
     |  |  +--rw size?     uint32
     |  +--rw heartbeat-always?   empty
     +--rw include
     |  +--rw empty
     |  |  +--rw values?   empty
     |  +--rw select-leaves-on-events?   empty
     +--rw destination-groups
     |  +--rw destination-group* [destination-id]
     |     +--rw ipv6-destinations
     |     |  +--rw ipv6-destination* [ipv6-address destination-port]
     |     |     +--rw ipv6-address        inet:ipv6-address-no-zone
     |     |     +--rw destination-port    xr:Cisco-ios-xr-port-number
     |     |     +--rw encoding?           Encode-type
     |     |     +--rw protocol!
     |     |        +--rw protocol        Proto-type
     |     |        +--rw tls-hostname?   xr:Cisco-ios-xr-string
     |     |        +--rw no-tls?         empty
     |     |        +--rw packetsize?     uint32
     |     |        +--rw compression?    Mdt-compression
     |     +--rw ipv4-destinations
     |     |  +--rw ipv4-destination* [ipv4-address destination-port]
     |     |     +--rw ipv4-address        inet:ipv4-address-no-zone
     |     |     +--rw destination-port    xr:Cisco-ios-xr-port-number
     |     |     +--rw encoding?           Encode-type
     |     |     +--rw protocol!
     |     |        +--rw protocol        Proto-type
     |     |        +--rw tls-hostname?   xr:Cisco-ios-xr-string
     |     |        +--rw no-tls?         empty
     |     |        +--rw packetsize?     uint32
     |     |        +--rw compression?    Mdt-compression
     |     +--rw destinations
     |     |  +--rw destination* [address port]
     |     |     +--rw address-family?   Address-family
     |     |     +--rw address           xr:Cisco-ios-xr-string
     |     |     +--rw port              xr:Cisco-ios-xr-port-number
     |     |     +--rw encoding?         Encode-type
     |     |     +--rw protocol!
     |     |        +--rw protocol        Proto-type
     |     |        +--rw tls-hostname?   xr:Cisco-ios-xr-string
     |     |        +--rw no-tls?         empty
     |     |        +--rw packetsize?     uint32
     |     |        +--rw compression?    Mdt-compression
     |     +--rw vrf?                 xr:Cisco-ios-xr-string
     |     +--rw destination-id       xr:Cisco-ios-xr-string
     +--rw gnmi-target-defined
     |  +--rw minimum-cadence?   uint32
     |  +--rw cadence-factor?    uint32
     +--rw strict-timer?              empty
     +--rw enable?                    empty
     +--rw max-sensor-paths?          uint32
     +--rw max-containers-per-path?   uint32
     +--rw tcp-send-timeout?          uint32
"""