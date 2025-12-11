class ITTicket:
    """Represents an IT support ticket."""

    def __init__(
        self,
        db_id: int,
        ticket_id: str,
        subject: str,
        priority: str,
        status: str,
        category: str,
        description: str,
        created_date: str | None = None,
        resolved_date: str | None = None,
        assigned_to: str = "Unassigned",
    ):
        self.db_id = db_id          # primary key in DB (id)
        self.ticket_id = ticket_id  # unique ticket identifier (ticket_id)
        self.subject = subject
        self.priority = priority
        self.status = status
        self.category = category
        self.description = description
        self.created_date = created_date
        self.resolved_date = resolved_date
        self.assigned_to = assigned_to

    def assign_to(self, staff: str) -> None:
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        self.__status = "Closed"

    def get_status(self) -> str:
        return self.__status

    def __str__(self) -> str:
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] – {self.__status} "
            f"(assigned to: {self.__assigned_to})"
        )
