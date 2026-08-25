from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.employee_service import EmployeeService
from app.messages.messages import (
    MSG_CREATED, MSG_UPDATED, MSG_TERMINATED, MSG_DELETED
)

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
            'firstName':      request.form.get('firstName', ''),
            'secondName':     request.form.get('secondName', ''),
            'firstLastname':  request.form.get('firstLastname', ''),
            'secondLastname': request.form.get('secondLastname', ''),
            'document':       request.form.get('document', ''),
            'hireDate':       request.form.get('hireDate', ''),
        }
        emp, errors, code = service.create(data)
        if errors:
            return render_template('employees/register.html', error=errors[0], form_data=data)
        flash(MSG_CREATED, 'success')
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
    flash(MSG_TERMINATED, 'success')
    return redirect(url_for('employees.detail', id=id))


@employees_bp.route('/employees/<int:id>/edit', methods=['POST'])
def edit(id):
    data = {
        'firstName':      request.form.get('firstName', ''),
        'secondName':     request.form.get('secondName', ''),
        'firstLastname':  request.form.get('firstLastname', ''),
        'secondLastname': request.form.get('secondLastname', ''),
        'document':       request.form.get('document', ''),
        'hireDate':       request.form.get('hireDate', ''),
        'status':         request.form.get('status', ''),
    }
    emp, errors, code = service.update(id, data)
    if errors:
        original = service.get_by_id(id)
        return render_template(
            'employees/detail.html',
            employee=original.to_dict() if original else {},
            error=errors[0]
        )
    flash(MSG_UPDATED, 'success')
    return redirect(url_for('employees.detail', id=id))


@employees_bp.route('/employees/<int:id>/delete', methods=['POST'])
def delete(id):
    ok, errors, code = service.delete(id)
    if errors:
        original = service.get_by_id(id)
        return render_template(
            'employees/detail.html',
            employee=original.to_dict() if original else {},
            error=errors[0]
        )
    flash(MSG_DELETED, 'success')
    return redirect(url_for('employees.list'))