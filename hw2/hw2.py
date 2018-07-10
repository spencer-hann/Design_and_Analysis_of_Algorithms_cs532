import random
import test

class Tree:
    def __init__(self):
        self.root = None

    def Insert(self,z):
        if not self.root:
            self.root = z
            return
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if z.key < y.key:
            y.left = z
        else:
            y.right = z

    def Transplant(self,u,v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def Delete(self,z):
        if z.left is None:
            self.Transplant(z,z.right)
        elif z.right is None:
            self.Transplant(z,z.left)
        else:
            y = z.right.Min()
            if y.parent is not None:
                self.Transplant(y,y.right)
                y.right = z.right
                y.right.parent = y
            self.Transplant(z,y)
            y.left = z.left
            y.left.parent = y

    def __str__(self):
        if self.root:
            return self.__to_string(self.root.left) \
                + str(self.root.key) \
                + self.__to_string(self.root.right)
        return ""

    def __to_string(self, root):
        if root is None:
            return ""
        return ("("
            + self.__to_string(root.left)
            + str(root.key)
            + self.__to_string(root.right)
            + ")")

    def basic_tree(self):
        self.root = None
        self.Insert(Node(8))
        self.Insert(Node(4))
        self.Insert(Node(2))
        self.Insert(Node(6))
        self.Insert(Node(12))
        self.Insert(Node(10))
        self.Insert(Node(14))
        self.Insert(Node(1))
        self.Insert(Node(3))
        self.Insert(Node(5))
        self.Insert(Node(7))
        self.Insert(Node(9))
        self.Insert(Node(11))
        self.Insert(Node(13))
        self.Insert(Node(15))

    def even_tree(self):
        self.root = None
        self.Insert(Node(8))
        self.Insert(Node(4))
        self.Insert(Node(2))
        self.Insert(Node(6))
        self.Insert(Node(12))
        self.Insert(Node(10))
        self.Insert(Node(14))

    def Insert_test(self):
        print("testing insert into empty tree\nTest: ",end='')
        self.root = None
        self.Insert(Node(1))
        if str(self) != "1":
            print("Failed")
            return 0
        print("Passed")

        self.even_tree()
        print("basic tree: " + str(self))
        if str(self) != "((2)4(6))8((10)12(14))":
            print("error w/ testing string")
            return 0

        print("Inserting:  14")
        self.Insert(Node(14))
        test = str(self)
        print(test + "\nTest:",end='')
        if test != "((2)4(6))8((10)12(14(14)))":
            print("Failed")
            return 0
        else:
            print("Passed")

        print("Inserting:  4")
        self.Insert(Node(4))
        test = str(self)
        print(test + "\nTest:",end='')
        if test != "((2)4((4)6))8((10)12(14(14)))":
            print("Failed")
            return 0
        else:
            print("Passed")

        return 1

    @staticmethod
    def Delete_test():
        tree = Tree()
        tree.basic_tree()
        string = str(tree)
        print("Delete Test: \n" + string)
        if string != "(((1)2(3))4((5)6(7)))8(((9)10(11))12((13)14(15)))":
            print("Error building tree")
            return False

        print("deleting:  root")
        tree.Delete(tree.root)
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "(((1)2(3))4((5)6(7)))9((10(11))12((13)14(15)))":
            print("Passed")
        else: print("Failed"); return 0;

        print("deleting:  root")
        tree.Delete(tree.root)
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "(((1)2(3))4((5)6(7)))10((11)12((13)14(15)))":
            print("Passed")
        else: print("Failed"); return 0;

        print("deleting:  min")
        tree.Delete(tree.root.Min())
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "((2(3))4((5)6(7)))10((11)12((13)14(15)))":
            print("Passed")
        else: print("Failed"); return 0;

        print("deleting:  min")
        tree.Delete(tree.root.Min())
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "((3)4((5)6(7)))10((11)12((13)14(15)))":
            print("Passed")
        else: print("Failed"); return 0;

        print("deleting:  max")
        tree.Delete(tree.root.Max())
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "((3)4((5)6(7)))10((11)12((13)14))":
            print("Passed")
        else: print("Failed"); return 0;

        print("deleting:  max")
        tree.Delete(tree.root.Max())
        string = str(tree)
        print (string + "\nTest:  ",end='')
        if string == "((3)4((5)6(7)))10((11)12(13))":
            print("Passed")
        else: print("Failed"); return 0;

        print("finishing...")
        while tree.root:
            tree.Delete(tree.root)
            print(tree)

        return True


    def height(self):
        if self.root:
            return self.root.height()
        return 0

    @staticmethod
    def avg_height_test():
        i = 1000
        sum_ = 0

        while i:
            lst = list(range(0, 1024)) #exclusive bounds
            tree = Tree()
            j = 1024
            while j:
                j -= 1
                tree.Insert(Node(lst.pop(random.randint(0,j))))
            sum_ += tree.height()
            i -= 1

        return sum_ / 1000.0

class Node:
    def __init__(self,k):
        self.key = k
        self.left = None
        self.right = None
        self.parent = None

    def InOrderWalk(self):
        s = ""
        if self.left is not None:
            s += self.left.InOrderWalk()
        s += str(self.key)
        if self.right is not None:
            s += self.right.InOrderWalk()
        return s

    @staticmethod
    def InOrderWalk_test():
        tree = Tree()
        tree.basic_tree()
        if tree.root.InOrderWalk() != "123456789101112131415":
            return False
        if tree.root.left.InOrderWalk() != "1234567":
            return False
        if tree.root.right.InOrderWalk() != "9101112131415":
            return False
        if tree.root.Min().InOrderWalk() != "1":
            return False
        return True

    def Search(self,k):
        if k ==self.key:
            return self
        if k < self.key and self.left is not None:
            return self.left.Search(k)
        if k > self.key and self.right is not None:
            return self.right.Search(k)
        return None

    @staticmethod
    def Search_test():
        tree = Tree()
        tree.basic_tree()
        if tree.root.Search(8) == None:
            return False
        if tree.root.right.Search(8) != None:
            return False
        if tree.root.Search(1) == None:
            return False
        if tree.root.left.Search(1) == None:
            return False
        if tree.root.right.Search(1) != None:
            return False
        if tree.root.Search(2) == None:
            return False
        if tree.root.Search(-1) != None:
            return False
        if tree.root.Search(12) == None:
            return False
        if tree.root.right.Search(12) == None:
            return False
        if tree.root.Search(10) == None:
            return False
        if tree.root.Search(11) == None:
            return False
        if tree.root.Search(7) == None:
            return False
        return True

    def Min(self):
        x = self
        while x.left is not None:
            x = x.left
        return x

    @staticmethod
    def Min_test():
        tree = Tree()
        tree.basic_tree()
        if tree.root.Min().key != 1:
            return False
        if tree.root.left.Min().key != 1:
            return False
        if tree.root.right.Min().key != 9:
            return False
        return True

    def Max(self):
        x = self
        while x.right is not None:
            x = x.right
        return x

    def Succ(self):
        x = self
        if x.right is not None:
            return x.right.Min()
        y = x.parent
        while y is not None and x == y.right:
            x = y
            y = y.parent
        return y

    @staticmethod
    def Succ_test():
        tree = Tree()
        tree.basic_tree()
        if tree.root.Succ().key != 9:
            return False
        if tree.root.right.Succ().key != 13:
            return False
        if tree.root.left.Succ().key != 5:
            return False
        if tree.root.Min().Succ().key != 2:
            return False
        if tree.root.Search(9).Succ().key != 10:
            return False
        if tree.root.Max().Succ() != None:
            return False
        return True

    def height(self):
        if self.left:
            left = self.left.height()
        else:
            left = 0
        if self.right:
            right = self.right.height()
        else:
            return left + 1
        return (left if left > right else right) + 1


#tree=Tree()
#if tree.Insert_test(): print("All tests Passed")
#if Tree.Delete_test(): print("All tests passed.")
#if Node.Search_test(): print("Search Test Passed")
#else: print("Search Test Failed")
#if Node.Min_test(): print("Min Test Passed")
#else: print("Min Test Failed")
#if Node.Succ_test(): print("Succ Test Passed")
#else: print("Succ Test Failed")
if Node.InOrderWalk_test(): print("InOrderWalk Test Passed")
else: print("InOrderWalk Test Failed")
#print("Average height test: " + str(Tree.avg_height_test()))
