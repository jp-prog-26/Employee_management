"""Modelo principal del empleado.

Representa la estructura que se guarda en la base de datos y la que se usa
para mostrar la información en la interfaz. La clase también ayuda a convertir
los registros de SQLite en objetos Python y viceversa.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Employee:
    """Entidad que representa a un empleado dentro de la aplicación.

    Aporta una forma clara de trabajar con los datos del empleado en
    servicio, repositorio y vistas, evitando manipular diccionarios sueltos.
    """

    id: int
    document: str
    firstName: str
    firstLastname: str
    hireDate: str
    status: str
    secondName: Optional[str] = ''
    secondLastname: Optional[str] = ''
    endDate: Optional[str] = None

    @property
    def fullName(self) -> str:
        """Nombre completo compuesto por los 4 campos (omite los vacíos)."""
        parts = [self.firstName, self.secondName, self.firstLastname, self.secondLastname]
        return ' '.join(p for p in parts if p and p.strip())

    @staticmethod
    def from_row(row) -> 'Employee':
        """Crea un objeto Employee a partir de una fila de SQLite.

        Esta compatibilidad permite leer tanto registros nuevos como datos antiguos
        que puedan venir con el campo full_name y sin columnas separadas.
        """
        keys = row.keys() if hasattr(row, 'keys') else []
        first_name = (row['first_name'] or '') if 'first_name' in keys else ''
        second_name = (row['second_name'] or '') if 'second_name' in keys else ''
        first_lastname = (row['first_lastname'] or '') if 'first_lastname' in keys else ''
        second_lastname = (row['second_lastname'] or '') if 'second_lastname' in keys else ''

        # Retrocompatibilidad: si no tiene nombres separados pero sí full_name
        if not first_name and not first_lastname and 'full_name' in keys and row['full_name']:
            parts = (row['full_name'] or '').strip().split()
            if len(parts) == 1:
                first_name = parts[0]
            elif len(parts) == 2:
                first_name, first_lastname = parts[0], parts[1]
            elif len(parts) == 3:
                first_name, first_lastname, second_lastname = parts[0], parts[1], parts[2]
            elif len(parts) >= 4:
                first_name, second_name, first_lastname = parts[0], parts[1], parts[2]
                second_lastname = ' '.join(parts[3:])

        return Employee(
            id=row['id'],
            document=row['document'],
            firstName=first_name,
            secondName=second_name,
            firstLastname=first_lastname,
            secondLastname=second_lastname,
            hireDate=row['hire_date'],
            status=row['status'],
            endDate=row['end_date'],
        )

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para enviarlo a templates o JSON."""
        return {
            'id': self.id,
            'document': self.document,
            'firstName': self.firstName,
            'secondName': self.secondName,
            'firstLastname': self.firstLastname,
            'secondLastname': self.secondLastname,
            'fullName': self.fullName,
            'hireDate': self.hireDate,
            'endDate': self.endDate,
            'status': self.status,
        }