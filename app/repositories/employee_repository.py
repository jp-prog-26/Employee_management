from app.database import get_db
from app.models.employee import Employee
from typing import Optional, List


class EmployeeRepository:
    """Capa de acceso a datos: todas las queries SQL viven aqui."""

    def get_all(self, status: Optional[str] = None, search: Optional[str] = None) -> List[Employee]:
        db = get_db()
        query = 'SELECT * FROM employees WHERE 1=1'
        params = []

        if status in ('ACTIVE', 'INACTIVE'):
            query += ' AND status = ?'
            params.append(status)

        if search:
            query += ' AND (full_name LIKE ? OR document LIKE ?)'
            like = f'%{search}%'
            params.extend([like, like])

        query += ' ORDER BY id DESC'
        rows = db.execute(query, params).fetchall()
        return [Employee.from_row(r) for r in rows]

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        db = get_db()
        row = db.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        return Employee.from_row(row) if row else None

    def get_by_document(self, document: str) -> Optional[Employee]:
        db = get_db()
        row = db.execute('SELECT * FROM employees WHERE document = ?', (document,)).fetchone()
        return Employee.from_row(row) if row else None

    def create(self, document: str, full_name: str, hire_date: str) -> Employee:
        db = get_db()
        cursor = db.execute(
            'INSERT INTO employees (document, full_name, hire_date, status) VALUES (?, ?, ?, ?)',
            (document, full_name, hire_date, 'ACTIVE')
        )
        db.commit()
        return self.get_by_id(cursor.lastrowid)

    def update_status(self, employee_id: int, status: str) -> Optional[Employee]:
        db = get_db()
        db.execute('UPDATE employees SET status = ? WHERE id = ?', (status, employee_id))
        db.commit()
        return self.get_by_id(employee_id)

    def terminate(self, employee_id: int, end_date: str) -> Optional[Employee]:
        db = get_db()
        db.execute(
            'UPDATE employees SET status = ?, end_date = ? WHERE id = ?',
            ('INACTIVE', end_date, employee_id)
        )
        db.commit()
        return self.get_by_id(employee_id)

    def delete(self, employee_id: int) -> bool:
        db = get_db()
        cursor = db.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        db.commit()
        return cursor.rowcount > 0

    def get_recent(self, limit: int = 5) -> List[Employee]:
        db = get_db()
        rows = db.execute(
            'SELECT * FROM employees ORDER BY id DESC LIMIT ?', (limit,)
        ).fetchall()
        return [Employee.from_row(r) for r in rows]

    def count_by_status(self) -> dict:
        db = get_db()
        rows = db.execute(
            'SELECT status, COUNT(*) as total FROM employees GROUP BY status'
        ).fetchall()
        counts = {'ACTIVE': 0, 'INACTIVE': 0}
        for r in rows:
            counts[r['status']] = r['total']
        counts['TOTAL'] = counts['ACTIVE'] + counts['INACTIVE']
        return counts