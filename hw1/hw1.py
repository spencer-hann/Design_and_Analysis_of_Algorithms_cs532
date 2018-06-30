class Element:
    def __init__(self, key):
        self.key = key;
        self.next = None;
        self.prev = None;

    def __str__(self):
        return str(self.key)

    def full_str(self):
        string = str(self.key)
        self = self.next
        while self:
            string += " -> " + self.__str__();
            self = self.next
        return string

    def search(self, k):
        head = self
        while head and head.key != k:
            head = head.next
        return head

class DoublyLinkedList:
    def __init__(self):
        self.head = None;

    def __str__(self):
        if self.head:
            return self.head.full_str();
        return ""

    def insert(self, x):
        if self.head:
            x.next = self.head
            self.head.prev = x
        self.head = x

    def delete(self, x):
        if x == None or self.head == None:
            return
        if x.next:
            x.next.prev = x.prev
        if x.prev:
            x.prev.next = x.next
        else:
            self.head = x.next
        x.next = None
        x.prev = None

    def search(self, k):
        return self.head.search(k)

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self,x):
        x.next = self.head
        self.head = x

    def delete(self, x):
        if x == None: return
        if x == self.head:
            self.head = x.next
            return

        search = self.head
        while search and search != x:
            prev = search
            search = search.next
            
        if search == None: return
        prev.next = search.next

    def search(self, k):
        return self.head.search(k)

    def __str__(self):
        if self.head:
            return self.head.full_str();
        return ""

    def __len__(self):
        head = self.head
        count = 0
        while head:
            count += 1
            head = head.next
        return count

    def __eq__(self, lst):
        head1 = self.head
        head2 = lst.head
        while head1 and head2:
            if head1.key != head2.key:
                return False
            head1 = head1.next
            head2 = head2.next
        return not (head1 or head2)

    def display_with(self,lst2):
        print("list1: ",end='')
        print(self)
        print("length: %i" % self.__len__())
        print("list2: ",end='')
        print(lst2)
        print("length: %i" % lst2.__len__())
        print("list1 == list2: " + str(self == lst2))

class CircularDoublyLinkedList(DoublyLinkedList):

    def __init__(self):
        self.head = Element(None)
        self.head.next = self.head
        self.head.prev = self.head

    def insert(self, x):
        if x is None: return
        x.prev = self.head
        x.next = self.head.next
        x.prev.next = x
        x.next.prev = x

    def search(self, k):
        if self.head.next == self.head:
            return None
        self.head.prev.next = None
        tmp = self.head.next.search(k)
        self.head.prev.next = self.head
        return tmp

    def __str__(self):
        if self.head.next == self.head:
            return ""
        self.head.prev.next = None
        tmp = self.head.next.full_str()
        self.head.prev.next = self.head
        return tmp

    def __len__(self):
        if self.head.next == self.head:
            return 0
        head = self.head.next
        count = 0
        while head != self.head:
            head = head.next
            count += 1
        return count
    
    def display(self):
        print(self)
        tmp = self.head.prev
        print("in reverse: (circular)", end='')
        while tmp.key is not None:
            print(" <-> " + tmp.__str__(),end='')
            tmp = tmp.prev
        print("\nlength: %i" % self.__len__())

def display_reverse(lst):
    print("in reverse: ",end='')
    if lst == None or lst.head == None: 
        print("None")
    current = lst.head;
    while current.next:
        current = current.next
    while current:
        print(current.__str__() + " ",end='')
        current = current.prev
    print()

def list_build(lst,lst2=None):
    print("\nbuilding/resetting list1...")
    if type(lst) is CircularDoublyLinkedList:
        lst.head.next = lst.head
        lst.head.prev = lst.head
    else:
        lst.head = None
    lst.insert(Element(4));
    lst.insert(Element(3));
    lst.insert(Element(2));
    lst.insert(Element(1));
    if lst2 is not None:
        print("building/resetting list2...")
        lst2.head = None
        lst2.insert(Element(4));
        lst2.insert(Element(3));
        lst2.insert(Element(2));
        lst2.insert(Element(1));

def dll_tests():
    print("\n# Doubly Linked List tests #")
    lst = DoublyLinkedList();
    list_build(lst)
    print(lst)
    display_reverse(lst)

    print("\nlist1 insert: 1")
    lst.insert(Element(1))
    print(lst)
    display_reverse(lst)

    list_build(lst)
    print("list1 search and delete: 1")
    lst.delete(lst.search(1))
    print(lst)
    display_reverse(lst)

    list_build(lst)
    print("list1 search and delete: 2")
    lst.delete(lst.search(2))
    print(lst)
    display_reverse(lst)

    list_build(lst)
    print("list1 search and delete: 3")
    lst.delete(lst.search(3))
    print(lst)
    display_reverse(lst)

    list_build(lst)
    print("list1 search and delete: 4")
    lst.delete(lst.search(4))
    print(lst)
    display_reverse(lst)

    list_build(lst)
    print("search: 5")
    print(lst.search(5))
    print(lst)
    display_reverse(lst)

def lll_tests():
    print("\n# Singly Linked List tests #")
    lst = SinglyLinkedList();
    lst2 = SinglyLinkedList();
    list_build(lst,lst2)
    lst.display_with(lst2)
    print()

    print("list1 insert: 1")
    lst.insert(Element(1))
    lst.display_with(lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 1")
    lst.delete(lst.search(1))
    lst.display_with(lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 2")
    lst.delete(lst.search(2))
    lst.display_with(lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 3")
    lst.delete(lst.search(3))
    lst.display_with(lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 4")
    lst.delete(lst.search(4))
    lst.display_with(lst2)

    list_build(lst,lst2)
    print("search: 5")
    print(lst.search(5))
    lst.display_with(lst2)

def cll_tests():
    print("\n# Circular linked list tests #")
    lst = CircularDoublyLinkedList()
    list_build(lst)
    lst.display();

    print("list1 search and delete: 1")
    lst.delete(lst.search(1))
    lst.display()

    list_build(lst)
    print("list1 search and delete: 2")
    lst.delete(lst.search(2))
    lst.display()

    list_build(lst)
    print("list1 search and delete: 3")
    lst.delete(lst.search(3))
    lst.display()

    list_build(lst)
    print("list1 search and delete: 4")
    lst.delete(lst.search(4))
    lst.display()

    list_build(lst)
    print("list1 search: 5")
    print(lst.search(5))
    lst.display()

print()
dll_tests()
print()
lll_tests()
print()
cll_tests()
print()
