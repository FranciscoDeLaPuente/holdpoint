---
titulo: "Cierre de la prueba de concepto de la pasarela"
proyecto: "Holdpoint (TFM AI4Devs, LIDR)"
autor: "Francisco de la Puente González"
fecha: 2026-11-24
rama: "poc/pasarela"
---

# Cierre de la prueba de concepto de la pasarela

La prueba de concepto no impide seguir con Holdpoint: las comprobaciones 1 a 4 están en verde y la 5 está medida. Antes de cerrarla quedan tres pruebas cortas que deciden cómo se diseña la espera de una llamada retenida. Este documento es la entrada de la sesión que las hace y cierra la prueba.

**Límite de tiempo: una hora para las tres pruebas.** Si alguna se complica, se anota «sin resolver» y se cierra igual. Vale lo de «Alcance y calendario» del plan de arranque.

## Estado

| # | Comprobación | Resultado |
| --- | --- | --- |
| 1 | Claude Code ve las herramientas a través de la pasarela | Verde |
| 2 | Una llamada atraviesa la pasarela y el resultado vuelve | Verde |
| 3 | La pasarela deja constancia de la llamada | Verde |
| 4 | Error propio «bloqueada por política» | Verde |
| 5 | Tiempo de espera de Claude Code | Medido: 60 s por defecto |

Entorno de las pruebas: .NET 10.0.404, `ModelContextProtocol.AspNetCore` 2.4.0, Claude Code 2.1.331 en modo `claude -p` con el modelo Haiku. El detalle está en `poc/README.md`.

## Hallazgos para la arquitectura

1. **La espera no puede ser una sola llamada abierta sin más.** Claude Code corta a los 60 s por defecto, y una aprobación humana suele tardar más. `MCP_TOOL_TIMEOUT` sube el límite, pero es configuración de cada usuario y no se puede dar por supuesta.
2. **La pasarela tiene su propio límite.** El `HttpClient` interno de `HttpClientTransport` corta a los 100 s si no se le pasa uno con `Timeout` infinito. El SDK 2.4.0 no documenta un tiempo de espera por petición en `McpClient`.
3. **La cancelación se propaga.** Cuando Claude Code corta, la cancelación llega a la pasarela y esta la pasa al servidor. La máquina de estados de la llamada retenida necesita el estado «cancelada por el agente», además de aprobada, rechazada y caducada.
4. **El error de política funciona sin instrucciones.** Con `IsError = true` y el texto «Bloqueada por política», el agente no reintenta, comprueba el estado y se lo explica al usuario. El mensaje puede llevar después el motivo y el identificador de la aprobación.
5. **`isError` llega como `null`, no como `false`,** cuando el servidor no lo marca. El registro de auditoría debe normalizarlo.

## Pruebas pendientes

Se hacen en la rama `poc/pasarela`, con los mismos dos servicios y el parámetro `segundos` de `listar_tareas`. Cada resultado se añade a `poc/README.md` y al Issue de la prueba de concepto.

### P1. ¿Las notificaciones de progreso reinician el límite de 60 s?

Es la prueba que más pesa: si funciona, la pasarela puede mantener abierta la llamada retenida sin que el usuario toque su configuración.

1. Registrar en la pasarela si el `tools/call` de Claude Code trae `_meta.progressToken`. Sin ese token, el protocolo no permite enviar progreso: el resultado es «no» y se pasa a P2.
2. Si lo trae, que la pasarela envíe `notifications/progress` cada 10-15 s mientras espera. Comprobar en el SDK 2.4.0 cómo se envían desde un manejador; no inventar la API.
3. Probar `listar_tareas` con `segundos = 120` y `MCP_TOOL_TIMEOUT` sin definir.

Resultado: pasa (el límite se reinicia), no pasa (corta a los 60 s), o no aplica (no hay token).

### P2. ¿Claude Code soporta Tasks de MCP?

Solo comprobarlo, no implementarlo. Registrar en la pasarela las capacidades que declara el cliente en `initialize` y anotar si incluye `tasks`. El SDK tiene la extensión `ModelContextProtocol.Extensions.Tasks` para llamadas largas con consulta de estado; esta prueba dice si el cliente podría usarla.

### P3. Uso interactivo

Una sesión de `claude` interactiva (sin `-p`) conectada a la pasarela: listar tareas e intentar borrar una. Anotar cómo se ve la herramienta bloqueada en la interfaz y si cambia algo respecto a `-p`. La demo de la entrega será interactiva.

## Qué decide cada resultado

No se decide aquí: estos son los caminos que la arquitectura de BMAD tiene que valorar con los datos.

| Si… | El camino natural es… |
| --- | --- |
| P1 pasa | Llamada abierta con progreso cada pocos segundos, con un tiempo máximo propio de Holdpoint y caducidad al llegar a él |
| P1 no pasa y P2 sí | Llamadas largas como tareas de MCP, con consulta de estado |
| Ni P1 ni P2 | Respuesta inmediata «pendiente de aprobación» con un identificador, y una herramienta de la pasarela para consultar el estado. Subir `MCP_TOOL_TIMEOUT` queda como opción documentada para esperas cortas |

En cualquier caso, el `HttpClient` de la pasarela va sin límite propio o con uno mayor que el de Holdpoint, y la cancelación del agente pasa la llamada a «cancelada por el agente».

## Cierre

1. **Pruebas P1 a P3** en `poc/pasarela`, con sus resultados en `poc/README.md`. Commit referenciando el Issue de la prueba de concepto.
2. **`/registro-ia`.** Antes de ejecutarlo, Francisco cuenta qué corrigió o reorientó durante la prueba. Que el agente comprobara la API en la documentación del paquete antes de escribir código fue una instrucción suya: es criterio humano y va en `Prompts.md`.
3. **`docs/entrada-bmad.md` en `main`,** sin código, con lo que pide el plan de arranque más:
    - la tabla de resultados y los hallazgos de este documento;
    - los resultados de P1 a P3 y los caminos para la espera;
    - los estados de la llamada retenida: pendiente, aprobada, rechazada, caducada y cancelada por el agente.
4. **Comentario en el Issue** con los resultados y la decisión, y cierre del Issue.
5. **Decisión de Francisco** sobre seguir con Holdpoint. Se puede adelantar al 25 de noviembre por la mañana, como permitía el plan; si es que sí, el brief y el PRD empiezan ese mismo día.
