---
titulo: "Entrada de BMAD: Holdpoint, torre de control para agentes de IA"
proyecto: "Holdpoint (TFM AI4Devs, LIDR)"
autor: "Francisco de la Puente González"
fecha: 2026-11-24
estado: "Entrada del brief y el PRD. Prueba de concepto terminada; el 26 de noviembre de 2026 se decidió seguir con Holdpoint"
---

# Entrada de BMAD: Holdpoint

Este documento es la entrada del brief y el PRD (sesión 3). **El 26 de noviembre de 2026 se decidió seguir con Holdpoint.** Resume la visión, lo que enseñó la prueba de concepto y lo que exige la entrega 1. Es corto a propósito: manda [la visión de producto](vision/vision-producto.md) y, en el calendario, [el plan](plan-arranque.md).

## 1. Visión en breve

Holdpoint es una pasarela entre los agentes de IA y las herramientas que usan por MCP. Para cada llamada aplica una política (permitir, bloquear o pedir aprobación), comprueba con un supervisor si encaja con la tarea declarada y lo registra todo para poder reproducir la sesión. Hoy el acceso de un agente a un servidor MCP es todo o nada, los permisos de clientes como Claude Code son locales y no hay registro común de qué hizo cada agente ni quién lo autorizó.

| Usuario | Qué hace |
| --- | --- |
| Administrador (tech lead) | Registra servidores MCP y define la política de cada herramienta |
| Responsable | Aprueba o rechaza en tiempo real las llamadas retenidas |
| Auditor | Reproduce sesiones: qué hizo cada agente y quién lo autorizó |
| Agente de IA | Llama a las herramientas a través de la pasarela, sin ver las credenciales reales |

Stack previsto: .NET 10 con el SDK oficial de MCP para C#, React con Vite, PostgreSQL y SignalR.

## 2. Alcance del MVP

Las cinco historias imprescindibles, cada una de extremo a extremo (panel, API, pasarela y base de datos):

1. **Registrar un servidor.** El administrador registra un servidor MCP detrás de la pasarela y ve sus herramientas.
2. **Políticas.** El administrador decide por herramienta si se permite, se bloquea o pide aprobación; la política inicial se propone según el riesgo que declara cada herramienta.
3. **Aprobación en tiempo real.** El responsable aprueba o rechaza las llamadas retenidas viendo sus argumentos. Si nadie decide a tiempo, caduca. Al aprobar puede permitir esa herramienta durante el resto de la sesión.
4. **Supervisor de intención.** El responsable sabe si cada llamada encaja con el objetivo declarado de la sesión. El supervisor evalúa las llamadas que no son de solo lectura; si una no encaja, se retiene aunque la política la permita.
5. **Reproducir una sesión.** El auditor recorre una sesión paso a paso: qué pidió el agente, qué se decidió, quién y qué devolvió la herramienta.

**Deseables, no obligatorias:** freno automático si un agente entra en bucle, y un hook de Claude Code que envíe también las herramientas propias del agente a la misma bandeja.

**Fuera de alcance:** transporte stdio (solo HTTP), recursos y prompts de MCP (solo herramientas), más de un servidor real (uno de ejemplo, un gestor de tareas), OAuth (credenciales fijas de prueba), inspección de lo que devuelven las herramientas, credenciales de usuario por agente, torre local, multiempresa, nube y alta disponibilidad. La inspección de lo que devuelven las herramientas y las credenciales de usuario son líneas futuras; el detalle está en la visión.

## 3. Reglas de alcance y calendario

Valen para todas las sesiones de BMAD. Hay siete días para documentar (26 nov-2 dic) y BMAD tiende a ampliar el alcance.

1. **El alcance es el de la visión:** las cinco historias. Nada nuevo entra sin el visto bueno explícito de Francisco.
2. **Lo que BMAD proponga fuera de alcance** va a una lista de líneas futuras en el PRD, no a la UX, la arquitectura ni las épicas.
3. **Documentos proporcionados:** cada artefacto cubre solo lo que necesitan las cinco historias y la entrega 1.
4. **Las fechas mandan.** Se recorta profundidad o alcance, nunca la fecha de entrega.
5. **Sin extras por defecto:** el camino más ligero que produzca brief, PRD, UX, arquitectura e historias, y no a la elicitación avanzada, al party mode y a los pasos opcionales, salvo que Francisco los pida.

**Orden de recorte si hay riesgo:** (1) las deseables fuera del todo; (2) la UX como listado de pantallas con su contenido, sin maquetas; (3) la historia 5 como listado de la sesión, no reproducción paso a paso; (4) la historia 2 con políticas manuales, sin propuesta inicial por riesgo; (5) la historia 3 y el supervisor (historia 4) no se recortan.

## 4. Resultado de la prueba de concepto

