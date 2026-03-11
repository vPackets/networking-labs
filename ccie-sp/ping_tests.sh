#!/bin/bash
echo '====================================='
echo 'Starting Ping Tests across the topology'
echo '====================================='

echo -e '\n-----------------------------------------'
echo 'Testing PE1 -> P3 (10.3.11.3)'
docker exec clab-basic-sp-topology-PE1 xr_cli "ping 10.3.11.3 count 2"
echo 'Testing P3 -> PE1 (10.3.11.11)'
docker exec clab-basic-sp-topology-P3 xr_cli "ping 10.3.11.11 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing P3 -> PE2 (10.3.12.12)'
docker exec clab-basic-sp-topology-P3 xr_cli "ping 10.3.12.12 count 2"
echo 'Testing PE2 -> P3 (10.3.12.3)'
docker exec clab-basic-sp-topology-PE2 xr_cli "ping 10.3.12.3 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing PE1 -> P4 (10.4.11.4)'
docker exec clab-basic-sp-topology-PE1 xr_cli "ping 10.4.11.4 count 2"
echo 'Testing P4 -> PE1 (10.4.11.11)'
docker exec clab-basic-sp-topology-P4 xr_cli "ping 10.4.11.11 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing P4 -> P5 (10.4.5.5)'
docker exec clab-basic-sp-topology-P4 xr_cli "ping 10.4.5.5 count 2"
echo 'Testing P5 -> P4 (10.4.5.4)'
docker exec clab-basic-sp-topology-P5 xr_cli "ping 10.4.5.4 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing P5 -> P6 (10.5.6.6)'
docker exec clab-basic-sp-topology-P5 xr_cli "ping 10.5.6.6 count 2"
echo 'Testing P6 -> P5 (10.5.6.5)'
docker exec clab-basic-sp-topology-P6 xr_cli "ping 10.5.6.5 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing P6 -> PE2 (10.6.12.12)'
docker exec clab-basic-sp-topology-P6 xr_cli "ping 10.6.12.12 count 2"
echo 'Testing PE2 -> P6 (10.6.12.6)'
docker exec clab-basic-sp-topology-PE2 xr_cli "ping 10.6.12.6 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing RR1 -> P4 (10.4.101.4)'
docker exec clab-basic-sp-topology-RR1 xr_cli "ping 10.4.101.4 count 2"
echo 'Testing P4 -> RR1 (10.4.101.101)'
docker exec clab-basic-sp-topology-P4 xr_cli "ping 10.4.101.101 count 2"

echo -e '\n-----------------------------------------'
echo 'Testing RR2 -> P6 (10.6.102.6)'
docker exec clab-basic-sp-topology-RR2 xr_cli "ping 10.6.102.6 count 2"
echo 'Testing P6 -> RR2 (10.6.102.102)'
docker exec clab-basic-sp-topology-P6 xr_cli "ping 10.6.102.102 count 2"
