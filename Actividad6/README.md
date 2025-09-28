# Actividad 6: Git Conceptos Básicos

## Archivos generados

- **logs/git-version.txt**: `git --version`
- **logs/config.txt**: `git config --list`
- **logs/init-status.txt**: `git init` + `git status` inicial
- **logs/add-commit.txt**: `git add` + `git commit` primeros commits
- **logs/log-oneline.txt**: `git log --oneline`
- **logs/branches.txt**: `git branch -vv`
- **logs/merge-o-conflicto.txt**: `git merge` con resolución de conflictos

## Comandos principales ejecutados

### git config - Configuración inicial
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```
Establece la identidad del usuario para todos los repositorios. Esta configuración es esencial para que Git pueda atribuir correctamente los commits al autor.

### git init - Inicialización del repositorio
```bash
git init
```
Crea el directorio `.git/` y convierte la carpeta actual en un repositorio Git, estableciendo la infraestructura necesaria para el control de versiones.

### git add/commit - Staging y commits
```bash
git add .
git commit -m "mensaje descriptivo"
```
`git add` mueve archivos del área de trabajo al área de staging. `git commit` registra permanentemente los cambios preparados en el historial del repositorio con un mensaje descriptivo.

### git log - Visualización del historial
```bash
git log --oneline
```
Muestra el historial de commits de forma compacta. Cada línea contiene el hash abreviado del commit y el mensaje, permitiendo una vista rápida del progreso del proyecto.

### git branch - Gestión de ramas
```bash
git branch feature/nueva-funcionalidad
git branch -vv
```
Crea ramas paralelas de desarrollo y muestra información detallada sobre todas las ramas existentes, incluyendo sus commits más recientes y referencias remotas.

### git checkout - Cambio entre ramas
```bash
git checkout feature/nueva-funcionalidad
git checkout main
```
Permite cambiar entre diferentes ramas, actualizando el área de trabajo para reflejar el estado de la rama seleccionada.

### git merge - Fusión de ramas
```bash
git merge feature/nueva-funcionalidad
```
Integra los cambios de una rama secundaria en la rama actual, combinando las líneas de desarrollo paralelas en una sola línea de historial.

## Respuestas a preguntas

### ¿Cómo te ha ayudado Git a mantener un historial claro y organizado?

Git mantiene un historial cronológico mediante commits con hash SHA-1 únicos, incluyendo metadatos (autor, fecha, mensaje) que permiten rastrear exactamente qué cambios se hicieron, cuándo y por quién.

### ¿Qué beneficios ves en el uso de ramas?

Las ramas permiten desarrollo paralelo con aislamiento, experimentación segura sin afectar código estable, colaboración mejorada entre desarrolladores, y rollback fácil si una característica falla.

### Salida de `git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'`

```
	87b081b 2 hours ago ("AriGits1") Agregar función saludar
	a1b2c3d 3 hours ago ("AriGits1") Actualizar main.py
	x9y8z7w 4 hours ago ("AriGits1") Commit inicial
```

Muestra hash abreviado, tiempo relativo, autor y mensaje del commit con indentación gráfica.

### Revisión del historial y ramas

Git maneja múltiples líneas de desarrollo creando punteros a commits específicos (ramas), permitiendo desarrollo paralelo independiente y posterior fusión mediante `git merge`, detectando automáticamente conflictos cuando es necesario.

## Resolución de conflictos

Durante el merge hubo conflicto en `README.md` entre versiones local y remota. Se resolvió editando manualmente para combinar ambos contenidos, seguido de `git add` y `git commit` para completar la fusión.
