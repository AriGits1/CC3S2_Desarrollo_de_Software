# Actividad 22 - Observabilidad con Prometheus, Loki, Tempo y MCP

## ¿De qué trata?

Esta actividad es sobre observabilidad - básicamente aprender a monitorear aplicaciones usando herramientas modernas. El stack incluye:

- **FastAPI**: La app que vamos a monitorear
- **Prometheus**: Para métricas
- **Loki**: Para logs
- **Tempo**: Para trazas distribuidas
- **Grafana**: Para visualizar todo
- **MCP Server**: Un servidor que resume todo para LLMs

## Cómo levantar el proyecto

```bash
cd Observabilidad-mcp

# Crear entorno virtual
python -m venv bdd
source bdd/bin/activate  # Linux/Mac
# .\bdd\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependencias
make deps

# Levantar todo
make up

# Ver que esté corriendo
docker ps
```

## Generar tráfico

Si `make demo-traffic` no funciona (por espacios en la ruta), usar:

```bash
for i in {1..20}; do
  curl -s http://localhost:8000/healthz > /dev/null
  curl -s http://localhost:8000/api/v1/items > /dev/null
  curl -s http://localhost:8000/api/v1/error > /dev/null
  sleep 0.3
done
```

## URLs importantes

| Servicio | URL | Login |
|----------|-----|-------|
| App | http://localhost:8000/docs | - |
| Grafana | http://localhost:3000 | admin / devsecops |
| Prometheus | http://localhost:9090 | - |
| MCP | http://localhost:8080/api/summary | - |

## Para apagar

```bash
make down
```

## Archivos de la actividad

- `observabilidad-telemetria.md` - Conceptos básicos
- `metrics-prometheus.md` - Queries de Prometheus
- `logs-loki-logql.md` - Queries de Loki
- `traces-tempo-traceql.md` - Queries de Tempo
- `grafana-alerting.md` - Dashboard y alertas
- `devsecops-observabilidad.md` - Relación con DevSecOps
