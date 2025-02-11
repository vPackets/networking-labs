#!/bin/bash

 ip link set down xrd03-host
 ip link set down xrd04-host
 ip link set down xrd22-host
 ip link set down xrd14-host
 ip link set down xrd15-host

 brctl delbr xrd03-host
 brctl delbr xrd04-host
 brctl delbr xrd22-host
 brctl delbr xrd14-host
 brctl delbr xrd15-host

