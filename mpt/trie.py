import rlp
from mpt import db, utils

BLANK_ROOT = ''
BLANK_NODE = b''

# node types
(BLANK, BRANCH, LEAF, EXTENSION) = tuple(range(4))


def bin_to_nibbles(key: bytes) -> list:
    """
    Takes a string and creates a list with the nibbles (4 bits).

    :param key: The string which is encoded into nibbles
    :return: List which contains the nibbles
    """
    nibbles = []
    for k in key:
        # divmod returns (quotient, reminder)
        nibbles += divmod(k, 16)
    return nibbles


def pack_nibbles(nibbles: list, terminator: bool) -> bytes:
    """
    Takes a list of nibbles and adds the proper encoding for a leaf or extension node

    :param nibbles: List of nibbles
    :param terminator: True for leaf, False for extension
    :return: A string which containing of all nibbles
    """
    odd = len(nibbles) % 2
    # terminator tells if it is a leaf (True) or extension (False)
    flag = 2 if terminator else 0
    # in case the length is odd, we have to add the one
    flag += 1 if odd else 0
    # join flag and nibbles to one list
    nibbles = ([flag] + nibbles) if odd else ([flag, 0] + nibbles)
    key = []
    for i in range(0, len(nibbles), 2):
        key.append((nibbles[i] << 4) + nibbles[i + 1])
    b = bytes(key)
    return b


def unpack_to_nibbles(bin_data: bytes) -> list:
    """
    unpack packed binary data to nibbles

    :param bin_data: binary packed from nibbles
    :return: nibbles sequence, may have a terminator
    """
    o = bin_to_nibbles(bin_data)
    flags = o[0]
    if flags & 1 == 1:
        o = o[1:]
    else:
        o = o[2:]
    return o


def starts_with(full: list, part: list) -> bool:
    """
    test whether the items in the part is the leading items of the full

    :param full: The list with all entries
    :param part: List with partial content of full
    :return: True if items of part is leading items of full
    """
    if len(full) < len(part):
        return False
    return full[:len(part)] == part


def is_key_value_type(node_type: int) -> bool:
    """
    The function checks if the given node type is a leaf or extension node

    :param node_type: The node type to be checked
    :return: True in case it is a leaf/extension node, otherwise False
    """
    return node_type in [LEAF, EXTENSION]


