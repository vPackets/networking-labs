from flask import Flask, request, jsonify, send_from_directory
from ncclient import manager
import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

device = {
    "address": "198.18.128.3",
    "netconf_port": 830,
    "username": "netconf",
    "password": "C1sco12345!"
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/provision_vlan', methods=['POST'])
def provision_vlan():
    data = request.json
    vlan_id = data.get("vlan_id")
    vlan_name = data.get("vlan_name")

    if not vlan_id or not vlan_name:
        return jsonify({"message": "Missing VLAN ID or Name"}), 400

    # Build the XML you want to push
    add_vlan = f"""
    <config>
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
    </config>
    """

    try:
        with manager.connect(host=device["address"],
                              port=device["netconf_port"],
                              username=device["username"],
                              password=device["password"],
                              hostkey_verify=False) as m:
            # Send the config
            edit_response = m.edit_config(target="running", config=add_vlan)

            # Commit (optional depending on platform)
            commit_response = m.commit()

        # Prepare what to send back to the frontend
        return jsonify({
            "message": f"Provisioned VLAN {vlan_id} successfully.",
            "sent_xml": add_vlan.strip(),
            "edit_reply": str(edit_response),
            "commit_reply": str(commit_response)
        })
    except Exception as e:
        print(e)
        return jsonify({
            "message": f"Failed to provision VLAN {vlan_id}.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)