import os
import re
import ipaddress
import subprocess
import sys

# Paths
TOPOLOGY_FILE = 'topologies/00-basic-topology.clab.yaml'
LAB_PREFIX = 'clab-basic-sp-topology'

def parse_topology(file_path):
    nodes = {}
    links = []
    mode = None
    current_node = None
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.strip().startswith('#'): continue
        if line.startswith('  nodes:'):
            mode = 'nodes'
            continue
        elif line.startswith('  links:'):
            mode = 'links'
            continue
        elif line.startswith('topology:') or line.startswith('mgmt:') or line.startswith('  kinds:'):
            mode = None
            
        if mode == 'nodes':
            m = re.match(r'^    ([a-zA-Z0-9_-]+):', line)
            if m:
                current_node = m.group(1)
                nodes[current_node] = {'name': current_node, 'exec': []}
            if current_node:
                m_kind = re.search(r'kind:\s*([a-zA-Z0-9_-]+)', line)
                if m_kind: nodes[current_node]['kind'] = m_kind.group(1)
                
                m_cfg = re.search(r'startup-config:\s*([^,\}\s]+)', line)
                if m_cfg: nodes[current_node]['startup-config'] = m_cfg.group(1)
                
                m_exec = re.search(r'-\s*(ip addr add \S+ dev \S+)', line)
                if m_exec: nodes[current_node]['exec'].append(m_exec.group(1))
                
                m_mgmt = re.search(r'mgmt-ipv4:\s*([0-9\.]+)', line)
                if m_mgmt: nodes[current_node]['mgmt-ipv4'] = m_mgmt.group(1)

        elif mode == 'links':
            m_link = re.search(r'-\s*endpoints:\s*\["([^"]+)",\s*"([^"]+)"\]', line)
            if m_link:
                links.append((m_link.group(1), m_link.group(2)))
                
    return nodes, links

def parse_configs(nodes, base_dir):
    interfaces = {}
    for node, info in nodes.items():
        interfaces[node] = {}
        kind = info.get('kind', '')
        if kind == 'linux':
            for cmd in info.get('exec', []):
                m = re.search(r'ip addr add ([0-9\.]+)/(\d+) dev (\S+)', cmd)
                if m:
                    ip = m.group(1)
                    prefix = int(m.group(2))
                    interfaces[node][m.group(3)] = {'ip': ip, 'prefix': prefix, 'mask': None}
        else:
            cfg_path = info.get('startup-config')
            if cfg_path:
                cfg_path = cfg_path.replace('../', '')
                full_path = os.path.join(base_dir, cfg_path)
                try:
                    with open(full_path, 'r') as f:
                        cfg_content = f.read()
                    intf_blocks = re.split(r'^interface ', cfg_content, flags=re.MULTILINE)[1:]
                    for block in intf_blocks:
                        lines = block.strip().split('\n')
                        intf_name = lines[0].strip()
                        ip = None
                        mask = None
                        for iline in lines[1:]:
                            iline = iline.strip()
                            if iline.startswith('ipv4 address ') or iline.startswith('ip address '):
                                parts = iline.split()
                                if len(parts) >= 4 and parts[2] != 'dhcp':
                                    ip = parts[2]
                                    mask = parts[3]
                        if ip and mask:
                            interfaces[node][intf_name] = {'ip': ip, 'mask': mask}
                except FileNotFoundError:
                    # Ignore missing files gracefully
                    pass
    return interfaces

