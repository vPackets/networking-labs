# Basic eBGP Lab Setup Between Two Routers

## Overview
This lab sets up a basic external BGP (eBGP) peering between two routers `Cisco8201-1` and `Cisco8201-2`, facilitating the exchange of routing information.

## Router Configurations

### Cisco8201-1 Configuration

#### Basic Setup
- **Hostname:** Cisco8201-1
- **Logging:** Console logging is disabled.

#### Interfaces
- **Loopback0:**
  - IP Address: 10.1.1.1/32
- **FourHundredGigE0/0/0/0:**
  - IP Address: 192.0.2.1/24
  - Status: No shutdown (enabled)
- **FourHundredGigE0/0/0/1:**
  - IP Address: 10.0.0.1/24
  - Status: No shutdown (enabled)

#### BGP Configuration
- **Local AS:** 65000
- **Router ID:** 1.1.1.1
- **Address Family:** IPv4 Unicast
- **Advertised Network:** 192.0.2.0/24
- **eBGP Neighbor:** 10.0.0.2 (AS 65100)
- **Route Policy:** ALLOW (for both inbound and outbound routes)

### Cisco8201-2 Configuration

#### Basic Setup
- **Hostname:** Cisco8201-2
- **Logging:** Console logging is disabled.

#### Interfaces
- **Loopback0:**
  - IP Address: 10.2.2.2/32
- **FourHundredGigE0/0/0/0:**
  - IP Address: 203.0.113.1/24
  - Status: No shutdown (enabled)
- **FourHundredGigE0/0/0/1:**
  - IP Address: 10.0.0.2/24
  - Status: No shutdown (enabled)

#### BGP Configuration
- **Local AS:** 65100
- **Router ID:** 2.2.2.2
- **Address Family:** IPv4 Unicast
- **Advertised Network:** 203.0.113.0/24
- **eBGP Neighbor:** 10.0.0.1 (AS 65000)
- **Route Policy:** ALLOW (for both inbound and outbound routes)

## Lab Objective

The primary objective of this lab is to establish eBGP peering between `Cisco8201-1` and `Cisco8201-2`, ensuring they can exchange routing information. This setup provides a basic understanding of inter-AS routing and BGP operations in a controlled lab environment.




