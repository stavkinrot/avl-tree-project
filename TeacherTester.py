''' In order to run the tester:
    1.  Make sure your AVLTree.py file and AVLTreeTester2022.py
        file are both in the same directory.
    2.  Run your AVLTree.py file
    3.  Run the AVLTreeTester2022.py file
    4.  Your grade should be written in the terminal.
        Only failed tests will be presented in the terminal,
        together with the AssertionError that made them fail.


    Note: if you want to see the time each test took, add the following commands:
    1. Add this to def setUp(cls) method - cls.start_time = time.time()
    2. Add this method:
        def tearDown(self):
            t = time.time() - self.start_time
            print("%s: %.3f " % (self.id()[31:], t))
'''


import time
import unittest, random
import numpy as np
from AVLTree import AVLNode , AVLTree


GRADE = 0
MAX_GRADE = 70
NUMBER_OF_TESTS = 32
PASSED_TESTS = 0


class AVLTreeTester2022(unittest.TestCase):


    @staticmethod
    def add_points(x: float, is_the_test_finished = True):
        global GRADE, PASSED_TESTS
        GRADE += x
        if is_the_test_finished:
            PASSED_TESTS += 1


    @staticmethod
    def in_order(tree: AVLTree):
        lst = []
        def in_order_rec(node: AVLNode, in_order_lst: list[str]):
            if node is not None and node.is_real_node():
                in_order_rec(node.get_left(), in_order_lst)
                in_order_lst.append(node.get_value())
                in_order_rec(node.get_right(), in_order_lst)
        in_order_rec(tree.get_root(), lst)
        return lst


    @classmethod
    def setUp(cls):
        cls.tree = AVLTree()
        cls.tree_2 = AVLTree()

    @staticmethod
    def create_tree(values, random_order = False):
        if random_order: random.shuffle(values)
        tree = AVLTree()
        for val in values:
            tree.insert(val ,str(val))
        return tree


    def test_basic_avl_node_get(self):
        self.tree.insert(2,"2")
        self.tree.insert(1,"1") #    '2'
        self.tree.insert(3,"3") # '1'   '3'
        root = self.tree.get_root()
        self.assertTrue(root.is_real_node(), "FAIL - root should be a real node")
        self.assertEqual(root.get_height(), 1)
        self.assertTrue(root.get_left().is_real_node())
        self.assertTrue(root.get_right().is_real_node())
        self.assertEqual(root.get_left().get_height(), 0)
        self.assertEqual(root.get_right().get_height(), 0)
        self.assertEqual(root.get_left().get_parent(), root)
        self.assertEqual(root.get_right().get_parent(), root)
        self.add_points(20)


    def test_empty_tree(self):
        self.assertTrue(self.tree.size() == 0, "FAIL - tree.empty() on a new tree should return True")
        self.add_points(2)

    def test_left_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([30, 25, 35, 40])
        self.assertEqual(1 , avl_tree.delete(avl_tree.search(25)) , "FAIL in left rotation after deletion")
        self.add_points(0.5)

    def test_right_left_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([9, 8, 11, 10])
        self.assertEqual(2 , avl_tree.delete(avl_tree.search(8)) , "FAIL in right-left rotation after deletion")
        self.add_points(0.5)

    def test_left_right_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([10, 8, 11, 9])
        self.assertEqual(2 , avl_tree.delete(avl_tree.search(11)) , "FAIL in left-right rotation after deletion")
        self.add_points(0.5)

    def test_right_rotation_after_deletion(self):
        # Example from slide 84 in AVL tree presentation from moodle
        avl_tree = self.create_tree([3, 2, 4, 1])
        self.assertEqual(1 , avl_tree.delete(avl_tree.search(4)) , "FAIL in right rotation after deletion")
        self.add_points(0.5)



    def test_single_rotations_on_linear_insertions_and_deletions(self): #TODO CHECK THIS

        avl_tree = AVLTree()

        self.assertEqual(0 ,avl_tree.insert(1 , "1") ,  "FAIL - after inserting one node into an empty tree, zero rotations should be done")
        self.assertEqual(1 ,avl_tree.insert(2 , "2") , "FAIL - after inserting 1 ,2  into an empty tree, zero rotations and one height change should be done")
        self.assertEqual(2 , avl_tree.insert(3 , "3") , "FAIL - after inserting 1 ,2 , 3 into an empty tree, 1 rotation and one height changeshould be done")
        self.assertEqual(2, avl_tree.insert(4 , "4")  , "FAIL - after inserting 4 into a tree that had 1 ,2 ,3 inserted prior, zero rotations and 2 height changes should be done")
        self.assertEqual(2 , avl_tree.insert(5 , "5") , "FAIL - after inserting 5 into a tree that had 1 ,2 ,3 ,4 inserted prior, 1 rotation should be done and one height change should be done")
        self.add_points(0.5 , False)

        for i in range(6,13):
            avl_tree.insert(i , str(i))

        avl_tree.delete(avl_tree.search(9))
        self.assertEqual(0 ,avl_tree.delete(avl_tree.search(11)) ,  "FAIL - after inserting 1 ,2 ,3 ,4 ,5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 and then deleting 9 and 11, zero rotations should be done on second deletion")
        self.add_points(0.5)

    def test_delete_operations_simple_1(self):
        self.tree.insert(2,"2")
        self.tree.insert(1,"1")
        self.tree.insert(3,"3")
        #   2
        # 1   3
        self.assertEqual(self.tree.delete(self.tree.search(1)), 0, "FAIL - deleting '1' should cost 0 re-balancing op")
        self.assertEqual(self.tree.delete(self.tree.search(3)), 1, "FAIL - deleting '3' should cost 1 re-balancing op")
        self.assertEqual(self.tree.delete(self.tree.search(2)), 0, "FAIL - deleting '2' should cost 0 re-balancing op")
        self.add_points(0.5)


    def test_delete_operations_simple_2(self):
        # From slide 90 in AVL presentatin from moodle
        avl_tree = self.create_tree([15, 8, 22, 4 ,20, 11, 24, 2, 18, 9, 12, 13])

        self.assertEqual(avl_tree.size() , 12 , "FAIL - Before deletion, size of tree from slide 90 in AVL presentation should be 12")
        self.assertEqual(15 , avl_tree.get_root().get_key() ,  "FAIL - Before deletion, root of tree from slide 90 in AVL presentation should be 15")

        self.add_points(1 , False)

        # Delete root
        self.assertEqual(3 , avl_tree.delete(avl_tree.search(24)))
        self.assertEqual(avl_tree.get_root().get_key(), 11, "FAIL - After deleting 24 in tree from slide 90 in AVL presentation, root should be 11")
        self.add_points(1, False)

        self.assertEqual(3 , avl_tree.get_root().get_height() , "FAIL - After deleting 24 in tree from slide 90 in AVL presentation, root height should be 3")
        self.add_points(1)


    def test_do_10000_insertions_and_deletions(self):
        avl_tree = AVLTree()
        for i in range(10000):
            avl_tree.insert(i, "num" + str(i))

        # Check tree size after insertions
        self.assertEqual(avl_tree.size() , 10000 , "FAIL - after 10000 insertions, size should be 10000")

        for i in range(10000):
            avl_tree.delete(avl_tree.get_root())

        self.assertEqual(avl_tree.size() , 0 , "FAIL - after deleting all nodes size should be 0")
        self.add_points(2)

    def test_order_after_insertions(self):
        test_list = [23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000]
        avl_tree = AVLTree()
        for num in test_list:
            avl_tree.insert(num , str(num))

        self.assertEqual(avl_tree.get_root().get_height() , 3 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - height of root should be 3")
        self.assertEqual(avl_tree.get_root().get_key() , 23 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root should be 23")
        self.assertEqual(avl_tree.get_root().get_left().get_key() , 2 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's left son should be 2")
        self.assertEqual(avl_tree.get_root().get_right().get_key(), 60, "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's right son should be 60")
        self.add_points(3)

    def test_order_after_deletions(self):
        test_list = [23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000]

        avl_tree = AVLTree()
        for num in test_list:
            avl_tree.insert(num , str(num))

        self.assertEqual(avl_tree.delete(avl_tree.search(1)) , 0 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , zero rotations should be done")
        self.assertEqual(avl_tree.delete(avl_tree.search(2)), 1, "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 and 2 , 1 rotation should be done")
        self.assertEqual(avl_tree.get_root().get_height() , 2 , "FAIL -  after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 ,2 - height should be 2")

        self.assertEqual(avl_tree.delete(avl_tree.search(999)), 0, "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , 2 and 999, zero rotations should be done")
        self.assertEqual(avl_tree.delete(avl_tree.search(33)), 0, "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 and then deleting 1 , 2 , 999 and 33, zero rotations should be done")
        self.add_points(3)

    def test_delete_first_check_size(self):
        real_length = 0
        for i in range(100):
            self.tree.insert(i,str(i))
            real_length += 1
            self.assertEqual(real_length , self.tree.size() , "FAIL: Tree size incorrect")
        for i in range(99):
            self.tree.delete(self.tree.search(i))
            real_length -= 1
            self.assertEqual(real_length, self.tree.size(), "FAIL: Tree size incorrect")

        self.add_points(1)


    def test_list_to_array_empty(self):
        self.assertEqual(self.tree.avl_to_array(), [], "FAIL - avl_to_array() should return [] for an empty tree")
        self.tree.insert(1,"1")
        self.assertNotEqual(self.tree.avl_to_array(), [], "FAIL - avl_to_array() should not return [] for a non-empty tree")
        self.add_points(1)


    def test_avl_to_array_identical_vals(self):
        lst = [i for i in range(1000)]
        copy = []
        for i in range(1000):
            copy.append((i , str(i)))
        random.shuffle(lst)
        T = self.create_tree(lst)
        self.assertEqual(copy,T.avl_to_array(), "FAIL - avl_to_array() is not consistent with the insertion order provided")
        self.add_points(1)


    def test_avl_to_array_random(self):

        python_list_numbers = []

        for i in range(50):
            random_number = random.randint(0,10000)
            while random_number in python_list_numbers:
                random_number = random.randint(0,10000)
            python_list_numbers.append(random_number)
            self.tree.insert(random_number,str(random_number))

        python_list_numbers.sort()
        python_list = []
        for num in python_list_numbers:
            python_list.append((num , str(num)))
        avl_list = self.tree.avl_to_array()
        self.assertEqual(python_list, avl_list, "FAIL - problem in avl_to_array")
        self.add_points(2)



    def test_size_of_empty_tree(self):
        self.assertEqual(self.tree.size(), 0, "FAIL - tree.size() on an empty tree should return 0")
        self.tree.insert(0,"0")
        self.assertNotEqual(self.tree.size(), 0, "FAIL - tree.length() on a non-empty tree should not return 0")
        self.assertEqual(self.tree.size(), 1, "FAIL - tree.size() a tree with one node should return 1")
        self.add_points(1)


    def test_length_after_insert(self):
        length = 0
        for i in range(10):
            self.tree.insert(10-i,"insert_number_"+str(i))
            length += 1
            self.assertEqual(length, self.tree.size(), "FAIL - Length error, first loop, iteration {}".format(str(i)))
        more_to_add = [11 ,12 ,13 ,14 ,15 ,16 ,17, 18, 19 ,20]
        for i in more_to_add:
            self.tree.insert(i,"insert_number_"+str(i))
            length += 1
            self.assertEqual(length, self.tree.size(), "FAIL - Length error, second loop, iteration {}".format(str(i)))
        self.add_points(1)

    def test_length_after_many_insertions(self):
        length = 0
        avl_tree = AVLTree()
        in_tree = []

        for i in range(100):

            rand_num = random.randint(0, 10000)

            while rand_num in in_tree:
                rand_num = random.randint(0, 10000)

            avl_tree.insert(rand_num , str(rand_num))
            in_tree.append(rand_num)
            length += 1
            self.assertEqual(length, avl_tree.size(), "FAIL - Length error, third loop, iteration {}".format(str(i)))

        self.add_points(1)

    def test_size_after_delete(self):
        for i in range(1000):
            self.tree.insert(i,str(i))
        for j in range(999):
            self.tree.delete(self.tree.get_root())
            self.assertEqual(self.tree.size(), 999 - j, "FAIL - Length error")
        self.tree.delete(self.tree.get_root())
        self.assertEqual(self.tree.size(), 0, "FAIL - Length error after deleting all the nodes from the list")
        self.add_points(2)

    def calc_height_diff(self, tree_1: AVLTree, tree_2: AVLTree):
        if tree_1.empty() and tree_2.empty(): return 0
        elif tree_1.empty(): return tree_2.get_root().get_height() + 1
        elif tree_2.empty(): return tree_1.get_root().get_height() + 1
        return abs(tree_1.get_root().get_height() - tree_2.get_root().get_height())


    def test_split_simple(self):
        avl_tree = AVLTree()
        avl_tree.insert(4, "D")
        avl_tree.insert(2, "B")
        avl_tree.insert(6, "F")
        avl_tree.insert(1, "A")
        avl_tree.insert(3, "C")
        avl_tree.insert(5, "E")
        avl_tree.insert(7, "G")

        key = 4
        left_tree, right_tree = avl_tree.split(avl_tree.search(key))

        left_tree_list = left_tree.avl_to_array()
        actual_left_list = [(1 , "A") , (2 , "B") , (3 , "C")]
        self.assertEqual(left_tree_list , actual_left_list , "FAIL - Split didn't assign correct nodes to splitted trees")
        right_tree_list = right_tree.avl_to_array()
        actual_right_list = [(5, "E") , (6, "F") , (7, "G")]
        self.assertEqual(right_tree_list , actual_right_list , "FAIL - Split didn't assign correct nodes to splitted trees")

        self.add_points(2)


    def test_double_rotation_1(self):
        avl_tree = AVLTree()
        avl_tree.insert(4 , str(4))
        avl_tree.insert(6, str(6))
        self.assertEqual(3 , avl_tree.insert(5, str(5)) , "FAIL: inserting 4 ,6 ,5 into an empty tree should result in a double rotation and a height change")
        self.add_points(1)

    def test_double_rotation_2(self):
        avl_tree = AVLTree()
        avl_tree.insert(6, str(6))
        avl_tree.insert(4 , str(4))

        self.assertEqual(3 , avl_tree.insert(5, str(5)) , "FAIL: inserting 4 ,6 ,5 into an empty tree should result in a double rotation and a height change")
        self.add_points(1)

    def test_join_simple(self):
        left_tree = AVLTree()
        left_tree.insert(2, "B")
        left_tree.insert(1, "A")

        right_tree = AVLTree()
        right_tree.insert(4, "D")
        right_tree.insert(6, "F")
        right_tree.insert(5, "E")

        key = 3

        left_tree.join(right_tree, key, "C")
        correct_array = [(1, "A") , (2, "B") , (3 , "C") , (4, "D") , (5, "E") , (6, "F")]
        self.assertEqual(left_tree.avl_to_array() , correct_array)
        self.add_points(2)


    def test_non_succesful_search(self):
        self.assertEqual(self.tree.search(0), None, "FAIL - tree.search() on an empty tree should return -1")
        for i in range(10):
            self.tree.insert(i, str(i))
        self.assertEqual(self.tree.search(11), None, "FAIL - tree.search() should return None " \
                                                        "whenever val is not in the tree")
        self.add_points(1)


    def test_search(self):
        for i in range(100):
            self.tree.insert(i,str(i))
        for i in range(100):
            self.assertEqual(self.tree.search(i).get_key(),i)
            self.assertEqual(self.tree.search(i).get_value(), str(i))
        self.add_points(1)


    def test_search_complex(self):
        N = 100
        T = self.create_tree([i for i in range(N)],random_order=True)
        in_order = self.in_order(T)
        lst = [str(i) for i in range(N)]
        for i in range(N):
            lst[T.search(i).get_key()] = str(i)
        self.assertEqual(in_order,lst)
        self.add_points(2)


    def test_search_after_delete(self):
        N = 100
        T = self.create_tree([i for i in range(N)], random_order=True)
        for i in range(N):
            self.assertNotEqual(T.search(i), None, "FAIL - search should return None iff str({}) is not in the tree".format(i))
            T.delete(T.search(i))
            self.assertEqual(T.search(i), None, "FAIL - search should return None iff str({}) is not in the tree".format(i))
        self.add_points(1.5)

    def test_split_and_join(self):
        # Create a full tree in order to easily check return value of split
        avl_tree = self.create_tree([10, 5, 20, 2, 11, 6, 21])

        # split on minimum
        left_tree , right_tree = avl_tree.split(avl_tree.search(10))
        # self.assertEqual(3 , left_tree.size() , "FAIL - split") #Test removed for 2024A
        # self.assertEqual(3, right_tree.size(), "FAIL - split") #Test removed for 2024A


        self.assertEqual(1 , left_tree.join(right_tree , 10 , str(10)) , "FAIL - join return value")
        self.add_points(1.5, False)

        avl_tree = self.create_tree([10, 5, 20, 2, 11, 6, 21])
        left_tree, right_tree = avl_tree.split(avl_tree.search(2))
        left_tree.insert(2, str(2))
        self.assertEqual(3 , left_tree.join(right_tree , 3 , str(3)) , "FAIL - join return value")

        self.add_points(1)

    def test_big_join(self):
        N = 100

        left_tree_list = []
        for i in range(N):
            left_tree_list.append((i , str(i)) )
        right_tree_list = []
        for i in range(N+5, 2*N+5):
            right_tree_list.append((i, str(i)))
        left_tree = self.create_tree([i for i in range(N)], random_order=True)
        right_tree = self.create_tree([i for i in range(N+5, 2*N+5)] , random_order=True)

        join_key = N+2
        left_tree.join(right_tree , join_key , str(join_key))
        left_tree_list.append((join_key , str(join_key)))
        left_tree_list.extend(right_tree_list)

        self.assertEqual(left_tree_list , left_tree.avl_to_array() , "FAIL in joining big trees")
        self.add_points(1)

    def test_big_split(self):
        N = 1000
        avl_tree = self.create_tree([i for i in range(N)], random_order=True)
        split_key = 787
        right_tree , left_tree = avl_tree.split(avl_tree.search(split_key))

        right_tree_list = []
        for i in range(787):
            right_tree_list.append((i , str(i)))

        left_tree_list = []
        for i in range(788, N):
            left_tree_list.append((i , str(i)))

        self.assertEqual(left_tree_list, left_tree.avl_to_array(), "FAIL in splitting big tree")
        self.assertEqual(right_tree_list, right_tree.avl_to_array(), "FAIL in splitting big tree")
        self.add_points(1)

    def test_inserts_and_avl_node_functions(self):
        # Example from https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99
        node_list = [41 , 20 , 65 , 11, 29, 50 , 91, 31 , 72 , 99]
        avl_tree = self.create_tree(node_list)

        # Check get_key and get_value
        for i in node_list:
            self.assertEqual(i , avl_tree.search(i).get_key(), "FAIL - get key")
            self.assertEqual(str(i), avl_tree.search(i).get_value(), "FAIL - get value")
        self.add_points(1.5 , False)

        # Check root properties
        self.assertEqual(41, avl_tree.get_root().get_key() , "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root should be 41")
        self.assertNotEqual(False, avl_tree.get_root().is_real_node())
        self.assertIsNone(avl_tree.get_root().get_parent() , "FAIL - Root should have no parent")

        self.add_points(1, False)

        # Check get parent
        roots_right_son = avl_tree.get_root().get_right()
        roots_left_son = avl_tree.get_root().get_left()
        self.assertEqual(avl_tree.get_root() , roots_right_son.get_parent() , "FAIL in get parent")
        self.assertEqual(avl_tree.get_root(), roots_left_son.get_parent(), "FAIL in get parent")
        self.add_points(1, False)

        # Check heights
        roots_right_right_grandson = roots_right_son.get_right()
        self.assertEqual(1, roots_right_right_grandson.get_height(), "FAIL in tree heights")
        self.assertEqual(3, avl_tree.get_root().get_height(), "FAIL in tree heights")
        self.assertEqual(2, roots_right_son.get_height(), "FAIL in tree heights")
        self.add_points(1, False)

        # Check is real node on real nodes
        self.assertNotEqual(False , roots_right_son.is_real_node())
        self.assertNotEqual(False, roots_left_son.is_real_node())
        self.add_points(1, False)

        # Check tree formation
        self.assertEqual(65 , roots_right_son.get_key() , "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root's right son is 65")
        #self.assertEqual(5 , roots_right_son.size() , "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") Test removed for 2024A
        self.assertEqual(20, roots_left_son.get_key(), "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99")
        #self.assertEqual(4 , roots_left_son.size() , "FAIL - tree size incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") #Test removed for 2024A

        self.assertEqual(91 , roots_right_right_grandson.get_key() , "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99")
        self.add_points(1, False)


        # Check virtual node properties
        childless_nodes = [avl_tree.search(11), avl_tree.search(31), avl_tree.search(50), avl_tree.search(72),
                           avl_tree.search(99)]
        for node in childless_nodes:
            self.assertFalse(node.get_right().is_real_node() , "FAIL - is_real_node returns true for virtual node")
            self.assertFalse(node.get_left().is_real_node() , "FAIL - is_real_node returns true for virtual node")
            self.assertEqual(None, node.get_right().get_right(), "FAIL - get_right should return None for a virtual node")
            self.assertEqual(None, node.get_right().get_left(), "FAIL - get_left should return None for a virtual node")
            self.assertEqual(None, node.get_left().get_right(), "FAIL - get_right should return None for a virtual node")
            self.assertEqual(None, node.get_left().get_left(), "FAIL - get_left should return None for a virtual node")
        self.add_points(1)



    @classmethod
    def tearDownClass(self):
        super()
        # print("\n\n")
        # print("==Tester Results:==")
        # print("  # Of Tests: {}    ".format(NUMBER_OF_TESTS))
        # print("Successful Tests: {}".format(PASSED_TESTS))
        # print(" Failed Tests: {}   ".format(NUMBER_OF_TESTS - PASSED_TESTS))
        # print("The Final Grade is: ")
        # print("  {} out of {}      ".format(round(GRADE,1), MAX_GRADE))
        # print("\n\n")
        print(GRADE)

if __name__ == '__main__':
    unittest.main(verbosity = 0)
    #Change verbosity = 0 or verbosity = 2 for less/more details from tests

