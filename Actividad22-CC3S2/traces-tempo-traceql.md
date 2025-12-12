# Parte D - Trazas con Tempo

## Qué son las trazas

Una traza es el recorrido completo de una request. Cada "paso" dentro de la traza se llama **span**. Sirve para ver:
- Cuánto tardó cada parte
- Dónde falló algo
- Qué servicios se llamaron

## Cómo buscar trazas

1. Ir a Grafana → **Explore**
2. Seleccionar **Tempo** como datasource
3. Cambiar a **TraceQL**
4. Escribir la query y ejecutar

## Queries básicas

### Todas las trazas del servicio
```traceql
{ service.name = "demo-app" }
```

### Trazas de un endpoint específico
```traceql
{ service.name = "demo-app" && http.target = "/api/v1/error" }
```

### Trazas con errores
```traceql
{ service.name = "demo-app" && status = error }
```

### Trazas lentas (más de 500ms)
```traceql
{ service.name = "demo-app" && duration > 500ms }
```

## Estructura de una traza

Cuando clickeas en una traza, ves algo así:

```
Trace ID: abc123...
├── GET /api/v1/items (120ms) ← span raíz
│   └── list_items (100ms)    ← span hijo
```

Cada span tiene:
- **Trace ID**: identificador de toda la traza
- **Span ID**: identificador de este paso
- **Duration**: cuánto tardó
- **Attributes**: info extra como `http.method`, `http.status_code`

## Los spans que crea esta app

La app tiene estos spans definidos en el código:
- `list_items` - cuando llamas a /api/v1/items
- `cpu_bound_work` - cuando llamas a /api/v1/work
- `error_endpoint` - cuando llamas a /api/v1/error

## Propagación de contexto

Para que las trazas funcionen entre servicios, se pasan headers HTTP especiales:
```
traceparent: 00-{trace_id}-{span_id}-01
```

Así cada servicio sabe a qué traza pertenece la request.

## Verificar con MCP

```bash
curl http://localhost:8080/api/traces-summary
```

Debería mostrar algo como:
```json
{
  "recent_traces": 48,
  "error_traces": 0
}
```
