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

**Sin probar:** si las notificaciones de progreso (`notifications/progress`) de la pasarela reinician el contador de 60 s en Claude Code; el uso interactivo (no `-p`); y otros modelos o versiones de Claude Code.

## Decisión del 26 de noviembre

Las comprobaciones 1 a 4 están en verde y la 5 está medida, así que la prueba de concepto no impide seguir con la torre de control. La decisión es de Francisco.