def map_interface_name(clab_intf, kind):
    if kind == 'cisco_xrd':
        return clab_intf.replace('Gi', 'GigabitEthernet')
    elif kind == 'cisco_csr1000v':
        m = re.match(r'eth(\d+)', clab_intf)
        if m:
            idx = int(m.group(1))
            # Standard vrnetlab CSR1000v mapping: eth0 is Gi1 (mgmt), eth1 is Gi2, eth2 is Gi3
            return f"GigabitEthernet{idx + 1}"
    return clab_intf

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    topo_path = os.path.join(base_dir, TOPOLOGY_FILE)
    
    if not os.path.exists(topo_path):
        print(f"Topology file not found: {topo_path}")
        sys.exit(1)
        
    print(f"Parsing topology: {TOPOLOGY_FILE}")
    nodes, links = parse_topology(topo_path)
    
    print("Parsing configurations...")
    interfaces = parse_configs(nodes, base_dir)
    
    print("-" * 115)
    print(f"{'Endpoint 1':<25} | {'IP 1':<18} | {'Endpoint 2':<25} | {'IP 2':<18} | {'Status':<15}")
    print("-" * 115)
    
    validations = []
    all_passed = True
    
    for link in links:
        ep1, ep2 = link
        node1, intf1_clab = ep1.split(':')
        node2, intf2_clab = ep2.split(':')
        
        kind1 = nodes.get(node1, {}).get('kind', '')
        kind2 = nodes.get(node2, {}).get('kind', '')
        
        intf1_cfg = map_interface_name(intf1_clab, kind1)
        intf2_cfg = map_interface_name(intf2_clab, kind2)
        
        ip_info1 = interfaces.get(node1, {}).get(intf1_cfg)
        ip_info2 = interfaces.get(node2, {}).get(intf2_cfg)
        
        ip1_str = ip_info1['ip'] if ip_info1 else "MISSING"
        ip2_str = ip_info2['ip'] if ip_info2 else "MISSING"
        
        status = "FAIL"
        network1 = None
        network2 = None
        
        if ip_info1 and ip_info2:
            try:
                if ip_info1.get('prefix'):
                    network1 = ipaddress.IPv4Interface(f"{ip_info1['ip']}/{ip_info1['prefix']}").network
                else:
                    network1 = ipaddress.IPv4Interface(f"{ip_info1['ip']}/{ip_info1['mask']}").network
                    
                if ip_info2.get('prefix'):
                    network2 = ipaddress.IPv4Interface(f"{ip_info2['ip']}/{ip_info2['prefix']}").network
                else:
                    network2 = ipaddress.IPv4Interface(f"{ip_info2['ip']}/{ip_info2['mask']}").network
                    
                if network1 == network2:
                    status = "PASS"
                else:
                    status = "SUBNET_MISMATCH"
            except Exception:
                status = "PARSE_ERROR"
                
        if status != "PASS":
            all_passed = False
            
        print(f"{ep1:<25} | {ip1_str:<18} | {ep2:<25} | {ip2_str:<18} | {status:<15}")
        
        # Save validation object for ping checks
        if status == "PASS":
            validations.append({
                'node1': node1, 'node2': node2,
                'ip1': ip1_str, 'ip2': ip2_str,
                'kind1': kind1, 'kind2': kind2,
                'mgmt1': nodes.get(node1, {}).get('mgmt-ipv4'),
                'mgmt2': nodes.get(node2, {}).get('mgmt-ipv4'),
            })

    print("-" * 115)
    
    if not all_passed:
        print("\nWARNING: Some validation checks failed! Verify config interfaces and IPs.")
    
    # Generate ping testing script
    script_path = os.path.join(base_dir, 'ping_tests.sh')
    print(f"\nGenerating ping test script ({script_path})...")
    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("echo '====================================='\n")
        f.write("echo 'Starting Ping Tests across the topology'\n")
        f.write("echo '====================================='\n")
        
        for val in validations:
            # Ping from Node 1 to Node 2
            cmd1 = build_ping_cmd(val['node1'], val['kind1'], val['ip2'], val['mgmt1'])
            # Ping from Node 2 to Node 1
            cmd2 = build_ping_cmd(val['node2'], val['kind2'], val['ip1'], val['mgmt2'])
            
            f.write(f"\necho -e '\\n-----------------------------------------'\n")
            f.write(f"echo 'Testing {val['node1']} -> {val['node2']} ({val['ip2']})'\n")
            f.write(f"{cmd1}\n")
            f.write(f"echo 'Testing {val['node2']} -> {val['node1']} ({val['ip1']})'\n")
            f.write(f"{cmd2}\n")

    os.chmod(script_path, 0o755)
    print("Run './ping_tests.sh' to execute the reachability validation tests.")

def build_ping_cmd(node, kind, target_ip, mgmt_ip):
    if kind == 'cisco_xrd':
        return f"docker exec {LAB_PREFIX}-{node} xr_cli \"ping {target_ip} count 2\""
    elif kind == 'linux':
        return f"docker exec {LAB_PREFIX}-{node} ping -c 2 {target_ip}"
    elif kind == 'cisco_csr1000v':
        if not mgmt_ip:
            return f"echo 'No management IP for {node} to SSH into'"
        return f"sshpass -p cisco123 ssh -o StrictHostKeyChecking=no cisco@{mgmt_ip} \"ping {target_ip} repeat 2\""
    return f"echo 'Unknown kind {kind} for node {node}'"

if __name__ == "__main__":
    main()
