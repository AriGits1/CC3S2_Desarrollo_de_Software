# Parte F - DevSecOps y Observabilidad

## Cómo encaja la observabilidad en cada fase

### 1. Planificación / Diseño
Antes de codear, hay que pensar:
- ¿Qué métricas vamos a necesitar?
- ¿Qué logs son importantes?
- ¿Cuáles son los SLOs? (ej: 99.9% disponibilidad)

### 2. Construcción y CI
Durante el desarrollo:
- Tests que verifican que la instrumentación funciona
- Escaneo de seguridad del código (como `bandit` en este proyecto)
- Verificar que no se logueen datos sensibles

### 3. Despliegue (CD)
Al hacer deploy:
- Verificar que los servicios arranquen bien
- Comparar métricas antes/después del deploy
- Si algo sale mal, rollback automático

### 4. Operación
En producción:
- Dashboards para ver el estado actual
- Alertas cuando algo se sale de lo normal
- On-call que responde a incidentes

### 5. Mejora continua
Después de incidentes:
- Post-mortems basados en datos reales
- Identificar qué métricas faltaban
- Mejorar alertas y runbooks

## Gates DevSecOps

Un "gate" es un checkpoint que debe pasar antes de continuar.

### Gate 1: Pre-deploy
Antes de pasar a producción, verificar:
```bash
# El collector está UP
up{job="otel-collector"} == 1

# No hay muchos errores en staging
count_over_time({job="demo-app"} |= "ERROR" [5m]) < 5
```

### Gate 2: Post-deploy
Después del deploy, durante los primeros minutos:
- Monitorear que el error rate no suba
- Verificar que hay trazas fluyendo
- Si algo falla → rollback

### Gate 3: Seguridad
Alertas para detectar cosas raras:
```logql
# Posible SQL injection
{job="demo-app"} |~ "(?i)select.*from|union.*select"

# Muchos 404 (alguien escaneando)
count_over_time({job="demo-app"} |= "404" [5m]) > 100
```

## El servidor MCP

El MCP Server es un agregador que junta info de Prometheus, Loki y Tempo en un solo JSON.

```bash
curl http://localhost:8080/api/summary
```

Devuelve algo así:
```json
{
  "service": "demo-app",
  "metrics": { "requests_per_second": 0.0 },
  "logs": { "error_count_5m": 4, "sample_errors": [...] },
  "traces": { "recent_traces": 48 }
}
```

### ¿Para qué sirve?

1. **Para LLMs/AI**: Un agente puede leer este JSON y ayudar a diagnosticar problemas
2. **Simplifica consultas**: No necesitas saber PromQL, LogQL y TraceQL
3. **Automatización**: Scripts pueden consumir este endpoint para tomar decisiones

### Ejemplo de uso con IA

Imagina un chatbot que cuando hay una alerta:
1. Lee `/api/summary`
2. Analiza los errores
3. Sugiere qué revisar o ejecuta un runbook

Esto es lo que llaman "AIOps" - usar IA para operaciones.

## Conclusión

La observabilidad no es algo que agregas al final, es parte del diseño desde el principio. Este stack de Prometheus + Loki + Tempo + Grafana es bastante estándar en la industria y sirve como base para implementar buenas prácticas de DevSecOps.
