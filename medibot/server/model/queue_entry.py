from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from medibot.server.model.patient import Patient

@dataclass
class Queue:
    """ a queue entry"""
    patient: Patient
    priority: int
    description: str

    def __str__(self) -> str:
        return f"[patient={self.patient}, priority={self.priority}, description={self.description}]"