"""Patrón Factory
Encapsula la lógica de creación de objetos para recursos Terraform del tipo null_resource.
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone

class NullResourceFactory:
    """
    Fábrica para crear bloques de recursos `null_resource` en formato Terraform JSON.
    Cada recurso incluye triggers personalizados y valores únicos para garantizar idempotencia.
    """

    @staticmethod
    def _generate_null_resource_block(name: str, triggers: Dict[str, Any]) -> Dict[str, Any]:
        """Estructura el diccionario final del recurso null_resource."""
        return {
            "resource": [{
                "null_resource": [{
                    name: [{
                        "triggers": triggers
                    }]
                }]
            }]
        }

    @staticmethod
    def create(name: str, triggers: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Crea un bloque de recurso Terraform tipo `null_resource` con triggers personalizados.
        
        Args:
            name: Nombre del recurso dentro del bloque.
            triggers: Diccionario de valores personalizados que activan recreación del recurso.
                      Si no se proporciona, se inicializa con un UUID y un timestamp UTC.

        Returns:
            Diccionario compatible con la estructura JSON de Terraform para null_resource.
        """
        triggers = triggers or {}

        # Agrega un trigger por defecto: UUID aleatorio para asegurar unicidad
        triggers.setdefault("factory_uuid", str(uuid.uuid4()))

        # Agrega un trigger con timestamp actual en UTC
        triggers.setdefault("timestamp", datetime.now(tz=timezone.utc).isoformat())

        return NullResourceFactory._generate_null_resource_block(name, triggers)

class TimestampedNullResourceFactory(NullResourceFactory):
    """
    Fábrica especializada que crea un null_resource usando un timestamp con formato
    personalizado ('fmt') como el único trigger.
    """
    @staticmethod
    def create(name: str, fmt: str) -> Dict[str, Any]:
        """
        Crea un null_resource cuyo trigger principal es un timestamp formateado.

        Args:
            name: Nombre del recurso dentro del bloque.
            fmt: String de formato para el timestamp (e.g., '%Y%m%d').

        Returns:
            Diccionario compatible con la estructura JSON de Terraform para null_resource.
        """
        # 1. Genera el timestamp con el formato proporcionado
        ts = datetime.utcnow().strftime(fmt)
        
        # 2. Define el diccionario de triggers usando 'ts'
        triggers = {
            "formatted_timestamp": ts
        }

        # 3. Retorna la estructura del recurso
        return NullResourceFactory._generate_null_resource_block(name, triggers)

# --- Validación interna ---
if __name__ == '__main__':
    # Validación de la fábrica base
    base_resource = NullResourceFactory.create("base_config")
    print("Recurso Base:")
    print(base_resource)

    # Validación de la fábrica extendida con formato '%Y%m%d'
    timestamped_resource = TimestampedNullResourceFactory.create("daily_build", "%Y%m%d")
    print("\nRecurso Timestamped (Formato %Y%m%d):")
    print(timestamped_resource)