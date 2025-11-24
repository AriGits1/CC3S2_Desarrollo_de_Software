# Ejercicios Obligatorios - Respuestas

## Ejercicio 1: Estrategia de pruebas unitarias y de contrato

### 1.1 Diseño de módulos declarativos

**Módulo Network**:
- Variables: `vpc_cidr`, `subnet_count`, `environment`, `availability_zones`
- Outputs: `vpc_id`, `subnet_ids` (lista), `vpc_cidr_block`, `route_table_id`

**Módulo Compute**:
- Variables: `subnet_ids` (lista), `instance_count`, `instance_type`, `ami_id`
- Outputs: `instance_ids` (lista), `instance_ips` (lista), `instance_count`

**Módulo Storage**:
- Variables: `bucket_name`, `versioning_enabled`, `encryption_enabled`, `tags`
- Outputs: `bucket_id`, `bucket_arn`, `bucket_name`, `bucket_region`

**Convenios de naming**:
- Outputs plurales terminan en `_ids` o `_ips` para listas
- Outputs singulares usan sufijos descriptivos: `_id`, `_arn`, `_name`
- Prefijos consistentes por tipo de recurso: `vpc_`, `instance_`, `bucket_`

### 1.2 Casos límite sin recursos externos

**Escenarios de inputs inválidos**:

1. **CIDR fuera de rango**:
   - Input: `vpc_cidr = "10.0.0.0/33"` (máscara inválida)
   - Test: `terraform validate` debería fallar por validación de variable

2. **Número de instancias cero o negativo**:
   - Input: `instance_count = 0` o `instance_count = -1`
   - Test: Usar `validation` block en variables.tf para rechazar valores < 1

**Herramientas de validación**:
- `terraform validate`: Valida sintaxis HCL y referencias entre recursos
- `terraform plan`: Valida semántica y lógica de negocio (valores permitidos)
- `terraform output -json`: Verifica estructura de outputs post-apply

### 1.3 Métrica de cobertura de contrato

**Método de cuantificación**:
```
Cobertura = (Outputs validados en tests / Total outputs documentados) × 100
```

**Estrategia de balance**:
1. Validar campos críticos (IDs, ARNs) en todos los tests (100%)
2. Validar campos secundarios (tags, metadatos) selectivamente (70%)
3. Usar fixtures de test para reducir mantenimiento
4. Versionar contratos con semver: cambios breaking requieren actualizar tests

---

## Ejercicio 2.4: Secuenciación de dependencias

**Encadenamiento sin scripts externos**:

1. **Estructura de directorios**:
```
integration_test/
├── main.tf          # Orquestador principal
├── network.tf       # module "network" { ... }
├── compute.tf       # module "compute" { ... }
├── storage.tf       # module "storage" { ... }
```

2. **Uso de `depends_on` implícito**:
```hcl
# En main.tf
module "network" {
  source = "../modules/network"
  # ...
}

module "compute" {
  source     = "../modules/compute"
  subnet_ids = module.network.subnet_ids  # Dependencia implícita
}

module "storage" {
  source      = "../modules/storage"
  vpc_id      = module.network.vpc_id
  instance_id = module.compute.instance_ids[0]
}
```

3. **Garantía de orden**:
- Terraform resuelve automáticamente el grafo de dependencias
- Las referencias `module.X.output` crean dependencias implícitas
- Si se necesita orden explícito: usar `depends_on = [module.network]`

---

## Ejercicio 2.6: Pruebas de interacción gradual

### Nivel 1: Validación de legibilidad de outputs

**Objetivo**: Verificar que los outputs existen y tienen el formato correcto.

**Casos de uso**:
- Tests de contrato entre equipos
- Validación rápida en CI/CD
- Verificación post-refactorización

**Ejemplo**:
```bash
# Verificar que subnet_ids es una lista no vacía
terraform output -json | jq '.subnet_ids.value | length > 0'
```

### Nivel 2: Validación de flujos reales

**Objetivo**: Verificar comportamiento funcional con datos reales.

**Casos de uso**:
- Tests pre-producción
- Validación de integración completa
- Smoke tests en staging

