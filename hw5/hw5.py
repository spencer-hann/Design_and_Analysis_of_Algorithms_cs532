def pair_sort(w,v):
    l = list(zip(w,v))
    l.sort(key=lambda k: k[0])
    w = [x[0] for x in l]
    v = [x[1] for x in l]
    return w, v

def version1(w_array,v_array,weight):
    N = len(w_array)
    b = [[0 for w in range(weight+1)] for i in range(N)]
    for w in range(weight+1):
        b[0][w] = 0
        if w_array[0] <= w:
            b[0][w] = v_array[0]
        for i in range(1,N):
            b[i][w] = b[i-1][w]
            if w_array[i] <= w:
                bI = b[i-1][w-w_array[i]] + v_array[i]
                if (bI > b[i][w]):
                    b[i][w] = bI
    return b[N-1][weight], find_path(b, N-1, weight, v_array, w_array)

def knapsack3(W,w,v):
    table = [[None for j in range(W+1)] for i in range(len(v))]
    val = knapsack3_(w,v,table,len(v)-1,W)
    sol = find_path(table, len(v)-1, W, v, w)
    return val, sol

def knapsack3_(w,v,table,i,j):
    if j == 0 or i == 0:
        table[i][j] = 0 if w[0] > j else v[0]
        #display(table)
        return table[i][j]
    if table[i-1][j] == None:
        table[i][j] = knapsack3_(w,v,table,i-1,j)
    else: table[i][j] = table[i-1][j]
    if w[i] <= j:
        if table[i-1][j-w[i]] == None:
            tmp = knapsack3_(w,v,table,i-1,j-w[i])
        else: tmp = table[i-1][j-w[i]]
        tmp += v[i]
        if tmp > table[i][j]:
            table[i][j] = tmp
    #display(table)
    return table[i][j]


def find_path(table, i, j, v, w):
    sol = []
    #display(table)

    while i > 0 and j > 0:
        if table[i][j] != table[i-1][j]:
            j -= w[i]
            sol += [(w[i],v[i])]
        i -= 1

    if j>0: sol += [(w[i],v[i])]

    return sol

def display(table):
    print()
    for i in range(len(table)):
        for j in table[i]:
            if j != None:
                print("{0} ".format(j),end='')
            else:
                print('x ',end='')
        print()

def knapsack1(W,w,v):
    #w,v = pair_sort(w,v)
    table = [[0 for i in range(W)] for j in range(len(v))]

    for i in range(W):
        table[0][i] = v[0] if w[0] <= i+1 else 0

    for i in range(1,len(v)):
        for j in range(W):
            if w[i] <= j+1:
                if j-w[i] < 0: #check bounds of table
                    table[i][j] = max(table[i-1][j], v[i])
                else:
                    table[i][j] = max(table[i-1][j], table[i-1][j-w[i]] + v[i])
            else:
                table[i][j] = table[i-1][j]

    return table[len(v)-1][W-1]

def knapsack2(W,w,v):
    #w,v = pair_sort(w,v)
    table = [[0 for i in range(W)] for j in range(len(v))]

    for i in range(W):
        table[0][i] = v[0] if w[0] <= i+1 else 0
    for i in range(1,len(v)):
        for j in range(W):
            if w[i] <= j+1:
                if j-w[i] < 0: #check bounds of table
                    table[i][j] = max(table[i-1][j], v[i])
                else:
                    table[i][j] = max(table[i-1][j], table[i-1][j-w[i]] + v[i])
            else:
                table[i][j] = table[i-1][j]

    return table[len(v)-1][W-1], find_path_old(table, len(v)-1, W-1, v, w)

def find_path_old(table, i, j, v, w):
    sol = []
    #display(table)

    while i > 0 and j >= 0:
        if table[i][j] != table[i-1][j]:
            j -= w[i]
            sol += [(w[i],v[i])]
        i -= 1

    if i >= 0 and j >= 0:
        sol += [(w[i],v[i])]

    return sol

class min_heap:
    def __init__(self, length=5):
        self.heap = [0 for i in range(length)]
        self.len = length
        self.size = -1

    def __getitem__(self, i):
        return self.heap[i]

    def __setitem__(self, i, x):
        self.heap[i] = x

    def __str__(self):
        s = ""
        for i in range(self.size+1):
            s += str(self[i]) + ", "
        return s[:-2]

    @staticmethod
    def parent(i):
        return (i-1)//2 if i > 0 else 0

    @staticmethod
    def left(i):
        return 2*(i+1)

    @staticmethod
    def right(i):
        return 2*(i+1) - 1

    def exchange(self, a, b):
        tmp = self[a]
        self[a] = self[b]
        self[b] = tmp

    def heapify_original(self,i):
        A = self # to match textbook
        if i < 0 or i > A.size: return
        l = left(i)
        r = rght(i)
        if l <= A.size and A[l] < A[i]:
            smallest = l
        else: smallest = i
        if r <= A.size and A[r] < A[smallest]:
            smallest = r
        if smallest != i:
            A.exchange(i,smallest)
            A.heapify(smallest)

    def heapify(self,i):
        A = self # to match textbook
        if i < 0 or i > A.size: return

        while(1):
            l = left(i)
            r = rght(i)
            if l <= A.size and A[l] < A[i]:
                smallest = l
            else: smallest = i
            if r <= A.size and A[r] < A[smallest]:
                smallest = r
            if smallest != i:
                A.exchange(i,smallest)
                i = smallest
                continue
            return

    def heap_check(self):
        for i in range(self.size):
            if self[i] < self[prnt(i)]:
                return False
        return True

    def build(self):
        if self.size < 0:
            from random import shuffle
            self.heap = [i for i in range(self.len)]
            shuffle(self.heap)
            self.size = self.len-1

        for i in range(self.size//2, -1, -1):
            self.heapify(i)
        #if not self.heap_check(): print("ERROR: "+str(self))

    def extract(A):
        if A.size < 0: return None
        min_ = A[0]
        A[0] = A[A.size]
        A.size -= 1
        A.heapify(0)
        return min_

    def insert(self, val):
        if self.size == self.len-1:
            print("heap is full")
            return 0
        self.size += 1
        i = self.size
        self[i] = val

        while i > 0 and self[prnt(i)] > self[i]:
            self.exchange(prnt(i),i)
            i = prnt(i)
        return 1

    @staticmethod
    def test():
        t = min_heap(50)
        print("Performing build tests...")
        for i in range(10000):
            t.build()
            if not t.heap_check():
                print("Heap check Failed")
                return 0
            t.size = -1 # reset so that build will reshuffle
        print("tests passed.")

        print("Performing extract tests...")
        l = []
        comp = [i for i in range(t.len)]
        for i in range(10000):
            t.build()
            while t.size > -1:
                l.append(t.extract())
            if l != comp:
                print("Extract failed")
                print("list should be sorted: ")
                print(l)
                return 0
            l.clear()
            t.size = -1
        print("tests passed.")
        print("All tests passed.")
        return 1



# min_heap static funcs:
prnt = min_heap.parent
left = min_heap.left
rght = min_heap.right


import random
for i in range(100000):
    v = [random.randint(1,50) for i in range(20)]
    w = [random.randint(1,50) for i in range(20)]
    W = random.randint(1,100)
    a = version1(w,v,W)
    b = knapsack3(W,w,v)
    if a != b:
        print("Error")
        print("v, w")
        for j in range(len(v)):
            print("{0}, {1}".format(v[j],w[j]))
        break
    print(a)
    print(b)
