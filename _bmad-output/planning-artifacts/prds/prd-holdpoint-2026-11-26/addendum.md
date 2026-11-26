---
title: "Anexo del PRD: Holdpoint"
created: 2026-11-26
updated: 2026-11-27
---

# Anexo del PRD: Holdpoint

Notas técnicas para la arquitectura que salieron al redactar el PRD. El resto del detalle técnico (prueba de concepto, caminos de espera, estados y alternativas) está en el [anexo del brief](../../briefs/brief-holdpoint-2026-11-26/addendum.md).

## Pistas para la arquitectura

- **Sesión.** El candidato natural es la sesión del transporte HTTP de MCP (`Mcp-Session-Id`): una sesión (en el sentido del glosario del PRD) por conexión del agente. Lo decide la arquitectura (pregunta abierta 4 del PRD).
- **Objetivo declarado.** La pasarela añade a la lista de herramientas una herramienta propia (por ejemplo `declarar_objetivo`), que no reenvía a ningún servidor (FR-9). Su descripción debe pedir al agente que la llame al empezar.
- **Espera.** Si se elige el camino A (ver los [caminos de espera](../../briefs/brief-holdpoint-2026-11-26/addendum.md#caminos-para-la-espera-de-una-llamada-retenida)), la pasarela manda `notifications/progress` cada 10 s con un campo `message` que explique la espera («esperando aprobación, quedan 4 min»). La espera máxima por defecto es de 5 min (FR-16). A partir de 120 s, Claude Code interactivo pasa la llamada a segundo plano. El resultado llega igual, pero conviene comprobarlo en la demo.
- **Tiempo máximo del supervisor.** 30 s por defecto (FR-19), bastante menos que la espera máxima.
- **Concurrencia.** La decisión sobre una llamada retenida es una única transición de estado: de pendiente a aprobada, rechazada, caducada o cancelada por el agente. Gana la primera (FR-14).
- **Usuarios de prueba.** Cuatro usuarios: uno por rol y uno con los tres roles (§4.1), definidos en la configuración de ejemplo.
- **Clasificación por anotaciones.** FR-4 y FR-7 se basan en una regla de MCP: si no se indica, `destructiveHint` vale `true`. Solo tiene sentido con `readOnlyHint: false`. En la revisión del PRD se aceptó de memoria. Hay que comprobarlo en la especificación de MCP antes de cerrar la arquitectura.
- **Integración continua.** El [principio 8 de la visión](../../../../docs/vision/vision-producto.md#principios-de-diseño) pide compilar y pasar las pruebas unitarias en Linux y en Windows, y las de extremo a extremo en Linux. Es práctica de desarrollo, no requisito del producto: se recoge en la arquitectura.
