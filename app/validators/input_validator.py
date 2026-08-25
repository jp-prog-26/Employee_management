from app.messages.messages import (
    MSG_NAME_REQUIRED, MSG_DOC_REQUIRED, MSG_DATE_REQUIRED,
    MSG_END_DATE_REQUIRED, MSG_INVALID_STATUS
)


def validate_create_input(data: dict) -> list:
    """Valida los campos requeridos para crear un empleado. Retorna lista de errores."""
    errors = []
    if not data.get('fullName', '').strip():
        errors.append(MSG_NAME_REQUIRED)
    if not data.get('document', '').strip():
        errors.append(MSG_DOC_REQUIRED)
    if not data.get('hireDate', '').strip():
        errors.append(MSG_DATE_REQUIRED)
    return errors


def validate_terminate_input(data: dict) -> list:
    """Valida los campos requeridos para terminar contrato."""
    errors = []
    if not data.get('endDate', '').strip():
        errors.append(MSG_END_DATE_REQUIRED)
    return errors


def validate_status_input(data: dict) -> list:
    """Valida que el status sea valido."""
    errors = []
    status = data.get('status', '')
    if status not in ('ACTIVE', 'INACTIVE'):
        errors.append(MSG_INVALID_STATUS)
    return errors