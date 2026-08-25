from flask import Blueprint, jsonify, request
from app.services.employee_service import EmployeeService
from app.messages.messages import MSG_NOT_FOUND, MSG_CREATED, MSG_TERMINATED, MSG_DELETED, MSG_UPDATED

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
service = EmployeeService()


# ------------------------------------------------------------------ #
# POST /api/v1/employees  — Registrar empleado
# ------------------------------------------------------------------ #
@api_bp.route('/employees', methods=['POST'])
def api_create():
    data = request.get_json(silent=True) or {}
    emp, errors, code = service.create(data)
    if errors:
        return jsonify({'error': errors[0]}), code
    return jsonify({'message': MSG_CREATED, 'employee': emp}), code


# ------------------------------------------------------------------ #
# GET /api/v1/employees  — Listar (filtros: ?status=ACTIVE&search=Juan)
# ------------------------------------------------------------------ #
@api_bp.route('/employees', methods=['GET'])
def api_list():
    status = request.args.get('status')
    search = request.args.get('search')
    employees = service.get_all(status=status, search=search)
    return jsonify([e.to_dict() for e in employees]), 200


# ------------------------------------------------------------------ #
# GET /api/v1/employees/<id>  — Detalle por ID
# ------------------------------------------------------------------ #
@api_bp.route('/employees/<int:employee_id>', methods=['GET'])
def api_detail(employee_id):
    emp = service.get_by_id(employee_id)
    if not emp:
        return jsonify({'error': MSG_NOT_FOUND}), 404
    return jsonify(emp.to_dict()), 200


# ------------------------------------------------------------------ #
# GET /api/v1/employees/doc/<doc>  — Buscar por documento
# ------------------------------------------------------------------ #
@api_bp.route('/employees/doc/<string:document>', methods=['GET'])
def api_by_document(document):
    emp = service.get_by_document(document)
    if not emp:
        return jsonify({'error': MSG_NOT_FOUND}), 404
    return jsonify(emp.to_dict()), 200


# ------------------------------------------------------------------ #
# PATCH /api/v1/employees/<id>/status  — Cambiar estado
# ------------------------------------------------------------------ #
@api_bp.route('/employees/<int:employee_id>/status', methods=['PATCH'])
def api_update_status(employee_id):
    data = request.get_json(silent=True) or {}
    emp, errors, code = service.update_status(employee_id, data)
    if errors:
        return jsonify({'error': errors[0]}), code
    return jsonify({'message': MSG_UPDATED, 'employee': emp}), code


# ------------------------------------------------------------------ #
# POST /api/v1/employees/<id>/terminate  — Finalizar contrato
# ------------------------------------------------------------------ #
@api_bp.route('/employees/<int:employee_id>/terminate', methods=['POST'])
def api_terminate(employee_id):
    data = request.get_json(silent=True) or {}
    emp, errors, code = service.terminate(employee_id, data)
    if errors:
        return jsonify({'error': errors[0]}), code
    return jsonify({'message': MSG_TERMINATED, 'employee': emp}), code


# ------------------------------------------------------------------ #
# DELETE /api/v1/employees/<id>  — Eliminar empleado
# ------------------------------------------------------------------ #
@api_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def api_delete(employee_id):
    ok, errors, code = service.delete(employee_id)
    if errors:
        return jsonify({'error': errors[0]}), code
    return jsonify({'message': MSG_DELETED}), code