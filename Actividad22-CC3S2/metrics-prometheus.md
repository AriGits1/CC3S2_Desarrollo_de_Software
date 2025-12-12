# Parte B - Métricas con Prometheus

## Verificar que el target está UP

1. Abrir http://localhost:9090
2. Ir a **Status → Target health**
3. Debería aparecer `otel-collector` con estado **UP**

Los labels que aparecen:
- `job="otel-collector"` → Es el nombre del grupo de targets
- `instance="otel-collector:8889"` → Es la dirección específica de este target

## Queries básicas

### Ver estado de targets
```promql
up
```
Devuelve 1 si está arriba, 0 si está caído.

### Filtrar por job específico
```promql
up{job="otel-collector"}
```

### Buscar métricas HTTP
Escribir `http` en el campo de query y ver qué aparece en el autocompletado. En este stack pueden aparecer cosas como:
- `http_server_duration_seconds_count`
- `http_server_duration_seconds_bucket`

## El problema del error rate

La actividad pide hacer una query de error rate 5xx, algo así:

```promql
sum(rate(http_server_requests_total{http_status_code=~"5.."}[5m]))
```

Pero en este stack **las métricas HTTP no aparecen** porque la app solo configura el exporter de trazas, no de métricas. Por eso el MCP Server muestra `requests_per_second: 0.0`.

### Qué sí funciona

Ver las métricas internas del Collector:
```promql
otelcol_receiver_accepted_spans
otelcol_exporter_sent_spans
```

## Mejores prácticas para métricas

1. **Usar counters para errores** - porque solo suben y permiten calcular tasas con `rate()`

2. **Nombres claros** - seguir el formato `nombre_unidad` como `http_request_duration_seconds`

3. **Cuidado con los labels** - no poner cosas como `user_id` porque explota la cantidad de series temporales
