import secrets
import hashlib
import binascii
import base58
import requests
import json
from pycoin.ecdsa.secp256k1 import secp256k1_generator, _r
from pycoin.encoding import b58

rpc_user = "emanuel"
rpc_pass = "1337"


def generatePrivateKeyHex(privateKey):
    bitsHexaDecimal = hex(privateKey)
    privateKeyHex = bitsHexaDecimal[2:]
    print("Private key hex: ", privateKeyHex)
    return privateKeyHex


def generatePrivateKey():
    bits = secrets.randbits(256)
    bitsHexaDecimal = hex(bits)
    print("private key numbers: ", bits)
    return bits


def generatePrivateKeyWifFormat(privateKey):
    k_hex = "%064x" % privateKey
    privateKeyWif = "80" + k_hex + "01"

    checksum = hashlib.sha256(
        hashlib.sha256(binascii.unhexlify(privateKeyWif)).digest()
    ).hexdigest()[:8]
    privateKeyWif = privateKeyWif + checksum
    privateKeyWif = b58.b2a_base58(binascii.unhexlify(privateKeyWif))
    print("private key wif: ", privateKeyWif)

    return privateKeyWif


def generatePublicKey(privateKey):
    publicKey = privateKey * secp256k1_generator
    print("public key: ", publicKey)
    return publicKey


# code borrowed from https://colab.research.google.com/drive/1Eb4bNE8HU9sULhEqEXCWwuQ9UkG-xsm4
def uncompressedPubKey(pubkey):
    x = "%064x" % pubkey[0]
    y = "%064x" % pubkey[1]
    uncompPubKey = "04" + x + y
    print("uncompressed public key", uncompPubKey)
    return uncompPubKey


# code borrowed from https://colab.research.google.com/drive/1Eb4bNE8HU9sULhEqEXCWwuQ9UkG-xsm4


def compressedPubKey(pubkey):
    x = "%064x" % pubkey[0]
    y = "%064x" % pubkey[1]
    compressedPubKey = ("02" if pubkey[1] % 2 == 0 else "03") + x
    print("compressed public key: ", compressedPubKey)
    return compressedPubKey


def generateBitcoinAddress(key):
    btcAddress = hashlib.new(
        "ripemd160", hashlib.sha256(binascii.unhexlify(key)).digest()
    ).hexdigest()
    return btcAddress


def convertHash160ToBtcAddress(hash160Address):
    sha256Input = "00" + hash160Address
    checksum = hashlib.sha256(
        hashlib.sha256(binascii.unhexlify(sha256Input)).digest()
    ).hexdigest()[:8]
    output = sha256Input + checksum
    btcAddress = b58.b2a_base58(binascii.unhexlify(output))
    return btcAddress


def getSpecificInfo(methodCall):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
    payload = {
        "method": methodCall,
        "params": [],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def getWalletInfo(methodCall, params):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
    payload = {
        "method": methodCall,
        "params": [params],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def createRawTrans(methodCall, params1, params2):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
    payload = {
        "method": methodCall,
        "params": [params1, params2],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

    return response


def impPubKey(methodCall, param1, param2, param3):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
    payload = {
        "method": methodCall,
        "params": [param1, param2, param3],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def sendToAddress(methodCall, param1, param2):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)
    payload = {
        "method": methodCall,
        "params": [param1, param2],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def getUserinput():
    userInput = input()
    return userInput


def printMenu():
    privateKey = generatePrivateKey()
    privateKeyWif = generatePrivateKeyWifFormat(privateKey)
    privateKeyHex = generatePrivateKeyHex(privateKey)
    pubkey = generatePublicKey(privateKey)
    compPubkey = compressedPubKey(pubkey)
    uncompPubkey = uncompressedPubKey(pubkey)

    hash160CompAddress = generateBitcoinAddress(compPubkey)
    hash160UnCompAddress = generateBitcoinAddress(uncompPubkey)

    compBtcAddress = convertHash160ToBtcAddress(hash160CompAddress)
    uncompBtcAddress = convertHash160ToBtcAddress(hash160UnCompAddress)
    print("Bitcoin address from compressed public key: ", compBtcAddress)
    print("Bitcoin address from uncompressed public key: ", uncompBtcAddress)

    result = sendToAddress("sendtoaddress", uncompBtcAddress, 0.001)["result"]

    # print(result)
    # print(getSpecificInfo("listunspent")["result"])
    txid = result
    transParams = [
        [
            {
                "txid": txid,
                "vout": 0,
            }
        ],
        {compBtcAddress: 0.000999},
    ]

    rawId = createRawTrans("createrawtransaction", transParams[0], transParams[1])[
        "result"
    ]
    # print(rawId)
    signedTrans = getWalletInfo("signrawtransaction", rawId)["result"]
    # print(signedTrans)
    sendRes = sendToAddress("sendrawtransaction", signedTrans["hex"], True)
    print("Result of sendrawtransaction: ", sendRes)
    rawmempool = getSpecificInfo("getrawmempool")["result"]
    print(
        "Result of getrawmempool where you can see the 'rawtransaction' added which was sent above: ",
        rawmempool,
    )
    print("\t\tSecond assignment")


printMenu()

#
