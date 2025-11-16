#!/usr/bin/env python3
"""
Script de migración: Legacy -> Terraform IaC
Lee config.cfg y run.sh, genera network.tf.json y main.tf.json equivalentes
"""

import os
import re
import json
import subprocess
import sys


def parse_config_file(config_path):
    """
    Lee config.cfg y extrae variables en formato KEY=VALUE
    Retorna un diccionario con las configuraciones
    """
    config = {}
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} no existe")
        return config
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignorar líneas vacías o comentarios
            if not line or line.startswith('#'):
                continue
            
            # Parsear KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config


def parse_run_script(script_path):
    """
    Lee run.sh y extrae el comando principal
    Retorna el comando a ejecutar
    """
    if not os.path.exists(script_path):
        print(f"Error: {script_path} no existe")
        return None
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Buscar líneas que contengan echo u otros comandos
    # Ignorar shebang y comentarios
    lines = content.split('\n')
    commands = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#!') and not line.startswith('#'):
            commands.append(line)
    
    # Retornar todos los comandos concatenados
    return ' && '.join(commands) if commands else 'echo "Legacy script"'


def generate_network_tf_json(config, output_dir):
    """
    Genera network.tf.json con variables basadas en config.cfg
    """
    variables = {}
    
    # Crear variables para cada configuración del legacy
    for key, value in config.items():
        var_name = key.lower()
        variables[var_name] = [{
            "type": "string",
            "default": value,
            "description": f"Variable migrada desde legacy config: {key}"
        }]
    
    # Añadir variables estándar
    if "name" not in variables:
        variables["name"] = [{
            "type": "string",
            "default": "legacy-app",
            "description": "Nombre del servidor migrado"
        }]
    
    if "network" not in variables:
        variables["network"] = [{
            "type": "string",
            "default": "legacy-network",
            "description": "Nombre de la red migrada"
        }]
    
    network_config = {
        "variable": [variables]
    }
    
    output_path = os.path.join(output_dir, "network.tf.json")
    with open(output_path, 'w') as f:
        json.dump(network_config, f, indent=4, sort_keys=True)
    
    print(f"✓ Generado: {output_path}")
    return output_path


def generate_main_tf_json(config, command, output_dir):
    """
    Genera main.tf.json con el recurso null_resource equivalente al script legacy
    """
    # Sustituir variables del legacy en el comando
    # Convertir $PORT -> ${var.port}
    terraform_command = command
    for key in config.keys():
        var_name = key.lower()
        # Reemplazar $VAR por ${var.var}
        terraform_command = terraform_command.replace(f'${key}', f'${{var.{var_name}}}')
    
    # Crear triggers basados en las variables del config
    triggers = {
        "name": "${var.name}",
        "network": "${var.network}"
    }
    
    # Añadir cada variable del config como trigger
    for key in config.keys():
        var_name = key.lower()
        triggers[var_name] = f"${{var.{var_name}}}"
    
    main_config = {
        "resource": [{
            "null_resource": [{
                "legacy_migrated": [{
                    "triggers": triggers,
                    "provisioner": [{
                        "local-exec": {
                            "command": terraform_command
                        }
                    }]
                }]
            }]
        }]
    }
    
    output_path = os.path.join(output_dir, "main.tf.json")
    with open(output_path, 'w') as f:
        json.dump(main_config, f, indent=4, sort_keys=True)
    
    print(f"✓ Generado: {output_path}")
    return output_path


def verify_with_terraform(tf_dir):
    """
    Ejecuta terraform init y terraform plan para verificar la configuración
    """
    print(f"\n{'='*60}")
    print("Verificando con Terraform...")
    print(f"{'='*60}\n")
    
    original_dir = os.getcwd()
    
    try:
        os.chdir(tf_dir)
        
        # Terraform init
        print("► Ejecutando: terraform init")
        result = subprocess.run(
            ['terraform', 'init'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("✗ Error en terraform init:")
            print(result.stderr)
            return False
        
        print("✓ terraform init exitoso\n")
        
        # Terraform plan
        print("► Ejecutando: terraform plan")
        result = subprocess.run(
            ['terraform', 'plan'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print("✗ Error en terraform plan:")
            print(result.stderr)
            return False
        
        print("✓ terraform plan exitoso")
        return True
        
    except FileNotFoundError:
        print("✗ Error: terraform no está instalado o no está en el PATH")
        return False
    
    finally:
        os.chdir(original_dir)


def main():
    """
    Función principal de migración
    """
    print(f"\n{'='*60}")
    print("MIGRACIÓN LEGACY -> TERRAFORM IaC")
    print(f"{'='*60}\n")
    
    # Directorios
    legacy_dir = "legacy"
    output_dir = "environments/legacy_migrated"
    
    # Archivos legacy
    config_file = os.path.join(legacy_dir, "config.cfg")
    run_script = os.path.join(legacy_dir, "run.sh")
    
    # Verificar que existen los archivos legacy
    if not os.path.exists(legacy_dir):
        print(f"✗ Error: El directorio '{legacy_dir}/' no existe")
        print("  Crea los archivos legacy primero:")
        print("  mkdir legacy")
        print("  echo 'PORT=8080' > legacy/config.cfg")
        print("  echo '#!/bin/bash' > legacy/run.sh")
        print("  echo 'echo \"Arrancando en puerto \\$PORT\"' >> legacy/run.sh")
        sys.exit(1)
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Paso 1: Leer configuración legacy
    print("1. Leyendo archivos legacy...")
    config = parse_config_file(config_file)
    command = parse_run_script(run_script)
    
    print(f"   Configuración encontrada: {config}")
    print(f"   Comando encontrado: {command}\n")
    
    # Paso 2: Generar archivos Terraform
    print("2. Generando archivos Terraform...")
    generate_network_tf_json(config, output_dir)
    generate_main_tf_json(config, command, output_dir)
    print()
    
    # Paso 3: Verificar con Terraform
    print("3. Verificando con Terraform...")
    success = verify_with_terraform(output_dir)
    
    # Resumen
    print(f"\n{'='*60}")
    if success:
        print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*60}")
        print(f"\nArchivos generados en: {output_dir}/")
        print("  - network.tf.json")
        print("  - main.tf.json")
        print("\nPara aplicar los cambios:")
        print(f"  cd {output_dir}")
        print("  terraform apply")
    else:
        print("✗ MIGRACIÓN COMPLETADA CON ADVERTENCIAS")
        print(f"{'='*60}")
        print("\nRevisa los archivos generados y ejecuta manualmente:")
        print(f"  cd {output_dir}")
        print("  terraform init")
        print("  terraform plan")
    
    print()


if __name__ == "__main__":
    main()
