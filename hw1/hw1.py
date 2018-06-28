class Element:
    def __init__(self, key):
        self.key = key;
        self.next = None;
        self.prev = None;

    def search(self, k):
        head = self
        while head.key != k && head != None:
            head = head.next
        if head == None:
            return false
        return head

class DoublyLinkedList:

    def __init__(self):
        self.head = None;

    def insert(self, x):
        if self.head != None:
            x.next = self.head
            self.head.prev = x
        self.head = x

    def delete(self, x):
        if x.next != None:
            x.next.prev = x.prev
        if x != self.head:
            x.prev.next = x.next
        else:
            self.head = x.next
        x.next = None
        x.prev = None

    def search(self, k):
        return self.search(k)

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self,x):
        x.next = self.head
        self.head = x

    def delete(self, x):
        search = self.head
        prev = None
        while search != x && search != None:
            prev = search
            search = search.next
        if search == None:
            return
        prev.next = search.next

    def search(self, k):
        return self.search(k)

    def __str__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __eq__(self):
        raise NotImplementedError

class CircularDoublyLinkedList:

    def __init__(self):
        raise NotImplementedError


    def insert(self, x):
        raise NotImplementedError

    def search(self, k):
