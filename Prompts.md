> Detalla en esta sección los prompts principales utilizados durante la creación del proyecto, que justifiquen el uso de asistentes de código en todas las fases del ciclo de vida del desarrollo. Esperamos un máximo de 3 por sección, principalmente los de creación inicial o  los de corrección o adición de funcionalidades que consideres más relevantes.
Puedes añadir adicionalmente la conversación completa como link o archivo adjunto si así lo consideras


## Uso de la IA en el proyecto

**Herramientas**

| Herramienta | Para qué |
| --- | --- |
| Claude en claude.ai (proyecto «ai4devs -TFM», con las lecciones del curso como fuentes) | Análisis previo: elección de la idea, visión de producto y plan de arranque |
| Claude Code (CLI) en WSL | Trabajo en el repositorio: arnés, prueba de concepto, documentación con BMAD y, en la entrega 2, el código |
| BMAD Method 6.12.4 (módulo BMM) | Método para brief, PRD, UX, arquitectura, épicas e historias, a partir de la sesión 3 |

**Modelos**

| Modelo | Tareas |
| --- | --- |
| Claude Opus 5.5 | Análisis previo en claude.ai y sesión 1 en Claude Code (84 respuestas). Previsto para razonar: brief, PRD, UX, arquitectura y revisión de código |
| Claude Sonnet | Previsto para generar código y tareas mecánicas (Issues, `/registro-ia`) |

**Contexto avanzado**

- `CLAUDE.md`: resumen del proyecto, alcance del MVP, calendario, reglas (`main` sin código hasta el 4 de diciembre, nada de PR ni de secretos), convenciones de ramas y commits y cuándo actualizar este registro.
- Skills propias: `/registro-ia` (redacta este fichero, con Sonnet) y `/revision-adversarial` (revisión hostil del diff de la rama, con Opus y en contexto aislado).
- Hooks: `UserPromptSubmit` captura cada prompt en `.registro-ia/`; `PreToolUse` bloquea ramas y commits que no siguen las convenciones; el hook `commit-msg` de git valida también los commits manuales. Las reglas viven en un solo fichero, `.githooks/convenciones.py`.
- BMAD 6.12.4 instalado con 29 skills para Claude Code, conversación y documentos en español.

**Fases del ciclo de vida**

| Fase | Estado |
| --- | --- |
| Análisis | Cubierta: matriz de nueve ideas y visión de producto (claude.ai) |
| Diseño | Cubierta en parte: plan de arranque y estructura del repositorio. Arquitectura, modelo de datos y API con BMAD (sesiones 3 a 6) |
| Implementación | Prevista: prueba de concepto (sesión 2) y entrega 2 |
| Pruebas | Prevista: `/revision-adversarial` y tests E2E de la entrega final |
| Despliegue | Prevista: docker-compose en la entrega 2 |
| Mantenimiento | Iniciada: hooks que hacen cumplir las convenciones y registro automático de la IA |

## Registro por hitos

### 2026-11-19 a 2026-11-23 · Análisis previo en claude.ai

**Qué se hizo:** nueve ideas de proyecto puntuadas con una matriz de ocho criterios sacados de la lección 1; la visión de producto de la torre de control (Holdpoint), con alcance, principios y prueba de concepto; la adaptación del plan a la lección 2; y el plan de arranque en Claude Code (`docs/plan-arranque.md`).

**Herramienta y modelos:** Claude en claude.ai, con las lecciones del curso como fuentes del proyecto. Claude Opus 5.5 en todas las conversaciones.

**Prompts clave:** las conversaciones se hicieron en claude.ai y no se capturaron textualmente; el resultado está en `docs/vision/vision-producto.md` y `docs/plan-arranque.md`.

**Criterio humano:**

