
"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """

    @type key: int or None
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.is_height_changed = False
        if key is not None: #initiaize the real node with 2 virtual children
            self.height = 0
            self.left = AVLNode(None, None)
            self.right = AVLNode(None, None)

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child (if self is virtual)
    """

    def get_left(self):
        return self.left
    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child (if self is virtual)
    """

    def get_right(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def get_parent(self):
        return self.parent

    """returns the key

    @rtype: int or None
    @returns: the key of self, None if the node is virtual
    """

    def get_key(self):
        if self.is_real_node():
            return self.key
        return None
    """returns the value

    @rtype: any
    @returns: the value of self, None if the node is virtual
    """

    def get_value(self):
        if self.is_real_node():
            return self.value
        return None

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def get_height(self):
        if self is None:
            return -1
        return self.height


    def get_balance(self):
        if self is None or not self.is_real_node():
            return 0
        return self.left.height - self.right.height


    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        self.parent = node

    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None



"""
A class implementing the ADT Dictionary, using an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = AVLNode(None, None)
        self.amountofnodes = 0

    """searches for a AVLNode in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: the AVLNode corresponding to key or None if key is not found.
    """
    def search(self, key):
        result = self._search_helper(self.root, key)
        if result.is_real_node():
            return result
        else:
            return None


    def _search_helper(self, node, key):
        if node == None:
            return AVLNode(None, None)
        currNode = node
        while currNode.is_real_node():
            if currNode.key == key:
                return currNode
            elif key < currNode.key:
                currNode = currNode.left
            else:
                currNode = currNode.right
        return AVLNode(None, None)


    """inserts val at position i in the dictionary

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: any
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def update_heights(self, node):
        while node is not None:
            old_height = node.height
            new_height = self.update_height(node)  # Assume this method updates the height of the node
            if old_height != new_height:
                node.is_height_changed = True
            node = node.get_parent()

    def insertAsBST(self, node):
        if self.root.key is None:
            self.root = node
        else:
            currNode = self.root
            parent = currNode.parent
            while currNode.is_real_node():
                parent = currNode
                if node.key < currNode.key:
                    currNode = currNode.left
                else:
                    currNode = currNode.right
            # insert node as child
            node.set_parent(parent)
            if node.key < parent.key:
                parent.set_left(node)
            else:
                parent.set_right(node)
        self.update_heights(node)
        return


    def insert(self, key, val):
        #increase tree size by 1:
        self.amountofnodes += 1
        node, rebalance_operations = self._insert_helper(self.root, key, val)
        return rebalance_operations

    def _insert_helper(self, node, key, val):
        #insert as in BST
        node_inserted = AVLNode(key, val)
        self.insertAsBST(node_inserted)
        #let parent be the parent of the inserted node
        parent = node_inserted.parent
        #rebalance
        rebalance_operations = self.rebalance(parent)
        return node, rebalance_operations

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def deleteAsBST(self, root, node, parent=None):
        if root.key is None:
            return root, parent
        if node.key < root.key:
            root.left, parent = self.deleteAsBST(root.left, node, root)
        elif node.key > root.key:
            root.right, parent = self.deleteAsBST(root.right, node, root)
        else:
            if root.left.key is None:
                temp = root.right
                if temp is not None:
                    temp.parent = root.parent
                if self.amountofnodes <= 2:
                    self.root = temp
                return temp, parent
            elif root.right.key is None:
                temp = root.left
                if temp is not None:
                    temp.parent = root.parent
                if self.amountofnodes <= 2:
                    self.root = temp
                return temp, parent
            succ = self.Successor(root)
            root.key = succ.key
            root.right, parent = self.deleteAsBST(root.right, succ, root)
        old_height = root.height
        root.height = 1 + max(root.left.get_height(), root.right.get_height())
        root.is_height_changed = (root.height != old_height)
        return root, parent

    def delete(self, node):
        #0 decrease size by 1:
        #1 Delete as in a BST tree
        # 2 Let parent be the deleted node's parent
        root, parent = self.deleteAsBST(self.root, node)
        self.amountofnodes -= 1
        #3 rebalance
        rebalance_operations = self.rebalance(parent, "Delete")
        return rebalance_operations

    """returns the successor of the given node

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        @rtype: AVLNode
        @returns: the node with the smallest key that is greater than the key of the given node
        """

    def Successor(self, node):
        current = node.right
        while current.left.key is not None:
            current = current.left
        return current
    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        stack = []
        array = []
        curr = self.root
        while curr.is_real_node() or len(stack) != 0:
            while curr.is_real_node():
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            array.append((curr.key, curr.value))
            curr = curr.right
        return array

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.amountofnodes

    """splits the dictionary at the i'th index

    @type node: AVLNode
    @pre: node is in self
    @param node: The intended node in the dictionary according to whom we split
    @rtype: list
    @returns: a list [left, right], where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):
        # initiate left and right trees with left and right children of node as root
        l_tree = AVLTree()
        if node.left.is_real_node():  # if node has smaller children
            l_tree.root = node.left
        # else: left stays empty
        r_tree = AVLTree()
        if node.right.is_real_node():  # if node has larger children
            r_tree.root = node.right
        # else: right stays empty
        if node == self.root:  # no spliting to do
            return l_tree, r_tree
        curr = node.parent
        prev = node
        while curr != None:
            if curr.key < prev.key:
                temp_tree = AVLTree()
                temp_tree.root = curr.left
                l_tree.join(temp_tree, curr.key, curr.value)
            else:
                temp_tree = AVLTree()
                temp_tree.root = curr.right
                r_tree.join(temp_tree, curr.key, curr.value)
            prev = curr
            curr = curr.parent
        return l_tree, r_tree


    """joins self with key and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: The key separting self with tree2
    @type val: any 
    @param val: The value attached to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def join(self, tree2, key, val):
        node = AVLNode(key, val)
        # empty trees cases
        if not self.root.is_real_node() or not tree2.root.is_real_node():
            if self.root.is_real_node():
                self.insert(key, val)
            elif tree2.root.is_real_node():
                tree2.insert(key, val)
                self.root = tree2.root
                self.amountofnodes = tree2.amountofnodes
            else:
                self.insert(key, val)
            return self.root.get_height() + 1

        # assuring tree2 keys are larger than self keys
        if self.root.key > tree2.root.key:
            temp = self.root
            self.root = tree2.root
            tree2.root = temp
        h1 = self.root.height
        h2 = tree2.root.height
        # joining the 2 trees makes legal AVL Tree
        if abs(h1 - h2) <= 1:
            a = self.root
            b = tree2.root
            node.set_right(b)
            node.set_left(a)
            a.set_parent(node)
            b.set_parent(node)
            self.root = node
            self.root.height = 1 + max(node.left.height, node.right.height)
        else:
            # tree2 is higher
            if h1 + 1 < h2:
                a = self.root
                a.parent = node
                node.left = a
                curr = tree2.root
                broken = False
                while curr.get_height() >= h1 + 1:
                    if curr.left.is_real_node():
                        curr = curr.left
                    else:
                        b = curr.left
                        c = curr
                        broken = True
                        break
                if not broken:
                    b = curr
                    c = curr.parent
                b.parent = node
                c.left = node
                node.right = b
                node.parent = c
                # update root of joined tree
                self.root = tree2.root
            # self is bigger than tree2
            else:
                b = tree2.root
                b.parent = node
                node.right = b
                curr = self.root
                broken = False
                while curr.height >= h2 + 1:
                    if curr.right.is_real_node():
                        curr = curr.right
                    else:
                        a = curr.right
                        c = curr
                        broken = True
                        break
                if not broken:
                    a = curr
                    c = curr.parent
                a.parent = node
                c.right = node
                node.left = a
                node.parent = c
            # root doesn't change
            # rebalance if needed
            self.rebalance(c)

        # update size of self
        self.amountofnodes += tree2.amountofnodes + 1
        return abs(h1 - h2) + 1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root


# Rebalancing methods

    def update_height(self, node):
        if node.key is None or not node.is_real_node():
            return -1
        node.height = 1 + max(node.left.get_height(), node.right.get_height())
        return node.height


    def left_rotate(self, node):
        right_child = node.right
        node.set_right(right_child.get_left())
        if right_child.get_left() is not None:
            right_child.get_left().set_parent(node)

        right_child.set_parent(node.get_parent())

        if node.get_parent() is None:
            self.root = right_child
        elif node == node.get_parent().get_left():
            node.get_parent().set_left(right_child)
        else:
            node.get_parent().set_right(right_child)

        right_child.set_left(node)
        node.set_parent(right_child)

        # Update heights
        old_height = node.height
        node.set_height(max(self.update_height(node.left), self.update_height(node.right)) + 1)
        node.is_height_changed = node.height != old_height
        right_old_height = right_child.height
        right_child.set_height(max(self.update_height(right_child.left), self.update_height(right_child.right)) + 1)
        right_child.is_height_changed = right_old_height != right_child.height

    def right_rotate(self, node):
        left_child = node.left
        node.set_left(left_child.get_right())
        if left_child.get_right() is not None:
            left_child.get_right().set_parent(node)

        left_child.set_parent(node.get_parent())

        if node.get_parent() is None:
            self.root = left_child
        elif node == node.get_parent().get_right():
            node.get_parent().set_right(left_child)
        else:
            node.get_parent().set_left(left_child)

        left_child.set_right(node)
        node.set_parent(left_child)

        # Update heights
        old_height = node.height
        node.set_height(max(self.update_height(node.left), self.update_height(node.right)) + 1)
        node.is_height_changed = node.height != old_height
        left_old_height = left_child.height
        left_child.set_height(max(self.update_height(left_child.left), self.update_height(left_child.right)) + 1)
        left_child.is_height_changed = left_child.height != left_old_height


    def rebalance(self, node, str = "Insert"):
        rebalancing_operations = 0
        while node is not None:
            balance = node.get_balance()
            #Case 3.2
            if -2<balance<2 and not node.is_height_changed:
                if str == "Delete":
                    node = node.parent
                    continue
                break
            elif -2<balance<2 and node.is_height_changed:
                node = node.parent
                rebalancing_operations += 1
                continue
            else:
                # Left heavy
                if balance > 1:
                    # Left Right Case
                    if node.left.get_balance() < 0:
                        self.left_rotate(node.left)
                        rebalancing_operations += 1
                    self.right_rotate(node)
                    rebalancing_operations += 1
                # Right heavy
                elif balance < -1:
                    # Right Left Case
                    if node.right.get_balance() > 0:
                        self.right_rotate(node.right)
                        rebalancing_operations += 1
                    self.left_rotate(node)
                    rebalancing_operations += 1
                node = node.parent
        return rebalancing_operations