Se hizo el 24 de noviembre de 2026 en la rama `poc/pasarela` (Issue #1), con .NET 10.0.404, `ModelContextProtocol.AspNetCore` 2.4.0 y Claude Code 2.1.331 con el modelo Haiku. Un servidor de ejemplo con dos herramientas (`listar_tareas`, solo lectura, y `borrar_tarea`, destructiva) detrás de una pasarela que hace de servidor y de cliente MCP por HTTP.

| # | Comprobación | Resultado |
| --- | --- | --- |
| 1 | Claude Code ve las herramientas a través de la pasarela | Verde |
| 2 | Una llamada atraviesa la pasarela y el resultado vuelve | Verde |
| 3 | La pasarela deja constancia de la llamada | Verde (consola) |
| 4 | Error propio «bloqueada por política» | Verde |
| 5 | Tiempo de espera de Claude Code | 60 s por defecto |
| P1 | Las notificaciones de progreso reinician el límite de 60 s | Sí |
| P2 | Claude Code declara soporte de Tasks de MCP | Lo declara; no probado |
| P3 | Uso interactivo | Funciona; la interfaz añade matices |

### Hallazgos para la arquitectura

1. **El SDK sirve para la pasarela.** Un proxy completo cabe en dos manejadores (`WithListToolsHandler`, `WithCallToolHandler`) más un `McpClient` hacia el servidor real. Todo lo usado existe en 2.4.0; se comprobó en la documentación XML del paquete antes de escribir código.
2. **Claude Code corta a los 60 s por defecto,** tanto en `claude -p` como en interactivo. Se sube con `MCP_TOOL_TIMEOUT`, que es configuración de cada usuario y no se puede dar por supuesta.
3. **El progreso reinicia ese límite (P1).** Claude Code manda un `progressToken` en cada `tools/call`; si la pasarela envía `notifications/progress` cada 10 s, la llamada sigue viva. Probado con 120 s y 300 s, sin tope hasta ahí. La API es `McpSession.NotifyProgressAsync`. Con una llamada de 120 s sin progreso se cancela a los 60,0 s, y con progreso pasa.
4. **El `Message` del progreso se ve en la interfaz** («Calling pasarela · 42s… esperando»), así que puede explicar por qué espera la llamada.
5. **Claude Code interactivo pasa a segundo plano las llamadas de más de 120 s:** devuelve un aviso («moved to the background as task …»), el agente sigue y se le notifica el resultado. Es comportamiento de la interfaz, no del protocolo (la pasarela ve una sola llamada). No sobrevive a cerrar la sesión.
6. **Claude Code declara la extensión de Tasks (P2)** (`io.modelcontextprotocol/tasks`) además de `roots` y `elicitation`. Existe un paquete aparte, `ModelContextProtocol.Extensions.Tasks` 2.4.0. No se instaló ni se probó.
7. **La pasarela tiene su propio límite:** el `HttpClient` interno de `HttpClientTransport` corta a los 100 s salvo que se le pase uno con `Timeout` infinito.
8. **La cancelación se propaga.** Cuando Claude Code corta, la pasarela recibe la cancelación y la pasa al servidor.
9. **El error de política funciona sin instrucciones.** Con `IsError = true` y el texto «Bloqueada por política», el agente no reintenta, comprueba el estado y se lo explica al usuario. En interactivo la vista normal solo muestra «1 failed»; el texto está en la vista ampliada (`ctrl+o`).
10. **`isError` llega como `null`, no `false`,** cuando el servidor no lo marca. El registro de auditoría debe normalizarlo.

### Qué no valida la prueba

El supervisor, la concurrencia, la persistencia, el objetivo declarado por una herramienta de la pasarela (principio 5 de la visión), otros agentes distintos de Claude Code, otros modelos y el modo de permisos por defecto de Claude Code (se probó en modo `-p` y en modo auto).

### Caminos para la espera de una llamada retenida

Se valoran en la arquitectura; estos son los que los datos permiten.

| Camino | Qué exige | Riesgo |
| --- | --- | --- |
| A. Llamada abierta con progreso cada pocos segundos, con un tiempo máximo propio de Holdpoint y caducidad al llegar a él | Que el cliente mande `progressToken`. Probado con Claude Code | Un cliente que no lo mande vuelve al límite de 60 s |
| B. Llamadas largas como tareas de MCP | La extensión de Tasks en la pasarela. Claude Code la declara | Sin probar |
| C. Respuesta inmediata «pendiente de aprobación» con un identificador y una herramienta de la pasarela para consultar el estado. `MCP_TOOL_TIMEOUT` queda como opción documentada | Que el agente consulte | Depende de que el agente lo haga bien |

Con cualquiera de los tres, el `HttpClient` de la pasarela va sin límite propio, o con uno mayor que el máximo de Holdpoint, y la cancelación del agente pasa la llamada a «cancelada por el agente». El principio 3 de la visión («por ejemplo 60 segundos») ya no tiene por qué ser 60: con el camino A el máximo lo fija Holdpoint.

### Estados de la llamada retenida

Pendiente, aprobada, rechazada, caducada y **cancelada por el agente**. Los otros cuatro salen de la visión; el quinto, de que el cliente puede cortar mientras la llamada espera.

## 5. Lo que exige la entrega 1

Solo documentación, sin código, en la rama `feature/entrega-1-fp` (3 dic; fecha límite el 4 dic), más el Typeform. Sin pull request.

- **`README.md`:** ficha, descripción, arquitectura, **modelo de datos**, **API**, historias de usuario, tickets de trabajo y stack. Sin textos de ejemplo de la plantilla.
- **`Prompts.md`:** herramientas, modelos, contexto avanzado, de 3 a 5 prompts clave y criterio humano.
- **Tickets en GitHub Issues,** etiquetados `backend`, `frontend` y `bd`, con una épica por historia imprescindible, desde el desglose de BMAD.
- **Coherencia** entre arquitectura, modelo de datos, API y tickets.
- **IA usada o prevista** en al menos 4 de las 6 fases del ciclo de vida: análisis, diseño, implementación, pruebas, despliegue y mantenimiento.
- Si el modelo de datos o la API no salen detallados de BMAD, se completan en `docs/`.

Para la entrega 2 se prevé que la primera funcionalidad de extremo a extremo sea la historia 1 (registrar un servidor), que aprovecha la conexión de la prueba de concepto.
