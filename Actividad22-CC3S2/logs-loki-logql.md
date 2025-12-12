# Parte C - Logs con Loki

## Cómo ver los logs

1. Ir a Grafana http://localhost:3000 (admin/devsecops)
2. Click en **Explore** (el ícono de brújula)
3. Arriba seleccionar **Loki** como datasource
4. En el campo de query escribir:

```logql
{job="demo-app"}
```

5. Click en **Run query**

Si no aparece nada, hay que generar tráfico primero y verificar que Promtail esté funcionando.

## Filtrar por contenido

### Solo errores
```logql
{job="demo-app"} |= "ERROR"
```

### Solo warnings
```logql
{job="demo-app"} |= "WARNING"
```

### Errores pero sin health checks
```logql
{job="demo-app"} |= "ERROR" != "healthz"
```

### Buscar con regex
```logql
{job="demo-app"} |~ "error|fail|exception"
```

## Ejemplos de logs que genera la app

```
2025-12-11 04:25:18,100 INFO Health check OK
2025-12-11 04:25:19,200 INFO Listing items
2025-12-11 04:25:31,107 ERROR Simulated error endpoint called
2025-12-11 04:25:45,300 WARNING Slow request simulated
```

## Contar logs

### Errores en los últimos 5 minutos
```logql
count_over_time({job="demo-app"} |= "ERROR" [5m])
```

### Tasa de errores por segundo
```logql
rate({job="demo-app"} |= "ERROR" [1m])
```

## Uso en DevSecOps

Los logs sirven para:
- **Detectar ataques**: buscar patrones sospechosos como SQL injection
- **Debugging**: ver qué pasó antes de un error
- **Auditoría**: registrar quién hizo qué
- **Alertas**: crear alertas cuando hay muchos errores seguidos

## Nota: Si Loki no muestra datos

Verificar que Promtail está corriendo y enviando:
```bash
docker logs promtail --tail 20
```

Si hay errores 500, reiniciar Loki y luego Promtail:
```bash
docker restart loki
docker restart promtail
```
