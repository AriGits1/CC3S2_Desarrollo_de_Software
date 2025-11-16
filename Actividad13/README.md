# Proyecto Terraform - Infrastructure as Code (IaC)


##  Propósito de la Actividad

Este proyecto tiene como objetivo comprender y aplicar los principios fundamentales de **Infrastructure as Code** (IaC) usando Terraform, específicamente:

1. **Gestión declarativa de infraestructura**: Definir recursos mediante código JSON
2. **Detección y remediación de drift**: Identificar cambios manuales no autorizados
3. **Migración de sistemas legacy**: Convertir configuraciones tradicionales a IaC
4. **Buenas prácticas**: Aplicar versionamiento, nomenclatura, y manejo seguro de secretos
5. **Automatización**: Generar múltiples entornos mediante scripts Python

---



##  Instrucciones de Ejecución

### Prerequisitos

```bash
# Instalar Terraform
# Windows: descargar de https://www.terraform.io/downloads
# macOS: brew install terraform
# Linux: sudo apt install terraform

# Instalar jq (formateador JSON)
# Windows Git Bash:
curl -L -o ~/bin/jq.exe https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-windows-amd64.exe

# Instalar Python 3.x (si no lo tienes)
```

### Paso 1: Generar Entornos

```bash
# Generar 10 entornos (app1 a app10)
python generate_envs.py

# Resultado: crea carpetas environments/app1/ hasta environments/app10/
```

### Paso 2: Inicializar y Verificar un Entorno

```bash
# Navegar a un entorno
cd environments/app1

# Inicializar Terraform (descarga providers)
terraform init

# Ver plan de ejecución (qué cambios se aplicarán)
terraform plan

# Aplicar cambios
terraform apply

# Ver estado actual
terraform show
```

### Paso 3: Migrar Sistema Legacy

```bash
# Crear entorno legacy de ejemplo
python setup_legacy.py

# Migrar a Terraform
python migrate_legacy.py

# Verificar resultado
cd environments/legacy_migrated
terraform init
terraform plan
```

### Paso 4: Formatear y Validar

```bash
# Formatear JSON con jq
cd modules/simulated_app
jq . network.tf.json > tmp && mv tmp network.tf.json

# Validar todos los entornos
cd environments/app1
terraform validate
```

---

##  Respuestas a Preguntas - Fase 1

### 1. ¿Cómo interpreta Terraform el cambio de variable?

Terraform interpreta los cambios de variables mediante un **proceso de reconciliación en 3 etapas**:

1. **Lectura del estado actual**: Lee `terraform.tfstate` para conocer el estado desplegado
2. **Evaluación de la configuración**: Procesa los archivos `.tf.json` y evalúa las expresiones `${var.xxx}`
3. **Generación del plan**: Compara estado actual vs. configuración deseada y calcula los cambios necesarios

**Ejemplo práctico:**
```
Cambio: "default": "local-network" → "default": "lab-net"

Terraform detecta:
~ null_resource.local_server
  ~ triggers.network: "local-network" → "lab-net"

Acción: Actualizar el trigger (update in-place)
```

### 2. ¿Qué diferencia hay entre modificar el JSON vs. parchear directamente el recurso?

| Aspecto | Modificar JSON (IaC) | Parchear Recurso Directamente |
|---------|---------------------|-------------------------------|
| **Trazabilidad** | ✅ Cambios registrados en Git | ❌ Sin historial |
| **Reproducibilidad** | ✅ Mismo resultado en cualquier entorno | ❌ Configuración única |
| **Auditoría** | ✅ Quién, cuándo, por qué | ❌ Sin registro |
| **Reversión** | ✅ `git revert` fácil | ❌ Manual y propenso a errores |
| **Drift** | ✅ Terraform detecta y corrige | ❌ Genera inconsistencias |

**Conclusión:** Modificar el JSON respeta el paradigma IaC donde el código es la única fuente de verdad.

### 3. ¿Por qué Terraform no recrea todo el recurso, sino que aplica el cambio "in-place"?

Terraform utiliza metadatos de cada atributo:

- **Atributos con `ForceNew: false`**: Permiten actualización in-place
- **Atributos con `ForceNew: true`**: Requieren destruir y recrear

Para `null_resource.triggers`, los cambios NO requieren recreación, solo actualizan metadata.

**Beneficios:**
- Evita downtime innecesario
- Mantiene IDs y referencias intactas
- Reduce operaciones destructivas

### 4. ¿Qué pasa si editas directamente `main.tf.json` en lugar de la plantilla de variables?

**Consecuencias:**

1. **Pérdida de centralización**: `network.tf.json` es el "single source of truth"
2. **Drift de generación**: Al ejecutar `generate_envs.py`, tus cambios se sobrescriben
3. **Inconsistencia entre entornos**: Imposible mantener paridad
4. **Dificultad de mantenimiento**: Cada entorno requiere edición manual

**Flujo correcto:**
```
Editar: modules/simulated_app/network.tf.json
    ↓
Regenerar: python generate_envs.py
    ↓
Verificar: terraform plan
```

---

##  Respuestas a Preguntas Abiertas - Fase 4

### 1. ¿Cómo extenderías este patrón para 50 módulos y 100 entornos?

**Estrategias:**

