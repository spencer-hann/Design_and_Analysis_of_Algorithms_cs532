import random

class Tree:
    def __init__(self):
        self.root = None

    def Insert(self,z):
        if self.root is None:
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
            if y.parent != z:
                self.Transplant(y,y.right)
                y.right = z.right
                y.right.parent = y
            self.Transplant(z,y)
            y.left = z.left
            y.left.parent = y

    def Delete(self,z):
        if z.left is None:
            self.Transplant(z,z.right)
        elif z.right is None:
            self.Transplant(z,z.left)
        else:
            y = z.right.Min()
            y.left = z.left
            z.left.parent = y
            self.Transplant(z,z.right)

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

    def __str__(self):
        s = ""
        if self.left is not None:
            s += "(" + str(self.left) + ")"
        s += str(self.key)
        if self.right is not None:
            s += "(" + str(self.right) + ")"
        return s

    def Height(self):
        r = 0
        l = 0
        if self.left is not None:
            l = self.left.Height()+1
        if self.right is not None:
            r = self.right.Height()+1
        return max(1,r,l)

    def Search(self,k):
        if k ==self.key:
            return self
        if k < self.key and self.left is not None:
            return self.left.Search(k)
        if k > self.key and self.right is not None:
            return self.right.Search(k)
        return None

    def Min(self):
        x = self
        while x.left is not None:
            x = x.left
        return x

    def Max(self):
        x = self
        while x.right is not None:
            x = x.right
        return x

    def Succ(self):
        x = self
        if x.right is not None:
            return x.right.min()
        y = x.parent
        while y is not None and x == y.right:
            x = y
            y = y.parent
        return y

    def CreateList(self):
        l = []
        if self.left:
            l = self.left.CreateList()
        l.append(self.key)
        if self.right:
            l.extend(self.right.CreateList())
        return l

    def CreateListX(self, l):
        if self.left:
            self.left.CreateListX(l)
        l.append(self.key)
        if self.right:
            self.right.CreateListX(l)

def BuildTree1023():
    l = [x for x in range(1,1024)]
    t = Tree()
    while l != []:
        i = int(random.random()*len(l))
        t.Insert(Node(l[i]))
        del l[i]
    orig_height = t.root.Height()
    for i in range(1000):
        x = random.randint(1,1023)
        t.Delete(t.root.Search(x))
        t.Insert(Node(x))
    return orig_height, t.root.Height()

def BuildTrees():
    sum1, sum2 = 0, 0
    for i in range(1000):
        a, b = BuildTree1023()
        sum1 += a
        sum2 += b
        #print(sum1, sum2)
    print("original height: " + str(sum1/1000))
    print("post delete height: " + str(sum2/1000))

def main():
    t = Tree()
    t.Insert(Node(11))
    t.Insert(Node(9))
    t.Insert(Node(7))
    t.Insert(Node(6))
    t.Insert(Node(5))
    t.Insert(Node(3))
    t.Insert(Node(2))
    print(str(t.root))
    print(t.root.Height())

    BuildTrees()

if __name__ == "__main__":
    # execute only if run as a script 
    main()

