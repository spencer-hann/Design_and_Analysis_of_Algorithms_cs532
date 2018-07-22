from timeit import default_timer as timer;
from math import inf

class Alignmt:
    def __init__(self, v=inf, s=""):
        # initialize 'best' score to 
        # infinity for first comparison
        self.score = v
        self.str = s

    def __gt__(self, op):
        return self.score > op

    def __lt__(self, op):
        return self.score < op

    def __eq__(self, op):
        return self.score == op

    def __str__(self):
        return "%i %s" % (self.score, self.str)
    __repr__ = __str__

def version1(str1, str2, x=0, y=0, path=""):
    if x > len(str1) or y > len(str2):
        return
    if x == len(str1) and y == len(str2):
        print(path)
        return

    version1(str1, str2, x+1, y, path + '-')
    version1(str1, str2, x, y+1, path + '|')
    version1(str1, str2, x+1, y+1, path + '\\')

def exp_test():
    lst = []
    lst_ = []
    print("n:\ttime:")
    for i in range(10):
        lst.append(i)
        lst_.append(i)
        start = timer();
        version1(lst,lst_,0,0,"")
        end = timer();
        print(str(i+1) +"\t"+ str(end-start))

def version2(str1, str2, x=0, y=0, path="", score=0):
    if x > len(str1) or y > len(str2):
        return
    if x == len(str1) and y == len(str2):
        print(score,end=" ")
        print(path)
        return

    version2(str1, str2, x+1, y, path + '-', score+1)
    version2(str1, str2, x, y+1, path + '|', score+1)
    if x < len(str1) and y < len(str2):
        if str1[x] == str2[y]:
            version2(str1, str2, x+1, y+1, path + '\\', score)
        else:
            version2(str1, str2, x+1, y+1, path + '\\', score+1)

def version3(input1, input2):
    output = Alignmt()
    _version3(output, input1, input2)
    print(output)

def _version3(best, str1, str2, x=0, y=0, path="", score=0):
    if x > len(str1) or y > len(str2):
        return
    if x == len(str1) and y == len(str2):
        if best > score:
            best.score = score
            best.str = path
        return

    _version3(best, str1, str2, x+1, y, path+'-', score+1)
    _version3(best, str1, str2, x, y+1, path+'|', score+1)
    if x < len(str1) and y < len(str2):
        if str1[x] == str2[y]:
            _version3(best, str1, str2, x+1, y+1, path+'\\', score)
        else:
            _version3(best, str1, str2, x+1, y+1, path+'\\', score+1)

def display(arr):
    x = -1
    y = -1
    while arr.get((x,y)):
        while arr.get((x,y)):
            print(arr[(x,y)],end='\t')
            if len(arr[(x,y)].str) < 6:
                print(end='\t')
            x += 1
        print()
        x = -1
        y += 1
    print()

def version4(input1, input2):
    # init the table's first row and column
    output = {(-1,-1):Alignmt(0)}
    for x in range(len(input1)):
        output[(x,-1)] = Alignmt(x+1,"-"*(x+1))
    for y in range(len(input2)):
        output[(-1,y)] = Alignmt(y+1,"|"*(y+1))

    print("limits: (%i,%i)" % (len(input1),len(input2)))

    _version4(output, input1, input2, len(input1)-1, len(input2)-1)
    display(output)
    print(output[(len(input1)-1,len(input2)-1)])

def _version4(arr, str1, str2, x=0, y=0):
    if x >= len(str1) or y >= len(str2):
        return

    above = arr.get((x,y-1))
    if not above:
        above = _version4(arr, str1, str2, x, y-1)
    left = arr.get((x-1,y))
    if not left:
        left = _version4(arr, str1, str2, x-1, y)
    diagon = arr.get((x-1,y-1))

    if above < diagon:
        if above < left:
            arr[(x,y)] = Alignmt(above.score+1, above.str + "|")
    elif left < diagon:
        arr[(x,y)] = Alignmt(left.score+1, left.str + "-")
    elif str1[x] == str2[y]:
        arr[(x,y)] = Alignmt(diagon.score, diagon.str + "\\")
    else:
        arr[(x,y)] = Alignmt(diagon.score+1, diagon.str + "\\")

    #display(arr)
    return arr[(x,y)]

str1 = ["A","B","C","C","D"]
str2 = ["A","E","B","F","C","D"]
#version1(str1, str2)
#version2(str1, str2)
#version3(str1, str2)
version4(str1, str2)
#exp_test()
