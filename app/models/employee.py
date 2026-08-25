from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    id: int
    document: str
    fullName: str
    hireDate: str
    status: str
    endDate: Optional[str] = None

    @staticmethod
    def from_row(row) -> 'Employee':
        return Employee(
            id=row['id'],
            document=row['document'],
            fullName=row['full_name'],
            hireDate=row['hire_date'],
            status=row['status'],
            endDate=row['end_date'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'document': self.document,
            'fullName': self.fullName,
            'hireDate': self.hireDate,
            'endDate': self.endDate,
            'status': self.status,
        }