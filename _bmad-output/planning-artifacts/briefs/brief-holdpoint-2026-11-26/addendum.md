---
title: "Anexo del brief: Holdpoint"
created: 2026-11-26
updated: 2026-11-26
---

# Anexo del brief: Holdpoint

Detalle para el PRD y la arquitectura que no cabe en el brief. La prueba de concepto, los caminos de espera y los estados resumen la sección 4 de [docs/entrada-bmad.md](../../../../docs/entrada-bmad.md). Los principios vienen de la visión y las alternativas, de una búsqueda propia.

## Resultado de la prueba de concepto

Rama `poc/pasarela` (Issue #1), 24 de noviembre de 2026, con .NET 10.0.404, `ModelContextProtocol.AspNetCore` 2.4.0 y Claude Code 2.1.331 con Haiku. Servidor de ejemplo con `listar_tareas` (solo lectura) y `borrar_tarea` (destructiva).

| # | Comprobación | Resultado |
| --- | --- | --- |
| 1 | Claude Code ve las herramientas a través de la pasarela | Verde |
| 2 | Una llamada atraviesa la pasarela y el resultado vuelve | Verde |
| 3 | La pasarela deja constancia de la llamada | Verde (consola) |
| 4 | Error propio «bloqueada por política» | Verde |
| 5 | Tiempo de espera de Claude Code | 60 s por defecto |

**Hallazgos que condicionan el diseño:**

- El proxy cabe en dos manejadores del SDK (`WithListToolsHandler`, `WithCallToolHandler`) y un `McpClient` hacia el servidor real.
- Claude Code corta a los 60 s (`MCP_TOOL_TIMEOUT` lo cambia, pero es configuración de cada usuario). Las notificaciones de progreso cada 10 s reinician ese límite: probado hasta 300 s.
- El `Message` del progreso se ve en la interfaz de Claude Code y puede explicar por qué espera la llamada.
- En interactivo, Claude Code pasa a segundo plano las llamadas de más de 120 s. La llamada en segundo plano no sobrevive al cierre de la sesión.
- Claude Code declara la extensión de Tasks de MCP; no se probó.
- El `HttpClient` interno del transporte corta a los 100 s salvo que se configure sin límite.
- La cancelación del agente se propaga hasta el servidor.
- Con `IsError = true` y un texto de motivo, el agente no reintenta y se lo explica al usuario.
- `isError` llega como `null` cuando el servidor no lo marca: la auditoría debe normalizarlo.

**Lo que no valida:** el supervisor, la concurrencia, la persistencia, la declaración del objetivo con una herramienta de la pasarela, otros agentes y modelos, y el modo de permisos por defecto de Claude Code.

## Caminos para la espera de una llamada retenida

Se deciden en la arquitectura.

| Camino | Qué exige | Riesgo |
| --- | --- | --- |
| A. Llamada abierta con progreso periódico y tiempo máximo propio de Holdpoint | Que el cliente mande `progressToken` (probado con Claude Code) | Un cliente que no mande `progressToken` vuelve al límite de 60 s |
| B. Extensión de Tasks de MCP | La extensión de Tasks en la pasarela | Sin probar |
| C. Respuesta inmediata «pendiente» con identificador y herramienta de consulta | Que el agente consulte | Depende del agente |

En los tres caminos, el `HttpClient` de la pasarela va sin límite propio, o con uno mayor que el máximo de Holdpoint.

### Estados de la llamada retenida

Pendiente, aprobada, rechazada, caducada y cancelada por el agente.

## Principios de diseño heredados de la visión

- Herramienta sin anotar: pide aprobación hasta que el administrador la clasifica. Basta con clasificarla una vez.
- El supervisor funciona en modo simulado o con Ollama, para no depender de claves de API.
- Claude Code se entrega a los desarrolladores con configuración gestionada (`managed-settings.json`, `managedMcpServers` y `allowedMcpServers` con `allowManagedMcpServersOnly`). En el MVP solo se documenta con un fichero de ejemplo.
- Multiplataforma: docker-compose en Linux y en Windows con Docker Desktop.
- Stack previsto: .NET 10 con el SDK oficial de MCP para C#, React con Vite, PostgreSQL y SignalR.

## Roles en el MVP

Administrador y responsable pueden ser la misma persona o distintas. Criterio de Francisco: un único usuario es aceptable en el MVP; separar los roles solo si cuesta poco. Lo decide el PRD.

## Alternativas revisadas

Búsqueda en la web del 26 de noviembre de 2026. «nv»: no verificado en una fuente. Antes de afirmar algo marcado «nv» hay que comprobarlo en el repositorio o la documentación del producto.

| Alternativa | Abierto | Política por herramienta | Aprobación humana | Supervisor LLM | Auditoría | Despliegue |
| --- | --- | --- | --- | --- | --- | --- |
| [arbit](https://docs.rs/crate/arbit/0.17.0) | Sí, MIT | Sí: permitir/denegar con patrones, `approval_required`, límites | Solo por API REST, con 60 s y rechazo al caducar; el panel solo muestra la auditoría | No descrito | Sí (SQLite, webhook); reproducción no descrita | Ligero: Docker, docker-compose, Helm |
| [McpVanguard](https://pypi.org/project/mcp-vanguard/) | Sí, MIT | Reglas deterministas; nv si son por herramienta | No descrita | Opcional (Ollama, OpenAI); no consta que compare con un objetivo de sesión | Logs JSON y recibos; reproducción no descrita | `pip install` |
| [Docker MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | Sí, MIT (nv) | Filtrado e interceptores; políticas avanzadas de pago | No descrita | No descrito | Logs y trazas | Ligero (contenedores) |
| [Permit MCP Gateway](https://docs.permit.io/permit-mcp-gateway/human-in-the-loop) | No, comercial | Sí | Sí: bandeja, email o Slack, 5 min; solo plan Enterprise | nv | Historial de aprobaciones | SaaS |
| [TrueFoundry AI Gateway](https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval) | No, comercial | Sí | Sí, con caducidad | nv | nv | SaaS o empresa |
| [Consul (HashiCorp)](https://developer.hashicorp.com/consul/docs/agentic-mesh/mcp-gateway) | No, comercial | Sí | Marca las llamadas; la aprobación la resuelve la aplicación | nv | nv | Pesado (malla de servicios) |
| [Permisos de Claude Code](https://code.claude.com/docs/en/permissions) | No | Sí: permitir, preguntar o denegar por herramienta | En el terminal, no en un panel | Modo auto con clasificador; nv si usa un objetivo declarado | Transcripciones locales | Nada que desplegar, pero solo protege a ese cliente |

**Conclusión:** el parecido más directo es arbit. Lo que suma Holdpoint es la bandeja web en un producto abierto, el supervisor contra el objetivo declarado y la reproducción de la sesión, todo en un despliegue ligero. «No descrito» no equivale a «no existe».