- **Estructura modular jerárquica**: Separar en `networking/`, `compute/`, `database/`, etc.
- **Generación dinámica con matrices**: Usar loops en Python para 50×100 = 5,000 configuraciones
- **Terraform Workspaces**: `dev`, `staging`, `prod`
- **Remote State**: Compartir outputs entre módulos
- **CI/CD paralelo**: Ejecutar `terraform plan` en paralelo para múltiples entornos

```python
# Ejemplo de generación escalable
MODULES = ['networking', 'compute', 'database', 'monitoring']
ENVIRONMENTS = ['dev', 'staging', 'prod']
REPLICAS = {'dev': 10, 'staging': 30, 'prod': 60}

for module in MODULES:
    for env in ENVIRONMENTS:
        for i in range(REPLICAS[env]):
            generate_instance(module, env, i)
```

### 2. ¿Qué prácticas de revisión de código aplicarías a los `.tf.json`?

**Validación automática:**
- **Pre-commit hooks**: `jq --check` para validar sintaxis
- **CI/CD**: `terraform validate` en todos los entornos
- **Análisis de seguridad**: `tfsec`, `checkov`

**Checklist manual:**
- [ ] ¿Sintaxis JSON válida?
- [ ] ¿Nomenclatura consistente?
- [ ] ¿Variables sensibles marcadas como `sensitive: true`?
- [ ] ¿Sin secretos hardcodeados?
- [ ] ¿Plan muestra solo cambios esperados?
- [ ] ¿Documentación actualizada?

**Proceso:**
1. Desarrollador: hace cambios, ejecuta `terraform plan` localmente
2. CI: valida, escanea seguridad, genera plans
3. Reviewer: revisa plans en comentarios del PR
4. Merge: requiere ≥2 aprobaciones + CI verde

### 3. ¿Cómo gestionarías secretos en producción (sin Vault)?

**Opciones:**

1. **Variables de entorno:**
   ```bash
   export TF_VAR_api_key="sk-xxxxx"
   terraform apply
   ```

2. **Archivos .tfvars NO versionados:**
   ```bash
   # secrets.auto.tfvars (en .gitignore)
   api_key = "sk-xxxxx"
   ```

3. **Cloud Secrets Manager:**
   ```bash
   # AWS Secrets Manager
   aws secretsmanager get-secret-value --secret-id prod/api/key
   
   # AWS Systems Manager Parameter Store
   aws ssm get-parameter --name /prod/api/key --with-decryption
   ```

4. **Cifrado con git-crypt:**
   ```bash
   git-crypt init
   echo "secrets.tfvars filter=git-crypt" >> .gitattributes
   ```

5. **Variables marcadas como sensitive:**
   ```json
   {
     "variable": [{
       "api_key": [{
         "type": "string",
         "sensitive": true
       }]
     }]
   }
   ```

** NUNCA:** Hardcodear en `.tf.json`, commitear secretos, compartir por Slack/email

### 4. ¿Qué workflows de revisión aplicarías a los JSON generados?

**Pipeline CI/CD:**

```yaml
# Validación
- Validar sintaxis JSON (jq)
- Terraform validate
- Formateo automático

# Seguridad
- tfsec (vulnerabilidades)
- checkov (compliance)
- Detectar secretos expuestos

# Plan
- terraform plan en todos los entornos
- Publicar plans en comentarios del PR
- Estimación de costos

# Apply
- dev: automático después de merge
- staging: automático con notificación
- prod: manual con aprobación
```

**Pre-commit hooks:**
```bash
# .git/hooks/pre-commit
1. Validar JSON con jq
2. Formatear automáticamente
3. Buscar secretos expuestos
4. Regenerar entornos si templates cambiaron
```

**Auto-regeneración:**
```python
# watch_and_regenerate.py
# Vigila cambios en modules/ y regenera automáticamente
```

---

##  Comandos Útiles

```bash
# Formatear todos los JSON
find . -name "*.tf.json" -exec sh -c 'jq --sort-keys . "$1" > "$1.tmp" && mv "$1.tmp" "$1"' _ {} \;

# Validar sintaxis
find . -name "*.tf.json" -exec jq empty {} \;

# Validar todos los entornos
for d in environments/*/; do (cd "$d" && terraform validate); done

# Limpiar estados
find environments -name ".terraform" -type d -exec rm -rf {} +
find environments -name "terraform.tfstate*" -exec rm -f {} +

# Plan en todos los entornos
for d in environments/*/; do 
    echo "=== $d ===" 
    (cd "$d" && terraform plan)
done
```

---

##  Conclusiones

Este proyecto demuestra los principios fundamentales de Infrastructure as Code:

- **Declarativo sobre imperativo**: Definimos "qué" queremos, no "cómo"
- **Versionamiento**: Todo cambio queda registrado en Git
- **Reproducibilidad**: Los mismos archivos producen la misma infraestructura
- **Automatización**: Scripts Python generan configuraciones sin intervención manual
- **Detección de drift**: Terraform identifica y corrige cambios manuales

**Lecciones aprendidas:**
- El código es la única fuente de verdad
- Los cambios manuales rompen la consistencia
- La migración de legacy a IaC es posible y beneficiosa
- Las buenas prácticas son esenciales desde el inicio

---

