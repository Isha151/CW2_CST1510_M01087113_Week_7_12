class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    def __init__(self, username: str, password_hash: str, role: str):
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role

    def get_username(self) -> str:
        return self.__username 
    
    def get_role(self) -> str:
        return self.__role
    
    def get_password_hash(self) -> str:
        return self._password_hash
                                     
    def __str__(self) -> str:
        return f"User({self.__username}, role={self.__role})"