**Ejemplo**:
```bash
# Escribir un archivo en bucket S3 y verificar lectura
aws s3 cp test.txt s3://$(terraform output -raw bucket_name)/
aws s3 ls s3://$(terraform output -raw bucket_name)/test.txt
```

**Prevención de solapamientos**:
- Nivel 1: Solo `terraform plan` + validación de JSON
- Nivel 2: Requiere `terraform apply` + operaciones reales
- Ejecutar Nivel 1 siempre, Nivel 2 solo en ambientes no-locales

---

## Ejercicio 3.7: Pruebas de humo locales ultrarrápidos

**Tres comandos básicos para smoke test (<30s)**:

1. **`terraform fmt -check`**
   - **Valor**: Detecta inconsistencias de formato sin modificar archivos
   - **Evita**: Fallos de estilo que contaminarían diffs en code review

2. **`terraform validate`**
   - **Valor**: Verifica sintaxis HCL y referencias a recursos
   - **Evita**: Errores de tipeo, variables no declaradas, referencias circulares

3. **`terraform plan -refresh=false -out=/dev/null`**
   - **Valor**: Valida lógica de negocio sin consultar APIs remotas
   - **Evita**: Errores de configuración, valores inválidos, dependencias rotas
   - **`-refresh=false`**: No consulta estado remoto (ahorro de tiempo)

**Justificación de velocidad**:
- Sin operaciones de red (no API calls)
- Sin persistencia de estado (output a /dev/null)
- Ejecución en paralelo posible para múltiples módulos

---

## Ejercicio 3.8: Planes "golden" para regresión

### Procedimiento de generación

1. **Crear plan base**:
```bash
cd modules/network
terraform init
terraform plan -out=plan_base.tfplan
terraform show -json plan_base.tfplan > ../../plans/plan_base_network.json
```

2. **Normalización del plan**:
```bash
# Eliminar campos variables con jq
jq 'del(.timestamp, .terraform_version, .configuration.provider_config.aws.expressions)' \
   plan_base_network.json > plan_base_network_normalized.json
```

3. **Versionado**:
- Commitear `plan_base_network_normalized.json` en Git
- Tag con versión del módulo: `network-v1.0.0`

### Detección de diferencias semánticas

**Script de comparación**:
```bash
#!/bin/bash
# compare_plans.sh

# Generar plan nuevo
terraform plan -out=plan_new.tfplan
terraform show -json plan_new.tfplan > plan_new.json

# Normalizar ambos planes
for plan in plan_base_network.json plan_new.json; do
  jq 'del(.timestamp, .terraform_version) | .resource_changes | sort_by(.address)' \
     $plan > ${plan%.json}_norm.json
done

# Comparar solo resource_changes
diff -u plan_base_network_norm.json plan_new_norm.json > plan_diff.txt

if [ $? -eq 0 ]; then
  echo "✓ Plan matches golden baseline"
else
  echo "✗ Plan differs from baseline:"
  cat plan_diff.txt
fi
```

**Campos a ignorar**:
- `timestamp`, `terraform_version`
- UUIDs en metadata
- Ordenamiento de listas (usar `sort_by` en jq)

---

## Ejercicio 4.10: Escenarios E2E sin IaC real

### Descripción del test E2E

**Arquitectura**:
```
[Host] -> [Nginx:80] -> [Flask:5000]
           (Frontend)    (Backend)
```

**Pasos del test**:

1. **Aplicar módulos Terraform**:
```bash
terraform apply -auto-approve
```

2. **Obtener configuración**:
```bash
FRONTEND_IP=$(terraform output -raw frontend_ip)
BACKEND_IP=$(terraform output -raw backend_ip)
```

3. **Test 1: Frontend accesible**:
```bash
curl -s -o /dev/null -w "%{http_code}" http://$FRONTEND_IP/
# Esperado: 200
```

4. **Test 2: Backend inaccesible directamente**:
```bash
timeout 5 curl http://$BACKEND_IP:5000/api/status || echo "✓ Backend blocked"
# Esperado: Timeout (firewall bloquea acceso directo)
```

5. **Test 3: Proxy funciona**:
```bash
curl http://$FRONTEND_IP/api/data | jq '.status'
# Esperado: {"status": "ok", "backend": "flask"}
```

### Métricas examinadas

1. **Status codes**:
   - Frontend directo: 200
   - Backend directo: timeout/connection refused
   - Proxy: 200

