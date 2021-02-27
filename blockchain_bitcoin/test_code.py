# json-rpc-example.py
#
# Windows, install in command prompt: 'python -m pip install requests'
# Maybe needed, linux, install using: 'pip3 install requests'
#
# A good bitcoin.conf-file:
#
# server=1
# rpcuser=username
# rpcpassword=password
# txindex=1
#
import requests
import json

rpc_user = "emanuel"
rpc_pass = "1337"
url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
headers = {"content-type": "application/json"}
# Hämta hashvärdet på block nr 99
# Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
payload = {
    "method": "getblockhash",
    "params": [99],
}
response = requests.post(url, data=json.dumps(payload), headers=headers).json()

print(response)
print("----------------")
# Hämta info om blockchain
payload = {"method": "getblockchaininfo"}
response = requests.post(url, data=json.dumps(payload), headers=headers).json()
print("Blockchain size:", response["result"]["blocks"], "blocks")
