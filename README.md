# 👥 Sistema de Gestión de Empleados

Sistema básico para la gestión administrativa de empleados de una empresa. Permite registrar, consultar y actualizar la información del personal, así como gestionar la finalización de los contratos.

## 🚀 Funcionalidades

El sistema permite realizar las siguientes operaciones:

* **Registrar empleados:** Crear nuevos registros de empleados en el sistema.
* **Consultar empleados:** Obtener y visualizar la información de un empleado.
* **Actualizar estado:** Modificar el estado actual de un empleado.
* **Finalizar contrato:** Registrar la fecha de finalización del contrato y actualizar el estado del empleado.

## 📋 Reglas de negocio

Para garantizar la correcta gestión de la información, el sistema implementa las siguientes reglas:

* El **nombre completo** del empleado es obligatorio.
* El **documento de identidad** debe ser único para cada empleado.
* Todo empleado nuevo debe registrarse inicialmente con el estado **`ACTIVE`**.
* Cuando finaliza el contrato de un empleado, su estado debe cambiar a **`INACTIVE`**.
* La **fecha de finalización** del contrato no puede ser anterior a la **fecha de ingreso** del empleado.

## 🎯 Objetivo

Desarrollar una solución sencilla que permita llevar un control administrativo básico del personal, asegurando la integridad de la información y el cumplimiento de las reglas de negocio establecidas.