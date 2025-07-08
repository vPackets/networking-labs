from flask import Flask, request, jsonify, render_template
from xml.dom.minidom import parseString
import html
from ncclient import manager

app = Flask(__name__)

device = {
    "address": "198.18.128.3",
    "netconf_port": 830,
    "username": "netconf",
    "password": "C1sco12345!"
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/provision_vlan', methods=['POST'])
def provision_vlan():
    data = request.get_json()
    vlan_id = data.get("vlan_id")
    vlan_name = data.get("vlan_name")

    add_vlan = f"""
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
      <bd-items>
        <bd-items>
          <BD-list>
            <fabEncap>vlan-{vlan_id}</fabEncap>
            <name>{vlan_name}</name>
          </BD-list>
        </bd-items>
      </bd-items>
    </System>
    """

    sent_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config>
      {add_vlan}
    </config>
  </edit-config>
</rpc>"""

    try:
        with manager.connect(
            host=device["address"],
            port=device["netconf_port"],
            username=device["username"],
            password=device["password"],
            hostkey_verify=False
        ) as m:
            edit_response = m.edit_config(target="running", config=f"<config>{add_vlan}</config>")
            commit_response = m.commit()

            # Prettify and escape XML responses
            sent_xml_pretty = html.escape(parseString(sent_xml).toprettyxml(indent="  "))
            edit_reply_pretty = html.escape(parseString(edit_response.xml).toprettyxml(indent="  "))
            commit_reply_pretty = html.escape(parseString(commit_response.xml).toprettyxml(indent="  "))

            # Compose final response HTML
            status_message = f"""
<b>Status:</b> Provisioned VLAN {vlan_id} successfully.<br><br>
<b>Sent XML:</b><br><pre>{sent_xml_pretty}</pre><br>
<b>Edit Reply:</b><br><pre>{edit_reply_pretty}</pre><br>
<b>Commit Reply:</b><br><pre>{commit_reply_pretty}</pre>
"""
            return jsonify({"message": status_message})

    except Exception as e:
        return jsonify({
            "message": f"<b>Error:</b> {html.escape(str(e))}",
        }), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)
    