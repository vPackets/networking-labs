This script can be used to test adding and deleting config using netconf over time. 

The script creates a user defined number of VRFs and sub-interfaces within those VRFs using netconf.

It then deletes the VRFs and sub-interfaces and repeats this process over time.

To run the script you can use the following syntax:

python3 vrf_subint.py <ip_address> <username> <password> <start_subinterface_number> <end_subinterface_number>

The example below will create 10 VRFs and 10 sub-interfaces starting at number 101 to 110:

python3 vrf_subint.py 10.225.251.38 cisco cisco 101 110

This script requires the ncclient python module
