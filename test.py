import unittest
from seedPhraseGeneration import generate256BitMnemonicPhrase, generateSeed, generateMasterXprv, generateMasterXpub, generateNormalChildXprv, generateHardenedChildXprv, serializeKey
import ecdsa 

referenceData = [
	[
		"0000000000000000000000000000000000000000000000000000000000000000",
		"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art",
		"bda85446c68413707090a52022edd26a1c9462295029f2e60cd7c4f2bbd3097170af7a4d73245cafa9c3cca8d561a7c3de6f5d4a10be8ed2a5e608d68f92fcc8",
		"xprv9s21ZrQH143K32qBagUJAMU2LsHg3ka7jqMcV98Y7gVeVyNStwYS3U7yVVoDZ4btbRNf4h6ibWpY22iRmXq35qgLs79f312g2kj5539ebPM"
	],
	[
		"7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f",
		"legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth title",
		"bc09fca1804f7e69da93c2f2028eb238c227f2e9dda30cd63699232578480a4021b146ad717fbb7e451ce9eb835f43620bf5c514db0f8add49f5d121449d3e87",
		"xprv9s21ZrQH143K3Y1sd2XVu9wtqxJRvybCfAetjUrMMco6r3v9qZTBeXiBZkS8JxWbcGJZyio8TrZtm6pkbzG8SYt1sxwNLh3Wx7to5pgiVFU"
	],
	[
		"8080808080808080808080808080808080808080808080808080808080808080",
		"letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic bless",
		"c0c519bd0e91a2ed54357d9d1ebef6f5af218a153624cf4f2da911a0ed8f7a09e2ef61af0aca007096df430022f7a2b6fb91661a9589097069720d015e4e982f",
		"xprv9s21ZrQH143K3CSnQNYC3MqAAqHwxeTLhDbhF43A4ss4ciWNmCY9zQGvAKUSqVUf2vPHBTSE1rB2pg4avopqSiLVzXEU8KziNnVPauTqLRo"
	],
	[
		"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
		"zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote",
		"dd48c104698c30cfe2b6142103248622fb7bb0ff692eebb00089b32d22484e1613912f0a5b694407be899ffd31ed3992c456cdf60f5d4564b8ba3f05a69890ad",
		"xprv9s21ZrQH143K2WFF16X85T2QCpndrGwx6GueB72Zf3AHwHJaknRXNF37ZmDrtHrrLSHvbuRejXcnYxoZKvRquTPyp2JiNG3XcjQyzSEgqCB"
	]
]

class TestSeedGeneration(unittest.TestCase):

	def test_seed_generation(self):
		for testData in referenceData:
			entropy = testData[0]
			seedPhraseExpected = testData[1]
			seedExpected = testData[2]

			entropy = int(entropy, 16).to_bytes(32, byteorder="big")

			seedPhraseData = generate256BitMnemonicPhrase(entropy)

			self.assertEqual(seedPhraseData["mnemonicPhrase"], seedPhraseExpected)

			seed = generateSeed(seedPhraseData["mnemonicPhrase"], "TREZOR")

			self.assertEqual(str(seed.hex()), seedExpected)      

	def test_private_key_generation(self):
		seed = '67f93560761e20617de26e0cb84f7234aaf373ed2e66295c3d7397e6d7ebe882ea396d5d293808b0defd7edd2babd4c091ad942e6a9351e6d075a29d4df872af'
		privateKeyExpected = 'f79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9'
		chainExpected = '463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b'
		publicKeyExpected = '0252c616d91a2488c1fd1f0f172e98f7d1f6e51f8f389b2f8d632a8b490d5f6da9'

		xprvData = generateMasterXprv(seed)
		self.assertEqual(str(xprvData['chain']), chainExpected)
		self.assertEqual(str(xprvData['masterKey']), privateKeyExpected)

		xpubData = generateMasterXpub(bytes.fromhex(xprvData['masterKey']), xprvData['chain'])

		self.assertEqual(str(xpubData["masterKey"]), publicKeyExpected)


	def test_normal_extended_child_private_key_generation(self):
		childPublicKeyExpected = '030204d3503024160e8303c0042930ea92a9d671de9aa139c1867353f6b6664e59'
		childPrivateKeyExpected = '39f329fedba2a68e2a804fcd9aeea4104ace9080212a52ce8b52c1fb89850c72'
		childChainExpected = '05aae71d7c080474efaab01fa79e96f4c6cfe243237780b0df4bc36106228e31'

		parentPrivateKey = 'f79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9'
		parentChain = '463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b'
		parentPublicKey = '0252c616d91a2488c1fd1f0f172e98f7d1f6e51f8f389b2f8d632a8b490d5f6da9'

		# Generate a child key pairing with index of zero.
		childKeyData = generateNormalChildXprv(parentPrivateKey, parentPublicKey, parentChain, 0, hex(ecdsa.SECP256k1.order))

		self.assertEqual(childKeyData['privateKey'], childPrivateKeyExpected)
		self.assertEqual(childKeyData['publicKey'], childPublicKeyExpected)
		self.assertEqual(childKeyData['chain'], childChainExpected)

	def test_hardened_extended_child_private_key_generation(self):
		childPublicKeyExpected = '0355cff4a963ce259b08be9a864564caca210eb4eb35fcb75712e4bba7550efd95'
		childPrivateKeyExpected = '7272904512add56fef94c7b4cfc62bedd0632afbad680f2eb404e95f2d84cbfa'
		childChainExpected = 'cb3c17166cc30eb7fdd11993fb7307531372e565cd7c7136cbfa4655622bc2be'

		parentPrivateKey = 'f79bb0d317b310b261a55a8ab393b4c8a1aba6fa4d08aef379caba502d5d67f9'
		parentChain = '463223aac10fb13f291a1bc76bc26003d98da661cb76df61e750c139826dea8b'

		# Generate a child key pairing with index of zero.
		childKeyData = generateHardenedChildXprv(parentPrivateKey, parentChain, 2147483648, hex(ecdsa.SECP256k1.order))

		self.assertEqual(childKeyData['privateKey'], childPrivateKeyExpected)
		self.assertEqual(childKeyData['publicKey'], childPublicKeyExpected)
		self.assertEqual(childKeyData['chain'], childChainExpected)


	def test_serialise_key(self):
		parentPubKey = '0252c616d91a2488c1fd1f0f172e98f7d1f6e51f8f389b2f8d632a8b490d5f6da9'
		chain = '05aae71d7c080474efaab01fa79e96f4c6cfe243237780b0df4bc36106228e31'
		privKey = '39f329fedba2a68e2a804fcd9aeea4104ace9080212a52ce8b52c1fb89850c72'

		serialisedKeyExpected = 'xprv9tuogRdb5YTgcL3P8Waj7REqDuQx4sXcodQaWTtEVFEp6yRKh1CjrWfXChnhgHeLDuXxo2auDZegMiVMGGxwxcrb2PmiGyCngLxvLeGsZRq'

		isPrivateKey = True
		depth = '01'
		childNumber = '00000000'

		serialisedKey = serializeKey(parentPubKey, privKey, chain, depth, childNumber,isPrivateKey)

		self.assertEqual(serialisedKey, serialisedKeyExpected)

if __name__ == '__main__':
  unittest.main()