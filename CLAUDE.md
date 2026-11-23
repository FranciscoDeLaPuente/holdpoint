# Holdpoint

Holdpoint es una torre de control para agentes de IA: una pasarela MCP que aplica a cada llamada una política (permitir, bloquear o pedir aprobación), comprueba con un supervisor si encaja con la tarea declarada y lo registra todo para poder reproducir la sesión. Es el proyecto final (TFM) del curso AI4Devs de LIDR, de Francisco de la Puente.

- Visión de producto: [docs/vision/vision-producto.md](docs/vision/vision-producto.md). El alcance manda: [Alcance del MVP](docs/vision/vision-producto.md#alcance-del-mvp) (5 historias) y [Fuera de alcance del MVP](docs/vision/vision-producto.md#fuera-de-alcance-del-mvp). Lo que esté fuera de alcance no se diseña ni se implementa sin que Francisco lo pida.
- Plan de sesiones y decisiones: [docs/plan-arranque.md](docs/plan-arranque.md).

## Calendario

| Fecha | Hito |
| --- | --- |
| 24-25 nov | Prueba de concepto en `poc/pasarela` |
| 26 nov | Decisión: seguir con Holdpoint o cambiar de propuesta |
| 26 nov-2 dic | Documentación de la entrega 1 con BMAD |
| 3 dic | Rama `feature/entrega-1-fp` y Typeform |
| 4 dic | Fecha límite de la entrega 1 |

## Dónde vive cada cosa

| Ruta | Contenido |
| --- | --- |
| `README.md` | Ficha de la entrega (plantilla de LIDR). Se compone a partir de los artefactos de BMAD: los resume y enlaza, no los copia |
| `Prompts.md` | Registro del uso de la IA. Lo mantiene `/registro-ia` |
| `_bmad/` | Instalación de BMAD 6.12. No se edita a mano; la configuración propia va en `_bmad/custom/` |
| `_bmad-output/` | Artefactos de BMAD (brief, PRD, UX, arquitectura, épicas), en su estructura estándar |
| `docs/` | Solo lo que BMAD no genera: visión, plan, `entrada-bmad.md` y lo que falte de modelo de datos o API |
| `.claude/` | `settings.json`, hooks y skills (las propias y las de BMAD) |
| `.githooks/` | Convenciones de ramas y commits (`convenciones.py`) y hook `commit-msg` de git |
| `.registro-ia/` | Prompts en bruto. En `.gitignore`: nunca se sube |
| `poc/` | Prueba de concepto, solo en la rama `poc/pasarela` hasta el 4 de diciembre |

`src/`, `tests/` y `deploy/` llegan en la entrega 2; su reparto lo decide la arquitectura de BMAD.

## Reglas

- **`main` no lleva código hasta el 4 de diciembre**: solo documentación y la configuración del arnés (`.claude/`, `.githooks/`, `_bmad/`). El código de la prueba de concepto va en `poc/pasarela`, en `poc/`, y se fusiona después de la entrega 1.
- **Nunca se abre una pull request**, y menos contra el repo de LIDR. La entrega es una rama más el Typeform.
- **Nada de secretos** en el repo: solo `.env.example` con valores de prueba.
- **Todo en español**: documentos, commits, Issues y comentarios en el código.
- **BMAD no se usa en la prueba de concepto**, que se hace en vibe coding. BMAD empieza en la sesión 3 (brief y PRD), partiendo de `docs/entrada-bmad.md`.
- **Modelos**: Opus para razonar (brief, PRD, UX, arquitectura, revisión de código); Sonnet para generar código y tareas mecánicas. Se fija con `model:` en la cabecera de skills y subagentes.

## Ramas

Formato: `main`, `feature/entrega-N-fp` (la de LIDR) o `<tipo>/<slug-en-kebab-case>`.

- Tipos: `poc`, `feature`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`.
- Número de Issue opcional al principio del slug: `feature/12-registrar-servidor`, `fix/34-timeout-espera`, `docs/arquitectura`.

## Commits

Conventional Commits en español: `<tipo>(<ámbito opcional>): <descripción>`.

- Tipos: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`.
- Descripción en presente (`añade`, `corrige`), en minúscula y sin punto final. Asunto de 72 caracteres como máximo.
- `Refs #n` en el cuerpo cuando haya Issue.

**Cómo se hacen cumplir.** Las reglas están en un solo sitio, `.githooks/convenciones.py`:

- Hook `PreToolUse` de Claude Code: bloquea los `git checkout -b`, `git switch -c`, `git branch` y `git commit -m` que no cumplan.
- Hook `commit-msg` de git: valida todos los commits, también los manuales. Tras clonar hay que activarlo una vez con `git config core.hooksPath .githooks`.

## Registro de IA

- Cada prompt se captura solo (hook `UserPromptSubmit` → `.claude/hooks/registrar-prompt.sh` → `.registro-ia/AAAA-MM-DD.jsonl`).
- **Ejecuta `/registro-ia` al cerrar cada hito**: sesión 1, prueba de concepto, brief y PRD, UX, arquitectura, tickets y entrega. Si un hito se cierra sin haberla ejecutado, recuérdaselo a Francisco.
- `cleanupPeriodDays: 180` para conservar las transcripciones hasta la entrega final.

## Skills propias

- `/registro-ia [hito]`: actualiza `Prompts.md`.
- `/revision-adversarial [rama base]`: revisión hostil del diff de la rama, en contexto aislado con Opus. Solo informa.
- `/bmad-help`: punto de entrada a BMAD.
