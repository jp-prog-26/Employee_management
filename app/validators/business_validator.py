"""Reglas específicas del negocio para empleados.

Estas validaciones no solo revisan formato sino también la lógica de negocio:
si un documento ya existe, si una fecha final es válida y si un empleado ya fue
marcado como inactivo antes de volver a intentarlo.
"""

from app.messages.messages import MSG_DATE_ORDER, MSG_ALREADY_INACTIVE, MSG_DUPLICATE_DOC
from datetime import datetime


def _parse_date(date_str: str):
    """Intenta parsear una fecha en formatos YYYY-MM-DD o DD/MM/YYYY."""
    # Las fechas pueden venir desde el navegador en formato ISO o desde formularios locales.
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def validate_no_duplicate_document(repo, document: str, exclude_id: int = None) -> list:
    """Verifica que no exista otro empleado con el mismo documento."""

    # Se busca el empleado por documento para evitar duplicados, pero se excluye
    # al registro actual cuando se está editando.

    existing = repo.get_by_document(document)
    if existing and existing.id != exclude_id:
        return [MSG_DUPLICATE_DOC]
    return []


def validate_date_order(hire_date: str, end_date: str) -> list:
    """Verifica que la fecha de finalizacion no sea anterior a la de ingreso."""
    # Se comparan fechas reales para garantizar que la terminación del contrato
    # no contradiga la fecha de ingreso registrada.
    hire = _parse_date(hire_date)
    end = _parse_date(end_date)
    if hire and end and end < hire:
        return [MSG_DATE_ORDER]
    return []


def validate_not_already_inactive(employee) -> list:
    """Verifica que el empleado no este ya inactivo."""
    # Evita que se intente cerrar el contrato dos veces sobre el mismo registro.
    if employee and employee.status == 'INACTIVE':
        return [MSG_ALREADY_INACTIVE]
    return []