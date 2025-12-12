# Parte E - Dashboard y Alertas en Grafana

## Crear el dashboard

1. En Grafana, ir a **Dashboards → New → New Dashboard**
2. Click en **Add visualization**
3. Guardar como "Dashboard Actividad 22 - demo-app"

## Paneles que agregué

### Panel 1: Error Count (Loki)
- **Datasource**: Loki
- **Query**: `count_over_time({job="demo-app"} |= "ERROR" [1m])`
- **Tipo**: Time series

Muestra cuántos errores hay por minuto.

### Panel 2: OTEL Collector Status (Prometheus)
- **Datasource**: Prometheus
- **Query**: `up{job="otel-collector"}`
- **Tipo**: Stat

Muestra si el collector está UP (1) o DOWN (0).

### Panel 3: Application Logs (Loki)
- **Datasource**: Loki
- **Query**: `{job="demo-app"}`
- **Tipo**: Logs

Muestra los logs en tiempo real.

## Crear una alerta

### Pasos
1. En un panel, click en **Alert → Create alert rule**
2. Configurar la condición
3. Definir cuándo disparar

### Mi configuración de alerta

- **Query**: `count_over_time({job="demo-app"} |= "ERROR" [5m])`
- **Condición**: `IS ABOVE 5`
- **Evaluar cada**: 1 minuto
- **Durante**: 5 minutos (para evitar falsas alarmas)
- **Labels**: `severity=warning`, `service=demo-app`

### ¿Por qué estos valores?

- **Umbral de 5**: Es razonable para un demo. En producción sería un porcentaje.
- **5 minutos de duración**: Para no alertar por un pico momentáneo.
- **Warning y no critical**: Porque son errores simulados del demo.

## Contact points (no configurado)

En un entorno real, las alertas irían a:
- Slack: `#alerts-platform`
- Email: `equipo@empresa.com`
- PagerDuty: para cosas críticas

## Cómo esto ayuda a DevOps/SRE

1. **Detección rápida**: Te enteras antes que los usuarios
2. **Contexto inmediato**: El dashboard muestra qué está pasando
3. **Automatización**: Puedes hacer que se ejecuten runbooks automáticamente
