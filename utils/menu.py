import os
import platform


def print_menu():
    print("--- Help Desk Menu ---")
    print("1. Create Ticket")
    print("2. View All Tickets")
    print("3. Close Ticket")
    print("4. Analytics Dashboard")
    print("5. View History")
    print("6. Undo Last Action")
    print("7. Process Next Ticket")
    print("8. Exit")


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        if "TERM" in os.environ:
            os.system("clear")
        else:
            print("\n" * 100)


def format_duration(td):
    """
    Returns the duration between two datetime objects in a human-readable format.
    """
    total_seconds = int(td.total_seconds())

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)
