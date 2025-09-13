1. Introducción a DevOps: ¿Qué es y qué no es?

¿Qué es DevOps?
DevOps es un enfoque que integra desarrollo y operaciones para entregar software rápidamente y con alta calidad. Promueve la colaboración, la automatización y la entrega continua de software.

¿Qué no es DevOps?
No es solo usar herramientas como Docker o Jenkins, ni es un solo rol. Tampoco es un proceso lineal como en Waterfall, donde las etapas son rígidas y separadas.

1.2. DevOps: Desde el código hasta la producción

DevOps cubre todo el ciclo de vida del software:

Desarrollo (Code): Se escribe el código.

Construcción (Build): Se compila y se prueba automáticamente.

Despliegue (Deploy): Se lanza el software en producción.

Monitoreo (Monitor): Se sigue el rendimiento en producción.

A diferencia de Waterfall, donde todo se hace en etapas separadas, en DevOps se hace todo de forma continua.

1.3. "You Build It, You Run It"

Este principio significa que los desarrolladores también son responsables de que su código funcione bien en producción. En el laboratorio, esto significa que los mismos desarrolladores configuran las alertas y monitorean su propio software.

1.4. Mitos vs Realidades

Mitos:

DevOps es solo herramientas.

DevOps es solo un rol.

DevOps es solo CI/CD.

Realidades:

DevOps es Cultura, Automatización, Medición, Lean y Compartir (CALMS).

Se basa en feedback constante.

Usa métricas y gates de calidad para garantizar que el software funcione correctamente antes de llegar a producción.

2. CALMS en Acción

Culture (Cultura): Colaboración entre desarrollo y operaciones. Ejemplo: alertas automáticas en Slack.

Automation (Automatización): Uso de Makefile para automatizar tareas como la construcción y el despliegue.

Lean (Eficiencia): Minimizar desperdicios en el proceso, optimizando el tiempo de entrega.

Measurement (Medición): Usar métricas como los endpoints de salud para monitorear el sistema.

Sharing (Compartir): Documentación de procedimientos y análisis de incidentes (runbooks y postmortems).

3. DevSecOps: Integración de Seguridad

DevSecOps es una extensión de DevOps que incluye seguridad desde el principio. Esto implica integrar prácticas de seguridad como la verificación de certificados TLS y escaneo de dependencias en el pipeline de CI/CD.

Escenario Retador: Si un certificado SSL falla, el equipo debe estar preparado para mitigar el problema rápidamente. Esto se puede lograr con monitoreo continuo y pruebas de seguridad automatizadas.

4. 12-Factor App en el Laboratorio

1. Configuración por entorno (Config): Usar archivos .env para separar configuraciones como base de datos y credenciales.

2. Port Binding: Cada microservicio debe funcionar en su propio puerto.

3. Logs como flujos: Los logs deben ser enviados a un servicio como ELK Stack para ser procesados como flujos de datos.

4. Statelessness: Las aplicaciones deben ser sin estado; si necesitan almacenamiento, usan bases de datos externas (por ejemplo, Redis)
