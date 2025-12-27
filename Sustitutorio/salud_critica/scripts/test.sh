#!/bin/bash
set -e

echo "=== Pruebas de Infraestructura ==="

FAILED=0

# Test 1: Imagenes construidas
echo ""
echo "[Test 1] Verificando imagenes Docker..."
for svc in acquisition inference audit; do
    if docker images | grep -q "$svc.*v1"; then
        echo "✓ Imagen $svc:v1 existe"
    else
        echo "✗ Imagen $svc:v1 NO encontrada"
        FAILED=$((FAILED+1))
    fi
done

# Test 2: SBOMs generados
echo ""
echo "[Test 2] Verificando SBOMs..."
for svc in acquisition inference audit; do
    if [ -f "sbom-$svc.json" ]; then
        echo "✓ SBOM $svc generado"
    else
        echo "✗ SBOM $svc faltante"
        FAILED=$((FAILED+1))
    fi
done

# Test 3: Manifests tienen SecurityContext
echo ""
echo "[Test 3] Validando SecurityContext..."
if grep -q "runAsNonRoot: true" k8s/all.yaml; then
    echo "✓ runAsNonRoot configurado"
else
    echo "✗ runAsNonRoot faltante"
    FAILED=$((FAILED+1))
fi

if grep -q "capabilities:" k8s/all.yaml && grep -q "drop: \[ALL\]" k8s/all.yaml; then
    echo "✓ Capabilities eliminadas"
else
    echo "✗ Capabilities no configuradas"
    FAILED=$((FAILED+1))
fi

# Test 4: NetworkPolicies existen
echo ""
echo "[Test 4] Validando NetworkPolicies..."
for svc in acquisition inference audit; do
    if grep -q "${svc}-policy" k8s/all.yaml; then
        echo "✓ NetworkPolicy $svc existe"
    else
        echo "✗ NetworkPolicy $svc faltante"
        FAILED=$((FAILED+1))
    fi
done

# Test 5: Health checks configurados
echo ""
echo "[Test 5] Validando Health Checks..."
if grep -q "livenessProbe" k8s/all.yaml && grep -q "readinessProbe" k8s/all.yaml; then
    echo "✓ Health checks configurados"
else
    echo "✗ Health checks faltantes"
    FAILED=$((FAILED+1))
fi

# Resumen
echo ""
echo "==================================="
if [ $FAILED -eq 0 ]; then
    echo "✓ Todas las pruebas pasaron"
    exit 0
else
    echo "✗ $FAILED pruebas fallaron"
    exit 1
fi
