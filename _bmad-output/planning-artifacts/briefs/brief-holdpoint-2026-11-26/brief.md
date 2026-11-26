---
title: "Brief de producto: Holdpoint"
status: final
created: 2026-11-26
updated: 2026-11-26
---

# Brief de producto: Holdpoint

> *Where AI agents wait for clearance.*

## Resumen

Holdpoint es una torre de control para agentes de IA. Se pone entre los agentes y las herramientas que usan por MCP, y decide sobre cada llamada: la deja pasar, la bloquea o la retiene hasta que una persona la apruebe. Además, un supervisor con un LLM comprueba si la llamada encaja con la tarea que el agente declaró al empezar, y todo queda registrado para poder reproducir la sesión.

Hoy el control es todo o nada: si el agente tiene un servidor MCP conectado, puede usar todas sus herramientas. Holdpoint lo convierte en una política por herramienta, con intervención humana solo cuando hace falta y un registro común de qué hizo cada agente y quién lo autorizó.

Es el proyecto final del curso AI4Devs de LIDR. No busca abrir una línea de negocio: el objetivo es desarrollar un proyecto real con IA, de principio a fin, que tenga sentido fuera del curso. Será libre, de código abierto y ligero: arranca con Docker Compose, sin cuentas externas.

## El problema

- **Acceso todo o nada.** Un agente con un servidor MCP conectado puede llamar a cualquiera de sus herramientas, también a las destructivas.
- **Permisos locales.** En clientes como Claude Code, cada desarrollador decide los permisos en su máquina y se los aprueba a sí mismo. El equipo no tiene una política común.
- **Sin rastro común.** No hay un registro compartido de qué llamó cada agente, con qué argumentos y quién lo autorizó.
- **Los errores se descubren tarde.** Un error de criterio del agente, como borrar lo que no debía, se ve cuando ya está hecho.

**Escenario.** Se pide a un agente «limpia los tickets duplicados del proyecto». Las búsquedas pasan solas. Cuando intenta borrar un ticket, la llamada queda retenida y el responsable ve en el panel qué ticket quiere borrar, junto con el veredicto del supervisor. Si la rechaza, el agente recibe el motivo («no es duplicado, es otro navegador») y ajusta su plan. Al terminar, la sesión entera se puede reproducir.

## La solución

Holdpoint es una pasarela MCP por HTTP con un panel web en tiempo real.

1. **Solo la pasarela tiene las llaves.** Tiene las credenciales de los servicios reales y es la única que llega a los servidores MCP, así que el agente no puede saltársela.
2. **La persona es la excepción.** Las herramientas de solo lectura pasan directas. Para el resto, la política propone un punto de partida según el riesgo que declara cada herramienta (anotaciones `readOnlyHint` y `destructiveHint` de MCP), y el administrador la ajusta.
3. **Supervisor de intención.** Al empezar la sesión, el agente declara su objetivo. El supervisor evalúa cada llamada que no es de solo lectura contra ese objetivo; si no encaja, la retiene aunque la política la permita.
4. **Aprobación en tiempo real.** Las llamadas retenidas aparecen en el panel con sus argumentos y el veredicto del supervisor. El responsable aprueba o rechaza, y, si nadie decide a tiempo, la llamada caduca y el agente recibe un error claro con el motivo. Al aprobar, puede permitir esa herramienta el resto de la sesión.
5. **Todo queda registrado, sin secretos.** Cada llamada, decisión y respuesta se guarda, con los argumentos sensibles ocultos, y el auditor puede recorrer la sesión entera.

La prueba de concepto (24 y 25 de noviembre) confirmó lo crítico: Claude Code usa las herramientas a través de la pasarela, entiende un bloqueo por política y aguanta una llamada retenida más de 60 s gracias a las notificaciones de progreso. [Detalle en el anexo](addendum.md).

## Qué lo diferencia

