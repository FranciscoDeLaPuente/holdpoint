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
| 5 | Tiempo de espera de Claude Code | Pendiente |

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
