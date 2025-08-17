from datetime import datetime
import json

from services.constants import TicketStatusEnum
from services.history import History
from utils.menu import format_duration


class Serializable:
    def to_dict(self):
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                result[k] = v.isoformat()
            else:
                result[k] = v
        return result

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)


class Ticket(Serializable):
    def __init__(self, id, title, priority, reporter, parent_id=None, assignee=None, status=TicketStatusEnum.OPEN.label,
                 created_at=datetime.now(), closed_at=None):
        self.id = id
        self.title = title
        self.priority = priority
        self.reporter = reporter
        self.assignee = assignee
        self.status = status
        self.parent_id = parent_id
        self.created_at = datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at
        self.closed_at = datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at

    def assign(self, assignee):
        self.assignee = assignee

    def close(self):
        self.closed_at = datetime.now()
        self.status = TicketStatusEnum.CLOSED.label

    @property
    def ticket_solve_duration(self):
        if self.closed_at is not None:
            return self.closed_at - self.created_at
        return None

    def __repr__(self):
        return (
            f"Ticket(id = {self.id}, Title = '{self.title}', "
            f"Priority = {self.priority}, Status = {self.status}, Parent = {self.parent_id}, "
            f"Created At = {self.created_at.strftime('%d %b %Y, %I:%M %p')}), Reporter = {self.reporter}, "
            f"Assignee = {self.assignee}, "
            f"Closed At = {self.closed_at.strftime('%d %b %Y, %I:%M %p') if self.closed_at else None}, "
            f"Duration To Close = {format_duration(self.ticket_solve_duration)})"
        )
