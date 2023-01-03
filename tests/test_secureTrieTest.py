from unittest import TestCase

from mpt.trie import Trie
from sha3 import keccak_256
from tests import DB_PATH
from tests import delete_db_dir


class TrieTest(TestCase):
    def tearDown(self):
        delete_db_dir()

    def test_emptyValue(self):
        test = [
            [keccak_256(b"do").digest(), b"verb"],
            [keccak_256(b"ether").digest(), b"wookiedoo"],
            [keccak_256(b"horse").digest(), b"stallion"],
            [keccak_256(b"shaman").digest(), b"horse"],
            [keccak_256(b"doge").digest(), b"coin"],
            [keccak_256(b"ether").digest(), ""],
            [keccak_256(b"dog").digest(), b"puppy"],
            [keccak_256(b"shaman").digest(), ""],
        ]
        h = self._feed_trie(test)
        self.assertTrue(
            h.hex()
            == "29b235a58c3c25ab83010c327d5932bcf05324b7d6b1185e650798034783ca9d"
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

    def _feed_trie(self, test_data: list) -> bytes:
        t = Trie(DB_PATH)
        for data in test_data:
            if data[1]:
                t.update(data[0], data[1])
            else:
                t.delete(data[0])
        return t.get_root_hash()
