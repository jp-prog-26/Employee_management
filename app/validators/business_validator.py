from app.messages.messages import MSG_DATE_ORDER, MSG_ALREADY_INACTIVE, MSG_DUPLICATE_DOC
from datetime import datetime


def _parse_date(date_str: str):
    """Intenta parsear una fecha en formatos YYYY-MM-DD o DD/MM/YYYY."""
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def validate_no_duplicate_document(repo, document: str, exclude_id: int = None) -> list:
    """Verifica que no exista otro empleado con el mismo documento."""
    existing = repo.get_by_document(document)
    if existing and existing.id != exclude_id:
        return [MSG_DUPLICATE_DOC]
    return []


def validate_date_order(hire_date: str, end_date: str) -> list:
    """Verifica que la fecha de finalizacion no sea anterior a la de ingreso."""
    hire = _parse_date(hire_date)
    end = _parse_date(end_date)
    if hire and end and end < hire:
        return [MSG_DATE_ORDER]
    return []


def validate_not_already_inactive(employee) -> list:
    """Verifica que el empleado no este ya inactivo."""
    if employee and employee.status == 'INACTIVE':
        return [MSG_ALREADY_INACTIVE]
    return []