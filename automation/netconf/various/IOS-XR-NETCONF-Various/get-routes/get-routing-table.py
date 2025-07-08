from ncclient import manager

nc = manager.connect_ssh(host='10.225.251.6', username='cisco', password='cisco', device_params={"name": "iosxr"})

with open('routes-get-ipv4-unicast.xml', 'r') as fp:
    payload=fp.read()

reply = nc.get(filter=('subtree', payload))

print(reply.xml)


