import json
import os
from models.ticket import Ticket

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.json")


def load_state():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            tickets = json.load(f)

            return [Ticket(**t) for t in tickets]
        except json.JSONDecodeError:
            return []


def save_state(tickets):
    with open(DATA_FILE, "w") as f:
        json.dump([t.to_dict() for t in tickets],
            f,
            indent=4
        )
