class Element:
    def __init__(self, key):
        self.key = key;
        self.next = None;
        self.prev = None;

    def __str__(self):
        return "%d " % (self.key)

    def full_str(self):
        string = ""
        while self:
            string += self.__str__();
            self = self.next
        return string + " "

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
        return self.head.full_str();

    def insert(self, x):
        if self.head:
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
        return self.head.search(k)

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self,x):
        x.next = self.head
        self.head = x

    def delete(self, x):
        if x == self.head:
            self.head = x.next
            return
        search = self.head
        while search != x and search:
            prev = search
            search = search.next
        if search == None:
            return
        prev.next = search.next

    def search(self, k):
        return self.head.search(k)

    def __str__(self):
        return self.head.full_str();

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
        raise NotImplementedError

lst = SinglyLinkedList();
lst.insert(Element(4));
lst.insert(Element(3));
lst.insert(Element(2));
lst.insert(Element(1));
print lst
lst.delete(lst.head);
print lst
lst.delete(lst.head.next);
print lst
lst.delete(lst.head.next);
print lst
lst.delete(lst.head);
print lst
lst.delete(lst.head);
print lst

