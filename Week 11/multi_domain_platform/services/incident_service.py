from models.security_incident import SecurityIncident
from services.database_manager import DatabaseManager


class IncidentService:
    """Handles CRUD operations for cybersecurity incidents."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_all(self) -> list[SecurityIncident]:
        rows = self.db.fetch_all("SELECT * FROM cyber_incidents")

        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row[0],
                date=row[1],
                incident_type=row[2],
                severity=row[3],
                status=row[4],
                description=row[5],
                reported_by=row[6],
            )
            incidents.append(incident)

        return incidents

    def create(self, incident: SecurityIncident):
        self.db.execute_query(
            """
            INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                incident.date,
                incident.incident_type,
                incident.severity,
                incident.status,
                incident.description,
                incident.reported_by
            )
        )

    def update_status(self, incident_id: int, new_status: str):
        self.db.execute_query(
            "UPDATE cyber_incidents SET status = ? WHERE id = ?",
            (new_status, incident_id)
        )

    def delete(self, incident_id: int):
        self.db.execute_query(
            "DELETE FROM cyber_incidents WHERE id = ?",
            (incident_id,)
        )
