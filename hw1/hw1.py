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
        if head == None:
            return false
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

    def display_reverse(self):
        if self.head == None: return
        current = self.head;
        string = ""
        while current:
            string = current.__str__() + " " + string
            current = current.next
        print("in reverse: " + string)

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

class CircularDoublyLinkedList(DoublyLinkedList):

    def __init__(self):
        self.head = Element(None)
        self.head.next = self.head.prev = self.head

    def insert(self, x):
        if x is None: return
        x.next = head.next
        head.next = x
        x.next.prev = x

    def search(self, k):
        if self.head.next == self.head:
            return ""
        self.head.prev.next = None
        tmp = self.head.next.search()
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

def dlist_display(lst1,lst2):
    print("list1: ",end='')
    print(lst1)
    lst1.display_reverse()
    print("list2: ",end='')
    print(lst2)
    lst2.display_reverse()

def slist_display(lst1,lst2):
    print("list1: ",end='')
    print(lst1)
    print("length: %i" % lst1.__len__())
    print("list2: ",end='')
    print(lst2)
    print("length: %i" % lst2.__len__())
    print("list1 == list2: " + str(lst1 == lst2))

def clist_display(lst1,lst2):
    print("list1: ", end='')
    print(lst1)
    print(lst1.display_reverse())
    print("length: %i" % lst1.__len__())
    print("list2: ",end='')
    print(lst2)
    print(lst2.display_reverse())
    print("length: %i" % lst2.__len__())

def list_build(lst1,lst2):
    print("\nbuilding/resetting lists...")
    lst1.head = None
    lst2.head = None
    lst1.insert(Element(4));
    lst1.insert(Element(3));
    lst1.insert(Element(2));
    lst1.insert(Element(1));
    lst2.insert(Element(4));
    lst2.insert(Element(3));
    lst2.insert(Element(2));
    lst2.insert(Element(1));

def dll_tests():
    print("\n# Doubly Linked List tests #")
    lst = DoublyLinkedList();
    lst2 = DoublyLinkedList();
    list_build(lst,lst2)
    dlist_display(lst,lst2)
    print()

    print("list1 insert: 1")
    lst.insert(Element(1))
    dlist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 1")
    lst.delete(lst.search(1))
    dlist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 2")
    lst.delete(lst.search(2))
    dlist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 3")
    lst.delete(lst.search(3))
    dlist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 4")
    lst.delete(lst.search(4))
    dlist_display(lst,lst2)

def lll_tests():
    print("\n\n# Singly Linked List tests #")
    lst = SinglyLinkedList();
    lst2 = SinglyLinkedList();
    list_build(lst,lst2)
    slist_display(lst,lst2)
    print()

    print("list1 insert: 1")
    lst.insert(Element(1))
    slist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 1")
    lst.delete(lst.search(1))
    slist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 2")
    lst.delete(lst.search(2))
    slist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 3")
    lst.delete(lst.search(3))
    slist_display(lst,lst2)

    list_build(lst,lst2)
    print("list1 search and delete: 4")
    lst.delete(lst.search(4))
    slist_display(lst,lst2)

print()
dll_tests()
print()
#lll_tests()
print()
#cll_tests()
print()
