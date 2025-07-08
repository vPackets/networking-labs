from ncclient import manager

nc = manager.connect_ssh(host='10.225.251.11', username='cisco', password='cisco', device_params={"name": "iosxr"})

with open('infra-stats-get.xml', 'r') as fp:
    payload=fp.read()

reply = nc.get(filter=('subtree', payload))

print(reply.xml)


