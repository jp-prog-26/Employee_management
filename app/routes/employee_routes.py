from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.employee_service import EmployeeService

employees_bp = Blueprint('employees', __name__)
service = EmployeeService()


@employees_bp.route('/')
def dashboard():
    stats = service.get_dashboard_stats()
    return render_template('dashboard.html', **stats)


@employees_bp.route('/employees')
def list():
    employees = service.get_all()
    return render_template('employees/list.html', employees=[e.to_dict() for e in employees])


@employees_bp.route('/employees/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'fullName': request.form.get('fullName', ''),
            'document': request.form.get('document', ''),
            'hireDate': request.form.get('hireDate', ''),
        }
        emp, errors, code = service.create(data)
        if errors:
            return render_template('employees/register.html', error=errors[0], form_data=data)
        return redirect(url_for('employees.detail', id=emp['id']))
    return render_template('employees/register.html')


@employees_bp.route('/employees/<int:id>')
def detail(id):
    emp = service.get_by_id(id)
    if not emp:
        return render_template('errors/404.html'), 404
    return render_template('employees/detail.html', employee=emp.to_dict())


@employees_bp.route('/employees/<int:id>/end_contract', methods=['POST'])
def end_contract(id):
    data = {'endDate': request.form.get('endDate', '')}
    emp, errors, code = service.terminate(id, data)
    if errors:
        original = service.get_by_id(id)
        return render_template(
            'employees/detail.html',
            employee=original.to_dict() if original else {},
            error=errors[0]
        )
    return redirect(url_for('employees.detail', id=id))