- BMAD trabaja con su estructura estándar y la entrega se compone después a partir de sus artefactos, en lugar de obligarlo a escribir en `docs/`.
- La prueba de concepto se hace sin BMAD, para no meter ceremonia en una prueba rápida.
- El agente de la prueba de concepto prepara la entrada de BMAD.
- Los tickets salen del desglose de BMAD, no se escriben a mano.
- Se cuestionó la recomendación de no hacer fork del repo oficial. Se mantuvo porque un fork trae los Issues desactivados y propone las PR contra el repo de LIDR.
- Se incluye el paso de UX de BMAD para el panel, una parte del método que Francisco no había usado porque suele trabajar en backend.

**Commits:** ninguno; trabajo previo al repositorio.

### 2026-11-23 · Sesión 1: repositorio y arnés

**Qué se hizo:** rama `main`, `README.md` y `Prompts.md` de la plantilla de LIDR, `.gitignore` y `.editorconfig`; instalación no interactiva de BMAD 6.12.4 en español; `CLAUDE.md`; registro de IA automático (hook de captura, skill `/registro-ia` y retención de transcripciones a 180 días); convenciones de ramas y commits reforzadas con hooks de Claude Code y de git; skill `/revision-adversarial`. Se comprobó que el hook captura los prompts, que bloquea una rama (`prueba`) y un commit (`cosas`) mal formados y que `/bmad-help` responde.

**Herramienta y modelos:** Claude Code (CLI) en WSL, con Claude Opus 5.5 (84 respuestas en la sesión).

**Prompts clave:**

1. «Lee docs/plan-arranque.md y ejecuta la sesión 1. Antes de tocar nada, dame el plan paso a paso y dime qué necesitas de mí, por ejemplo si el instalador de BMAD lo lanzo yo. Respeta las reglas de «Alcance y calendario».» → Plan de la sesión en modo planificación, con las preguntas sobre la plantilla, el instalador y la rama antes de tocar nada.
2. «Reglas de alcance: las que mencionas. el Alcance lo tienes en el fichero @docs/vision/vision-producto.md» (al rechazar el primer plan) → El plan y `CLAUDE.md` enlazan el alcance y lo que queda fuera del MVP en la visión.
3. «tambien crearemos una skill de revision adversial, reglas de nombrado de rams, y de commit. estas 2 últimas las reforzaremos con un hook que verifique el formato antes de crear una rama y hacer un commit respectivamente» → `.githooks/convenciones.py`, hooks `PreToolUse` y `commit-msg` y la skill `/revision-adversarial`.

**Criterio humano:**

- Rechazó el primer plan para señalar que el alcance está en la visión de producto: quería evitar desvíos del MVP.
- Añadió la revisión adversarial y las convenciones de ramas y commits con hooks para que la disciplina no dependa de él, para que el código generado lo revise una mirada distinta de la del agente que lo escribió y porque la entrega valora ese contexto avanzado.
- Limitó la revisión adversarial al código porque BMAD ya trae sus propias revisiones de documentos.
- Pidió que el agente lanzara el instalador de BMAD en modo no interactivo para que fuera reproducible y quedara registrado.
- Eligió las convenciones propuestas: ramas `<tipo>/<slug>`, Conventional Commits en español y validación de commits doble (Claude Code y `commit-msg` de git). Dio la URL del repo de la plantilla y aprobó renombrar `master` a `main`.

**Commits:** commit de cierre de la sesión 1 en `main`.

## Índice

1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 1. Descripción general del producto

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.2. Descripción de componentes principales:**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

**Prompt 1:** (sesión 1, Claude Code) «Lee docs/plan-arranque.md y ejecuta la sesión 1. Antes de tocar nada, dame el plan paso a paso y dime qué necesitas de mí […]» → estructura del repositorio y arnés del proyecto.

**Prompt 2:**

**Prompt 3:**

### **2.4. Infraestructura y despliegue**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.5. Seguridad**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.6. Tests**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 3. Modelo de Datos

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 4. Especificación de la API

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 5. Historias de Usuario

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 6. Tickets de Trabajo

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 7. Pull Requests

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**