Ninguna pieza es nueva por separado: hay pasarelas abiertas con políticas y aprobación por API, productos de pago con bandeja de aprobaciones y permisos locales en clientes como Claude Code ([comparación en el anexo](addendum.md#alternativas-revisadas)). Lo que no aparece junto en ninguna alternativa revisada es lo que Holdpoint integra:

- **Aprobación en un panel web en tiempo real, en un producto abierto.** Las alternativas abiertas la ofrecen solo por API; las que tienen bandeja son de pago.
- **Un supervisor que compara cada llamada con el objetivo declarado de la sesión**, no solo con reglas o firmas fijas.
- **La reproducción de la sesión**: qué pidió el agente, qué se decidió y quién, y qué devolvió la herramienta.
- **Ligereza**: arranca con Docker Compose; supervisor simulado o con Ollama.

No es lo primero: es una integración ligera y abierta de controles que hoy están dispersos, para que un equipo pequeño gane control sin perder agilidad.

## A quién sirve

| Usuario | Qué necesita | Cómo sabe que funciona |
| --- | --- | --- |
| Administrador (tech lead) | Registrar servidores MCP y fijar la política de cada herramienta sin escribirla desde cero | Las herramientas aparecen con una política propuesta que solo tiene que revisar |
| Responsable | Decidir rápido sobre las llamadas que importan, con contexto | Ve qué pide el agente, con qué argumentos y si encaja con la tarea, y decide en segundos |
| Auditor | Saber qué hizo cada agente y quién lo autorizó | Recorre cualquier sesión de principio a fin |
| Agente de IA | Usar las herramientas sin ver credenciales y entender por qué se le detiene | Recibe resultados o errores con motivo, y ajusta su plan |

En un equipo pequeño, administrador y responsable suelen ser la misma persona, el tech lead ([roles en el anexo](addendum.md#roles-en-el-mvp)).

**La comunidad** puede arrancarlo en local, estudiarlo y adaptarlo a sus propios servidores MCP.

## Criterios de éxito

El MVP está terminado cuando, en la entrega final:

1. Un agente con guion fijo intenta borrar una tarea, la llamada queda retenida, se aprueba desde el panel y el agente recibe el resultado (prueba de extremo a extremo).
2. Una llamada directa al servidor MCP, sin pasar por la pasarela, falla (prueba de seguridad).
3. El supervisor marca como «no encaja» las llamadas contrarias al objetivo en un conjunto de casos de prueba.
4. Quien lo evalúa lo arranca con Docker Compose, datos de prueba y un `.env.example`, sin preguntar nada.
5. La sesión de la demo se reproduce entera desde el panel, y el panel muestra qué porcentaje de las llamadas necesitó aprobación humana.

## Alcance

**Dentro: cinco historias**, cada una de extremo a extremo (panel, API, pasarela y base de datos):

1. **Registrar un servidor** MCP y ver sus herramientas.
2. **Políticas** por herramienta: permitir, bloquear o pedir aprobación.
3. **Aprobación en tiempo real** de las llamadas retenidas, con caducidad.
4. **Supervisor de intención** sobre las llamadas que no son de solo lectura.
5. **Reproducir una sesión** de principio a fin.

**Fuera del MVP:**

- Transporte stdio (solo HTTP).
- Recursos y prompts de MCP (solo herramientas).
- Más de un servidor real: uno de ejemplo, un gestor de tareas.
- OAuth: credenciales fijas de prueba.
- Multiempresa, nube y alta disponibilidad.
- Freno automático por bucle y hook de Claude Code (ver «Visión»).

## Visión

Si el MVP funciona, Holdpoint crece hacia un control centralizado del uso de la IA en una empresa, no solo de MCP; por eso el nombre no lleva MCP. Las líneas futuras, por orden aproximado:

- **Credenciales por usuario:** cada agente actúa en nombre de una persona o un rol, y la política depende de quién pide. Esa confianza puede ahorrar la aprobación de una persona, pero nunca la revisión del supervisor.
- **Inspección de respuestas:** revisar lo que devuelven las herramientas para detectar instrucciones inyectadas.
- **Torre local y operaciones locales:** que pasen por la torre los servidores MCP del portátil y las herramientas propias del agente (terminal, edición de ficheros), por ejemplo con un hook de Claude Code.
- **Freno automático** cuando un agente entra en bucle, por ejemplo demasiados borrados por minuto.
- **Comunidad:** abrir el proyecto a contribuciones, con adaptadores para más servidores y clientes MCP.
