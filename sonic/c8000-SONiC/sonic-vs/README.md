# sonic-vs
This repo contains kvm xml and config files for launching and running a 12-node sonic-vs CLOS topology as shown in the diagram. There are two sets of router configurations, IPv6/BGP numbered and unnumbered, depending on your preference. The numbered and unnumbered folders contain their own READMEs as well.

<img src="/diagrams/sonic-vs-clos.png" width="1200">

Requirements: 1 vCPU and 4GB memory per vs. The topology in this repo has been tested on an Ubuntu 20.04 host.

Instructions:
1. acquire a sonic-vs image
2. edit the image path in the sonic kvm xml files as needed
3. define and launch kvms:
```
sudo virsh define sonic01.xml
sudo virsh start sonic01
```
4. attach to sonic VMs via the console port defined in the xml files. 
   - Example from sonic01 xml:
```
    <console type='tcp'>
      <source mode='bind' host='127.0.0.1' service='8001'/>
      <protocol type='telnet'/>
      <target type='serial' port='0'/>
    </console>
```
   - telnet to console:
```
telnet localhost 8001
```
5. default user/pw: admin/YourPaSsWoRd

6. the xml files create a mgt port attached to linux bridge virbr0, which should allocate a DHCP address for the mgt port IP. Example:
```
brmcdoug@naja:~/sonic$ telnet 0 8001
Trying 0.0.0.0...
Connected to 0.
Escape character is '^]'.

sonic login: admin
Password: 
Linux sonic 5.10.0-18-2-amd64 #1 SMP Debian 5.10.140-1 (2022-09-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Sat Apr  8 02:33:24 UTC 2023 from 192.168.122.1 on pts/0
admin@sonic:~$ show ip interfaces 
Interface    Master    IPv4 address/mask    Admin/Oper    BGP Neighbor    Neighbor IP
-----------  --------  -------------------  ------------  --------------  -------------
docker0                240.127.1.1/24       up/down       N/A             N/A
eth0                   192.168.122.116/24   up/up         N/A             N/A
lo                     127.0.0.1/16         up/up         N/A             N/A
admin@sonic:~$ 
```
7. ssh to the mgt IP then scp the config files to the sonic instance
```
scp brmcdoug@192.168.122.1:/home/brmcdoug/sonic-vs/config/sonic04/* .
```
```
admin@sonic04:~$ scp brmcdoug@192.168.122.1:/home/brmcdoug/sonic-vs/config/sonic04/* .
brmcdoug@192.168.122.1's password: 
config_db.json   100% 8426     5.5MB/s   00:00    
frr.conf        100% 2383     3.1MB/s   00:00
```
8. Replace the original config files with your new ones:
```
sudo mv config_db.json /etc/sonic/
sudo mv frr.conf /etc/sonic/frr/
```
9. reload config:
```
sudo config reload
```
Output:
```
admin@sonic04:~$ sudo config reload
Clear current config and reload config in config_db format from the default config file(s) ? [y/N]: y
Disabling container monitoring ...
Stopping SONiC target ...
Running command: /usr/local/bin/sonic-cfggen  -j /etc/sonic/init_cfg.json  -j /etc/sonic/config_db.json  --write-to-db
Running command: /usr/local/bin/db_migrator.py -o migrate
Running command: /usr/local/bin/sonic-cfggen -d -y /etc/sonic/sonic_version.yml -t /usr/share/sonic/templates/sonic-environment.j2,/etc/sonic/sonic-environment
Restarting SONiC target ...
Enabling container monitoring ...
Reloading Monit configuration ...
Reinitializing monit daemon
```
Note: config reload takes a couple minutes, and interfaces coming up takes a couple minutes more

Handy sonic CLI commands:
```
show interfaces status
show ip interfaces
show ipv6 interfaces
```
Invoke FRR CLI:
```
vtysh
```
Example:
```
admin@sonic04:~$ vtysh

Hello, this is FRRouting (version 8.4-dev).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

sonic04# 
```
