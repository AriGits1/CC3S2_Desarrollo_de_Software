# Actividad 17: Pruebas en IaC con Terraform

## Descripción de Módulos

### 1. Módulo `network`
**Propósito**: Gestiona la infraestructura de red básica.

**Variables de entrada**:
- `vpc_cidr`: CIDR block para la VPC (ej: "10.0.0.0/16")
- `subnet_count`: Número de subnets a crear
- `environment`: Nombre del entorno (dev, staging, prod)

**Outputs**:
- `vpc_id`: ID de la VPC creada
- `subnet_ids`: Lista de IDs de subnets
- `vpc_cidr_block`: CIDR block de la VPC

---

### 2. Módulo `compute`
**Propósito**: Gestiona instancias de cómputo y configuración.

**Variables de entrada**:
- `subnet_ids`: Lista de subnets donde desplegar instancias
- `instance_count`: Número de instancias a crear
- `instance_type`: Tipo de instancia (ej: "t2.micro")

**Outputs**:
- `instance_ids`: Lista de IDs de instancias
- `instance_ips`: IPs privadas de las instancias
- `instance_count`: Número de instancias creadas

---

### 3. Módulo `storage`
**Propósito**: Gestiona almacenamiento y buckets.

**Variables de entrada**:
- `bucket_name`: Nombre del bucket de almacenamiento
- `versioning_enabled`: Habilitar versionado (true/false)
- `encryption_enabled`: Habilitar encriptación (true/false)

**Outputs**:
- `bucket_id`: ID del bucket
- `bucket_arn`: ARN del bucket
- `bucket_name`: Nombre del bucket

---

### 4. Módulo `firewall`
**Propósito**: Define reglas de acceso y políticas de seguridad.

**Variables de entrada**:
- `allowed_ports`: Lista de puertos permitidos
- `allowed_cidrs`: Lista de CIDRs permitidos
- `vpc_id`: ID de la VPC donde aplicar reglas

**Outputs**:
- `firewall_policy`: Objeto JSON con la política completa
- `security_group_id`: ID del grupo de seguridad
- `rules_count`: Número de reglas aplicadas

**Validación**: Rechaza puertos fuera del rango 1-65535 y CIDRs mal formados.

---

### 5. Módulo `dns`
**Propósito**: Gestiona registros DNS y mapeo hostname->IP.

**Variables de entrada**:
- `hostnames`: Lista de nombres de host
- `ip_addresses`: Lista de IPs correspondientes
- `zone_name`: Nombre de la zona DNS

**Outputs**:
- `dns_mapping`: Mapa de hostname->IP
- `zone_id`: ID de la zona DNS
- `records_count`: Número de registros creados

**Validación**: Rechaza nombres con espacios o caracteres no válidos (solo alfanuméricos, guiones y puntos).

---

## Estructura del Proyecto

```
Actividad17-CC3S2/
├── README.md
├── Ejercicios_obligatorios.md
├── modules/
│   ├── network/
│   ├── compute/
│   ├── storage/
│   ├── firewall/
│   └── dns/
├── scripts/
│   ├── run_smoke.sh
│   └── run_all.sh
├── plans/
│   └── plan_base_network.json
└── evidencia/
    ├── smoke_run.txt
    ├── all_run.txt
    └── e2e_http_check.txt
```

## Ejecución de Pruebas

### Pruebas de humo (< 30s)
```bash
./scripts/run_smoke.sh
```

### Suite completa de pruebas
```bash
./scripts/run_all.sh
```

## Pirámide de Pruebas

1. **Unitarias**: Validación de módulos aislados
2. **Contrato**: Verificación de interfaces entre módulos
3. **Integración**: Pruebas de módulos encadenados
4. **Humo**: Validación rápida de sintaxis y semántica
5. **Regresión**: Comparación contra planes dorados
6. **E2E**: Validación completa del flujo
