In order to understand Ethereum's core functionalities, I am implementing parts of it for myself. Here I am implementing
the Merkle Patricia Trie (MPT) purely in Python 3.

## Install

```shell
pip install ethereum-merkle-patricia-trie
```

## Requirements

In order to use the package, you need to install LevelDb on your system.

## Tests

In order to run the tests, execute the following command:
```bash
$ python -m unittest
```
## Usage

Here an example on how to use the package:


    from mpt.trie import Trie

    t = Trie('./testdb')
    t.update(b'abcd', b'hello world')

    print(t.get_value(b'abcd'))

    print(t.get_root_hash())

    t.delete(b'abcd')


## Upload to Pypi

Uploading and testing using test Pypi

    python -m build
    python -m twine upload --repository testpypi dist/*
    pip install --index-url https://test.pypi.org/simple/ --no-deps merklePatriciaTrie   


Uploading to Pypi

    python -m build
    python -m twine upload dist/*
