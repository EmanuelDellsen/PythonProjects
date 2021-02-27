import requests
import json
import datetime

rpc_user = "username"
rpc_pass = "password"


def getSpecificInfo(methodCall, params):

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


def getTransactionInfo(methodCall, params, trueorfalse):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)

    payload = {
        "method": methodCall,
        "params": [params, trueorfalse],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def getRPCInfo(method):

    url = "http://%s:%s@localhost:8332" % (rpc_user, rpc_pass)
    headers = {"content-type": "application/json"}
    # Hämta hashvärdet på block nr 99
    # Tänk på att “params” är en lista med alla parametrar till anropet (här bara 1 parameter)

    payload = {
        "method": method,
        "params": [],
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response


def printMenu():
    print("\t\tBitcoin Edu Explorer")
    print("===========================================")
    print("Amount of blocks:", getRPCInfo("getblockchaininfo")["result"]["blocks"])
    print(
        "Size on the harddrive:",
        getRPCInfo("getblockchaininfo")["result"]["size_on_disk"] / 1000000,
        "MB",
    )
    print(
        "The latest block:", getRPCInfo("getblockchaininfo")["result"]["bestblockhash"]
    )
    print(
        "Mempool size:",
        getRPCInfo("getmempoolinfo")["result"]["size"],
        "transactions",
    )
    print("Connections:", getRPCInfo("getnetworkinfo")["result"]["connections"])
    print("===========================================")
    print("Menu")
    print("\t1. Show block (add block nr)")
    print("\t2. Show block (add hash nr)")
    print("\t3. Show transaction")
    print("\t4. Show outputs for address")


def getUserinput():
    userInput = input()
    return userInput


def showBlockBasedOnNr():
    print("Based on a number, which block would you like to show?")
    blockNr = getUserinput()
    blockHashNr = getSpecificInfo("getblockhash", int(blockNr))["result"]
    block = getSpecificInfo("getblock", blockHashNr)["result"]
    print("--------------------------------------------")
    print("Block hash: ", block["hash"])
    # check if previous block exists because of corner case with genesis block
    if "previousblockhash" in block:
        print("Prev. hash: ", block["previousblockhash"])
    else:
        print("Prev. hash: Does not exist, this was the first block")
    print("Merkle root: ", block["merkleroot"])
    print("Height: ", block["height"])
    print("Time: ", datetime.datetime.fromtimestamp(block["time"]))
    print("Difficulty: ", block["difficulty"])
    print("Transactions: ", len(block["tx"]))
    i = 0
    for transaction in block["tx"]:
        print("\tTx ", i, ":", transaction)
        i += 1


def showBlockBasedOnHashNr():
    print("Based on a hash number, which block would you like to show?")
    blockHashNr = getUserinput()
    block = getSpecificInfo("getblock", blockHashNr)["result"]
    print("--------------------------------------------")
    print("Block hash: ", block["hash"])
    print("Prev. hash: ", block["previousblockhash"])
    print("Merkle root: ", block["merkleroot"])
    print("Height: ", block["height"])
    print("Time: ", datetime.datetime.fromtimestamp(block["time"]))
    print("Difficulty: ", block["difficulty"])
    print("Transactions: ", len(block["tx"]))
    i = 0
    for transaction in block["tx"]:
        print("\tTx ", i, ":", transaction)
        i += 1


def showTransaction():
    print("Which transaction would you like to show more information about?")
    transactionNr = getUserinput()
    transaction = getTransactionInfo("getrawtransaction", transactionNr, True)["result"]
    print("--------------------------------------------")
    print("Txid (hash):", transaction["hash"])
    print("Part of block:", transaction["blockhash"])
    print("Inputs:", len(transaction["vin"]))
    print("Outputs:", len(transaction["vout"]))
    i = 0
    for output in transaction["vout"]:
        addresses = []
        for address in output["scriptPubKey"]["addresses"]:
            addresses.append(address)
            print("\tOutput ", i, ":", output["value"], "BTE to address:", address)
        i += 1


def showOutputsForAddress():
    print("What is the address that you would like to show outputs for?")
    btcAddress = getUserinput()
    amountOfBlocks = getRPCInfo("getblockchaininfo")["result"]["blocks"]
    # startIndex = amountOfBlocks - 2000
    # teacherStart = 46288
    # teacherEnd = 48287
    blockHashes = []
    blocks = []
    addresses = []
    # i = teacherStart
    j = 0
    for i in range(amountOfBlocks):
        blockHashNr = getSpecificInfo("getblockhash", i)["result"]
        blockHashes.append(blockHashNr)
        if i == j * 100:
            j += 1
            print("We have collected", i, "block hashes")
    j = 0

    for i in range(len(blockHashes)):
        block = getSpecificInfo("getblock", blockHashes[i])["result"]
        blocks.append(block)
        if i == j * 100:
            j += 1
            print(
                "We have stored ",
                i,
                "blocks which will be searched through for the address you entered",
            )
    k = 0
    for i in range(len(blocks)):
        if i == k * 200:
            print("Searching through block ", blocks[i]["height"])
            k += 1
        for transactionNr in blocks[i]["tx"]:
            result = getTransactionInfo("getrawtransaction", transactionNr, True)[
                "result"
            ]
            if result is not None:
                transaction = json.dumps(result)
                trans_disc = json.loads(transaction)
                if "vout" in trans_disc.keys():
                    vout = trans_disc.get("vout")
                    voutDict = vout[0]
                    if "scriptPubKey" in voutDict.keys():
                        scriptPubKey = voutDict.get("scriptPubKey")
                        if "addresses" in scriptPubKey.keys():
                            transactionAddresses = scriptPubKey.get("addresses")
                            for address in transactionAddresses:
                                k = 0
                                if address == btcAddress:
                                    print(
                                        "Block:",
                                        blocks[i]["height"],
                                        ", Tx: ",
                                        transactionNr,
                                        "\n\tOutput:",
                                        k,
                                        ":",
                                        voutDict.get("value"),
                                        "BTE",
                                    )
                                k += 1

                        else:
                            print(
                                "No addresses list in found in \n",
                                json.dumps(scriptPubKey, indent=2),
                            )
                    else:
                        print(
                            "No script pub key object found in \n",
                            json.dumps(result, indent=2),
                        )
                else:
                    print("No vout list found in \n", json.dumps(result, indent=2))


def userChoice(userInput):
    if userInput == "1":
        showBlockBasedOnNr()
    if userInput == "2":
        showBlockBasedOnHashNr()
    if userInput == "3":
        showTransaction()
    if userInput == "4":
        showOutputsForAddress()
    else:
        print("faulty input")


printMenu()
userInput = getUserinput()
userChoice(userInput)
