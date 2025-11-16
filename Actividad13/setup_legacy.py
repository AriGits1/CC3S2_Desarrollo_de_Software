#!/usr/bin/env python3
"""
Script para crear archivos legacy de ejemplo
Ejecutar antes de migrate_legacy.py
"""

import os


def create_legacy_environment():
    """
    Crea un entorno legacy de ejemplo con config.cfg y run.sh
    """
    legacy_dir = "legacy"
    
    # Crear directorio
    os.makedirs(legacy_dir, exist_ok=True)
    
    # Crear config.cfg
    config_content = """# Configuración del servidor legacy
PORT=8080
HOST=localhost
APP_NAME=LegacyApp
ENVIRONMENT=production
"""
    
    config_path = os.path.join(legacy_dir, "config.cfg")
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print(f"✓ Creado: {config_path}")
    
    # Crear run.sh
    run_content = """#!/bin/bash
# Script de arranque legacy
echo "Arrancando $APP_NAME en puerto $PORT"
echo "Host: $HOST - Entorno: $ENVIRONMENT"
"""
    
    run_path = os.path.join(legacy_dir, "run.sh")
    with open(run_path, 'w') as f:
        f.write(run_content)
    
    # Hacer ejecutable
    os.chmod(run_path, 0o755)
    
    print(f"✓ Creado: {run_path}")
    print(f"\n✓ Entorno legacy creado en '{legacy_dir}/'")
    print("\nAhora ejecuta:")
    print("  python migrate_legacy.py")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CREANDO ENTORNO LEGACY DE EJEMPLO")
    print("="*60 + "\n")
    
    create_legacy_environment()
    
    print()
