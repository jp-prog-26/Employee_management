from app.repositories.employee_repository import EmployeeRepository
from app.validators.input_validator import (
    validate_create_input, validate_terminate_input, validate_status_input
)
from app.validators.business_validator import (
    validate_no_duplicate_document, validate_date_order, validate_not_already_inactive
)
from app.messages.messages import MSG_NOT_FOUND
from typing import Optional, List
from app.models.employee import Employee


class EmployeeService:
    """Capa de logica de negocio. Coordina validaciones y repositorio."""

    def __init__(self):
        self.repo = EmployeeRepository()

    # ------------------------------------------------------------------ #
    # Lecturas
    # ------------------------------------------------------------------ #

    def get_all(self, status: Optional[str] = None, search: Optional[str] = None) -> List[Employee]:
        return self.repo.get_all(status=status, search=search)

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return self.repo.get_by_id(employee_id)

    def get_by_document(self, document: str) -> Optional[Employee]:
        return self.repo.get_by_document(document)

    def get_recent(self, limit: int = 5) -> List[Employee]:
        return self.repo.get_recent(limit)

    def get_dashboard_stats(self) -> dict:
        counts = self.repo.count_by_status()
        recent = self.repo.get_recent(5)
        return {
            'totalEmployees': counts['TOTAL'],
            'activeEmployees': counts['ACTIVE'],
            'inactiveEmployees': counts['INACTIVE'],
            'recentEmployees': [e.to_dict() for e in recent],
        }

    # ------------------------------------------------------------------ #
    # Escrituras
    # ------------------------------------------------------------------ #

    def create(self, data: dict) -> tuple:
        """
        Crea un empleado.
        Retorna (employee_dict, errors_list, http_status_code).
        """
        errors = validate_create_input(data)
        if errors:
            return None, errors, 400

        errors += validate_no_duplicate_document(self.repo, data['document'].strip())
        if errors:
            return None, errors, 409

        emp = self.repo.create(
            document=data['document'].strip(),
            full_name=data['fullName'].strip(),
            hire_date=data['hireDate'].strip(),
        )
        return emp.to_dict(), [], 201

    def update_status(self, employee_id: int, data: dict) -> tuple:
        """Actualiza el estado de un empleado."""
        errors = validate_status_input(data)
        if errors:
            return None, errors, 400

        emp = self.repo.get_by_id(employee_id)
        if not emp:
            return None, [MSG_NOT_FOUND], 404

        emp = self.repo.update_status(employee_id, data['status'])
        return emp.to_dict(), [], 200

    def terminate(self, employee_id: int, data: dict) -> tuple:
        """Finaliza el contrato de un empleado."""
        errors = validate_terminate_input(data)
        if errors:
            return None, errors, 400

        emp = self.repo.get_by_id(employee_id)
        if not emp:
            return None, [MSG_NOT_FOUND], 404

        errors += validate_not_already_inactive(emp)
        if errors:
            return None, errors, 409

        errors += validate_date_order(emp.hireDate, data['endDate'].strip())
        if errors:
            return None, errors, 400

        emp = self.repo.terminate(employee_id, data['endDate'].strip())
        return emp.to_dict(), [], 200

    def delete(self, employee_id: int) -> tuple:
        """Elimina un empleado."""
        emp = self.repo.get_by_id(employee_id)
        if not emp:
            return False, [MSG_NOT_FOUND], 404
        self.repo.delete(employee_id)
        return True, [], 200