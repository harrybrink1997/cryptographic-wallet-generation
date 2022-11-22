import hashlib
import binascii
import hmac
import math, os, sys
from mnemonic import Mnemonic
import ecdsa
import base58
from Crypto.Hash import RIPEMD160



def generate256BitMnemonicPhrase(entropy):
  f = open("./bip39WordList.txt")
  bip39WordList = f.read()
  bip39WordList = bip39WordList.split("\n")

  entropyHex = entropy.hex()
  hexCheckSum = hashlib.sha256(entropy).hexdigest()
  firstEightBitsHex = hexCheckSum[0:2]

  mnemonicHex = entropyHex + firstEightBitsHex

  walletSeedBinary = format(int(mnemonicHex, 16), '0264b')

  mnemonicPhrase = []

  for i in range(0, len(walletSeedBinary), 11):
    mnemonicWordBinary = walletSeedBinary[i:i+11]
    mnemonicWordInteger = int(mnemonicWordBinary, 2)
    mnemonicWordString = bip39WordList[mnemonicWordInteger]
    mnemonicPhrase.append(mnemonicWordString)

  f.close()

  return {
    "mnemonicPhrase": " ".join(mnemonicPhrase),
    "mnemonicHex": mnemonicHex
  }

def generateSeed(password, passphrase = ""):
  
  passwordBytes = password.encode('utf-8')
  passphraseBytes = ('mnemonic' + passphrase).encode('utf-8')

  seed = hashlib.pbkdf2_hmac(
    'sha512',
    passwordBytes,
    passphraseBytes,
    2048
  )
  return seed[:64]

def generateMasterXprv(seed):

  seed = hmac.new(b"Bitcoin seed", bytes.fromhex(seed), digestmod=hashlib.sha512).digest()
  chain = seed[32:]
  masterKey = seed[:32]

  return {
    "chain": chain.hex(),
    "masterKey": masterKey.hex()
  }

def generateMasterXpub(privateKey, chain):
  # Setup the ecdsa object with the corresponding bitcoin curve and private key
  signingKey = ecdsa.SigningKey.from_string(privateKey, curve=ecdsa.SECP256k1)

  # Get the verifying key for the inputted private key (public key)
  verifyingKey = signingKey.verifying_key
  
  publicKeyCompressed = verifyingKey.to_string('compressed').hex()

  depth = "00"
  parentFingerPrint = "00000000"
  childNumber = "00000000"


  xpubString = "0488b21e" + "00" + "00000000" + chain + publicKeyCompressed
  checkSum = hashlib.sha256(bytes.fromhex(xpubString)).hexdigest()[:2]

  xpubString = xpubString + checkSum

  base58xpub = base58.b58encode(bytes.fromhex(xpubString))

  # Return the compressed version of the coordinates (I.E. the compressed public key.) and the rest of the xpub data.
  return {  
    "masterKey": publicKeyCompressed,
    "xpub": base58xpub
  }


def createNormalChildXpub():
  pass

def generateNormalChildXprv(parentPrivKey, parentPubKey, chain, index, curveOrder):
  if (type(index) != int):
    return "Error"

  formattedIndex = "{:08x}".format(index)

  hmacData = bytes.fromhex(str(parentPubKey) + formattedIndex)
  hmacKey = bytes.fromhex(str(chain))

  hmacOutput = hmac.new(hmacKey, hmacData, digestmod=hashlib.sha512).digest()
  childXprv = hex((int(hmacOutput[:32].hex(), 16) + int(parentPrivKey, 16)) % int(curveOrder, 16))[2:]
  signingKey = ecdsa.SigningKey.from_string(bytes.fromhex(str(childXprv)), curve=ecdsa.SECP256k1)

  # Get the verifying key for the inputted private key (public key)
  verifyingKey = signingKey.verifying_key
  
  publicKeyCompressed = verifyingKey.to_string('compressed').hex()

  return {
    "privateKey": childXprv,
    "publicKey": publicKeyCompressed,
    "chain": hmacOutput[32:].hex()
  }

def generateHardenedChildXprv(parentPrivKey, chain, index, curveOrder):
  if (type(index) != int):
    return "Error"

  formattedIndex = "{:08x}".format(index)

  hmacData = bytes.fromhex("00" + str(parentPrivKey) + formattedIndex)
  hmacKey = bytes.fromhex(str(chain))

  hmacOutput = hmac.new(hmacKey, hmacData, digestmod=hashlib.sha512).digest()
  childXprv = hex((int(hmacOutput[:32].hex(), 16) + int(parentPrivKey, 16)) % int(curveOrder, 16))[2:]
  signingKey = ecdsa.SigningKey.from_string(bytes.fromhex(str(childXprv)), curve=ecdsa.SECP256k1)

  # Get the verifying key for the inputted private key (public key)
  verifyingKey = signingKey.verifying_key
  
  publicKeyCompressed = verifyingKey.to_string('compressed').hex()

  return {
    "privateKey": childXprv,
    "publicKey": publicKeyCompressed,
    "chain": hmacOutput[32:].hex()
  }


def hash160(data):
  ripemd160 = RIPEMD160.new()
  ripemd160.update((hashlib.sha256(data).digest()))

  return ripemd160.digest()

def serializeKey(parentPubKey, key, chain, depth, childNumber, isPrivateKey):
  # Depth is 1 byte
  # childNumber is 4 bytes - index number of this child from the parent
  # chain code is 32 bytes
  
  # Version is 4 bytes
  version = ""
  if (isPrivateKey):
    version = '0488ade4'
  else:
    version = '0488b21e'

  # parentFingerPrint is 4 bytes of hash160 parents public key
  parentFingerPrint = str(hash160(bytes.fromhex(str(parentPubKey)))[0:4].hex())


  # key size is 33 bytes
  if (isPrivateKey and (len(bytes.fromhex(key)) == 32)):
    key = "00" + str(key)


  serialisedHex = version + depth + parentFingerPrint + childNumber + str(chain) + key
  checkSum = hashlib.sha256(hashlib.sha256(bytes.fromhex(serialisedHex)).digest()).digest()[:4].hex()
  # base58 encode the result - for human readibility 
  base58serialisedKey = base58.b58encode(bytes.fromhex(serialisedHex + checkSum))

  return base58serialisedKey.decode('utf-8')

