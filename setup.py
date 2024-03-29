from setuptools import setup

readme = open("README.md", "r")
content = readme.read()
readme.close()

setup(
    name="ethereum-merkle-patricia-trie",
    packages=["mpt"],
    version="0.0.3",
    description="Pure Python 3 Merkle Patricia Trie implementation",
    long_description=content,
    long_description_content_type="text/markdown",
    url="https://github.com/jacekv/merklePatriciaTree",
    author="Jacek Varky",
    author_email="jaca347@gmail.com",
    install_requires=[
        "plyvel==1.5.0",
        "rlp==3.0.0",
        "pysha3==1.0.2",
    ],
    license="MIT",
    zip_safe=False,
)
