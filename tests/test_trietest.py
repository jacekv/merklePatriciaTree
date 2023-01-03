from unittest import TestCase

from mpt.trie import Trie
from tests import DB_PATH
from tests import delete_db_dir


class TrieTest(TestCase):
    def tearDown(self):
        delete_db_dir()

    def test_exampleTrie(self):
        test = [
            [b"do", b"verb"],  # ok
            [b"dog", b"puppy"],
            [b"doge", b"coin"],
            [b"horse", b"stallion"],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84"
        )

    def test_emptyValue(self):
        test = [
            [b"do", b"verb"],
            [b"ether", b"wookiedoo"],
            [b"horse", b"stallion"],
            [b"shaman", b"horse"],
            [b"doge", b"coin"],
            [b"ether", ""],
            [b"dog", b"puppy"],
            [b"shaman", ""],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "5991bb8c6514148a29db676a14ac506cd2cd5775ace63c30a4fe457715e9ac84"
        )

    def test_branchValueUpdate(self):
        test = [[b"abc", b"123"], [b"abcd", b"abcd"], [b"abc", b"abc"]]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "7a320748f780ad9ad5b0837302075ce0eeba6c26e3d8562c67ccc0f1b273298a"
        )

    def test_insertMiddleLeaf(self):
        test = [
            [b"key1aa", b"0123456789012345678901234567890123456789xxx"],
            [b"key1", b"0123456789012345678901234567890123456789Very_Long"],
            [b"key2bb", b"aval3"],
            [b"key2", b"short"],
            [b"key3cc", b"aval3"],
            [b"key3", b"1234567890123456789012345678901"],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "cb65032e2f76c48b82b5c24b3db8f670ce73982869d38cd39a624f23d62a9e89"
        )

    def test_branching(self):
        test = [
            [bytes.fromhex("04110d816c380812a427968ece99b1c963dfbce6"), b"something"],
            [bytes.fromhex("095e7baea6a6c7c4c2dfeb977efac326af552d87"), b"something"],
            [bytes.fromhex("0a517d755cebbf66312b30fff713666a9cb917e0"), b"something"],
            [bytes.fromhex("24dd378f51adc67a50e339e8031fe9bd4aafab36"), b"something"],
            [bytes.fromhex("293f982d000532a7861ab122bdc4bbfd26bf9030"), b"something"],
            [bytes.fromhex("2cf5732f017b0cf1b1f13a1478e10239716bf6b5"), b"something"],
            [bytes.fromhex("31c640b92c21a1f1465c91070b4b3b4d6854195f"), b"something"],
            [bytes.fromhex("37f998764813b136ddf5a754f34063fd03065e36"), b"something"],
            [bytes.fromhex("37fa399a749c121f8a15ce77e3d9f9bec8020d7a"), b"something"],
            [bytes.fromhex("4f36659fa632310b6ec438dea4085b522a2dd077"), b"something"],
            [bytes.fromhex("62c01474f089b07dae603491675dc5b5748f7049"), b"something"],
            [bytes.fromhex("729af7294be595a0efd7d891c9e51f89c07950c7"), b"something"],
            [bytes.fromhex("83e3e5a16d3b696a0314b30b2534804dd5e11197"), b"something"],
            [bytes.fromhex("8703df2417e0d7c59d063caa9583cb10a4d20532"), b"something"],
            [bytes.fromhex("8dffcd74e5b5923512916c6a64b502689cfa65e1"), b"something"],
            [bytes.fromhex("95a4d7cccb5204733874fa87285a176fe1e9e240"), b"something"],
            [bytes.fromhex("99b2fcba8120bedd048fe79f5262a6690ed38c39"), b"something"],
            [bytes.fromhex("a4202b8b8afd5354e3e40a219bdc17f6001bf2cf"), b"something"],
            [bytes.fromhex("a94f5374fce5edbc8e2a8697c15331677e6ebf0b"), b"something"],
            [bytes.fromhex("a9647f4a0a14042d91dc33c0328030a7157c93ae"), b"something"],
            [bytes.fromhex("aa6cffe5185732689c18f37a7f86170cb7304c2a"), b"something"],
            [bytes.fromhex("aae4a2e3c51c04606dcb3723456e58f3ed214f45"), b"something"],
            [bytes.fromhex("c37a43e940dfb5baf581a0b82b351d48305fc885"), b"something"],
            [bytes.fromhex("d2571607e241ecf590ed94b12d87c94babe36db6"), b"something"],
            [bytes.fromhex("f735071cbee190d76b704ce68384fc21e389fbe7"), b"something"],
            [bytes.fromhex("04110d816c380812a427968ece99b1c963dfbce6"), b""],
            [bytes.fromhex("095e7baea6a6c7c4c2dfeb977efac326af552d87"), b""],
            [bytes.fromhex("0a517d755cebbf66312b30fff713666a9cb917e0"), b""],
            [bytes.fromhex("24dd378f51adc67a50e339e8031fe9bd4aafab36"), b""],
            [bytes.fromhex("293f982d000532a7861ab122bdc4bbfd26bf9030"), b""],
            [bytes.fromhex("2cf5732f017b0cf1b1f13a1478e10239716bf6b5"), b""],
            [bytes.fromhex("31c640b92c21a1f1465c91070b4b3b4d6854195f"), b""],
            [bytes.fromhex("37f998764813b136ddf5a754f34063fd03065e36"), b""],
            [bytes.fromhex("37fa399a749c121f8a15ce77e3d9f9bec8020d7a"), b""],
            [bytes.fromhex("4f36659fa632310b6ec438dea4085b522a2dd077"), b""],
            [bytes.fromhex("62c01474f089b07dae603491675dc5b5748f7049"), b""],
            [bytes.fromhex("729af7294be595a0efd7d891c9e51f89c07950c7"), b""],
            [bytes.fromhex("83e3e5a16d3b696a0314b30b2534804dd5e11197"), b""],
            [bytes.fromhex("8703df2417e0d7c59d063caa9583cb10a4d20532"), b""],
            [bytes.fromhex("8dffcd74e5b5923512916c6a64b502689cfa65e1"), b""],
            [bytes.fromhex("95a4d7cccb5204733874fa87285a176fe1e9e240"), b""],
            [bytes.fromhex("99b2fcba8120bedd048fe79f5262a6690ed38c39"), b""],
            [bytes.fromhex("a4202b8b8afd5354e3e40a219bdc17f6001bf2cf"), b""],
            [bytes.fromhex("a94f5374fce5edbc8e2a8697c15331677e6ebf0b"), b""],
            [bytes.fromhex("a9647f4a0a14042d91dc33c0328030a7157c93ae"), b""],
            [bytes.fromhex("aa6cffe5185732689c18f37a7f86170cb7304c2a"), b""],
            [bytes.fromhex("aae4a2e3c51c04606dcb3723456e58f3ed214f45"), b""],
            [bytes.fromhex("c37a43e940dfb5baf581a0b82b351d48305fc885"), b""],
            [bytes.fromhex("d2571607e241ecf590ed94b12d87c94babe36db6"), b""],
            [bytes.fromhex("f735071cbee190d76b704ce68384fc21e389fbe7"), b""],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421"
        )

    def test_jeff(self):
        test = [
            [
                bytes.fromhex(
                    "0000000000000000000000000000000000000000000000000000000000000045"
                ),
                bytes.fromhex("22b224a1420a802ab51d326e29fa98e34c4f24ea"),
            ],
            [
                bytes.fromhex(
                    "0000000000000000000000000000000000000000000000000000000000000046"
                ),
                bytes.fromhex(
                    "67706c2076330000000000000000000000000000000000000000000000000000"
                ),
            ],
            [
                bytes.fromhex(
                    "0000000000000000000000000000000000000000000000000000001234567890"
                ),
                bytes.fromhex("697c7b8c961b56f675d570498424ac8de1a918f6"),
            ],
            [
                bytes.fromhex(
                    "000000000000000000000000697c7b8c961b56f675d570498424ac8de1a918f6"
                ),
                bytes.fromhex("1234567890"),
            ],
            [
                bytes.fromhex(
                    "0000000000000000000000007ef9e639e2733cb34e4dfc576d4b23f72db776b2"
                ),
                bytes.fromhex(
                    "4655474156000000000000000000000000000000000000000000000000000000"
                ),
            ],
            [
                bytes.fromhex(
                    "000000000000000000000000ec4f34c97e43fbb2816cfd95e388353c7181dab1"
                ),
                bytes.fromhex(
                    "4e616d6552656700000000000000000000000000000000000000000000000000"
                ),
            ],
            [
                bytes.fromhex(
                    "4655474156000000000000000000000000000000000000000000000000000000"
                ),
                bytes.fromhex("7ef9e639e2733cb34e4dfc576d4b23f72db776b2"),
            ],
            [
                bytes.fromhex(
                    "4e616d6552656700000000000000000000000000000000000000000000000000"
                ),
                bytes.fromhex("ec4f34c97e43fbb2816cfd95e388353c7181dab1"),
            ],
            [
                bytes.fromhex(
                    "0000000000000000000000000000000000000000000000000000001234567890"
                ),
                b"",
            ],
            [
                bytes.fromhex(
                    "000000000000000000000000697c7b8c961b56f675d570498424ac8de1a918f6"
                ),
                bytes.fromhex(
                    "6f6f6f6820736f2067726561742c207265616c6c6c793f000000000000000000"
                ),
            ],
            [
                bytes.fromhex(
                    "6f6f6f6820736f2067726561742c207265616c6c6c793f000000000000000000"
                ),
                bytes.fromhex("697c7b8c961b56f675d570498424ac8de1a918f6"),
            ],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "9f6221ebb8efe7cff60a716ecb886e67dd042014be444669f0159d8e68b42100"
        )

    def _feed_trie(self, test_data: list) -> bytes:
        t = Trie(DB_PATH)
        for data in test_data:
            if data[1]:
                t.update(data[0], data[1])
            else:
                t.delete(data[0])
        return t.get_root_hash()
