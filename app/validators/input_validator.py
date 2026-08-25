import re
from app.messages.messages import (
    MSG_FIRSTNAME_REQUIRED, MSG_LASTNAME_REQUIRED, MSG_NAME_MIN_LENGTH, MSG_NAME_ONLY_LETTERS,
    MSG_DOC_REQUIRED, MSG_DOC_TOO_SHORT, MSG_DOC_ONLY_DIGITS,
    MSG_DATE_REQUIRED, MSG_END_DATE_REQUIRED, MSG_INVALID_STATUS
)

# Patrón para nombres: solo letras (incluye tildes, ñ, diéresis), espacios, apóstrofes y guiones
NAME_REGEX = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$")
# Patrón para documento: solo dígitos numéricos
DOC_REGEX = re.compile(r"^\d+$")


def validate_create_input(data: dict) -> list:
    """Valida los campos requeridos para crear un empleado. Retorna lista de errores."""
    errors = []

    first_name      = data.get('firstName', '').strip()
    second_name     = data.get('secondName', '').strip()
    first_lastname  = data.get('firstLastname', '').strip()
    second_lastname = data.get('secondLastname', '').strip()
    document        = data.get('document', '').strip()

    # Primer nombre: obligatorio, mín 2 caracteres, solo letras
    if not first_name:
        errors.append(MSG_FIRSTNAME_REQUIRED)
    elif len(first_name) < 2:
        errors.append(MSG_NAME_MIN_LENGTH)
    elif not NAME_REGEX.match(first_name):
        errors.append(MSG_NAME_ONLY_LETTERS)

    # Segundo nombre: opcional, pero si se proporciona mín 2 caracteres y solo letras
    if second_name:
        if len(second_name) < 2:
            errors.append(MSG_NAME_MIN_LENGTH)
        elif not NAME_REGEX.match(second_name):
            errors.append(MSG_NAME_ONLY_LETTERS)

    # Primer apellido: obligatorio, mín 2 caracteres, solo letras
    if not first_lastname:
        errors.append(MSG_LASTNAME_REQUIRED)
    elif len(first_lastname) < 2:
        errors.append(MSG_NAME_MIN_LENGTH)
    elif not NAME_REGEX.match(first_lastname):
        errors.append(MSG_NAME_ONLY_LETTERS)

    # Segundo apellido: opcional, pero si se proporciona mín 2 caracteres y solo letras
    if second_lastname:
        if len(second_lastname) < 2:
            errors.append(MSG_NAME_MIN_LENGTH)
        elif not NAME_REGEX.match(second_lastname):
            errors.append(MSG_NAME_ONLY_LETTERS)

    # Documento: obligatorio, mín 3 caracteres, solo dígitos
    if not document:
        errors.append(MSG_DOC_REQUIRED)
    elif len(document) < 3:
        errors.append(MSG_DOC_TOO_SHORT)
    elif not DOC_REGEX.match(document):
        errors.append(MSG_DOC_ONLY_DIGITS)

    # Fecha de ingreso: obligatoria
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