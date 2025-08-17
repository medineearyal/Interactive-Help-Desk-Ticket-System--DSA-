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
    CLOSED = "Closed", 0

    def __init__(self, label, status):
        self.label = label
        self.status = status

    @classmethod
    def statuses(cls):
        return [member.status for member in cls]

    @classmethod
    def labels(cls):
        return [member.label for member in cls]

