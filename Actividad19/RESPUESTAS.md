# Conceptualización de Microservicios - Conclusiones

## 1. Evolución Arquitectónica

**Monolito → SOA → Microservicios**

- **Monolito**: Una sola unidad de despliegue, bases de datos compartidas, acoplamiento fuerte
- **SOA**: Servicios más grandes con ESB centralizado, orientación a reutilización
- **Microservicios**: Servicios pequeños independientes, descentralización, ownership de datos

## 2. Casos donde el Monolito Falla

### Caso 1: E-commerce con picos estacionales
- **Problema**: Black Friday requiere escalar catálogo y checkout, pero el monolito escala todo (incluido back-office innecesario)
- **Costo**: Infraestructura desperdiciada, respuesta lenta ante demanda variable

### Caso 2: SaaS Multi-tenant
- **Problema**: Clientes grandes saturan recursos afectando a todos, despliegue arriesgado impacta todos los tenants
- **Costo**: SLAs comprometidos, imposibilidad de aislar tenants premium

## 3. Definiciones Clave

**Microservicio**: Unidad de despliegue independiente que implementa una capacidad de negocio específica, expone contrato vía API (REST/gRPC), gestiona su propio estado.

**Aplicación de Microservicios**: Ecosistema que incluye servicios + API Gateway + balanceadores + observabilidad (métricas, logs distribuidos, trazas).

## 4. Problemas Típicos del Monolito

1. **Cadencia de despliegue reducida**: Un cambio pequeño requiere redesplegar todo, aumenta riesgo y tiempo
2. **Acoplamiento que impide escalado independiente**: No se puede escalar solo la funcionalidad con alta demanda

## 5. Beneficios de Microservicios

- **Aislamiento de fallos**: Un servicio caído no tumba todo el sistema
- **Escalado granular**: Escalar solo servicios con alta carga (ahorro de costos)
- **Autonomía de equipos**: Equipos pueden desplegar independientemente, diferentes stacks tecnológicos
- **Ciclos de innovación rápidos**: Cambios localizados, menor time-to-market

## 6. Desafíos y Mitigaciones

| Desafío | Mitigación |
|---------|-----------|
| **Complejidad de red/seguridad** | Service mesh (Istio), mTLS, políticas de red |
| **Orquestación distribuida** | Kubernetes, patrones de circuit breaker (Resilience4j) |
| **Consistencia de datos** | Patrones Saga (coreografía/orquestación), eventual consistency |
| **Testing distribuido** | Contract testing (Pact), pruebas de integración con testcontainers |

**Herramientas clave**:
- OpenAPI/Swagger para contratos
- Jaeger/Zipkin para trazabilidad distribuida
- Kafka/RabbitMQ para mensajería asíncrona

## 7. Principios de Diseño

### Domain-Driven Design (DDD)
Usar **bounded contexts** para delimitar servicios: cada contexto define un límite lingüístico y de datos claro.

**Ejemplo**: En e-commerce, `Catálogo`, `Carrito`, `Pagos`, `Inventario` son contextos separados con modelos propios.

### DRY en Microservicios
**Equilibrio crítico**: 
- **Librerías comunes** para cross-cutting concerns (logging, autenticación) → OK
- **Duplicación controlada** de lógica de negocio entre servicios → Preferible a acoplamiento vía librerías compartidas

**Decisión**: Mejor duplicar validaciones simples que crear dependencia fuerte entre servicios.

### Criterios de Tamaño
**Regla pragmática**: "Una capacidad de negocio por servicio"

- ✅ Servicio de `Notificaciones` (email, SMS, push)
- ❌ "Una tabla por servicio" es dogmático y fragmenta innecesariamente

**Heurística**: Si cambios en un servicio frecuentemente requieren cambios en otro, probablemente son uno solo.

---

## Decisiones de Diseño - Resumen Ejecutivo

1. **Partir monolito solo cuando el dolor justifique la complejidad** (no migrar prematuramente)
2. **Empezar con strangler pattern**: extraer funcionalidades de forma incremental
3. **Priorizar observabilidad desde día 1**: sin trazas distribuidas, debuggear es imposible
4. **Definir contratos explícitos**: versionamiento de APIs desde el inicio
5. **Aceptar eventual consistency**: diseñar UX considerando asincronía
