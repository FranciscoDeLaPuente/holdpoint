> Detalla en esta sección los prompts principales utilizados durante la creación del proyecto, que justifiquen el uso de asistentes de código en todas las fases del ciclo de vida del desarrollo. Esperamos un máximo de 3 por sección, principalmente los de creación inicial o  los de corrección o adición de funcionalidades que consideres más relevantes.
Puedes añadir adicionalmente la conversación completa como link o archivo adjunto si así lo consideras


## Uso de la IA en el proyecto

**Herramientas**

| Herramienta | Para qué |
| --- | --- |
| Claude en claude.ai (proyecto «ai4devs -TFM», con las lecciones del curso como fuentes) | Análisis previo: elección de la idea, visión de producto y plan de arranque |
| Claude Code (CLI) en WSL | Trabajo en el repositorio: arnés, prueba de concepto, documentación con BMAD y, en la entrega 2, el código |
| GitHub CLI (`gh`), lanzado desde Claude Code | Etiquetas, Issues y hitos del repositorio (la API de hitos con `gh api`) |
| `tmux` y `claude -p`, lanzados desde Claude Code | Probar la pasarela con un Claude Code real, en modo no interactivo y en una sesión interactiva |
| BMAD Method 6.12.4 (módulo BMM) | Método para brief, PRD, UX, arquitectura, épicas e historias, a partir de la sesión 3 |

**Modelos**

| Modelo | Tareas |
| --- | --- |
| Claude Opus 5.5 | Análisis previo en claude.ai, sesión 1 en Claude Code (84 respuestas) y sesión 3, brief y PRD con BMAD (129 respuestas, más 6 subagentes de revisión). Previsto también para UX, arquitectura y revisión de código |
| Claude Sonnet 5.5 | Prueba de concepto en Claude Code (228 respuestas): servidor de ejemplo y pasarela en .NET, Issue, etiquetas e hitos con `gh`, pruebas, `CLAUDE.md` y `docs/entrada-bmad.md`. En la sesión 3, las 8 primeras respuestas antes de cambiar a Opus y el subagente que buscó y comparó alternativas en la web. Previsto también para Issues y `/registro-ia` |
| Claude Haiku 5.5 | Solo como cliente de prueba: el Claude Code que se conectaba a la pasarela en las comprobaciones (67 respuestas). No generó código del repo |

**Contexto avanzado**

- `CLAUDE.md`: resumen del proyecto, alcance del MVP, calendario, reglas (`main` sin código hasta el 4 de diciembre, nada de PR ni de secretos), convenciones de ramas y commits y cuándo actualizar este registro.
- Skills propias: `/registro-ia` (redacta este fichero, con Sonnet) y `/revision-adversarial` (revisión hostil del diff de la rama, con Opus y en contexto aislado).
- Hooks: `UserPromptSubmit` captura cada prompt en `.registro-ia/`; `PreToolUse` bloquea ramas y commits que no siguen las convenciones; el hook `commit-msg` de git valida también los commits manuales. Las reglas viven en un solo fichero, `.githooks/convenciones.py`.
- En la prueba de concepto los hooks hicieron su trabajo: bloquearon cinco intentos de commit con el asunto de más de 72 caracteres, y hubo que acortarlos.
- BMAD 6.12.4 instalado con 29 skills para Claude Code, conversación y documentos en español.
- En la sesión 3 se usaron `bmad-product-brief`, `bmad-prd` y `bmad-review` (lentes de estructura y redacción). Cada artefacto lleva una `.memlog.md` con todas las decisiones y un anexo con el detalle técnico para los pasos siguientes. Las búsquedas y revisiones se hicieron con subagentes en contexto aislado: búsqueda de alternativas en la web, contraste del PRD con sus entradas y revisión con la lista de calidad de BMAD.
- Un hook `pre-commit` de git y el `PreToolUse` de Claude Code rechazan los commits directos en `main`; los cambios se integran con `git merge --no-ff`.

**Fases del ciclo de vida**

