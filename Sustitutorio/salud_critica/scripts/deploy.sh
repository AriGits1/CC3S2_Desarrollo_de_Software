#!/bin/bash
set -e

echo "=== Deployment con Aprobacion ==="

# Verificar que kubectl funciona
if ! kubectl cluster-info &>/dev/null; then
    echo "Error: kubectl no conectado a cluster"
    exit 1
fi

echo ""
echo "ADVERTENCIA: Despliegue en sistema critico de salud"
echo "Versiones:"
echo "  - acquisition: v1"
echo "  - inference: v1 (modelo v2.3.1)"
echo "  - audit: v1"
echo ""
read -p "Escribir 'APROBAR' para continuar: " approval

if [ "$approval" != "APROBAR" ]; then
    echo "Deployment cancelado"
    exit 1
fi

# Registrar aprobacion
cat >> deployment-log.txt <<EOF
---
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Approved by: $(whoami)@$(hostname)
Services: acquisition, inference, audit
---
EOF

echo ""
echo "Desplegando servicios..."

# Aplicar manifests
kubectl apply -f k8s/all.yaml

echo ""
echo "Esperando que pods esten ready..."
kubectl wait --for=condition=ready pod -l app=acquisition -n salud-critica --timeout=60s
kubectl wait --for=condition=ready pod -l app=inference -n salud-critica --timeout=60s
kubectl wait --for=condition=ready pod -l app=audit -n salud-critica --timeout=60s

echo ""
echo "=== Deployment Exitoso ==="
kubectl get all -n salud-critica

echo ""
echo "=== Health Check ==="
kubectl exec -n salud-critica deployment/acquisition -- curl -s http://localhost:8001/health
kubectl exec -n salud-critica deployment/inference -- curl -s http://localhost:8002/health
kubectl exec -n salud-critica deployment/audit -- curl -s http://localhost:8003/health
