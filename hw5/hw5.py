def pair_sort(w,v):
    l = list(zip(w,v))
    l.sort(key=lambda k: k[0])
    w = [x[0] for x in l]
    v = [x[1] for x in l]
    return w, v

def display(table):
    for i in range(len(table)):
        for j in table[i]:
            print("%i " % (j),end='')
        print()

def knapsack1(W,w,v):
    w,v = pair_sort(w,v)
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
    w,v = pair_sort(w,v)
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


v = [9,10,12, 20]
w = [2,1,3,4]
W = 6

print(knapsack2(W,w,v))