| Fase | Estado |
| --- | --- |
| Análisis | Cubierta: matriz de nueve ideas y visión de producto (claude.ai); brief con comparación de alternativas y PRD con 23 requisitos funcionales (BMAD) |
| Diseño | Cubierta en parte: plan de arranque y estructura del repositorio. Arquitectura, modelo de datos y API con BMAD (sesiones 3 a 6) |
| Implementación | Cubierta en parte: prueba de concepto (servidor de ejemplo y pasarela en .NET 10). El código funcional llega en la entrega 2 |
| Pruebas | Iniciada: ocho comprobaciones de la prueba de concepto contra un Claude Code real (`-p` e interactivo). Previstas: `/revision-adversarial` y tests E2E de la entrega final |
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

### 2026-11-24 · Prueba de concepto de la pasarela

**Qué se hizo:** un servidor MCP de ejemplo (`listar_tareas`, solo lectura, y `borrar_tarea`, destructiva) y una pasarela que hace de servidor para Claude Code y de cliente del servidor de ejemplo, en .NET 10 con el SDK oficial `ModelContextProtocol.AspNetCore` 2.4.0, por HTTP. Las cinco comprobaciones de «Supuestos a validar» salieron en verde (la quinta, medida: Claude Code corta a los 60 s). Después, las tres pruebas del cierre: las notificaciones de progreso reinician el límite de 60 s (P1), Claude Code declara la extensión de Tasks de MCP (P2) y el uso interactivo funciona igual, con matices de interfaz (P3). Además: etiquetas, hitos e Issue #1 en GitHub, las reglas de «Alcance y calendario» en `CLAUDE.md`, la revisión de coherencia de `CLAUDE.md`, y `docs/entrada-bmad.md` con resultados, hallazgos, caminos para la espera y estados de la llamada retenida. El Issue #1 quedó cerrado. El 26 de noviembre de 2026 Francisco decidió seguir con Holdpoint y lo anotó en el Issue.

**Herramienta y modelos:** Claude Code (CLI) en WSL con Claude Sonnet 5.5 (228 respuestas en la sesión). Claude Haiku 5.5 (67 respuestas) solo como cliente de prueba. La preparación del prompt se hizo antes en claude.ai.

**Prompts clave:**

1. «Sesión 2 del plan (docs/plan-arranque.md): prueba de concepto. Crea la rama poc/pasarela y trabaja solo en poc/. Sin BMAD, en vibe coding. […] Usa el SDK oficial de MCP para C#. Antes de escribir código, comprueba en el paquete instalado o en sus ejemplos oficiales cómo se llaman de verdad las clases y los métodos de esa versión. Si algo no existe, para y dímelo; no lo inventes. […]» → Servidor de ejemplo y pasarela. Los nombres se comprobaron en la documentación XML del paquete antes de escribir código; el único error de compilación en toda la prueba fue un `using` que faltaba.
2. «Antes de seguir: crea las etiquetas poc, backend, frontend y bd en GitHub con gh, y un Issue «Prueba de concepto de la pasarela» con la etiqueta poc, el objetivo, el enlace a «Supuestos a validar» de la visión y las cinco comprobaciones como lista de tareas. Referencia el Issue en todos los commits de poc/pasarela y marca cada comprobación cuando quede verificada.» → Cuatro etiquetas, el Issue #1 y los cuatro commits existentes reescritos con `Refs #1`.
3. «comprueba que claude.md no tenga reglas repetidas, analiza coherencia» → Informe con cinco solapes y tres incoherencias. La principal: la regla de modelos exigía `model:` en las skills, pero solo 2 de las 31 skills del repo lo llevan y las de BMAD no se editan. La corrección posterior («los modelos se fijaran en las skills que no sean de BMAD y/o escogiendolo en la sesion») deja la regla aplicable.
4. «lee poc/cierre-poc.md y ejecuta las tres pruebas pendientes, con una hora como máximo y el cierre» → P1 a P3 en unos 17 minutos (con una sesión interactiva manejada desde `tmux`), `docs/entrada-bmad.md` en `main` y el Issue #1 comentado y cerrado.

**Criterio humano:**

