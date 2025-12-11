class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(
        self,
        incident_id: int,
        date: str,
        incident_type: str,
        severity: str,
        status: str,
        description: str,
        reported_by: str | None = None,
    ):
        self.id = incident_id
        self.date = date
        self.incident_type = incident_type
        self.severity = severity
        self.status = status
        self.description = description
        self.reported_by = reported_by
 
    def get_id(self) -> int:
        return self.__id
    
    def get_severity(self) -> str:
        return self.__severity
 
    def get_status(self) -> str:
        return self.__status
 
    def get_description(self) -> str:
        return self.__description
 
    def update_status(self, new_status: str) -> None:
        self.__status = new_status
 
    def get_severity_level(self) -> int:
        """Return an integer severity level (simple example)."""
        mapping = {"low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def __str__(self) -> str:
         return (f"Incident {self.__id} [{self.__severity.upper()}] {self.__status}")