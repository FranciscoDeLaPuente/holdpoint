---
name: registro-ia
description: Redacta la entrada de Prompts.md (registro del uso de la IA en el TFM) a partir de los prompts capturados en .registro-ia/, los modelos de las transcripciones de Claude Code y el git log. Úsala al cerrar cada hito (sesión 1, prueba de concepto, brief y PRD, UX, arquitectura, tickets y entrega) o cuando Francisco pida actualizar el registro de IA.
argument-hint: "[hito] [notas o contexto adicional]"
model: sonnet
---

# Registro de IA

Mantienes `Prompts.md`, el registro del uso de la IA que pide la entrega del TFM (lección 1 de AI4Devs). Escribes en español, con frases claras y sin relleno. Nunca inventas lo que no está en las fuentes; lo que falte, se lo preguntas a Francisco.

## Entrada

- `$ARGUMENTS`: nombre del hito y, opcionalmente, notas o contexto extra (por ejemplo, trabajo hecho fuera de Claude Code, en claude.ai). Si no viene el hito, dedúcelo de la rama, el git log y `docs/plan-arranque.md` («Siguientes sesiones») y confírmalo con Francisco.

## Pasos

1. **Periodo.** Lee `.registro-ia/ultima-ejecucion` (una fecha ISO 8601). Si no existe, el periodo empieza en el primer prompt capturado.

2. **Prompts capturados.** Lee los `.registro-ia/AAAA-MM-DD.jsonl` del periodo. Cada línea es `{fecha, rama, sesion, transcripcion, prompt}`. Descarta los prompts triviales («sí», «continúa», aprobaciones) salvo que sean una corrección.

3. **Modelos reales.** Para cada `transcripcion` distinta (si no viene, busca `~/.claude/projects/<ruta del repo con / y . cambiados por ->/<sesion>.jsonl`), cuenta los modelos de las respuestas:

   ```bash
   jq -r 'select(.type=="assistant") | .message.model // empty' "$transcripcion" | sort | uniq -c
   ```

   En las mismas transcripciones, localiza los momentos de criterio humano: herramientas rechazadas (`tool_result` con «doesn't want to proceed» o «rejected»), respuestas a `AskUserQuestion` y prompts que corrigen o descartan algo («no», «mejor», «en lugar de», «cambia»).

4. **Cambios.** `git log --since=<inicio del periodo> --date=iso --format='%h %ad %s'` en todas las ramas (`--all`).

5. **Criterio humano.** Propón a Francisco, con `AskUserQuestion` o en una lista breve, los momentos del paso 3 en que corrigió, rechazó o eligió algo, y pregúntale el porqué de cada uno. Usa su respuesta textual, resumida pero sin cambiar el sentido. Si no contesta a alguno, no lo incluyas.

6. **Escribe en `Prompts.md`.** Respeta la estructura de la plantilla de LIDR (el índice y las secciones 1 a 7 con «Prompt 1/2/3») y no borres sus secciones. Mantén dos partes:

   - **Al principio, `## Uso de la IA en el proyecto`**, que se actualiza (no se duplica) en cada ejecución:
     - Herramientas (Claude Code CLI, claude.ai…) y para qué se usó cada una.
     - Modelos y para qué tareas, con los datos del paso 3.
     - Contexto avanzado: `CLAUDE.md`, skills (`/registro-ia`, `/revision-adversarial`, las de BMAD), hooks (captura de prompts, validación de ramas y commits), BMAD 6.12.
     - Fases del ciclo de vida cubiertas hasta ahora (análisis, diseño, implementación, pruebas, despliegue, mantenimiento): hacen falta al menos 4 de 6.
   - **`## Registro por hitos`**, justo después, con una entrada nueva por ejecución, la más reciente al final:

     ```markdown
     ### AAAA-MM-DD · <hito>
     **Qué se hizo:** …
     **Herramienta y modelos:** …
     **Prompts clave:** de 3 a 5, citados textualmente (recortados con «[…]» si son largos), cada uno con una línea sobre qué produjo.
     **Criterio humano:** qué se corrigió, rechazó o decidió y por qué (paso 5).
     **Commits:** hashes cortos y asuntos relevantes.
     ```

   - Si algún prompt clave corresponde a una sección de la plantilla (arquitectura, modelo de datos, API, historias, tickets…), cópialo además en el primer hueco «Prompt N» libre de esa sección, como máximo 3 por sección.

7. **Marca.** Escribe en `.registro-ia/ultima-ejecucion` la fecha ISO 8601 del último prompt incluido.

8. **Resumen.** Di a Francisco qué entrada has añadido y qué preguntas quedaron sin respuesta. No hagas commit: eso va en el commit del hito.

## Reglas

- Nada de secretos, tokens ni rutas personales fuera del repo en `Prompts.md`.
- El registro en bruto (`.registro-ia/`) no se sube nunca al repo.
- No reescribas entradas de hitos anteriores salvo que Francisco lo pida.