class Trie:

    def __init__(self, path: str, root_hash: str = BLANK_ROOT):
        """
        Initializes a new Trie object

        :param path (str): Path where to store the database
        :param root_hash (str): Root hash of the trie 
        """
        self.root_node = None
        self.root_hash = root_hash
        self.set_root_node(root_hash)
        self.db = db.DB('./testdb')

    def set_root_node(self, root_hash: str) -> None:
        """
        Sets the root node

        :param root_hash: String which represents the root hash
        """
        assert isinstance(root_hash, str)
        assert len(root_hash) in [0, 32]
        if root_hash == BLANK_ROOT:
            self.root_node = BLANK_NODE
        else:
            self.root_node = db.get(root_hash)

    def update(self, key: bytes, value: bytes) -> None:
        """
        Takes a key/value pair and adds the value in the appropriate location in the trie

        :param key: bytes with length <= 32
        :param value: a String
        """
        if not isinstance(key, bytes):
            raise Exception("Key must be of type bytes")

        if len(key) > 32:
            raise Exception("Max key length is 32")

        if not isinstance(value, bytes):
            raise Exception("Value must be bytes")

        self.root_node = self._update(self.root_node, bin_to_nibbles(key), value)

    def get_value(self, key: bytes) -> bytes:
        """
        Takes a key and returns the value stored under that key. If there is no
        value, empty bytes are returned.

        :param key: bytes with length <= 32
        """
        if not isinstance(key, bytes):
            raise Exception("Key must be of type bytes")

        if len(key) > 32:
            raise Exception("Max key length is 32")
        return self._get_value(self.root_node, bin_to_nibbles(key))

    def _get_value(self, node: bytes, key: list) -> bytes:
        """
        Takes a key and returns the value stored under that key. If there is no
        value, empty bytes are returned.

        :param node: List which is used to go down the rabbit hole
        :param key: List of key nibbles
        """
        node_type = self._get_node_type(node)
        if node_type == BLANK:
            return BLANK_NODE

        if node_type == BRANCH:
            if not key:
                return node[-1]
            return self._get_node(self._decode_to_node(node[key[0]]), key[1:])

        if node_type == LEAF:
            curr_key = unpack_to_nibbles(node[0])
            # If the key does not match with the given key, we return None
            if not starts_with(key, curr_key):
                return None

            # returning value if key match, otherwise the blank node
            return node[1] if key == curr_key else BLANK_NODE

        if node_type == EXTENSION:
            curr_key = unpack_to_nibbles(node[0])
            # If the key does not match with the given key, we return None
            if not starts_with(key, curr_key):
                return None
            return self._get_node(self._decode_to_node(node[1]), key[len(curr_key):])
            

    def get_root_hash(self) -> bytes:
        """
        Returns the current hash of the root node

        :return: Hash of the root node
        """
        self.root_hash = utils.sha3(rlp.encode(self.root_node))
        return self.root_hash

    def _update(self, node: list, key: list, value: bytes) -> list:
        """
        Recursive called method to update the trie with a new value with a given key

        :param node: A list on the path for the new value. Used to find the location for the new value
        :param key: Path for the new value
        :param value: The value to be stored in the trie
        :return: A new node
        """
        node_type = self._get_node_type(node)
        # in case the root node is still blank, set it to a leaf node
        if node_type == BLANK:
            # in case the root node is blank, we make it a leaf node
            return [pack_nibbles(key, True), value]

        elif node_type == BRANCH:
            # key array is empty
            if not key:
                # save the value
                node[-1] = value
            else:
                # otherwise decode the node at the position key[0] in the branch node and go further down the
                # rabbit whole
                new_node = self._update(self._decode_to_node(node[key[0]]), key[1:], value)
                node[key[0]], db_touch = self._encode_node(new_node)
            return node

        elif node_type == LEAF or node_type == EXTENSION:
            # check if the key length is even
            even = False if ((ord(node[0][0:1]) & 0x10) == 0x10) else True

            current_key = bin_to_nibbles(node[0])
            # we remove the encoding according to the parity
            current_key = current_key[2:] if even else current_key[1:]

            prefix = 0
            # compare the keys
            for i in range(0, min(len(current_key), len(key))):
                if current_key[i] != key[i]:
                    break
                prefix += 1

            remaining_key = key[prefix:]
            remaining_curr_key = current_key[prefix:]

            if len(remaining_key) == 0 and len(remaining_curr_key) == 0:
                # both keys are equal and have the same length
                if node_type == EXTENSION:
                    # Since we currently have a branch node, we decode the hash to the node and go one level deeper
                    # to update the value of the branch node
                    new_node = self._update(self._decode_to_node(node[1]), remaining_key, value)
                else:
                    # Since we have currently a leaf node, we update the value :)
                    return [node[0], value]
            elif len(remaining_curr_key) == 0:
                # the current key is shorter than the new one and it is exhausted
                if node_type == EXTENSION:
                    # we save the old node
                    old_node = node[:]
                    # we get the new node
                    new_node = self._update(self._decode_to_node(node[1]), remaining_key, value)
                    # compare and see if they are equal
                    if old_node != new_node:
                        # if not, delete the old node
                        self._delete_node(old_node)
                else:
                    # the old key is exhausted and that's why we make a branch node. There is a value under this path
                    # and the path is being extended too. That's the reason for a branch node.
                    new_node = [BLANK_NODE] * 17
                    # save the value in the branch node
                    new_node[-1] = node[1]
                    # create a leaf node with the remaining content
                    new_node[remaining_key[0]], db_touch = self._encode_node(
                        [pack_nibbles(remaining_key[1:], True), value]
                    )
            else:
                # both keys have some differences, so we make a branch node
                new_node = [BLANK_NODE] * 17

                if len(remaining_key) == 0:
                    # if the remaining key is exhausted, we insert the value into our branch node
                    new_node[-1] = value
                else:
                    # otherwise we create a leaf node, where the value is stored
                    new_node[remaining_key[0]], db_touch = self._encode_node(
                        [pack_nibbles(remaining_key[1:], True), value])

                if node_type == EXTENSION and len(remaining_curr_key) == 1:
                    # there is no key left of the extension key, so we set the hash here
                    new_node[remaining_curr_key[0]] = node[1]
                else:
                    # set terminator depending on the node type
                    terminator = True if node_type == LEAF else False
                    # saving the old path and value in a new leaf node
                    new_node[remaining_curr_key[0]], db_touch = self._encode_node(
                        [pack_nibbles(remaining_curr_key[1:], terminator), node[1]])

            # in case there is a prefix set, because some parts of the path are equal we have to create a new extension
            # node where the content is in
            if prefix:
                n, db_touch = self._encode_node(new_node)
                new_node = [pack_nibbles(current_key[:prefix], False), n]
            return new_node

    def delete(self, key: bytes) -> None:
        """
        Deletes a value which is under the given key

        :param key: Key to the value to be deleted
        """
        if not isinstance(key, bytes):
            raise Exception("Key must be of type bytes")

        if len(key) > 32:
            raise Exception("Max key length is 32")

        self.root_node = self._delete(self.root_node, bin_to_nibbles(key))

    @staticmethod
    def _get_node_type(node: list) -> int:
        """
        Returns the type of the node

        :param node: String or list
        :return: Node type
        """
        if node == BLANK_NODE:
            return BLANK
        elif len(node) == 2:
            # check if the terminator is set.
            return LEAF if (ord(node[0][0:1]) & 0x20) == 0x20 else EXTENSION
        elif len(node) == 17:
            return BRANCH
        return -1

    def _encode_node(self, node: list) -> (bytes, int):
        """
        Takes a node, encodes it and hash it. The set of (hash, node) is stored in the db, where the hash is the key
        to retrieve the data from the database.

        :param node: A list which represents a node
        :return: A hash over the node and a flag if the db has been used
        """
        if node == BLANK_NODE:
            return BLANK_NODE, 0
        assert isinstance(node, list)
        rlp_node = rlp.encode(node)

        # in case the encoded data has lesser than 32 characters, we return rather the node than the hash
        # can be used for some optimization in case the comments are out
        if len(rlp_node) < 32:
            return node, 0

        hash_key = utils.sha3(rlp_node)
        self.db.put(hash_key, rlp_node)
        return hash_key, 1

    def _decode_to_node(self, encoded: str) -> list:
        """
        Takes an encoded parameter and decodes it to a node. The parameter might be an rlp encoded node or a hash of a
        node which is stored in the db.

        :param encoded: Node encoded in either rlp or by a hash
        :return: Decoded node
        """
        if encoded == BLANK_NODE:
            return BLANK_NODE
        if isinstance(encoded, list):
            return encoded
        return rlp.decode(self.db.get(encoded))

    def _delete(self, node: list, key: list):
        """
        Recursive delete function :)

        :param node: List which is used to go down the rabbit hole
        :param key: Path we are following
        :return:
        """
        node_type = self._get_node_type(node)
        if node_type == BLANK:
            return BLANK_NODE

        if node_type == BRANCH:
            return self._delete_branch_node(node, key)

        if node_type == LEAF:
            return self._delete_leaf_node(node, key)

        if node_type == EXTENSION:
            return self._delete_extension_node(node, key)

    def _delete_branch_node(self, node: list, key: list) -> list:
        """
        Called when we have a branch node and check if we either follow the path or if we found value which is going
        to be deleted.

        :param node: List which represents the branch node
        :param key: A list of nibbles
        :return: A list which represents a new node
        """
        # if the key list is empty we set the value of the branch node to blank
        if not key:
            node[-1] = BLANK_NODE
            # normalize the branch node
            return self._normalize_branch_node(node)

        # Decode the node and go one step deeper into recursion
        n = self._delete(self._decode_to_node(node[key[0]]), key[1:])
        n, db_touch = self._encode_node(n)

        if n == node[key[0]]:
            return node

        node[key[0]] = n
        if n == BLANK_NODE:
            # Normalize the node
            return self._normalize_branch_node(node)

        return node

    def _delete_leaf_node(self, node: list, key: list) -> list:
        """
        Called when we have a leaf node.

        :param node: List which represents the leaf node
        :param key: A list of nibbles
        :return: In case the leaf node has the key given key the blank node is returned, otherwise the node itself
        """
        curr_key = unpack_to_nibbles(node[0])

        if not starts_with(key, curr_key):
            # key not found
            return node

        return BLANK_NODE if key == curr_key else node

    def _delete_extension_node(self, node: list, key: list) -> list:
        """
        Called when we have a extension node.

        :param node: List which represents the extension node
        :param key: A list of nibbles
        :return: In case the leaf node has the key given key the blank node is returned, otherwise the node itself
        """
        curr_key = unpack_to_nibbles(node[0])

        if not starts_with(key, curr_key):
            # key not found
            return node

        # we take the key parts which overlap, decode the node which is within the extension node and
        # call the delete function
        new_sub_node = self._delete(self._decode_to_node(node[1]), key[len(curr_key):])

        # if the hash hasn't changed, just return the node
        if self._encode_node(new_sub_node) == node[1]:
            return node

        # new sub node is BLANK_NODE
        if new_sub_node == BLANK_NODE:
            return BLANK_NODE

        # the hash has changed, therefore we check what type the subnode has
        new_sub_node_type = self._get_node_type(new_sub_node)

        # if it is a leaf or extension node
        if is_key_value_type(new_sub_node_type):
            # collapse subnode to this node, note this node will have same
            # terminator with the new sub node, and value does not change
            new_key = curr_key + unpack_to_nibbles(new_sub_node[0])
            terminator = True if new_sub_node_type == LEAF else False
            return [pack_nibbles(new_key, terminator), new_sub_node[1]]

        if new_sub_node_type == BRANCH:
            n, db_touch = self._encode_node(new_sub_node)
            # creating a extension node
            return [pack_nibbles(curr_key, False), n]

    def _normalize_branch_node(self, node: list) -> list:
        """
        Takes a node and checks if the type has to be changed (e.g. from branch to leaf).

        :param node: A list which represents the node
        :return: A list which represents a node
        """

        # count the blank nodes
        not_blank_items_count = sum(1 for x in range(17) if node[x])

        if not_blank_items_count > 1:
            return node

        # now only one item is not blank
        not_blank_index = [i for i, item in enumerate(node) if item][0]

        # the value item is not blank
        if not_blank_index == 16:
            return [pack_nibbles([], True), node[16]]

        # path item is not blank
        sub_node = self._decode_to_node(node[not_blank_index])
        sub_node_type = self._get_node_type(sub_node)

        if is_key_value_type(sub_node_type):
            # collapse subnode to this node, not this node will have same
            # terminator with the new sub node, and value does not change
            new_key = [not_blank_index] + unpack_to_nibbles(sub_node[0])
            terminator = True if sub_node_type == LEAF else False
            return [pack_nibbles(new_key, terminator), sub_node[1]]
        else:
            # since it is not a leaf or extension node, we have a branch node
            n, db_touch = self._encode_node(sub_node)
            # we pack it into an extension node
            return [pack_nibbles([not_blank_index], False), n]

    def _delete_node(self, node: list) -> None:
        """
        Deletes node from storage

        :param node: node in form of list, or BLANK_NODE
        :return: None
        """
        node_type = self._get_node_type(node)
        if node_type == BLANK:
            return
        elif node_type == EXTENSION:
            self.db.delete(utils.sha3(rlp.encode(node[1])))
        else:
            assert isinstance(node, list)
            encoded, db_touch = self._encode_node(node)
            if len(encoded) < 32:
                return
            self.db.delete(encoded)