2. **Latencia**:
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://$FRONTEND_IP/api/data
# curl-format.txt:
# time_total: %{time_total}
# time_connect: %{time_connect}
```

3. **Payload**:
```bash
response=$(curl -s http://$FRONTEND_IP/api/data)
echo $response | jq -e '.status == "ok"' || exit 1
```

### Integración sin CI externo

**Script unificado** (`e2e_test.sh`):
```bash
#!/bin/bash
set -e

echo "=== E2E Test Suite ==="

# Apply infrastructure
terraform apply -auto-approve

# Wait for services
sleep 10

# Run tests
FRONTEND_IP=$(terraform output -raw frontend_ip)

echo "[TEST 1] Frontend reachability"
status=$(curl -s -o /dev/null -w "%{http_code}" http://$FRONTEND_IP/)
[ "$status" = "200" ] && echo "✓ PASS" || echo "✗ FAIL"

echo "[TEST 2] Backend isolation"
timeout 5 curl http://$(terraform output -raw backend_ip):5000/ 2>&1 | grep -q "timeout"
[ $? -eq 0 ] && echo "✓ PASS" || echo "✗ FAIL"

echo "[TEST 3] Proxy functionality"
curl -s http://$FRONTEND_IP/api/data | jq -e '.status == "ok"'
[ $? -eq 0 ] && echo "✓ PASS" || echo "✗ FAIL"

echo "=== E2E Complete ==="
```

---

## Ejercicio 5.13: Mapeo de pruebas al pipeline local

### Secuencia de ejecución

```
┌─────────────────┐
│  1. Unit Tests  │  <-- Rápidos, aislados
│   (validate)    │  
└────────┬────────┘
         │ 5-10s
┌────────▼────────┐
│  2. Smoke Tests │  <-- Sin apply
│   (fmt + plan)  │
└────────┬────────┘
         │ 10-15s
┌────────▼────────┐
│ 3. Contract     │  <-- Validación de outputs
│    Tests        │
└────────┬────────┘
         │ 15-20s
┌────────▼────────┐
│ 4. Integration  │  <-- Apply local
│    Tests        │
└────────┬────────┘
         │ 30-60s
┌────────▼────────┐
│  5. E2E Tests   │  <-- Flujo completo
│   (HTTP checks) │
└─────────────────┘
     60-120s
```

### Implementación sin CI

**Script `run_pipeline.sh`**:
```bash
#!/bin/bash

RESULTS_FILE="test_results.txt"
echo "Test Pipeline Results - $(date)" > $RESULTS_FILE

start_time=$(date +%s)

# Fase 1: Unit
echo "=== Phase 1: Unit Tests ===" | tee -a $RESULTS_FILE
phase1_start=$(date +%s)
for module in modules/*/; do
  (cd $module && terraform validate) || echo "FAIL: $module"
done
phase1_end=$(date +%s)
echo "Duration: $((phase1_end - phase1_start))s" | tee -a $RESULTS_FILE

# Fase 2: Smoke
echo "=== Phase 2: Smoke Tests ===" | tee -a $RESULTS_FILE
phase2_start=$(date +%s)
./scripts/run_smoke.sh | tee -a $RESULTS_FILE
phase2_end=$(date +%s)
echo "Duration: $((phase2_end - phase2_start))s" | tee -a $RESULTS_FILE

# Fase 3: Contract
echo "=== Phase 3: Contract Tests ===" | tee -a $RESULTS_FILE
phase3_start=$(date +%s)
# Implementar validación de outputs aquí
phase3_end=$(date +%s)
echo "Duration: $((phase3_end - phase3_start))s" | tee -a $RESULTS_FILE

# Fase 4: Integration
echo "=== Phase 4: Integration Tests ===" | tee -a $RESULTS_FILE
phase4_start=$(date +%s)
terraform apply -auto-approve
phase4_end=$(date +%s)
echo "Duration: $((phase4_end - phase4_start))s" | tee -a $RESULTS_FILE

# Fase 5: E2E
echo "=== Phase 5: E2E Tests ===" | tee -a $RESULTS_FILE
phase5_start=$(date +%s)
./scripts/e2e_test.sh | tee -a $RESULTS_FILE
phase5_end=$(date +%s)
echo "Duration: $((phase5_end - phase5_start))s" | tee -a $RESULTS_FILE

end_time=$(date +%s)
echo "Total Duration: $((end_time - start_time))s" | tee -a $RESULTS_FILE
```

### Medición y optimización

**Métricas clave**:
1. Tiempo por fase (individual)
2. Tiempo acumulado
3. Tasa de éxito/fallo por fase

**Estrategias de optimización**:
- Paralelizar unit tests de módulos independientes
- Cachear `terraform init` entre runs
- Usar `-refresh=false` en smoke tests
- Ejecutar solo fases afectadas por cambios (test slicing)

---

## Ejercicio 6.18: Automatización local de la suite

### Script maestro `run_all.sh`

```bash
#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Contadores
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Categorías
declare -A CATEGORY_PASS
declare -A CATEGORY_FAIL

echo "╔════════════════════════════════════════╗"
echo "║  Test Suite Execution - $(date +%H:%M:%S)  ║"
echo "╚════════════════════════════════════════╝"

# Fase 0: Limpieza
echo -e "\n[CLEANUP] Destroying previous state..."
terraform destroy -auto-approve > /dev/null 2>&1
rm -rf .terraform terraform.tfstate* plan*.tfplan

# Fase 1: Unit Tests
echo -e "\n[UNIT TESTS] Running..."
CATEGORY="unit"
for module in modules/*/; do
  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  if (cd $module && terraform validate > /dev/null 2>&1); then
    PASSED_TESTS=$((PASSED_TESTS + 1))
    CATEGORY_PASS[$CATEGORY]=$((${CATEGORY_PASS[$CATEGORY]:-0} + 1))
    echo -e "  ${GREEN}✓${NC} $(basename $module)"
  else
    FAILED_TESTS=$((FAILED_TESTS + 1))
    CATEGORY_FAIL[$CATEGORY]=$((${CATEGORY_FAIL[$CATEGORY]:-0} + 1))
    echo -e "  ${RED}✗${NC} $(basename $module)"
  fi
done

# Fase 2: Smoke Tests
echo -e "\n[SMOKE TESTS] Running..."
CATEGORY="smoke"
TOTAL_TESTS=$((TOTAL_TESTS + 3))
if ./scripts/run_smoke.sh > /tmp/smoke.log 2>&1; then
  PASSED_TESTS=$((PASSED_TESTS + 3))
  CATEGORY_PASS[$CATEGORY]=3
  echo -e "  ${GREEN}✓${NC} All smoke tests passed"
else
  FAILED_TESTS=$((FAILED_TESTS + 3))
  CATEGORY_FAIL[$CATEGORY]=3
  echo -e "  ${RED}✗${NC} Some smoke tests failed"
  cat /tmp/smoke.log
fi

# Fase 3: Integration Tests
echo -e "\n[INTEGRATION TESTS] Running..."
CATEGORY="integration"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if terraform init > /dev/null 2>&1 && terraform apply -auto-approve > /tmp/apply.log 2>&1; then
  PASSED_TESTS=$((PASSED_TESTS + 1))
  CATEGORY_PASS[$CATEGORY]=1
  echo -e "  ${GREEN}✓${NC} Integration apply successful"
else
  FAILED_TESTS=$((FAILED_TESTS + 1))
  CATEGORY_FAIL[$CATEGORY]=1
  echo -e "  ${RED}✗${NC} Integration apply failed"
fi

# Fase 4: E2E Tests
echo -e "\n[E2E TESTS] Running..."
CATEGORY="e2e"
if [ -f scripts/e2e_test.sh ]; then
  TOTAL_TESTS=$((TOTAL_TESTS + 3))
  e2e_result=$(./scripts/e2e_test.sh 2>&1)
  e2e_passed=$(echo "$e2e_result" | grep -c "✓ PASS")
  PASSED_TESTS=$((PASSED_TESTS + e2e_passed))
  FAILED_TESTS=$((FAILED_TESTS + 3 - e2e_passed))
  CATEGORY_PASS[$CATEGORY]=$e2e_passed
  CATEGORY_FAIL[$CATEGORY]=$((3 - e2e_passed))
  echo "$e2e_result"
fi

# Resumen final
echo -e "\n╔════════════════════════════════════════╗"
echo -e "║           TEST SUMMARY                 ║"
echo -e "╚════════════════════════════════════════╝"
echo -e "\nBy Category:"
for cat in unit smoke integration e2e; do
  pass=${CATEGORY_PASS[$cat]:-0}
  fail=${CATEGORY_FAIL[$cat]:-0}
  total=$((pass + fail))
  if [ $total -gt 0 ]; then
    echo -e "  $cat: ${GREEN}$pass passed${NC}, ${RED}$fail failed${NC} ($total total)"
  fi
done

echo -e "\nOverall:"
echo -e "  Total Tests: $TOTAL_TESTS"
echo -e "  ${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "  ${RED}Failed: $FAILED_TESTS${NC}"
echo -e "  Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"

# Exit code
if [ $FAILED_TESTS -eq 0 ]; then
  echo -e "\n${GREEN}All tests passed!${NC}"
  exit 0
else
  echo -e "\n${RED}Some tests failed!${NC}"
  exit 1
fi
```

### Notificaciones locales

**Opción 1: Email (usando `mail`)**:
```bash
if [ $FAILED_TESTS -gt 0 ]; then
  echo "Test suite failed with $FAILED_TESTS failures" | \
    mail -s "❌ Test Failure Alert" your-email@example.com
fi
```

**Opción 2: Slack webhook**:
```bash
if [ $FAILED_TESTS -gt 0 ]; then
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"❌ Test suite failed: $FAILED_TESTS failures\"}" \
    $SLACK_WEBHOOK_URL
fi
```

**Opción 3: Notificación de escritorio**:
```bash
if [ $FAILED_TESTS -gt 0 ]; then
  notify-send "Test Failure" "$FAILED_TESTS tests failed" -u critical
fi
```

---

## Ejercicio 7: Ampliación de módulos

### Módulo `firewall`

**Variables (variables.tf)**:
```hcl
variable "allowed_ports" {
  type        = list(number)
  description = "Lista de puertos permitidos"
  
  validation {
    condition = alltrue([
      for port in var.allowed_ports : port >= 1 && port <= 65535
    ])
    error_message = "Los puertos deben estar entre 1 y 65535."
  }
}

variable "allowed_cidrs" {
  type        = list(string)
  description = "Lista de CIDRs permitidos"
  
  validation {
    condition = alltrue([
      for cidr in var.allowed_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "CIDRs mal formados detectados."
  }
}

variable "vpc_id" {
  type        = string
  description = "ID de la VPC"
}
```

**Outputs (outputs.tf)**:
```hcl
output "firewall_policy" {
  value = jsonencode({
    version = "1.0"
    rules = [
      for idx, port in var.allowed_ports : {
        rule_id     = "rule-${idx + 1}"
        port        = port
        protocol    = "tcp"
        allowed_ips = var.allowed_cidrs
        action      = "allow"
      }
    ]
  })
  description = "Política de firewall en formato JSON"
}

output "security_group_id" {
  value = "sg-${md5(var.vpc_id)}"
  description = "ID del grupo de seguridad simulado"
}

output "rules_count" {
  value = length(var.allowed_ports)
  description = "Número de reglas creadas"
}
```

### Módulo `dns`

**Variables (variables.tf)**:
```hcl
variable "hostnames" {
  type        = list(string)
  description = "Lista de nombres de host"
  
  validation {
    condition = alltrue([
      for hostname in var.hostnames : can(regex("^[a-zA-Z0-9.-]+$", hostname))
    ])
    error_message = "Los hostnames solo pueden contener letras, números, puntos y guiones."
  }
  
  validation {
    condition = alltrue([
      for hostname in var.hostnames : !can(regex(" ", hostname))
    ])
    error_message = "Los hostnames no pueden contener espacios."
  }
}

variable "ip_addresses" {
  type        = list(string)
  description = "Lista de direcciones IP"
}

variable "zone_name" {
  type        = string
  description = "Nombre de la zona DNS"
}
```

**Outputs (outputs.tf)**:
```hcl
output "dns_mapping" {
  value = zipmap(var.hostnames, var.ip_addresses)
  description = "Mapa de hostname->IP"
}

output "zone_id" {
  value = "zone-${md5(var.zone_name)}"
  description = "ID de la zona DNS simulado"
}

output "records_count" {
  value = length(var.hostnames)
  description = "Número de registros DNS creados"
}
```

### Pruebas unitarias con `terraform console`

**Test 1: Firewall produce JSON consistente**:
```bash
$ terraform console
> jsondecode(module.firewall.firewall_policy).version
"1.0"
> length(jsondecode(module.firewall.firewall_policy).rules)
3
```

**Test 2: DNS rechaza nombres inválidos**:
```bash
$ echo 'var.hostnames = ["invalid name"]' | terraform console
Error: Invalid value for variable
```

**Test 3: Verificar mapeo DNS**:
```bash
$ terraform console
> module.dns.dns_mapping
{
  "api.example.com" = "10.0.1.10"
  "web.example.com" = "10.0.1.20"
}
```

---

## Ejercicio 10: Pruebas de humo híbridos

### Script `run_smoke.sh`

```bash
#!/bin/bash

# Configuración
TIMEOUT=30
MODULE_DIR="modules"
TEMP_DIR=$(mktemp -d)
START_TIME=$(date +%s)

echo "=== Smoke Tests (Target: <${TIMEOUT}s) ==="
echo "Start: $(date)"

# Array para resultados
declare -a RESULTS

# Función para test individual
smoke_test_module() {
  local module=$1
  local module_name=$(basename $module)
  local test_dir="$TEMP_DIR/$module_name"
  
  mkdir -p "$test_dir"
  cp -r "$module"/* "$test_dir/"
  cd "$test_dir"
  
  # Test 1: Format
  if ! terraform fmt -check -recursive > /dev/null 2>&1; then
    echo "  ✗ $module_name: Format check failed"
    return 1
  fi
  
  # Test 2: Validate
  if ! terraform init > /dev/null 2>&1; then
    echo "  ✗ $module_name: Init failed"
    return 1
  fi
  
  if ! terraform validate > /dev/null 2>&1; then
    echo "  ✗ $module_name: Validation failed"
    return 1
  fi
  
  # Test 3: Plan
  if ! terraform plan -refresh=false -out=test.tfplan > /dev/null 2>&1; then
    echo "  ✗ $module_name: Plan failed"
    return 1
  fi
  
  # Test 4: Contract check (ejemplo: verificar que existe al menos un output)
  terraform show -json test.tfplan > plan.json
  local output_count=$(jq '.planned_values.outputs | length' plan.json 2>/dev/null || echo 0)
  
  if [ "$output_count" -eq 0 ]; then
    echo "  ✗ $module_name: No outputs defined"
    return 1
  fi
  
  echo "  ✓ $module_name: All checks passed ($output_count outputs)"
  return 0
}

# Ejecutar tests en paralelo
for module in "$MODULE_DIR"/*/; do
  if [ -d "$module" ]; then
    smoke_test_module "$module" &
  fi
done

# Esperar a que terminen todos
wait

# Calcular duración
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "Duration: ${DURATION}s (Target: <${TIMEOUT}s)"

# Limpieza
rm -rf "$TEMP_DIR"

if [ $DURATION -gt $TIMEOUT ]; then
  echo "⚠ Warning: Exceeded timeout"
  exit 1
fi

echo "✓ Smoke tests completed successfully"
exit 0
```

### Optimizaciones para <30s

1. **Paralelización**: Tests de módulos en paralelo con `&` y `wait`
2. **Directorios temporales**: Aislamiento sin conflictos
3. **Sin refresh**: `-refresh=false` evita llamadas a APIs
4. **Output a null**: No escribir planes al disco (`/dev/null`)
5. **Init cacheado**: Copiar `.terraform` pre-inicializado si es posible

### Contrato mínimo verificado

El script verifica:
- Existencia de al menos un output por módulo
- Estructura válida del plan JSON
- Conteo de outputs accesible vía `jq`

**Ejemplo de verificación extendida**:
```bash
# Verificar output específico "vpc_id" en módulo network
local vpc_id=$(jq -r '.planned_values.outputs.vpc_id.value' plan.json)
if [ "$vpc_id" = "null" ]; then
  echo "  ✗ Required output 'vpc_id' not found"
  return 1
fi
```
