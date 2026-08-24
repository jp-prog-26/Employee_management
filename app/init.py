from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Registro de Blueprint de rutas de empleados
    from app.routes.employee_routes import employees_bp, dashboard
    app.register_blueprint(employees_bp)

    # Alias para la ruta raíz y endpoint dashboard
    app.add_url_rule('/', endpoint='dashboard', view_func=dashboard)

    # Manejo de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app