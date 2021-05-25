#!/usr/bin/env python3

# m7-uppgift-p3-miner.py, Thomas L, Apr 2021.
#
# Use this file as a starting point for a Python miner.
#
# Good sources:
#  https://developer.bitcoin.org/reference/rpc/index.html
#  https://en.bitcoin.it/wiki/Protocol_documentation
#  https://developer.bitcoin.org/reference/transactions.html
#  https://en.bitcoin.it/wiki/Script
#  https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki (segwit)
#
# To pack int into binary bytes. Use one of:
# - bytes()
# - struct.pack()
# - to_bytes()

import requests
import json
import struct
import binascii
import hashlib
import time
import io
from datetime import datetime
from decode_block import decodeBlock, decodeHeader, Tx

RPC_USER = "emanuel"
RPC_PASS = "1337"

# Write best block (binary data) to this file. Then, view using
# decode_block (on command line).

BEST_BLOCK_FILE = "bestblock.bin"


def writeblock(blockbin):
    print("Writing binary block data to:", BEST_BLOCK_FILE)
    with open(BEST_BLOCK_FILE, "wb") as f:
        f.write(blockbin)


# Make RPC call to local node


def do_rpc(method, *args):
    url = "http://%s:%s@localhost:8332" % (RPC_USER, RPC_PASS)
    headers = {"content-type": "application/json"}
    payload = {
        "method": method,
        "params": list(args),
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    # HTTP status codes starting with 4xx indicate developer errors
    if r.status_code >= 400 and r.status_code < 500:
        r.raise_for_status()
    r = r.json()
    if r.get("error"):
        print("RPC API error:", r["error"])
    return r["result"]


def getBlockHeader(version, prevBlockHash, merkleRoot, time, bits, nonce):

    print(type(version))
    print(type(prevBlockHash))
    print(type(merkleRoot))
    print(type(time))
    print(type(bits))
    print(type(nonce))

    finalStringHeader = (
        str(version) + prevBlockHash + merkleRoot + str(time) + str(bits) + str(nonce)
    )
    print("Final string header ->", finalStringHeader)
    print(int(finalStringHeader, 16))
    return finalStringHeader.decode("hex")


def calculateHash(
    merkleRoot,
    prevBlockHash,
    timeStamp,
    difficultyBits,
    nonce,
    maxAttempts=10000000,
    startNonce=0,
):

    complete = False
    nonce = startNonce
    header = None
    i = 0

    while i <= maxAttempts:
        block = getBlockHeader(
            "00000020", prevBlockHash, merkleRoot, timeStamp, difficultyBits, nonce
        )
        print("inside while", block)
        blockHashNr = blockHash(block)
        target = calculateTarget(difficultyBits)

        if blockHashNr < target:
            complete = True
            break

        nonce += 1

    print("block->", block)
    print("blockhash->", blockHashNr)


def calculateTarget(difficultyBits):

    exponent = difficultyBits >> 24
    mask = difficultyBits & 0xFFFFFF
    targetHexString = "%064x" % (mask * (1 << (8 * (exponent - 3))))
    targetString = binascii.unhexlify(targetHexString)
    return targetString


def blockHash(block):
    print("inside blockhash", block, type(block))
    blockHash = hashlib.sha256(hashlib.sha256(block).digest()).digest()[::-1]
    return blockHash


# def createCoinBase()


# Start of actual mining code

onlineAddress = "bc1qqry6n26uhxhsrevrlfvsn5rfupvzw2tzdxqc8r"
blocktemp = do_rpc("getblocktemplate", {"rules": ["segwit"]})

# block = do_rpc(
#    "getrawtransaction",
#    ["f323e772a3766b3a6beb0a389bb10a3ff2d99ac7bb9e0216b02fd4435a501265", "1"],
# )
# print(block)

blockheight = blocktemp["height"]
prevBlockHash = blocktemp["previousblockhash"][::-1]

print(json.dumps(blocktemp, sort_keys=True, indent=2))

# my address in hex 00c9a9ab5cb9af01e583fa5909d069e058272962
# faketarget = b'000000ff00000000000000000000000000000000000000000000000000000000'

# Create coinbase (non segwit version)
# 020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff0703ee200202ef22ffffffff0200f2052a0100000016001400c9a9ab5cb9af01e583fa5909d069e0582729620000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000
#
# 02000000
# 0001
# 01
# 0000000000000000000000000000000000000000000000000000000000000000
# ffffffff
# 0703ee200202ef22
# ffffffff
# 0200f2052a0100000016001400c9a9ab5cb9af01e583fa5909d069e0582729620000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf9
# 0120000000000000000000000000000000000000000000000000000000000000000000000000
# get old block and get all info getrawtransaction
# 000000001761dbb8154669b98e62b6132eb24c6ca1fa6e309a24e7fad2f0c60a
# reverse engineering
# get block for blockheader
version = 2
address = "00c9a9ab5cb9af01e583fa5909d069e058272962"
nonce = 100000000

transVersion = "02000000"
txflag = "0001"
txAmount = "01"
coinbaseId = "0000000000000000000000000000000000000000000000000000000000000000"  # 64
output = "ffffffff"
blockheightByte = struct.pack("<I", blockheight)[0:3]
scriptBytes = len(blockheightByte)
scriptSig = binascii.hexlify(blockheightByte) + binascii.hexlify(b"westfall is awesome")
scriptSigWithString = "1703" + scriptSig.decode()
print("scriptsig->", scriptSigWithString)
sequence = "ffffffff"

finalStringInputWithoutSegwit = (
    transVersion + txAmount + coinbaseId + output + scriptSigWithString + sequence
)

print(finalStringInputWithoutSegwit)
locktime = "00000000"
finalVersionOutput = "0200f2052a0100000016001400c9a9ab5cb9af01e583fa5909d069e0582729620000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf9"
finalVersionTransInOutWithoutSegwit = (
    finalStringInputWithoutSegwit + finalVersionOutput + locktime
)
print(
    "Final transaction version without SegWit: ->", finalVersionTransInOutWithoutSegwit
)

tx_class = Tx(io.BytesIO(binascii.unhexlify(finalVersionTransInOutWithoutSegwit)))
tx_class.toString()

segwit = "01200000000000000000000000000000000000000000000000000000000000000000"
finalStringInputWithSegwit = (
    transVersion
    + txflag
    + txAmount
    + coinbaseId
    + output
    + scriptSigWithString
    + sequence
)
finalVersionTransSegwit = (
    finalStringInputWithSegwit + finalVersionOutput + segwit + locktime
)

tx_class_segwit = Tx(io.BytesIO(binascii.unhexlify(finalVersionTransSegwit)))
tx_class_segwit.toString()

headerVersion = "00000020"
prevBlockHashHeader = binascii.unhexlify(prevBlockHash)[::-1]
print(prevBlockHashHeader)

txid = binascii.unhexlify(finalVersionTransInOutWithoutSegwit)
txid = hashlib.sha256(txid).digest()
txid = hashlib.sha256(txid).digest()
txidHex = txid.hex()
print("txidHex->", txidHex)

blockVersionInt = "00000020"

blockTime = blocktemp["curtime"]
print(blockTime)
blockTime = struct.pack("<I", blockTime).hex()
print(blockTime)

bits = blocktemp["bits"]
bitsInt = int(bits, 16)
bitsLittleEnd = struct.pack("<I", bitsInt).hex()
print("after struct.pack ->", bitsLittleEnd)

target = blocktemp["target"]
maxAttempts = 10000000

# print("blockVersionInt", blockVersionInt, len(blockVersionInt))
# print("prevBlockHashlen", prevBlockHash, len(prevBlockHash))
# print("blockTime", str(blockTime), len(str(blockTime)))
# print("bitsLittleEndInt", str(bitsLittleEnd), len(str(bitsLittleEnd)))


finalString = (
    blockVersionInt + prevBlockHash + txidHex + str(blockTime) + str(bitsLittleEnd)
)
nonce = 0
printInt = 100000
bestHash = ""
prevHash = ""
belowTargetHashFound = False
optimalHash = "Did not manage to be better then target from getblocktemplate"
finalStringUnhex = ""
nonceTemp = ""
bestHeader = ""

for nonce in range(maxAttempts):
    nonceTemp = struct.pack("<I", nonce)
    finalStringUnhex = binascii.unhexlify(finalString + nonceTemp.hex())
    compareHash = hashlib.sha256(hashlib.sha256(finalStringUnhex).digest()).digest()[
        ::-1
    ]
    compareHashHex = binascii.hexlify(compareHash)
    currentHash = compareHashHex.decode()

    if nonce == 0:
        bestHash = currentHash
        print("First hash generated ->", bestHash)

    if nonce % printInt == 0:
        print("Best hash after", nonce, "iterations ->", bestHash)

    if currentHash < target:
        optimalHash = bestHash
        print("Hash under target found ->", optimalHash)
        belowTargetHashFound = True
    if currentHash < bestHash:
        bestHash = currentHash
        print("Newly found best hash after", nonce, "iterations ->", bestHash)
        bestHeader = finalStringUnhex.hex()

    prevHash = currentHash

print("Best hash found through", maxAttempts, "hashing iterations ->", bestHash)
print("We ran ", nonce, "iterations")
print("Hash under target ->", optimalHash)
print("txidHex ->", txidHex)
print("final string hex ->", bestHeader)

finalBlock = bestHeader + "01" + finalVersionTransSegwit
bestBlockBin = binascii.unhexlify(finalBlock)
print("Final block in hex ->", finalBlock)

writeblock(bestBlockBin)
print(decodeBlock(bestBlockBin))
print(binascii.hexlify(bestBlockBin))

# Example: write existing block 34500:
block34500 = "\
000000207e1591692154db00767cfc1cdd4586daf52c718aa20886f1018aa40c000000003c209bdf\
d413e385715ac33d390ae776e4b9268bb20e892bb7a807ad214902caff33f95b53d6001d1180683b\
01010000000001010000000000000000000000000000000000000000000000000000000000000000\
ffffffff0403c48600ffffffff0200f2052a010000001976a914699083774136dc464fcdcedefbb6\
5f8af79c873288ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c\
690689799962b48bebd836974e8cf901200000000000000000000000000000000000000000000000\
00000000000000000000000000"
# print(decodeBlock(binascii.unhexlify(block34500)))

# When valid block found:


blockhex = (
    bestBlockBin.hex()  # This is an already existing block, should give error "duplicate"
)
# r = do_rpc('submitblock', blockhex)
# print('API, submitblock, response: ', r)
