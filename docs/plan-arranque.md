---
titulo: "Plan de arranque del TFM en Claude Code"
proyecto: "Proyecto final AI4Devs (LIDR)"
autor: "Francisco de la Puente González"
fecha: 2026-11-23
version_editable: "https://claude.ai/artifact/VhWSsCsCHkp8AEGo2NNM8R"
---

# Plan de arranque del TFM en Claude Code

Este plan es la entrada de la primera sesión de Claude Code (CLI) en el repo del TFM: el agente lo lee y ejecuta la sesión 1. Las sesiones siguientes siguen la escaleta hasta la entrega 1, con envío el 3 de diciembre y fecha límite el 4.

## Contexto

El TFM es el proyecto final del curso AI4Devs de LIDR. La propuesta es Holdpoint, una torre de control para agentes de IA: una pasarela con aprobación humana que empieza por MCP. Su visión está en `docs/vision/vision-producto.md`, y la prueba de concepto decide el 26 de noviembre si se sigue con ella.

La entrega 1 es solo documentación, sin código:

- Va en dos ficheros del repo: `README.md` (ficha, descripción, arquitectura, modelo de datos, API, historias de usuario, tickets y stack) y `Prompts.md` (registro del uso de la IA).
- Se entrega con la rama `feature/entrega-1-fp` y el Typeform. No se abre ninguna pull request.
- La revisión valora el problema y el caso de uso, que el MVP sea viable, la coherencia entre arquitectura, modelo de datos, API y tickets, y el uso de la IA en al menos 4 de las 6 fases del ciclo de vida.
- Las reglas completas están en las lecciones 1 y 2 del curso. Si algo choca, manda la lección 1.

## Decisiones tomadas

| Tema | Decisión |
| --- | --- |
| Nombre | Holdpoint. Repo `holdpoint`, con el lema «Holdpoint — where AI agents wait for clearance» como descripción y los temas `ai-agents`, `human-in-the-loop`, `mcp` y `claude-code`. El nombre no se ata a MCP porque el producto irá más allá. |
| Repositorio | Uno solo, público, en la cuenta personal de GitHub. Contiene la prueba de concepto y el proyecto real. |
| Entorno | Claude Code (CLI) en WSL, con el repo clonado en el sistema de ficheros de Linux (`~/`). |
| Ramas | `main` lleva solo documentación hasta el 4 de diciembre. La prueba de concepto vive en la rama `poc/pasarela`, en la carpeta `poc/`, y se fusiona después de la entrega 1. |
| BMAD | Versión 6.12, la estable. Se instala con el arnés, pero no se usa en la prueba de concepto, que se hace en vibe coding para ir rápido. |
| Modelos | Opus para razonar (brief, PRD, UX, arquitectura y revisión de código) y Sonnet para generar código y tareas mecánicas (Issues, `/registro-ia`). En la prueba de concepto se empieza con Sonnet y se pasa a Opus si se atasca. Se fija en la cabecera de subagentes, comandos o skills (`model:`), y `/registro-ia` toma el modelo real de las transcripciones. |
| Artefactos de BMAD | Se quedan en su carpeta estándar (`_bmad-output/`) y con su estructura. `README.md` se compone a partir de ellos, y `docs/` solo guarda lo que BMAD no genera. |
| Entrada de BMAD | La redacta el agente de la prueba de concepto al terminarla, con la visión y lo aprendido. |
| Tickets | En GitHub Issues, creados por el agente a partir de las épicas e historias de BMAD: una épica por cada historia imprescindible. |
| Registro de IA | `Prompts.md` lo mantiene el agente: un hook captura cada prompt y la skill `/registro-ia` redacta las entradas. El registro en bruto no se sube al repo. |
| Material del curso | Las lecciones de LIDR no se suben al repo. |

## Estructura del repositorio

```
/
├── README.md           ← ficha de la entrega (plantilla de LIDR)
├── Prompts.md          ← registro de IA, lo mantiene el agente
├── CLAUDE.md
├── .claude/            ← settings.json, hooks y skills (también las de BMAD)
├── _bmad/              ← instalación de BMAD 6.12
├── _bmad-output/       ← artefactos de BMAD, en su estructura estándar
├── docs/
│   ├── plan-arranque.md    ← este plan
│   ├── vision/             ← visión de producto
│   └── entrada-bmad.md     ← lo genera la sesión 2
├── .registro-ia/       ← prompts en bruto (en .gitignore)
└── poc/                ← solo en la rama poc/pasarela hasta el 4 dic
```

