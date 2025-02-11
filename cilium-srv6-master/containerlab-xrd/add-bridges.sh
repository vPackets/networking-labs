#!/bin/bash

 brctl addbr xrd03-host
 brctl addbr xrd04-host
 brctl addbr xrd14-host
 brctl addbr xrd15-host
 brctl addbr xrd22-host
 brctl addbr xrd23-host
 brctl addbr xrd24-host

 ip link set up xrd03-host
 ip link set up xrd04-host
 ip link set up xrd14-host
 ip link set up xrd15-host
 ip link set up xrd22-host
 ip link set up xrd23-host
 ip link set up xrd24-host
