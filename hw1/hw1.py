class Element:
    def __init__(self, key):
        self.key = key;
        self.next = None;
        self.prev = None;

    def __str__(self):
        return "%d " % (self.key)

    def full_str(self):
        string = str(self.key)
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
            string = current.__str__() + string
            current = current.next
        print(string)

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


lst2 = SinglyLinkedList();
lst2.insert(Element(4));
lst2.insert(Element(3));
lst2.insert(Element(2));
lst2.insert(Element(1));
lst = SinglyLinkedList();
lst.insert(Element(4));
lst.insert(Element(3));
lst.insert(Element(2));
lst.insert(Element(1));
print(lst)
print(lst2)

if lst == lst2:
    print("yes")
else:
    print("no")

print(lst)
lst.delete(lst.head);
print(lst)
lst.delete(lst.head.next);
print(lst)
lst.delete(lst.head.next);
print(lst)
lst.delete(lst.head);
print(lst)

