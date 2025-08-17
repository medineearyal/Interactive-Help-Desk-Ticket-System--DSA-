import json
import os
from models.ticket import Ticket

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.json")


def load_state():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            tickets = data["tickets"]
            history = data["history"]

            return {
                "tickets": [Ticket(**t) for t in tickets],
                "history": history
            }
        except json.JSONDecodeError:
            return []


def save_state(tickets, history):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "tickets": [
                    t.to_dict() for t in tickets
                ],
                "history": history.to_list()
            },
            f,
            indent=4
        )
