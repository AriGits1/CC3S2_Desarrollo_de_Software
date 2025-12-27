# Respuestas Examen Sustitutorio

## Pregunta 1 (1pt): IaC + Supply Chain Security

### Justificación de la lectura 15

En sistema clínico, IaC + supply chain es indispensable para este proyecto porque:

**Reproducibilidad**: Cada deployment debe ser idéntico al aprobado
**SBOM**: Registra dependencias exactas (Flask, requests)
**Firmas**: Hash de imagen en SBOM garantiza integridad
**Provenance**: deployment-log.txt registra quién fue el que lo aprobó

### Ejemplo Disputa Técnica

Paciente diagnosticado con "arritmia" resulta falso positivo.

**Sin supply chain**:
- No hay registro de qué versión diagnostico, no se puede reproducir seria un caso perdido por falta de evidencia.

**Con supply chain enseñado en la lectura 19** implementado en nuestro proyecto:
1. `audit` service tiene evento firmado (hash SHA256)
2. SBOM muestra modelo v2.3.1 con dependencias exactas
3. deployment-log.txt prueba aprobación del comité
4. Se reproduce el diagnóstico
5. Defensa tiene evidencia técnica sólida

**Resolucion tambien en el Código**: En `scripts/build.sh` (genera SBOM), `services/audit/app.py` (firma eventos)

---

## Pregunta 2 (2pts): Cadena de Evidencia Técnica

### Problema
- Imagen reconstruida sin tag
- Cluster no puede probar versión
- Manifests no versionados

### Solución Implementada

**1. Qué se desplegó**
```bash
# SBOM contiene hash de imagen
"image_hash": "sha256:abc123..."
```

**2. Cuándo**
```yaml
# k8s/all.yaml
annotations:
  deployment.approved-by: "comite-clinico"
  # + timestamp en deployment-log.txt
```

**3. Quién**
```bash
# scripts/deploy.sh genera:
Approved by: usuario@hostname
Date: 2024-12-27T10:00:00Z
```

**4. Con qué dependencias**
```json
# sbom-inference.json
"dependencies": ["Flask==3.0.0", "requests==2.31.0"]
```


**En el Código**: Ver `scripts/build.sh` en líneas 20-28

---

## Pregunta 3 (1pt): Estándar Extremo IaC Limpia

**1. Commits firmados**
```bash
git config commit.gpgsign true
```

**2. PRs con doble aprobación**
- Comité clínico + seguridad

**3. Gates de seguridad**
- `scripts/test.sh` valida todo pre-deploy

**4. Secretos rotables**
```yaml
# Usar Kubernetes Secrets
# Rotar cada 90 días
```

**5. Variables con validación**
```python
# Validar al inicio
assert MODEL_VERSION is not None
```

### Anti-patrones Silenciosos

**1. Tag flotante**
```yaml
# MALO
image: inference:latest  # Puede cambiar sin aviso, problema critico abordado tambien en la pc5

# CORRECTO (implementado)
image: inference:v1  # + hash en SBOM
```

**Impacto clínico**: Diagnóstico usa modelo no aprobado

**2. Secretos en ConfigMap**
```yaml
# MALO, analisis de seguridad abordado en los proyectos de la pc4
ConfigMap:
  password: "secreto"

# CORRECTO
Secret:
  stringData: ...
```

**Impacto clínico**: Datos médicos expuestos, violación HIPAA

**Código**: Ver `scripts/test.sh` línea 15-35

---

## Pregunta 4 (1pt): 
## Lo vimos en Patrones de Diseño de la lectura 16

### Builder (Dockerfile)

```dockerfile
FROM python:3.11-slim AS builder
# Compilar dependencias
RUN pip wheel ...

FROM python:3.11-slim
# Runtime mínimo
COPY --from=builder /wheels /wheels
```

**Beneficios**:
- Imagen final pequeña
- Menos auditoría
- Recuperación rápida

### Prototype (Manifests)

Reutilizacion de la base de deployment para staging:
```yaml
# Base production
# Clona y modifica replicas/recursos
```

### Composite (Sistema)

Servicios independientes componen sistema completo:
```
Acquisition + Inference + Audit = Sistema Diagnóstico
```

**En el Código**: Se puede ver en `services/Dockerfile`, `k8s/all.yaml`

---

## Pregunta 5 (2pts): DIP/Mediator 

### Implementación de la lectura 17, patrones de dependencias IaC

**DIP**: Servicios no se conocen entre sí
```python
# inference no importa audit directamente
# Comunicación vía HTTP/NetworkPolicy
```

**Mediator**: Kubernetes Service
```yaml
Service: audit  # Mediator
  selector: app=audit
```

### Contratos Versionados
```python
@app.route('/v1/infer')  # Version en path
```

### Invariantes
```python
# services/audit/app.py
# Evento siempre tiene firma
event['signature'] = hashlib.sha256(...).hexdigest()
```

### Degradación Parcial

Si `audit` cae:
```python
try:
    # registrar en audit
except:
    # guardar local, continuar
    print("Event logged locally")
```

**En el Código se puede notar en**: `services/*/app.py`

---

## Pregunta 6 (1pt): Plan de Pruebas

Ver `scripts/test.sh` completo.

### 5 Defectos Detectables

1. **Imagen sin hash**: Verificar SBOM existe
2. **runAsNonRoot faltante**: grep en manifests
3. **Capabilities no dropped**: grep en manifests
4. **NetworkPolicy faltante**: grep por servicio
5. **Health checks missing**: grep livenessProbe

### 2 NO Detectables

**1. Modelo sin validación clínica**
- Detección: Revisión manual del comité
- Impacto: Diagnósticos incorrectos

**2. Aprobación manual no seguida**
- Detección: Auditoría de deployment-log.txt
- Impacto: Violación compliance

---

## Pregunta 7 (1pt): Despliegue Final

### Docker (Aislamiento) de la lectura 21

```dockerfile
# Usuario no privilegiado
RUN useradd -m -u 1001 app
USER app

# Builder pattern
FROM python:3.11-slim AS builder
...
```

### Kubernetes (Zero Trust) de la lectura22

```yaml
# NetworkPolicy default deny
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]

# Política específica por servicio
spec:
  podSelector:
    matchLabels:
      app: inference
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: audit
```

### Estrategia Conservadora

```bash
# scripts/deploy.sh
read -p "Escribir 'APROBAR': " approval
if [ "$approval" != "APROBAR" ]; then
    exit 1
fi

# Registro
cat >> deployment-log.txt <<EOF
Approved by: $(whoami)@$(hostname)
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF
```

### Evidencia No-Repudio

1. Hash de imagen en SBOM
2. Firma SHA256 en audit events
3. deployment-log.txt con timestamp
4. Annotations en manifests

**Código**: Ver `k8s/all.yaml`, `scripts/deploy.sh`

---
