# Patrones de Diseño para IaC con Terraform

## Fase 1: Exploración y Análisis

### 1. Singleton

**¿Cómo garantiza una sola instancia?**
- `SingletonMeta` es una metaclase que intercepta la creación de instancias mediante `__call__`
- Mantiene un diccionario `_instances` que almacena una única instancia por clase
- Antes de crear una nueva instancia, verifica si ya existe en el diccionario

**Rol del Lock:**
- `threading.Lock()` garantiza thread-safety en entornos concurrentes
- Previene race conditions cuando múltiples hilos intentan crear la instancia simultáneamente
- Asegura que solo un hilo pueda ejecutar el bloque de creación a la vez

---

### 2. Factory

**Encapsulación de creación:**
- La factory abstrae la lógica de construcción del `null_resource` de Terraform
- Centraliza los detalles de estructura JSON en un método estático
- El cliente solo necesita llamar `create(name)` sin conocer la estructura interna

**Propósito de triggers:**
- Los triggers fuerzan la recreación del recurso cuando cambian sus valores
- `factory_uuid` garantiza unicidad de cada recurso
- `timestamp` permite trackear cuándo fue generado el recurso

---

### 3. Prototype

**Diagrama UML:**
```
┌─────────────────────┐
│ ResourcePrototype   │
├─────────────────────┤
│ - template: dict    │
├─────────────────────┤
│ + clone(mutator)    │
└──────────┬──────────┘
           │
           ▼
    deepcopy(template)
           │
           ▼
      mutator(copy)
           │
           ▼
     return new_copy
```

**Rol del mutator:**
- Permite personalizar cada clon sin modificar el template original
- Recibe el clon recién creado y aplica transformaciones específicas
- Facilita crear variaciones (ej: renombrar recursos, añadir propiedades) manteniendo la estructura base

---

### 4. Composite

**Agregación de bloques:**
- `CompositeModule` actúa como contenedor de múltiples bloques Terraform
- `add()` acumula bloques individuales en una lista
- `export()` fusiona todos los children en un único diccionario JSON
- Combina recursos del mismo tipo (`resource.null_resource`) en un solo objeto válido para Terraform

---

### 5. Builder

**Orquestación de patrones:**

1. **Factory**: Crea el recurso base (`null_resource`)
2. **Prototype**: Convierte el recurso base en template clonable
3. **Clonación + Mutator**: Genera N copias personalizadas (renombrado `app_0`, `app_1`, etc.)
4. **Composite**: Agrega todos los clones en una estructura unificada
5. **Export**: Serializa el composite a JSON válido (`main.tf.json`)

**Flujo:**
```
Factory.create() → ResourcePrototype(template) → clone() × N → CompositeModule.add() → export(JSON)
```

El builder coordina estos patrones para construir infraestructura de forma declarativa y escalable.