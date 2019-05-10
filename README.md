In order to understand Ethereum's core functionalities, I am implementing those for myself. Here I am implementing
the Merkle Patrie Trie (MPT) purley in Python 3.

So far it passes some tests which are given at https://github.com/ethereum/tests/tree/develop/TrieTests

Currently it does not pass tests where the test data consists of hex data and I am not sure why.

What is currently left to do?

 - Fix the problem with the hex test cases
 - Comment the delete process
 - Merkle proofs?
