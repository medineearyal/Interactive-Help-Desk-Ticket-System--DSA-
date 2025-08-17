from traceback import print_tb

from services.ticket_service import TicketService
from utils.menu import print_menu, clear_screen
from utils.storage import save_state


def main():
    service = TicketService()

    try:
        while True:
            print_menu()

            choice = input("Enter choice: ").strip()

            if choice == "1":
                service.create_ticket()
            elif choice == "2":
                clear_screen()
                service.show_tickets()
            elif choice == "3":
                service.assign_ticket()
            elif choice == "4":
                service.close_ticket()
                print("\n\n")
            elif choice == "5":
                service.print_dashboard()
            elif choice == "6":
                service.history.display()
            elif choice == "7":
                service.undo()
            elif choice == "8":
                service.process_next_ticket()
            elif choice == "9":
                save_state(service.tickets)
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
    except Exception as e:
        save_state(service.tickets)
        print("Goodbye! Thank You For Using... Have a nice day!")

if __name__ == "__main__":
    main()
