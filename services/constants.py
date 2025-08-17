from enum import Enum


class TicketPriorityEnum(Enum):
    HIGH = "High", 0
    MEDIUM = "Medium", 1
    LOW = "Low", 2

    def __init__(self, label, priority):
        self.label = label
        self.priority = priority

    @classmethod
    def priorities(cls):
        return [member.priority for member in cls]

    @classmethod
    def labels(cls):
        return [member.label for member in cls]


class TicketStatusEnum(Enum):
    OPEN = "Open", 1
    ASSIGNED = "Assigned", 2
    CLOSED = "Closed", 3

    def __init__(self, label, status):
        self.label = label
        self.status = status

    @classmethod
    def statuses(cls):
        return [member.status for member in cls]

    @classmethod
    def labels(cls):
        return [member.label for member in cls]


class TicketActionEnum(Enum):
    CREATE = "Create", 0
    OPEN = "Open", 1
    ASSIGN = "Assign", 2
    CLOSE = "Close", 3
