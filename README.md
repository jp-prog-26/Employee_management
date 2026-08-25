# 👥 Sistema de Gestión de Empleados

Sistema básico para la gestión administrativa de empleados de una empresa. Permite registrar, consultar y actualizar la información del personal, así como gestionar la finalización de los contratos.

## 📑 Índice
 
- [Funcionalidades](#-funcionalidades)
- [Stack](#-stack)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Reglas de negocio](#-reglas-de-negocio)
- [FAQ / Problemas comunes](#-faq--problemas-comunes)

## 🚀 Funcionalidades

El sistema permite realizar las siguientes operaciones:

* **Registrar empleados:** Crear nuevos registros de empleados en el sistema.
* **Consultar empleados:** Obtener y visualizar la información de un empleado.
* **Actualizar estado:** Modificar el estado actual de un empleado.
* **Finalizar contrato:** Registrar la fecha de finalización del contrato y actualizar el estado del empleado.

## 🛠 Stack
 
- Python
- Flask `3.1.3`

## ⚙️ Instalación y ejecución
 
```bash
# 1. Clonar el repositorio
git clone https://github.com/jp-prog-26/Employee_management.git
cd Employee_management
 
# 2. Crear y activar un entorno virtual
python -m venv venv
 
# Windows
venv\Scripts\activate
 
# Linux / macOS
source venv/bin/activate
 
# 3. Instalar dependencias
pip install -r requirements.txt
 
# 4. Levantar el servidor
python run.py
```
 
Por defecto el servidor queda disponible en:
 
```
http://127.0.0.1:5000
```
 
> ℹ️ El proyecto corre en modo `debug=True` (recarga automática y trazas de error detalladas). No usar esta configuración en producción.

## 📋 Reglas de negocio

Para garantizar la correcta gestión de la información, el sistema implementa las siguientes reglas:

* El **nombre completo** del empleado es obligatorio.
* El **documento de identidad** debe ser único para cada empleado.
* Todo empleado nuevo debe registrarse inicialmente con el estado **`ACTIVE`**.
* Cuando finaliza el contrato de un empleado, su estado debe cambiar a **`INACTIVE`**.
* La **fecha de finalización** del contrato no puede ser anterior a la **fecha de ingreso** del empleado.

## 🎯 Objetivo

Desarrollar una solución sencilla que permita llevar un control administrativo básico del personal, asegurando la integridad de la información y el cumplimiento de las reglas de negocio establecidas.

## ❓ FAQ / Problemas comunes
 
**`ModuleNotFoundError: No module named 'flask'`**
El entorno virtual no está activado o no se instalaron las dependencias. Repetí los pasos 2 y 3 de instalación.
 
**El puerto 5000 ya está en uso**
Otro proceso lo está usando (en macOS suele ser AirPlay Receiver). Cambiá el puerto en `run.py`, en la línea `app.run(debug=True, port=5000)`, o cerrá el proceso que lo ocupa.
 
**Los cambios en el código no se reflejan**
Verificá que el servidor siga corriendo con `debug=True` (ya viene así por defecto) y que estés guardando los archivos dentro de la carpeta `app/`.