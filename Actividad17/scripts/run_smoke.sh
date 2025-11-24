#!/bin/bash

# Configuración
TIMEOUT=30
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MODULE_DIR="$PROJECT_ROOT/modules"
TEMP_DIR=$(mktemp -d)
START_TIME=$(date +%s)

echo "========================================="
echo "  SMOKE TESTS (Target: <${TIMEOUT}s)"
echo "========================================="
echo "Start: $(date)"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Contadores
TOTAL=0
PASSED=0
FAILED=0

# Función para test individual
smoke_test_module() {
  local module=$1
  local module_name=$(basename $module)
  local test_dir="$TEMP_DIR/$module_name"
  
  echo "[Testing $module_name]"
  
  mkdir -p "$test_dir"
  cp -r "$module"/* "$test_dir/" 2>/dev/null
  cd "$test_dir"
  
  # Test 1: Format check
  if ! terraform fmt -check -recursive > /dev/null 2>&1; then
    echo -e "  ${RED}✗${NC} Format check failed"
    return 1
  fi
  echo "  ✓ Format OK"
  
  # Test 2: Init
  if ! terraform init > /dev/null 2>&1; then
    echo -e "  ${RED}✗${NC} Init failed"
    return 1
  fi
  echo "  ✓ Init OK"
  
  # Test 3: Validate
  if ! terraform validate > /dev/null 2>&1; then
    echo -e "  ${RED}✗${NC} Validation failed"
    return 1
  fi
  echo "  ✓ Validation OK"
  
  # Test 4: Plan (sin refresh)
  if ! terraform plan -refresh=false -out=test.tfplan > /dev/null 2>&1; then
    echo -e "  ${RED}✗${NC} Plan failed"
    return 1
  fi
  echo "  ✓ Plan OK"
  
  # Test 5: Contract check - verificar outputs
  terraform show -json test.tfplan > plan.json 2>/dev/null
  local output_count=$(jq '.planned_values.outputs | length' plan.json 2>/dev/null || echo 0)
  
  if [ "$output_count" -eq 0 ]; then
    echo -e "  ${RED}✗${NC} No outputs defined"
    return 1
  fi
  echo "  ✓ Contract OK ($output_count outputs)"
  
  echo -e "${GREEN}✓ $module_name: All checks passed${NC}"
  echo ""
  return 0
}

# Ejecutar tests para cada módulo
for module in "$MODULE_DIR"/*/; do
  if [ -d "$module" ]; then
    TOTAL=$((TOTAL + 1))
    if smoke_test_module "$module"; then
      PASSED=$((PASSED + 1))
    else
      FAILED=$((FAILED + 1))
    fi
  fi
done

# Calcular duración
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "========================================="
echo "  SMOKE TESTS SUMMARY"
echo "========================================="
echo "Modules tested: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
  echo -e "${RED}Failed: $FAILED${NC}"
else
  echo "Failed: 0"
fi
echo "Duration: ${DURATION}s (Target: <${TIMEOUT}s)"

# Limpieza
rm -rf "$TEMP_DIR"

# Resultado
if [ $DURATION -gt $TIMEOUT ]; then
  echo -e "\n${RED}⚠ Warning: Exceeded timeout${NC}"
fi

if [ $FAILED -eq 0 ]; then
  echo -e "\n${GREEN}✓ All smoke tests passed successfully${NC}"
  exit 0
else
  echo -e "\n${RED}✗ Some smoke tests failed${NC}"
  exit 1
fi
