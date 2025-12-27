#!/bin/bash
set -e

echo "=== Building Docker Images ==="

SERVICES="acquisition inference audit"

for svc in $SERVICES; do
    echo "Building $svc..."
    
    # Copiar Dockerfile y requirements compartidos
    cp services/Dockerfile services/$svc/
    cp services/requirements.txt services/$svc/
    
    # Build con metadata
    docker build \
        --tag $svc:v1 \
        --label "service=$svc" \
        --label "version=v1" \
        --label "build-date=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        services/$svc/
    
    # Generar SBOM simple (sin herramientas externas)
    echo "{
  \"service\": \"$svc\",
  \"version\": \"v1\",
  \"image_hash\": \"$(docker images --no-trunc --quiet $svc:v1)\",
  \"build_date\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"dependencies\": [\"Flask==3.0.0\", \"requests==2.31.0\"]
}" > sbom-$svc.json
    
    echo "✓ Built $svc"
done

echo ""
echo "=== Build Summary ==="
docker images | grep -E "(acquisition|inference|audit)"

echo ""
echo "=== SBOMs Generated ==="
ls -lh sbom-*.json
