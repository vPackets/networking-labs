from ncclient import manager

with manager.connect(host="10.225.251.11", port=830, username="cisco", password="cisco", hostkey_verify=False, device_params={'name':'iosxr'}) as m:
    c = m.get_config(source='running').data_xml
    with open("%s.xml" % "host", 'w') as f:
        f.write(c)
