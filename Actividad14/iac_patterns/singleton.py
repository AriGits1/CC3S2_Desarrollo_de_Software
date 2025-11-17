"""Patrón Singleton

Asegura que una clase tenga una única instancia global, compartida en todo el sistema.
Esta implementación es segura para entornos con múltiples hilos (thread-safe).
"""

import threading
from typing import Any, Dict
from datetime import datetime, timezone

class SingletonMeta(type):
    """
    Metaclase Singleton segura para hilos (thread-safe).

    Asegura que todas las instancias de la clase que use esta metaclase
    compartan el mismo objeto (único en memoria).
    """
    _instances: Dict[type, "ConfigSingleton"] = {}
    _lock: threading.Lock = threading.Lock() 

    def __call__(cls, *args, **kwargs):
        """
        Controla la creación de instancias: solo permite una única instancia por clase.
        Si ya existe, devuelve la existente. Si no, la crea protegida por un lock.
        """
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigSingleton(metaclass=SingletonMeta):
    """
    Clase Singleton que actúa como contenedor de configuración global.
    Todas las clases del sistema pueden consultar y modificar esta configuración compartida.
    """

    def __init__(self, env_name: str = "default") -> None:
        """
        Inicializa la configuración con un nombre de entorno y un timestamp de creación.
        """
        self.env_name = env_name
        self.created_at = datetime.now(tz=timezone.utc).isoformat()
        self.settings: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor en la configuración global.
        """
        self.settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Recupera un valor de la configuración global.
        """
        return self.settings.get(key, default)

    def reset(self):
        """
        Limpia completamente el diccionario de configuración (settings),
        manteniendo inalterados el nombre del entorno y el timestamp de creación.
        """
        # TODO: implementar
        self.settings = {}
        
# --- Validación ---
if __name__ == '__main__':
    c1 = ConfigSingleton("dev")
    created = c1.created_at

    # 1. Se añade un valor
    c1.settings["x"] = 1
    print(f"Settings antes de reset: {c1.settings}")
    print(f"Created_at antes de reset: {c1.created_at}")

    # 2. Se llama al método reset
    c1.reset()

    # 3. Validaciones
    assert c1.settings == {}
    assert c1.created_at == created

    # Se crea una segunda instancia (debe ser la misma)
    c2 = ConfigSingleton("prod") 
    assert c2.settings == {} 
    assert c2.created_at == created # La fecha de creación debe ser la misma

    print("\n ¡Validación exitosa!")
    print(f"Settings después de reset: {c1.settings}")
    print(f"Created_at después de reset (inalterado): {c1.created_at}")
    print(f"Created_at de c2 (mismo que c1): {c2.created_at}")