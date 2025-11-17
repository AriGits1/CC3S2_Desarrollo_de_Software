"""
Genera la infraestructura de Terraform (main.tf.json) utilizando:
1. NullResourceFactory para crear un prototipo base.
2. ResourcePrototype para clonar el prototipo y aplicar mutaciones avanzadas.
"""
import json
import os
from factory import NullResourceFactory
from prototype import ResourcePrototype
from typing import Dict, Any

# ----------------------------------------------------------------------
# 1. Función Mutadora (Mutator)
# ----------------------------------------------------------------------

def add_welcome_file(block: Dict[str, Any]):
    """
    Mutador que realiza dos acciones en el bloque de recurso clonado:
    1. Añade un trigger 'welcome' al null_resource existente (app_0).
    2. Añade un nuevo bloque de recurso 'local_file' al nivel raíz 'resource'.
    """
    # 1. Mutación del null_resource existente (app_0)
    # NOTA: La estructura es: block -> resource[0] -> null_resource[0] -> app_0[0] -> triggers
    try:
        block["resource"][0]["null_resource"][0]["app_0"][0]["triggers"]["welcome"] = "¡Hola desde Prototype!"
    except (KeyError, IndexError):
        print("Advertencia: No se pudo modificar el trigger 'app_0'. Asegúrate de que el prototipo base contenga este recurso.")

    # 2. Adición del nuevo bloque 'local_file'
    # Se añade al nivel 'resource' dentro del array que contiene el null_resource.
    # El bloque local_file es una estructura {tipo: {nombre: {atributos}}}
    # NOTA: En la estructura de Terraform JSON, 'resource' es una lista de diccionarios.
    block["resource"].append({
        "local_file": [{
            "welcome_txt": [{
                "content": "Bienvenido al recurso mutado por Prototype.",
                "filename": "${path.module}/bienvenida.txt"
            }]
        }]
    })
    print("Mutator: Bloque 'local_file.welcome_txt' añadido.")


# ----------------------------------------------------------------------
# 2. Proceso de Generación
# ----------------------------------------------------------------------

# A. Crear un recurso base que actuará como Prototipo
base_resource_dict = NullResourceFactory.create(name="app_0")
base_prototype = ResourcePrototype(base_resource_dict)

# B. Clonar y Mutar el Prototipo
# Se usa la función mutadora 'add_welcome_file'
mutated_prototype = base_prototype.clone(mutator=add_welcome_file)
resource_block = mutated_prototype.data

# C. Estructura principal de Terraform (Proveedores)
terraform_config = {
    "terraform": {
        "required_providers": {
            "null": {
                "source": "hashicorp/null",
                "version": "~> 3.0"
            },
            # Añadir el proveedor 'local' para que 'local_file' funcione
            "local": { 
                "source": "hashicorp/local",
                "version": "~> 2.4"
            }
        }
    }
}

# D. Combina la configuración base y el recurso mutado
full_config = {**terraform_config, **resource_block}

# E. Genera el archivo main.tf.json
OUTPUT_DIR = "terraform"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "main.tf.json")

try:
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(full_config, f, indent=4)
    print(f"\n Archivo de configuración creado con éxito en: {OUTPUT_FILE}")
    print("   Contiene el 'null_resource' original y el nuevo 'local_file'.")

except Exception as e:
    print(f" Error al escribir el archivo: {e}")