`src/`, `tests/` y `deploy/` llegan en la entrega 2. Cómo se reparten por dentro (pasarela, API, panel, servidor de ejemplo) lo decide la arquitectura de BMAD.

## Registro de IA

`Prompts.md` lo mantiene el agente en dos capas, para no depender de que nadie se acuerde.

**Captura automática.** Un hook `UserPromptSubmit` en `.claude/settings.json` ejecuta un script que añade una línea JSON por prompt a `.registro-ia/AAAA-MM-DD.jsonl`, con fecha, rama, sesión y texto. El script no escribe nada por la salida estándar, porque en ese hook lo que sale se añade al contexto, y siempre termina con código 0 para no bloquear el prompt.

**Redacción al cerrar cada hito.** La skill `/registro-ia`:

1. Lee lo capturado desde la última ejecución, el modelo de cada respuesta en las transcripciones de Claude Code y el `git log` del mismo periodo.
2. Actualiza `Prompts.md` con la estructura de la plantilla de LIDR y cubre lo que pide la lección 1: herramientas, modelos, contexto avanzado (CLAUDE.md, skills, hooks, BMAD), de 3 a 5 prompts clave y criterio humano.
3. Para el criterio humano, propone los momentos en que Francisco corrigió o rechazó algo y le pregunta el porqué, en lugar de inventárselo.
4. Guarda en `.registro-ia/` la marca de la última ejecución.

**Retención.** `cleanupPeriodDays` a 180 en `.claude/settings.json`, para que Claude Code no borre las transcripciones antes de la entrega final.

Se ejecuta al final de la sesión 1, de la prueba de concepto, del brief y el PRD, del diseño de UX, de la arquitectura, de los tickets y de la entrega.

## Sesión 1: repositorio y arnés (23-24 nov)

**Antes de abrir Claude Code (Francisco):**

1. Crear el repo público `holdpoint` en GitHub con la cuenta personal, con el lema como descripción y sus temas, y clonarlo en WSL, dentro de `~/`.
2. Copiar `README.md` y `Prompts.md` de la plantilla oficial (repo AI4Devs-finalproject, enlace en la lección 1).
3. Copiar este plan a `docs/plan-arranque.md` y la visión a `docs/vision/vision-producto.md`.
4. Abrir `claude` en la raíz del repo y pedirle que lea `docs/plan-arranque.md` y ejecute la sesión 1.

**Lo que hace el agente, en este orden:**

1. `.gitignore` (`.registro-ia/`, `.env`, `bin/`, `obj/`, `node_modules/`) y `.editorconfig`.
2. Instalar BMAD con `npx bmad-method install` (necesita Node 20.12+, Python 3.10+ y uv): módulo BMM, herramienta Claude Code, conversación y documentos en español, carpeta de salida por defecto. El instalador es interactivo: lo lanza Francisco en su terminal, o el agente en modo no interactivo con `--modules bmm --tools claude-code --communication-language Spanish --document-output-language Spanish --yes` (comprobar las opciones con `--help`). Verificar que la versión instalada es la 6.12.x.
3. `CLAUDE.md`: qué es el proyecto en tres líneas, con enlaces a la visión y a este plan; dónde vive cada cosa; las ramas (`main` sin código hasta el 4 de diciembre y nunca abrir PR al repo de LIDR); nada de secretos, solo `.env.example`; documentos y commits en español; cuándo ejecutar `/registro-ia`; y que BMAD no se usa en la prueba de concepto.
4. El registro de IA de la sección anterior: hook, script, skill y `cleanupPeriodDays`. Claude Code lee los hooks al arrancar, así que hay que reiniciar la sesión o revisarlos en `/hooks` para que entren en vigor.
5. Primera entrada de `Prompts.md` con `/registro-ia`, a partir de la sección «Primera entrada de Prompts.md».
6. Commit en `main` y push.

**Hecho cuando:**

- Un prompt de prueba aparece en `.registro-ia/`.
- `/registro-ia` añade una entrada a `Prompts.md`.
- `/bmad-help` responde.
- `main` no contiene código.

## Siguientes sesiones

