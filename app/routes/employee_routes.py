from flask import Blueprint, render_template, request

employees_bp = Blueprint('employees', __name__)

# Datos de ejemplo (Mock Data)
MOCK_EMPLOYEES = [
    {
        "id": 1,
        "document": "123456789",
        "fullName": "Juan Pérez",
        "hireDate": "01/08/2026",
        "endDate": None,
        "status": "ACTIVE"
    },
    {
        "id": 2,
        "document": "987654321",
        "fullName": "María López",
        "hireDate": "15/07/2026",
        "endDate": None,
        "status": "ACTIVE"
    },
    {
        "id": 3,
        "document": "456789123",
        "fullName": "Carlos Gómez",
        "hireDate": "01/02/2026",
        "endDate": "15/08/2026",
        "status": "INACTIVE"
    }
]

@employees_bp.route('/')
def dashboard():
    total = len(MOCK_EMPLOYEES)
    active = sum(1 for e in MOCK_EMPLOYEES if e["status"] == "ACTIVE")
    inactive = sum(1 for e in MOCK_EMPLOYEES if e["status"] == "INACTIVE")
    return render_template(
        'dashboard.html',
        totalEmployees=total,
        activeEmployees=active,
        inactiveEmployees=inactive,
        recentEmployees=MOCK_EMPLOYEES
    )

@employees_bp.route('/employees')
def list():
    return render_template('employees/list.html', employees=MOCK_EMPLOYEES)

@employees_bp.route('/employees/register', methods=['GET', 'POST'])
def register():
    return render_template('employees/register.html')

@employees_bp.route('/employees/<int:id>')
def detail(id):
    emp = next((e for e in MOCK_EMPLOYEES if e["id"] == id), MOCK_EMPLOYEES[0])
    demoStatus = request.args.get('demoStatus') or request.args.get('demo_status')
    if demoStatus in ['ACTIVE', 'INACTIVE']:
        emp = dict(emp)
        emp['status'] = demoStatus
        if demoStatus == 'INACTIVE' and not emp.get('endDate'):
            emp['endDate'] = '23/08/2026'

    return render_template('employees/detail.html', employee=emp)

@employees_bp.route('/employees/<int:id>/end_contract', methods=['POST'])
def end_contract(id):
    return render_template('employees/detail.html', employee=MOCK_EMPLOYEES[2])