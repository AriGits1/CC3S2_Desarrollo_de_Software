# Actividad 5: Construyendo un pipeline DevOps con Make y Bash
## Capturas de la ejecucion de ejercicios

![Terminal](imagenes/Ejercicios_1_2_y_3.png)
![Terminal](imagenes/Ejercicio4_completo.png)
![Terminal](imagenes/Ejercicio6.png)
![Terminal](imagenes/Ejercicios_7_y_8.png)

## Parte 1 - Construir

### ¿Qué hace `build` y cómo funciona `$(PYTHON) $< > $@`?

El objetivo `build` del Makefile genera el archivo `out/hello.txt` a partir del script `src/hello.py`. La regla utiliza **variables automáticas** de Make:

- **`$<`**: Representa el **primer prerequisito** de la regla (en este caso `src/hello.py`)
- **`$@`**: Representa el **target** o archivo objetivo (en este caso `out/hello.txt`)
- **`$(@D)`**: Representa el **directorio** del target (`out/`)

La receta `$(PYTHON) $< > $@` se expande a `python3 src/hello.py > out/hello.txt`, ejecutando el script Python y redirigiendo su salida al archivo de destino. Primero crea el directorio con `mkdir -p $(@D)` para asegurar que existe la ruta de destino.

### Modo estricto y protecciones

El Makefile implementa **modo estricto** mediante:

- **`.SHELLFLAGS := -eu -o pipefail -c`**: 
  - `-e`: Termina inmediatamente si cualquier comando falla
  - `-u`: Error si se usa una variable no definida  
  - `-o pipefail`: Un pipe falla si cualquier comando en la cadena falla
  - `-c`: Ejecuta el comando que sigue

- **`.DELETE_ON_ERROR`**: Si una receta falla, Make automáticamente **elimina el archivo target** para evitar artefactos corruptos o parcialmente generados.

Estas protecciones evitan estados inconsistentes donde un build parcialmente fallido deje archivos corruptos que podrían confundir ejecuciones futuras.

### Idempotencia: Diferencia entre 1.ª y 2.ª corrida de `build`

**Primera ejecución:**
- Make compara timestamps: `src/hello.py` (fuente) vs `out/hello.txt` (target)
- Como `out/hello.txt` no existe, ejecuta la receta completa
- Crea el directorio `out/` y genera `out/hello.txt`
- Salida: `mkdir -p out` y `python3 src/hello.py > out/hello.txt`

**Segunda ejecución:**
- Make compara timestamps nuevamente
- `out/hello.txt` existe y es **más reciente** que `src/hello.py`
- Make concluye que el target está **actualizado**
- **No ejecuta ninguna receta** (idempotencia)
- Salida: `make: 'out/hello.txt' is up to date.`

Esta **incrementalidad** es fundamental en DevOps: solo se reconstruye lo que realmente cambió, ahorrando tiempo en builds grandes y complejos. Make utiliza el **grafo de dependencias** y las **marcas de tiempo** para determinar automáticamente qué trabajo es necesario.
