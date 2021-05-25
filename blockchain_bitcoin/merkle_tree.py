import hashlib
import binascii


merkleRootBlock2254 = "73bdc1c3bda40540f5a716a29634061fc9791e62d5a22f7c48197c321b96df2b"

block2254Hashes = [
    "68C79026FBDEC55F94518C504439B1D7DBE35A287EB0B24744143CFC3A224464",
    "D66E64DF7A9B855B7AB7660A0C95BE42A74981C5A01BB722109B2B4CECFED006",
]

merkleRootBlock2257 = "8a8f188b87cb1bb73425b26803e2497649c02157b2106f43ecc31f5f621381d3"

block2257Hashes = [
    "5F37CF8D6C81DAF9A0F5C3B4E6EA411E1D9E56FF744FC713E48DD3C7DBE9B711",
    "6E2EC0559E75DBF5E9976FFF119CBC8265F9C8033C827062F74ABEA9F854B011",
    "298CDCD5EEB3D1D90E7B288B3B84297D787BB2FE2CC7B26F6A10D1B613D39B94",
]


def hashCalc(hash1, hash2):
    print(type(hash1), type(hash2))
    turnedHash1 = binascii.unhexlify(hash1)[::-1]
    print(turnedHash1, "turned hash 1")
    turnedHash2 = binascii.unhexlify(hash2)[::-1]
    print(turnedHash2, "turned hash 2")

    concatinatedHash = turnedHash1 + turnedHash2
    print(concatinatedHash, "after concatination")
    firstSHA = hashlib.sha256(concatinatedHash).digest()
    print(firstSHA, "first SHA and digest")

    finalSHA = hashlib.sha256(firstSHA).digest()
    print(finalSHA, "final SHA and digest")
    return binascii.hexlify(finalSHA[::-1])


def merkleCalculator(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList) - 1, 2):
        newHashList.append(hashCalc(hashList[i], hashList[i + 1]))
    if len(hashList) % 2 == 1:  # odd, hash last item twice
        newHashList.append(hashCalc(hashList[-1], hashList[-1]))
    return merkleCalculator(newHashList)
    # secondSha = hashlib.sha256(firstSHA.encode)

    # print(secondSha)


CalculatedMerkleRootBlock2257 = str(merkleCalculator(block2257Hashes), "utf-8")
CalculatedMerkleRootBlock2254 = str(merkleCalculator(block2254Hashes), "utf-8")

print("Calculated MerkleRoot for block 2257 : " + CalculatedMerkleRootBlock2257)
print("Calculated MerkleRoot for block 2254 : " + CalculatedMerkleRootBlock2254)

if CalculatedMerkleRootBlock2257 == merkleRootBlock2257:
    print("The calculation of 2257 matches the provided one")
else:
    print("merkle roots do not match for block 2257")

if CalculatedMerkleRootBlock2254 == merkleRootBlock2254:
    print("The calculation of 2254 matches the provided one")
else:
    print("merkle roots do not match for block 2254")
