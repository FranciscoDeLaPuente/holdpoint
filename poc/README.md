# Prueba de concepto: pasarela MCP

Valida los supuestos de [Supuestos a validar](../docs/vision/vision-producto.md#supuestos-a-validar-la-prueba-de-concepto). Se hace en vibe coding, sin BMAD, y vive solo en la rama `poc/pasarela`.

## Qué hay

| Carpeta | Qué es | Puerto |
| --- | --- | --- |
| `servidor-ejemplo/` | Servidor MCP con `listar_tareas` (solo lectura) y `borrar_tarea` (destructiva) | 5100 |
| `pasarela/` | Servidor MCP para Claude Code y cliente del servidor de ejemplo; reenvía `tools/list` y `tools/call` | 5200 |

- .NET 10.0.404, instalado en `~/.dotnet` con `dotnet-install.sh` (no estaba en la máquina).
- SDK: `ModelContextProtocol.AspNetCore` **2.4.0** (arrastra `ModelContextProtocol` y `ModelContextProtocol.Core`). Los nombres se comprobaron con el XML de documentación del paquete instalado.
- API usada, toda existente en 2.4.0: `AddMcpServer().WithHttpTransport()`, `MapMcp`, `WithToolsFromAssembly`, `WithListToolsHandler`, `WithCallToolHandler`, `HttpClientTransport` / `HttpClientTransportOptions`, `McpClient.CreateAsync`, `ListToolsAsync`, `CallToolAsync(CallToolRequestParams)`.

## Cómo probarlo

```bash
cd poc/servidor-ejemplo && dotnet run   # terminal 1
cd poc/pasarela && dotnet run           # terminal 2
claude mcp add --transport http pasarela http://127.0.0.1:5200/mcp
```

## Resultados

| # | Comprobación | Resultado |
| --- | --- | --- |
| 1 | Claude Code ve las herramientas a través de la pasarela | ✅ Verde |
| 2 | Una llamada atraviesa la pasarela y el resultado vuelve | ✅ Verde |
| 3 | La pasarela deja constancia de la llamada | ✅ Verde |
| 4 | Error propio «bloqueada por política» | ✅ Verde |
| 5 | Tiempo de espera de Claude Code | ✅ Medido: **60 s** por defecto |
| P1 | Las notificaciones de progreso reinician el límite de 60 s | ✅ **Sí** |
| P2 | Claude Code declara soporte de Tasks de MCP | ✅ Lo declara (extensión `io.modelcontextprotocol/tasks`); no probado |
| P3 | Uso interactivo | ✅ Funciona igual; la interfaz añade matices |

### 1 y 2

Claude Code (`claude -p` con un `--mcp-config` temporal) se conecta a la pasarela (estado `connected`) y recibe `mcp__pasarela__borrar_tarea` y `mcp__pasarela__listar_tareas`. Al pedirle listar tareas, la llamada pasa por la pasarela, llega al servidor de ejemplo y devuelve las tres tareas. El reenvío se resuelve con dos manejadores (`WithListToolsHandler` y `WithCallToolHandler`).

### 3

La pasarela escribe en consola una línea por cada `tools/list`, `tools/call` (con nombre y argumentos) y resultado. Ejemplo real:

```
[pasarela] tools/call listar_tareas {}
[pasarela] resultado isError=
```

`isError` sale vacío cuando el servidor no lo marca (es `null`, no `false`). Solo consola, sin persistencia, como pide la comprobación.

### 4

La pasarela intercepta `borrar_tarea` y devuelve `CallToolResult { IsError = true }` con el texto «Bloqueada por política», sin llegar al servidor. En el log: `[pasarela] BLOQUEADA borrar_tarea`.

Claude Code (modelo Haiku, en `claude -p`) lo interpreta como un error de la herramienta: no reintenta, vuelve a listar las tareas para comprobar que no se borró nada y explica al usuario que hay una política que lo impide. Con el texto neutro se obtiene la misma conducta que con uno que indicaba «no reintentes; informa al usuario», así que el mensaje no necesita instrucciones. Para la entrega 2, el texto puede incluir el motivo y el identificador de la aprobación.

Sin probar aún: la reacción de otros modelos y el uso interactivo (no `-p`).

### 5

`listar_tareas` admite un parámetro `segundos` que retrasa la respuesta. Se prueba `claude -p` (Claude Code 2.1.331, modelo Haiku) contra la pasarela.

| Retardo | Configuración | Resultado |
| --- | --- | --- |
| 30 s | por defecto | ✅ Pasa (35 s en total) |
| 60 s | por defecto | ❌ «The operation timed out» (el servidor respondía justo en el límite) |
| 120 s | por defecto | ❌ «The operation timed out»; la sesión termina a los 65 s |
| 120 s | `MCP_TOOL_TIMEOUT=300000`, `HttpClient` de la pasarela con el tiempo por defecto | ❌ Falla a los 100,0 s |
| 120 s | `MCP_TOOL_TIMEOUT=300000` y `HttpClient.Timeout` infinito en la pasarela | ✅ Pasa (124 s en total) |

**Conclusiones para el diseño de la espera:**

- Claude Code corta a los **60 s** por defecto. En el log de la pasarela el manejador se cancela a los 60,008 s: llega la cancelación del cliente y la pasarela la propaga al servidor.
- El límite se sube con la variable de entorno `MCP_TOOL_TIMEOUT` (milisegundos) en el entorno de Claude Code. Es configuración del usuario, no de la pasarela: no se puede dar por supuesta.
- La pasarela tiene su propio límite: el `HttpClient` interno de `HttpClientTransport` corta a los 100 s si no se le pasa un `HttpClient` con `Timeout` infinito (se hace en `pasarela/Program.cs`). El SDK 2.4.0 no documenta un tiempo de espera por petición en `McpClient`.
- Una aprobación humana que tarde más de 60 s no se puede esperar con una sola llamada abierta, salvo que se amplíe `MCP_TOOL_TIMEOUT`. Hay que decidir en el diseño entre dos caminos: (a) documentar el aumento del límite en la configuración de Claude Code; (b) devolver pronto un resultado de «pendiente de aprobación» y que el agente vuelva a consultar. Conviene recoger los dos en la arquitectura.

**Pendiente de la sesión de cierre:** P1 (progreso), P2 (Tasks) y P3 (uso interactivo), más abajo.

## Pruebas de cierre (24 nov 2026)

Mismo entorno que la comprobación 5 (Claude Code 2.1.331, Haiku). La pasarela ahora registra las capacidades del cliente y el `progressToken`, y envía progreso cada `IntervaloProgreso` segundos (`dotnet run -- --IntervaloProgreso=10`; 0 = no enviar). `MCP_TOOL_TIMEOUT` sin definir en todas las pruebas (comprobado en el entorno y en los `settings.json`).

### API del SDK 2.4.0 usada

`McpServer.ClientCapabilities` y `ClientInfo`; `Params.ProgressToken` (`ProgressToken?`) y `Params.Meta`; `McpSession.NotifyProgressAsync(ProgressToken, ProgressNotificationValue, ...)`, con `ProgressNotificationValue` en el espacio de nombres `ModelContextProtocol`. `ModelContextProtocol.Extensions.Tasks` no viene en los tres paquetes instalados: es un paquete NuGet aparte (2.4.0) y no se instaló, porque P2 solo pide ver lo que declara el cliente.

### P1. Progreso: sí reinicia el límite

Claude Code envía `progressToken` en cada `tools/call` (valores 1, 2, 4, 5… dentro de `_meta`). La pasarela mandó una notificación cada 10 s.

| Retardo | Progreso | Resultado |
| --- | --- | --- |
| 120 s (`-p`) | sin progreso (control) | ❌ Cancelada por el cliente a los **60,0 s** |
| 120 s (`-p`) | cada 10 s | ✅ Pasa a los 120,0 s (12 notificaciones) |
| 300 s (`-p`) | cada 10 s | ✅ Pasa a los 300,0 s (29 notificaciones); no hay tope hasta ahí |

Sin probar: intervalos de progreso mayores de 10 s, esperas de más de 300 s y otras versiones de Claude Code.

### P2. Tasks: el cliente lo declara

En `initialize` Claude Code declara, entre otras, estas capacidades:

```json
{"roots":{"listChanged":true},"elicitation":{"form":{},"url":{}},"extensions":{"io.modelcontextprotocol/tasks":{}}}
```

Declara la extensión de Tasks (`io.modelcontextprotocol/tasks`), no una capacidad `tasks` propia. Declararla no demuestra que funcione con una herramienta de la pasarela: no se implementó ni se probó. El protocolo negociado es `2026-07-28`, y las capacidades y el cliente viajan también en el `_meta` de cada petición. Hay además `elicitation` (formularios y URL), que no estaba en el alcance de la prueba.

### P3. Uso interactivo

Sesión `claude` interactiva (con `tmux`, Haiku, modo auto activado) contra la pasarela.

- **Listar:** funciona. La vista normal dice «Called pasarela» y la ampliada (`ctrl+o`) muestra `pasarela - listar_tareas (MCP)` con el resultado.
- **Borrar (bloqueado):** la vista normal solo dice «Called pasarela 2 times · 1 failed». El texto `Error: Bloqueada por política` aparece solo en la vista ampliada. El agente lo cuenta como «una política del sistema» y no reintenta. En modo auto, el permiso de la herramienta lo concede el clasificador de Claude Code («Allowed by auto mode»); con el modo de permisos por defecto no se probó.
- **El progreso se ve:** durante la espera la interfaz muestra «Calling pasarela · 42s…» y debajo el `Message` de la notificación (`esperando`). Es la ocasión de mostrar al usuario por qué espera la llamada («pendiente de aprobación de …»).
- **A los 120 s Claude Code pasa la llamada a segundo plano:** devuelve «still running after 120s. It was moved to the background as task …», el agente sigue y la interfaz avisa al terminar («MCP task … completed»). La pasarela ve una sola `tools/call` que acaba a los 120,0 s, así que es un comportamiento de la interfaz y no el protocolo Tasks. No sobrevive a cerrar la sesión.
- **Sin progreso corta igual que en `-p`:** `segundos=100` sin notificaciones se cancela a los **59,7 s** y el agente informa de «timeout».

## Decisión del 26 de noviembre

Las comprobaciones 1 a 4 están en verde, la 5 está medida y las tres pruebas de cierre están hechas: la prueba de concepto no impide seguir con la torre de control. La decisión es de Francisco.
