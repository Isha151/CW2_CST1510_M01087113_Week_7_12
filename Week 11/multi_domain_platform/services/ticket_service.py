from models.it_ticket import ITTicket
from services.database_manager import DatabaseManager


class TicketService:
    """Handles CRUD operations for IT Tickets."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_all(self) -> list[ITTicket]:
        rows = self.db.fetch_all("SELECT * FROM it_tickets")

        tickets = []
        for row in rows:
            ticket = ITTicket(
                db_id=row[0],           # id
                ticket_id=row[1],       # ticket_id
                priority=row[2],
                status=row[3],
                category=row[4],
                subject=row[5],
                description=row[6],
                created_date=row[7],
                resolved_date=row[8],
                assigned_to=row[9],
            )
            tickets.append(ticket)

        return tickets

    def create(self, ticket: ITTicket):
        self.db.execute_query(
            """
            INSERT INTO it_tickets (ticket_id, priority, status, category, subject, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.ticket_id,
                ticket.priority,
                ticket.status,
                ticket.category,
                ticket.subject,
                ticket.description,
            )
        )

    def update(self, ticket: ITTicket):
        self.db.execute_query(
            """
            UPDATE it_tickets
            SET priority = ?, status = ?, category = ?, subject = ?, 
                description = ?, assigned_to = ?, resolved_date = ?
            WHERE id = ?
            """,
            (
                ticket.priority,
                ticket.status,
                ticket.category,
                ticket.subject,
                ticket.description,
                ticket.assigned_to,
                ticket.resolved_date,
                ticket.db_id
            )
        )

    def delete(self, db_id: int):
        self.db.execute_query(
            "DELETE FROM it_tickets WHERE id = ?",
            (db_id,)
        )
