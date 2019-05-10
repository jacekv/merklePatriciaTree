from unittest import TestCase
from mpt.trie import Trie

class TrieAnyOrder(TestCase):

    def test_singleItem(self):
      test = [
          [b"A", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
      ]
      h = self._feed_trie(test)
      self.assertTrue(h.hex() == "d23786fb4a010da3ce639d66d5e904a11dbc02746d1ce25029e53290cabf28ab")

    def test_dogs(self):
      test = [
          [b"doe", "reindeer"],
          [b"dog", "puppy"],
          [b"dogglesworth", "cat"]
      ]
      h = self._feed_trie(test)
      self.assertTrue(h.hex() == "8aad789dff2f538bca5d8ea56e8abe10f4c7ba3a5dea95fea4cd6e7c3a1168d3")

    def test_foo(self):
        test = [
            [b"foo", "bar"],
            [b"food", "bass"]
        ]
        h = self._feed_trie(test)
        self.assertTrue(h.hex() == "17beaa1648bafa633cda809c90c04af50fc8aed3cb40d16efbddee6fdf63c4c3")

    def test_smallValues(self):
        test = [
            [b"be", "e"],
            [b"dog", "puppy"],
            [b"bed", "d"]
        ]
        h = self._feed_trie(test)
        self.assertTrue(h.hex() == "3f67c7a47520f79faa29255d2d3c084a7a6df0453116ed7232ff10277a8be68b")

    def test_testy(self):
        test = [
            [b"test", "test"],
            [b"te", "testy"]
        ]
        h = self._feed_trie(test)
        self.assertTrue(h.hex() == "8452568af70d8d140f58d941338542f645fcca50094b20f3c3d8c3df49337928")

    def test_hex(self):
        test = [
            [b"\x00\x45", "\x01\x23\x45\x67\x89"],
            [b"\x45\x00", "\x98\x76\x54\x32\x10"]
        ]
        h = self._feed_trie(test)
        self.assertTrue(h.hex() == "285505fcabe84badc8aa310e2aae17eddc7d120aabec8a476902c8184b3a3503")

    def _feed_trie(self, test_data: list) -> bytes:
        t = Trie()
        for data in test_data:
            if data[1]:
                t.update(data[0], data[1])
            else:
                t.delete(data[0])
        return t.get_root_hash()