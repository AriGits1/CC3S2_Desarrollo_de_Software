# Actividad 9: pytest + coverage + fixtures + factories + mocking + TDD

**Autor:** Ariana Mercado  
**Curso:** CC3S2 - Desarrollo de Software  
**Fecha:** 10 Octubre 2025

## 📋 Descripción General

Este proyecto resuelve 7 actividades de testing en Python, demostrando dominio completo de las herramientas y técnicas modernas de testing profesional.

## 🚀 Cómo Ejecutar

### Requisitos Previos
- **Python:** 3.10 o superior
- **Sistema Operativo:** Linux/WSL, macOS, o Windows

### Instalación Paso a Paso

#### 1. Verificar versión de Python
- python3 --version
# Debe mostrar Python 3.10.x o superior

### 2. Crear entorno virtual
# Crear venv
- python3 -m venv .venv

# Activar venv
- source .venv/bin/activate        # /WSL
# .venv\Scripts\activate         # Windows CMD
# .venv\Scripts\Activate.ps1     # Windows PowerShell

###3. Instalar dependencias
- pip install -r requirements.txt
##Ejecutar todos los test
- make test_all
## Ejecutar test con cobertura
- make cov
##Ejecutar tests de una actividad específica
- cd soluciones/aserciones_pruebas
- pytest -v


