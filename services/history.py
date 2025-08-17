from models.node import Node

class History:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, ticket):
        node = Node(ticket)
        if not self.head:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def display(self):
        if not self.head:
            print("(no history yet)")
            return
        curr = self.head
        print("-- Ticket History (chronological) --")
        while curr:
            print(curr.ticket)
            curr = curr.next
        print()

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.ticket.id)
            curr = curr.next
        return result

