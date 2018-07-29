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
    return b[N-1][weight]

def display(table):
    for i in range(len(table)):
        for j in table[i]:
            print("%i " % (j),end='')
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

    return table[len(v)-1][W-1], find_path(table, len(v)-1, W-1, v, w)

def find_path(table, i, j, v, w):
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
    def __init__(self, length=0):
        if length:
            self.heap = [0 for i in range(length)]
        else: # undetermined size if none is given
            self.heap = []
        self.len = length
        self.size = -1

    def __len__(self):
        return self.size

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
        return (i-1)/2

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

    def valid_index(self, i, i2=0):
        return i>=0 and i<=self.size and i2>=0 and i2<=self.size

    def heapify(self,i):
        A = self # to match textbook
        if not A.valid_index(i): return
        l = left(i)
        r = rght(i)
        if A.valid_index(l,r) and A[l] < A[r]:
            smallest = l
        else: smallest = i
        if A.valid_index(r) and A[r] < A[smallest]:
            smallest = r
        if smallest != i:
            A.exchange(i,smallest)
            A.heapify(smallest)

    def build(self):
        if self.size < 0:
            from random import shuffle
            self.heap = [i for i in range(self.len)]
            shuffle(self.heap)
        self.size = self.len-1

        for i in range(self.size, -1, -1):
            self.heapify(i)

    def extract(A):
        if A.size < 0: return None
        min_ = A[0]
        A[0] = A[A.size]
        A.size -= 1
        A.heapify(0)
        return min_

    def insert(self, val):
        if self.size == self.len:
            print("heap is full")
            return
        self[self.size] = val
        self.size += 1
        while i > 0 and self[prnt(i)] > self[i]:
            self.exchange(prnt(i),i)
            i = prnt(i)


# min_heap static funcs:
prnt = min_heap.parent
left = min_heap.left
rght = min_heap.right

v = [2,1,3,4]
w = [2,1,3,4]
W = 6

#print(knapsack2(W,w,v))
#print(version1(w,v,W))
heap = min_heap(10)
heap.build()
print()
print(heap)
while(heap.size >= 0):
    print("size:" + str(heap.size))
    print("min: " + str(heap.extract()))
    print("heap: " + str(heap))
