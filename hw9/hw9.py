from typing import Tuple

class chars:
    def __init__(self,value: str):
        self.parent = None
        self.child = None
        self.sibling = None
        self.word = False
        self.value = value

    def __str__(self) -> str:
        if not self.parent: return self.value
        return str(self.parent) + '_' +self.value
    __repr__ = __str__

    def print_tree(self,indent: int = 0):
        print(' '*indent + self.value,end='')
        print(" W" if self.word else "")
        if self.child:
            self.child.print_tree(indent + len(self.value))
        if self.sibling:
            self.sibling.print_tree(indent)

    def add_child(self,other):
        other.parent = self
        if self.child == None:
            self.child = other
            return
        if other.value <= self.child.value:
            other.sibling = self.child
            self.child = other
            return
        prev = self.child
        next = prev.sibling
        while next and next.value < other.value:
            prev = next
            next = next.sibling
        other.sibling = next
        prev.sibling = other

    def find(self,string,indent=""):
        if string.find(self.value) != 0: return None
        string = string[len(self.value):]
        if string == "": return self
        next = self.child
        while next is not None:
            ret = next.find(string,indent+"  ")
            if ret is not None: return ret
            next = next.sibling
        return None

    def walk(self,prefix=""):
        prefix += self.value
        if self.child is None: return [prefix]

        results = []
        ch = self.child
        while ch is not None:
            results.extend(ch.walk(prefix))
            ch = ch.sibling
        return results

    def split_node(self, string: str):
        if not self.value.startswith(string): return
        tmp = chars(self.value[len(string):])
        tmp.child = self.child
        tmp.parent = self
        tmp.word = self.word
        self.word = False
        self.child = tmp
        self.value = string
        current = tmp.child
        while current:
            current.parent = tmp
            current = current.sibling

    def find_partial(self, string: str) -> Tuple['chars', str]:
        if self.value == string: return self, ""
        if string.startswith(self.value):
            if self.child:
                return self.child.find_partial(string[len(self.value):])
            return self, string[len(self.value):]
        if self.sibling:
            return self.sibling.find_partial(string)
        return self.parent, string

    def add_word(self, word: str):
        count = 0
        for i,j in zip(self.value, word):
            if i == j: count += 1
            else: break
        if not count:
            if self.sibling:
                self.sibling.add_word(word)
                return
            self.sibling = chars(word)
            self.sibling.parent = self.parent
            self.sibling.word = True
            return
        word = word[count:]
        if count != len(self.value):



def test2():
    top = chars("rom")
    top.find("rom").add_child(chars("ulus"))
    top.find("rom").add_child(chars("an"))
    top.print_tree()
    top.find("rom").split_node("r")
    top.find("r").add_child(chars("ub"))
    top.find("roman").add_child(chars("e"))
    top.print_tree()
    print("search for \"rubber\": ")
    print(top.find_partial("rubber"))
    print("search for \"roman\": ")
    print(top.find_partial("roman"))
    print("search for \"roma\": ")
    print(top.find_partial("roma"))
    print(top.walk())

test2()
