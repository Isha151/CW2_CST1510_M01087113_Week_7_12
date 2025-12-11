class Dataset:
    """
    Represents a data science dataset in the platform.
    """

    def __init__(
        self,
        dataset_id: int,
        dataset_name: str,
        category: str,
        source: str,
        last_updated: str,
        record_count: int,
        file_size_mb: float,
    ):
        self.id = dataset_id
        self.dataset_name = dataset_name
        self.category = category
        self.source = source
        self.last_updated = last_updated
        self.record_count = record_count
        self.file_size_mb = file_size_mb 

    def calculate_size_mb(self) -> float:
        return self.__size_bytes / (1024 * 1024)

    def get_source(self) -> str:
        return self.__source

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "dataset_name": self.dataset_name,
            "category": self.category,
            "source": self.source,
            "last_updated": self.last_updated,
            "record_count": self.record_count,
            "file_size_mb": self.file_size_mb,
        }