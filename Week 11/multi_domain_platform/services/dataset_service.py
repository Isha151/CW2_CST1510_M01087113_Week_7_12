from models.dataset import Dataset
from services.database_manager import DatabaseManager


class DatasetService:
    """Handles CRUD operations for dataset metadata."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_all(self) -> list[Dataset]:
        rows = self.db.fetch_all("SELECT * FROM datasets_metadata")
        return [
            Dataset(
                row[0], row[1], row[2], row[3],
                row[4], row[5], row[6]
            )
            for row in rows
        ]

    def create(self, dataset: Dataset):
        self.db.execute_query(
            """
            INSERT INTO datasets_metadata 
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                dataset.dataset_name,
                dataset.category,
                dataset.source,
                dataset.last_updated,
                dataset.record_count,
                dataset.file_size_mb,
            )
        )

    def update(self, dataset: Dataset):
        self.db.execute_query(
            """
            UPDATE datasets_metadata
            SET dataset_name = ?, category = ?, source = ?, last_updated = ?,
                record_count = ?, file_size_mb = ?
            WHERE id = ?
            """,
            (
                dataset.dataset_name,
                dataset.category,
                dataset.source,
                dataset.last_updated,
                dataset.record_count,
                dataset.file_size_mb,
                dataset.id
            )
        )

    def delete(self, dataset_id: int):
        self.db.execute_query(
            "DELETE FROM datasets_metadata WHERE id = ?",
            (dataset_id,)
        )
