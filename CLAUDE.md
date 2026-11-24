# Holdpoint

Holdpoint es una torre de control para agentes de IA: una pasarela MCP que aplica a cada llamada una política (permitir, bloquear o pedir aprobación), comprueba con un supervisor si encaja con la tarea declarada y lo registra todo para poder reproducir la sesión. Es el proyecto final (TFM) del curso AI4Devs de LIDR, de Francisco de la Puente.

- Visión de producto: [docs/vision/vision-producto.md](docs/vision/vision-producto.md), con el [Alcance del MVP](docs/vision/vision-producto.md#alcance-del-mvp) (5 historias) y lo [Fuera de alcance del MVP](docs/vision/vision-producto.md#fuera-de-alcance-del-mvp).
- Plan de sesiones y decisiones: [docs/plan-arranque.md](docs/plan-arranque.md).

## Alcance y calendario

El calendario es justo: hay siete días para documentar con BMAD, del 26 de noviembre al 2 de diciembre. BMAD tiende a ampliar el alcance buscando calidad, y eso acaba en una bola de nieve. Estas reglas valen para todas las sesiones:

| Fecha | Hito |
| --- | --- |
| 24-25 nov | Prueba de concepto en `poc/pasarela` |
| 26 nov | Decisión: seguir con Holdpoint o cambiar de propuesta |
| 26 nov-2 dic | Documentación de la entrega 1 con BMAD |
| 3 dic | Rama `feature/entrega-1-fp` y Typeform |
| 4 dic | Fecha límite de la entrega 1 |

1. **El alcance es el de la visión:** las cinco historias imprescindibles del MVP. Nada nuevo entra, ni se diseña ni se implementa, sin el visto bueno explícito de Francisco.
2. **Lo que BMAD proponga fuera de alcance va a una lista de líneas futuras** en el PRD, no a la UX, la arquitectura ni las épicas.
3. **Documentos proporcionados:** cada artefacto cubre solo lo que necesitan las cinco historias y la entrega 1. Mejor corto y coherente que completo.
4. **Las fechas mandan.** Si una sesión se alarga, se recorta profundidad o alcance, nunca la fecha de entrega.
5. **Sin extras por defecto:** en BMAD se elige el camino más ligero que produzca brief, PRD, UX, arquitectura e historias, y se dice que no a la elicitación avanzada, al party mode y a los pasos opcionales, salvo que Francisco los pida.

**Si hay riesgo, se recorta en este orden:**

1. Las deseables (freno automático por bucle y hook de Claude Code) quedan fuera del todo.
2. La UX se queda en un listado de pantallas con su contenido, sin maquetas.
3. La historia 5 se simplifica: un listado de la sesión en lugar de reproducción paso a paso.
4. La historia 2 se simplifica: políticas manuales, sin propuesta inicial según el riesgo de cada herramienta.
5. La aprobación en tiempo real (historia 3) y el supervisor (historia 4) no se recortan: son el núcleo y lo que diferencia el producto.

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
| `poc/` | Prueba de concepto de la pasarela (ver la primera regla de «Reglas») |

`src/`, `tests/` y `deploy/` llegan en la entrega 2; su reparto lo decide la arquitectura de BMAD.

## Reglas

- **`main` no lleva código hasta el 4 de diciembre**: solo documentación (`docs/`, `_bmad-output/`, `README.md`, `Prompts.md`) y la configuración del arnés (`.claude/`, `.githooks/`, `_bmad/`). El código de la prueba de concepto va en `poc/pasarela`, en `poc/`, y se fusiona después de la entrega 1.
- **Nunca se abre una pull request**, y menos contra el repo de LIDR. La entrega es una rama más el Typeform.
- **Nada de secretos** en el repo: solo `.env.example` con valores de prueba.
- **Todo en español**: documentos, commits, Issues y comentarios en el código.
- **BMAD no se usa en la prueba de concepto**, que se hace en vibe coding. BMAD empieza en la sesión 3 (brief y PRD), partiendo de `docs/entrada-bmad.md`.
- **Modelos**: Opus para razonar (brief, PRD, UX, arquitectura, revisión de código); Sonnet para generar código y tareas mecánicas. En las skills y subagentes propios se fija con `model:` en la cabecera. Las skills de BMAD (`bmad-*`) no se editan, así que su modelo se elige al abrir la sesión (`/model`).
- **Seguimiento en GitHub**: un Issue por trabajo, con las etiquetas `poc`, `backend`, `frontend` y `bd`, y los hitos «Entrega 1», «Entrega 2» y «Entrega final». La prueba de concepto es el Issue #1 y todos los commits de `poc/pasarela` llevan `Refs #1`. Desde la entrega 2 habrá un Project de GitHub mínimo y público; BMAD manda sobre el estado de las historias y el tablero solo lo refleja.

## Ramas

Formato: `main`, `feature/entrega-N-fp` (la de LIDR) o `<tipo>/<slug-en-kebab-case>`, con el número de Issue opcional al principio del slug: `feature/12-registrar-servidor`, `fix/34-timeout-espera`, `docs/arquitectura`. Los tipos permitidos están en `.githooks/convenciones.py`.

## Commits

Conventional Commits: `<tipo>(<ámbito opcional>): <descripción>`.

- Descripción en presente (`añade`, `corrige`), en minúscula y sin punto final. Los tipos y el límite del asunto (72 caracteres) están en `.githooks/convenciones.py`.
- `Refs #n` en el cuerpo cuando haya Issue.

**Cómo se hacen cumplir.** Las reglas están en un solo sitio, `.githooks/convenciones.py`; este fichero no las copia, para que no se desincronicen:

- Hook `PreToolUse` de Claude Code: bloquea los `git checkout -b`, `git switch -c`, `git branch` y `git commit -m` que no cumplan.
- Hook `commit-msg` de git: valida todos los commits, también los manuales. Tras clonar hay que activarlo una vez con `git config core.hooksPath .githooks`.

## Registro de IA

- Cada prompt se captura solo (hook `UserPromptSubmit` → `.claude/hooks/registrar-prompt.sh` → `.registro-ia/AAAA-MM-DD.jsonl`).
- **Ejecuta `/registro-ia` al cerrar cada hito**: sesión 1, prueba de concepto, brief y PRD, UX, arquitectura, tickets y entrega. Si un hito se cierra sin haberla ejecutado, recuérdaselo a Francisco.
- `cleanupPeriodDays: 180` para conservar las transcripciones hasta la entrega final.

## Skills

- Propias: `/registro-ia [hito]` actualiza `Prompts.md`; `/revision-adversarial [rama base]` hace una revisión hostil del diff de la rama, en contexto aislado con Opus, y solo informa.
- Las de BMAD empiezan por `bmad-`. El punto de entrada es `/bmad-help`.
