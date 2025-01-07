from datetime import datetime
from uuid import UUID
from shared_kernel.domain.entity import domain_entity

class User(domain_entity):
    def __init__(self, password, username, correo_electronico, id: UUID = None, created_at: datetime = None):
        super().__init__(id=id, created_at=created_at)
        self.username = username
        self.correo_electronico = correo_electronico
        self.password = password

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Usuario(id={self.id}, usuario={self.username}, correo_electronico={self.correo_electronico})"

usuario = User(username="cermait",password="123456", correo_electronico="juan@example.com")
print(usuario)


