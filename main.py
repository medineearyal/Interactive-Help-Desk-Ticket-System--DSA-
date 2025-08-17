from services.ticket_service import TicketService
from utils.menu import print_menu, clear_screen
from utils.storage import save_state


def main():
    service = TicketService()

    while True:
        print_menu()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            service.create_ticket()
        elif choice == "2":
            service.show_tickets()
        elif choice == "3":
            service.close_ticket()
        elif choice == "4":
            service.print_dashboard()
        elif choice == "5":
            service.history.display()
        elif choice == "6":
            service.undo()
        elif choice == "7":
            service.process_next_ticket()
        elif choice == "8":
            save_state(service.tickets, service.history)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