- Iniciativas de Francisco:
    - Llevar la prueba en GitHub desde el principio: Issue con las comprobaciones, etiquetas y un Project público. El Project es público para facilitar el acceso al revisor: [Holdpoint](https://github.com/users/FranciscoDeLaPuente/projects/2).
    - Pedir un documento de cierre con pruebas adicionales en lugar de dar la prueba por cerrada tras la comprobación 5.
    - Hacer la prueba en vibe coding y sin BMAD, para que no hubiera ceremonia (decidido al planificar).
- Propuestas de Claude en claude.ai que revisó y aceptó:
    - El prompt de la sesión: comprobar la API real del SDK antes de escribir código, dos herramientas en el servidor de ejemplo, prueba mínima sin base de datos, panel, tests ni Docker, y probar desde una sesión de Claude Code aparte.
    - Los hitos por entrega.
    - Las pruebas P1 a P3, con un límite de una hora.
- Decisiones tomadas durante la sesión, con su porqué:
    - Fijar la prueba de concepto el 24-25 de noviembre en toda la documentación: es lo primero que hay que hacer, porque es el estudio de viabilidad y determina la continuidad del proyecto.
    - Copiar las reglas de «Alcance y calendario» a `CLAUDE.md`: el alcance y el calendario son críticos en este proyecto. El calendario es la primera prioridad y, si corre riesgo, se recorta el alcance. Debe tenerse siempre presente.
    - Fijar los modelos en las skills propias o al abrir la sesión: economía de tokens, sin usar modelos más complejos de lo necesario. Es normal que el modelo de la sesión se quede sin cambiar por olvido, y fijarlo en las skills garantiza un uso racional.

**Commits:**

- `poc/pasarela` (reescritos para añadir `Refs #1`): `32a4032` pasarela que reenvía las llamadas; `6193c7c` comprobaciones 1, 2 y 3; `0ed7fda` bloqueo de `borrar_tarea`; `16ba7ea` tiempo de espera de Claude Code; `0e79b51` progreso y capacidades del cliente; `78c692c` resultados de P1 a P3; `5d2b4d8` integración de `main`.
- `main`: `32fee00` reglas de `CLAUDE.md`; `65385a4` plan y visión; `b452263` `docs/entrada-bmad.md`.

### 2026-11-26 y 27 · Sesión 3: brief y PRD con BMAD

**Qué se hizo:** antes de empezar, un hook `pre-commit` y una regla en el `PreToolUse` que impiden los commits directos en `main`. Después, el brief con `bmad-product-brief`, partiendo de `docs/entrada-bmad.md` y la visión: problema, solución, diferenciación frente a siete alternativas reales buscadas en la web (arbit, McpVanguard, Docker MCP Gateway, Permit, TrueFoundry, Consul y los permisos de Claude Code), usuarios, criterios de éxito, alcance y visión. Y el PRD con `bmad-prd`: cuatro recorridos de usuario, glosario, 23 requisitos funcionales en ocho funcionalidades, cinco no funcionales, métricas con contramétricas, orden de recorte, líneas futuras y cuatro preguntas abiertas para la arquitectura. El cierre de cada documento pasó por revisiones en subagentes aislados (contraste con las entradas, lista de calidad de BMAD y pulido de estructura y redacción), y se aplicaron sus hallazgos con el visto bueno de Francisco.

**Herramienta y modelos:** Claude Code (CLI) en WSL con BMAD 6.12.4. Claude Opus 5.5 en la sesión (129 respuestas) y en seis subagentes de revisión; Claude Sonnet 5.5 en las 8 primeras respuestas, hasta cambiar de modelo con `/model`, y en el subagente de búsqueda de alternativas.

**Prompts clave:**

1. «1. En mi opinion la diferencia la marca la ligereza del proyecto. Conbinado con que es libre y de código abierto. La combinación de la revisión humana, el revisor de intención con LLM, y el sistema de politicas ofrece control seguridad y agilidad. No conozco bien los productos del mercado. Delego en ti que los revises y compares con nuestra oferta. […]» → Búsqueda de alternativas en un subagente y la sección «Qué lo diferencia» del brief: ninguna pieza es nueva por separado; lo distintivo es integrarlas en un producto abierto y ligero.
2. «en el último punto ¿podriamos encajar distribuir harness a los agentes? […] ¿es tecnicamente posible?» y, poco después, «tengo una duda, lo de la "distribución de arnes" ahora que lo veo no me gusta tanto. parece un añadido poco integrado. tengo la sensación de que nos desvia del objetivo real» → La idea entró en la visión del brief y se retiró: trata de configurar al agente, no de controlar lo que hace.
3. «no entiendo la limitacion de un equipo de desarrollo ¿de donde viene ese limite?» → El agente reconoció que el límite de «un solo equipo» lo había deducido él. El PRD pasó a decir el límite real: sin aislamiento entre equipos o empresas.
4. «me gusta 1, pero eso nos lleva a un sistema de registro» (sobre identificar a cada agente con una credencial) y «los agentes ahora usaran un token y en el futuro se gestionaran desde el panel» → FR-10: agentes definidos en la configuración, sin pantalla de alta, y su gestión desde el panel como línea futura.

**Criterio humano:**

- Bloquear los commits directos en `main`: «red de seguridad, costumbre, disciplina». Aunque trabaje una sola persona, las ramas separan el trabajo y permiten llevar dos áreas a la vez sin mezclar el código. También son una red de seguridad frente a los agentes: no sería la primera vez que hay que tirar el trabajo por una deriva caótica, y no mezclarlo con la rama principal hasta estar seguro es lo mejor en todos los sentidos.
- Diferenciación: la ligereza y que sea libre y de código abierto; la comparación con el mercado se delegó en el agente.
- Lector del brief: además del tribunal, la comunidad open source. Todo proyecto abierto es candidato a ser mejorado y aprovechado por la comunidad; ese es el sentido del software libre.
- Retiró la «distribución del arnés» de la visión, que él mismo había propuesto, porque desviaba del objetivo real.
- Al leer el PRD detectó un límite que no venía de las fuentes (un solo equipo de desarrollo) y lo hizo corregir. También comprobó contra el brief que «las de solo lectura pasan directas» venía de la visión, lo que llevó a añadir en FR-7 que las anotaciones de MCP son pistas y no garantías.
- Quitó el límite de retardo de 100 ms: es un hándicap para un MVP y una decisión demasiado arbitraria. El retardo deseable es el menor posible, pero el soportable se sabrá más adelante.
- Eligió español con los textos preparados para traducir: dejar la base lista es barato; introducirla con el producto lanzado es caro y engorroso, y añadir idiomas después también es barato.
- No validó las líneas futuras que había añadido el agente (detectar cambios en las herramientas y exportar el registro): uno de los sentidos del MVP es que el propio cliente ayude a orientar la evolución del producto, y tenerlo todo decidido ocupa el backlog y restringe lo que el cliente demanda.
- Eligió tres roles fijos con usuarios de prueba, retener la llamada si no hay objetivo o si el supervisor falla, y una espera máxima de 5 minutos configurable.

**Commits:** `d993b5c` bloquea los commits directos en `main`; `a656e36` y `d0dfcce` anotan la decisión de seguir con Holdpoint; `f5db510` brief de producto y su anexo; `2d0d134` PRD y su anexo, en la rama `docs/brief-prd`.

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

**Prompt 1:** (sesión 3, brief con BMAD) «1. En mi opinion la diferencia la marca la ligereza del proyecto. Conbinado con que es libre y de código abierto. […] Delego en ti que los revises y compares con nuestra oferta. […]» → sección «Qué lo diferencia» del brief, con siete alternativas comparadas.

**Prompt 2:** (sesión 3) «tengo una duda, lo de la "distribución de arnes" ahora que lo veo no me gusta tanto. parece un añadido poco integrado. tengo la sensación de que nos desvia del objetivo real» → la visión del brief se queda en controlar lo que hacen los agentes.

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

**Prompt 1:** (sesión 3, PRD con BMAD) «los agentes ahora usaran un token y en el futuro se gestionaran desde el panel» → FR-10 del PRD: agentes con credencial fija en la configuración y su gestión desde el panel como línea futura.

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
