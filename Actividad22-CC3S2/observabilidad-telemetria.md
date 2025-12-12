# Parte A - Observabilidad y Telemetría

## Monitoreo vs Observabilidad

**Monitoreo** es más reactivo - defines qué métricas ver y te avisa cuando algo se sale del rango. Es como tener una alarma de humo: sabes que hay fuego pero no dónde exactamente.

**Observabilidad** es poder entender qué está pasando dentro del sistema mirando lo que sale de él. Te permite responder preguntas que no habías pensado antes, como "¿por qué este usuario tuvo un error a las 3pm?".

En resumen: monitoreo te dice QUE algo está mal, observabilidad te ayuda a entender POR QUÉ.

## Tipos de telemetría

### 1. Métricas (Prometheus)
Son números que se van acumulando. Por ejemplo:
- Cuántas requests llegaron (counter)
- Cuánta memoria se está usando (gauge)
- Distribución de tiempos de respuesta (histogram)

### 2. Logs (Loki)
Son los mensajes de texto que la app escribe. Tipo:
```
2025-12-11 10:30:45 ERROR Simulated error endpoint called
2025-12-11 10:30:46 INFO Health check OK
```

### 3. Trazas (Tempo)
Son como el "camino" que sigue una request. Cada paso es un "span". Sirve para ver dónde se tarda más o dónde falla.

### 4. Otros tipos (no implementados acá)
- **Eventos**: Como logs pero con estructura fija
- **Profiling**: Ver qué funciones consumen más CPU/memoria
- **Health checks**: Verificar que el servicio está vivo

## Diagrama del stack

```
App FastAPI ──────► OTEL Collector ──────► Prometheus (métricas)
     │                    │
     │                    └──────────────► Tempo (trazas)
     │
     └──► Logs ──► Promtail ─────────────► Loki (logs)
                                               │
                                               ▼
                                           Grafana ◄─── MCP Server
                                        (visualización)  (resumen para LLMs)
```

Básicamente:
1. La app genera métricas, logs y trazas
2. OTEL Collector recibe métricas y trazas, las manda a Prometheus y Tempo
3. Promtail lee los logs y los manda a Loki
4. Grafana consulta las 3 fuentes para mostrar dashboards
5. MCP Server hace un resumen en JSON de todo
