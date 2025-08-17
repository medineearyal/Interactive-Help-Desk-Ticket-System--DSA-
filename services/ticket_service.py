from models.ticket import Ticket
from services.constants import TicketStatusEnum, TicketPriorityEnum, TicketActionEnum
from services.history import History
from utils.menu import clear_screen
from utils.storage import load_state
import heapq
from collections import deque


class DashboardMixin:
    def build_dashboard_matrix(self):
        """
        Create a 2D list (matrix) of counts by priority vs status.
        Rows: priorities;
        Columns: [Open, Assigned, Closed]
        """

        tickets = getattr(self, "tickets")
        counts = {
            p: {
                s: 0 for s in TicketStatusEnum.labels()
            } for p in TicketPriorityEnum.labels()
        }

        for t in tickets:
            p = t.priority if t.priority in TicketPriorityEnum.labels() else TicketPriorityEnum.LOW.label
            s = t.status if t.status in TicketStatusEnum.labels() else TicketStatusEnum.OPEN.label
            counts[p][s] += 1

        matrix = [["Priority", *TicketStatusEnum.labels()]]
        for p in TicketPriorityEnum.labels():
            matrix.append(
                [p.title(), counts[p][TicketStatusEnum.OPEN.label], counts[p][TicketStatusEnum.ASSIGNED.label],
                 counts[p][TicketStatusEnum.CLOSED.label]])
        return matrix

    def print_dashboard(self):
        clear_screen()

        matrix = self.build_dashboard_matrix()
        print("\n-- Analytics Dashboard --\n")
        col_widths = [max(len(str(row[c])) for row in matrix) for c in range(len(matrix[0]))]

        def fmt_row(row):
            return "  ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

        print(fmt_row(matrix[0]))
        print("-" * (sum(col_widths) + 2 * (len(col_widths) - 1)))
        for r in matrix[1:]:
            print(fmt_row(r))
        print()


class TicketService(DashboardMixin):
    action_stack = []
    priority_queue = []
    queue = deque()

    def __init__(self):
        state = load_state()

        self.history = History()
        if state:
            self.tickets = state
            sorted_tickets = sorted(self.tickets, key=lambda t: t.created_at)

            for ticket in self.tickets:
                if ticket.status != TicketStatusEnum.CLOSED.label:
                    self.enqueue_for_processing(ticket)

                self.history.append(sorted_tickets)

        else:
            self.tickets = []

    def _next_id(self):
        return (self.tickets[-1].id + 1) if self.tickets else 1

    def _input_priority(self):
        while True:
            p = input("Enter priority (high/medium/low): ").strip().title()
            if p in TicketPriorityEnum.labels():
                return p
            print("Invalid priority. Try again.")

    def create_ticket(self):
        clear_screen()

        ticket_id = self._next_id()
        title = input("Enter title: ").strip()
        priority = self._input_priority()
        reporter = input("Enter Reporter: ").strip()

        print()
        if self.show_tickets():
            parent_raw = input("Parent ticket id (or leave blank): ").strip()
        else:
            parent_raw = None
        print()

        parent_id = int(parent_raw) if parent_raw else None

        new_ticket = Ticket(ticket_id, title, priority, reporter, parent_id)
        self.tickets.append(new_ticket)
        self.history.append(new_ticket)
        self.action_stack.append((TicketActionEnum.CREATE, ticket_id))
        self.enqueue_for_processing(new_ticket)

        print(f"Created ticket #{ticket_id}! \n\n")

    def show_tickets(self):
        print("-- All Tickets --")

        if not self.tickets:
            print("Alas, No Tickets are created yet.")
            return False
        for t in self.tickets:
            print(t)
        print()
        return True

    def show_open_tickets(self):
        if not self.tickets:
            print("No Open Tickets yet.")

        open_tickets = [ticket for ticket in self.tickets if ticket.status == TicketStatusEnum.OPEN.label]
        print("-- Open Tickets --")
        for t in open_tickets:
            print(t)
        print()

    def assign_ticket(self):
        assignee = input("Enter the Assignee Name: ").strip().title()
        self.show_open_tickets()

        while True:
            tid = int(input("Enter the ID of the Ticket: ").strip())
            ticket = self.get_ticket_by_id(tid)

            if ticket:
                ticket.assign(assignee)
                print(f"Ticket (#{ticket.id}) Successfully Assigned To: {assignee}")
                break
            else:
                print("Ticket Not Found, Try Again with a Valid ID.")


    def close_ticket(self):
        clear_screen()

        self.show_open_tickets()

        raw = input("Enter ticket id to close: ").strip()
        if not raw.isdigit():
            print("Invalid id.")
            return
        tid = int(raw)

        ticket = self.get_ticket_by_id(tid)
        if not ticket:
            print("Ticket not found.")
            return

        if ticket.status == TicketStatusEnum.CLOSED.label:
            print("Ticket already closed.")
            return

        if self.can_close(tid):
            if ticket.close():
                self.action_stack.append((TicketStatusEnum.CLOSED, tid))
                print("Ticket closed!")
            else:
                print("Dunno Who The Ticket Was Assigned To.")
        else:
            print("Cannot close: dependent parent still open (or missing).")

    def get_ticket_by_id(self, ticket_id):
        for t in self.tickets:
            if t.id == ticket_id:
                return t
        return None

    def can_close(self, ticket_id):
        """Return True if a ticket can be closed (all parents up the chain are closed)."""
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket is None:
            return False

        if ticket.parent_id is None:
            return True

        parent = self.get_ticket_by_id(ticket.parent_id)
        if parent is None:
            return False

        if parent.status != TicketStatusEnum.CLOSED.label:
            return False

        return self.can_close(parent.id)

    def enqueue_for_processing(self, ticket):
        """Place ticket into appropriate work structure."""
        pr = ticket.priority
        if pr == TicketPriorityEnum.HIGH.label:
            heapq.heappush(self.priority_queue, (TicketPriorityEnum.HIGH.priority, ticket.id))
        else:
            self.queue.append(ticket.id)

    def undo(self):
        if not self.action_stack:
            print("Nothing to undo.")
            return

        action, tid = self.action_stack.pop()
        t = self.get_ticket_by_id(tid)

        if action == TicketActionEnum.CREATE:
            if t in self.tickets:
                self.tickets.remove(t)
            try:
                self.queue.remove(tid)
            except ValueError:
                pass
            tmp = [(w, i) for (w, i) in self.priority_queue if i != tid]
            self.priority_queue.clear()
            for item in tmp:
                heapq.heappush(self.priority_queue, item)
            print(f"Undo: deleted ticket {tid}.")

        elif action == TicketActionEnum.CLOSE:
            if t:
                t.open()
                self.enqueue_for_processing(t)
                print(f"Undo: Reopened ticket {tid}.")

    def process_next_ticket(self):
        """
        Simulate processing the next ticket in line.
        High priority (heap) beats standard queue.
        """

        tid = None
        if self.priority_queue:
            _, tid = heapq.heappop(self.priority_queue)
        elif self.queue:
            tid = self.queue.popleft()

        if tid is None:
            print("No tickets to process.")
            return

        t = self.get_ticket_by_id(tid)
        if not t:
            print("Ticket not found.")
            return

        print(f"Processing ticket #{t.id}: {t.title} [priority={t.priority}]")
        while t.status != TicketStatusEnum.CLOSED.label:
            is_done = input("Is The Ticket Closed? (Y/N): ")
            if is_done.upper() == "Y":
                closed_by = input("Enter Who Closed The Ticket: ")
                t.close(closed_by)
                print(f"Ticket {t.id} has been processed Successfully. Thank You!!")
            else:
                break
