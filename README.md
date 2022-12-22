In order to understand Ethereum's core functionalities, I am implementing parts of it for myself. Here I am implementing
the Merkle Patrie Trie (MPT) purley in Python 3.

## Tests

In order to run the tests, execute the following command:
```bash
$ python -m unittest
```
## Usage

Here an example on how to use the package:
```python
from mpt.trie import Trie

t = Trie('./testdb')
t.update(b'abcd', b'hello world')

print(t.get(b'abcd'))

print(t.get_root_hash())

t.delete(b'abcd')
```