| Fecha | Sesión | Resultado |
| --- | --- | --- |
| 24-25 nov | 2. Prueba de concepto en `poc/pasarela`, en vibe coding y sin BMAD, con las cinco comprobaciones de la visión | `poc/README.md` con el resultado de cada comprobación y el tiempo de espera medido; `docs/entrada-bmad.md` en `main`; `/registro-ia` |
| 26 nov | Decisión | Seguir con Holdpoint o cambiar de propuesta |
| 26-27 nov | 3. BMAD: brief y PRD, partiendo de `docs/entrada-bmad.md` | Brief y PRD en `_bmad-output/` |
| 27-28 nov | 4. BMAD: UX del panel, con el agente de diseño de UX | Especificación de UX del panel en `_bmad-output/`, base de los tickets de frontend |
| 28-29 nov | 5. BMAD: arquitectura | Componentes, modelo de datos, API y stack. Si no detalla el modelo de datos o la API, se completan en `docs/` |
| 29-30 nov | 6. BMAD: épicas e historias, y tickets en GitHub Issues | Una épica por historia imprescindible; Issues etiquetados como backend, frontend y bd |
| 1-2 dic | 7. Coherencia y README | Comprobación de readiness de BMAD, `README.md` compuesto y `Prompts.md` al día |
| 3 dic | 8. Entrega | Rama `feature/entrega-1-fp` desde `main` y Typeform |
| Desde el 4 dic | Entrega 2 | Fusionar `poc/pasarela` en `main` y empezar el esqueleto |

**Contenido de `docs/entrada-bmad.md`.** Lo redacta el agente de la sesión 2 como entrada del brief: resumen de la visión, resultados de la prueba de concepto y limitaciones encontradas (SDK, tiempos de espera), alcance y fuera de alcance del MVP, las cinco historias y lo que exige la entrega 1 (modelo de datos, API y tickets de backend, frontend y base de datos). Se guarda en `main`, porque es documentación y BMAD trabaja allí.

**De BMAD al README.** El README resume y enlaza los artefactos de BMAD; no los copia enteros.

| Apartado del README | Sale de |
| --- | --- |
| Ficha y descripción general | Brief y PRD |
| Arquitectura y stack | Arquitectura de BMAD |
| Modelo de datos y API | Arquitectura de BMAD, o `docs/` si se completó allí |
| Historias de usuario | Épicas de BMAD |
| Tickets de trabajo | Historias de BMAD y GitHub Issues |

## Primera entrada de Prompts.md

Recoge el análisis previo hecho en claude.ai, en el proyecto «ai4devs -TFM», del 19 al 23 de noviembre. El agente la redacta a partir de esto:

- **Qué se hizo:** nueve ideas de proyecto puntuadas con una matriz de ocho criterios sacados de la lección 1; la visión de producto de la torre de control, con alcance, principios y prueba de concepto; la adaptación del plan a la lección 2; y este plan de arranque.
- **Herramienta:** Claude en claude.ai, con las lecciones del curso como fuentes del proyecto.
- **Criterio humano en este plan:**
    - BMAD trabaja con su estructura estándar y la entrega se compone después a partir de sus artefactos, en lugar de obligarlo a escribir en `docs/`.
    - La prueba de concepto se hace sin BMAD, para no meter ceremonia en una prueba rápida.
    - El agente de la prueba de concepto prepara la entrada de BMAD.
    - Los tickets salen del desglose de BMAD, no se escriben a mano.
    - Se cuestionó la recomendación de no hacer fork del repo oficial. Se mantuvo porque un fork trae los Issues desactivados y propone las PR contra el repo de LIDR.
    - Se incluye el paso de UX de BMAD para el panel, una parte del método que Francisco no había usado porque suele trabajar en backend.
- **Modelos:** Claude Opus 5.5 en todas las conversaciones de esta fase.

## Checklist de la entrega 1

- [ ] `README.md` con ficha, descripción, arquitectura, modelo de datos, API, historias, tickets y stack, sin textos de ejemplo de la plantilla
- [ ] `Prompts.md` con herramientas, modelos, contexto avanzado, prompts clave y criterio humano
- [ ] IA usada o prevista en al menos 4 de las 6 fases: análisis, diseño, implementación, pruebas, despliegue y mantenimiento
- [ ] Arquitectura, modelo de datos, API y tickets coherentes entre sí
- [ ] Rama `feature/entrega-1-fp` sin código
- [ ] Typeform enviado con el correo del calendario de formación y el enlace directo a la rama
