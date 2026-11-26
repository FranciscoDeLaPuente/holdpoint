---
title: "Conciliación de entradas del PRD: Holdpoint"
created: 2026-11-27
---

# Conciliación de entradas del PRD: Holdpoint

Contraste del [PRD](prd.md) y su [anexo](addendum.md) con sus tres entradas: el brief (con su anexo y su memlog), la visión de producto y `docs/entrada-bmad.md`. Las diferencias que la [memlog del PRD](.memlog.md) recoge como decisión de Francisco no se cuentan como huecos; se listan al final para que conste que se revisaron.

Leyenda de gravedad: **Alta** (afecta a arquitectura o épicas si no se corrige), **Media** (pérdida de matiz o trazabilidad), **Baja** (redacción o detalle).

## Resumen de hallazgos

| # | Tipo | Gravedad | Hallazgo |
| --- | --- | --- | --- |
| 1 | Contradicción interna con las entradas | Alta | §4.6 y FR-17 dan por hecha la «llamada abierta», pero la pregunta abierta 1 y FR-16 admiten el camino C (respuesta inmediata «pendiente»), donde no hay llamada abierta |
| 2 | Hueco | Alta | Se pierde el orden de recorte: el PRD no marca qué FR son recortables (FR-7, FR-23) ni cuáles son núcleo intocable (historias 3 y 4) |
| 3 | Contradicción / ambigüedad | Media | FR-8 no dice si clasificar una herramienta recalcula su política; UJ-1 cambia la política de una herramienta sin anotar en lugar de clasificarla, contra el principio 2 de la visión |
| 4 | Hueco | Media | Desaparecen «libre, de código abierto y ligero», la comunidad como lector y la dirección de la visión («control centralizado del uso de la IA») |
| 5 | Alcance colado | Media | FR-6 (auditar cambios de política), FR-7 (marcar propuestas no revisadas) y FR-5 («el MVP admite varios») no tienen respaldo en entradas ni memlog |
| 6 | Hueco | Baja | Principio 8 de la visión: la CI en Linux y Windows no aparece en NFR-4 |
| 7 | Hueco | Baja | Falta el problema (todo o nada, permisos locales, sin rastro común, errores tarde) |
| 8 | Hueco | Baja | Matices de líneas futuras perdidos (propósito de la inspección, freno por volumen, «no una garantía» de la torre local) |
| 9 | Ambigüedad | Baja | «Porcentaje que necesitó aprobación humana» sin definir (numerador y denominador) |

---

## 1. Brief (brief.md, addendum.md, .memlog.md)

### Huecos

**B-H1. Producto libre, de código abierto y ligero; comunidad como lector (Media).**
- Brief, Resumen: «Será libre, de código abierto y ligero: arranca con Docker Compose, sin cuentas externas.»
- Brief, Qué lo diferencia: «Aprobación en un panel web en tiempo real, en un producto abierto.»
- Brief, A quién sirve: «**La comunidad** puede arrancarlo en local, estudiarlo y adaptarlo a sus propios servidores MCP.»
- Memlog del brief: «Lector: tribunal de LIDR y además la comunidad open source; se añade un párrafo en 'A quién sirve' y una línea futura de comunidad.»
- PRD: no menciona la licencia ni el código abierto; §2 no nombra a la comunidad y §7.3 no tiene la línea «Comunidad». La memlog del PRD dice «lector tribunal LIDR + comunidad», así que la omisión no es una decisión.
- **Propuesta:** añadir a §1 una frase («Holdpoint es libre y de código abierto») y un NFR-6 «Licencia abierta: el repositorio incluye una licencia libre (por decidir) y la documentación para arrancarlo y adaptarlo». Añadir a §7.3: «Comunidad: abrir el proyecto a contribuciones, con adaptadores para más servidores y clientes MCP.»

**B-H2. Dirección de la visión a largo plazo (Baja).**
- Brief, Visión: «Holdpoint crece hacia un control centralizado del uso de la IA en una empresa, no solo de MCP; por eso el nombre no lleva MCP.»
- PRD §7.3: lista las líneas sin el hilo que las une.
- **Propuesta:** una frase de entrada en §7.3: «Las líneas futuras apuntan a un control centralizado del uso de la IA en una empresa, no solo de MCP.»

**B-H3. Propósito de la inspección de respuestas (Baja).**
- Brief, Visión: «**Inspección de respuestas:** revisar lo que devuelven las herramientas para detectar instrucciones inyectadas.»
- PRD §7.3: «Inspección de lo que devuelven las herramientas.»
- **Propuesta:** completar: «…para detectar instrucciones inyectadas».

**B-H4. El problema (Baja).**
- Brief, El problema: cuatro puntos («Acceso todo o nada», «Permisos locales», «Sin rastro común», «Los errores se descubren tarde»).
- PRD: no tiene sección de problema; §1 solo describe la solución. Los FR no se pueden trazar a un problema sin abrir el brief.
- **Propuesta:** en §1, un párrafo de dos líneas con los cuatro problemas y enlace al brief. No hace falta más.

**B-H5. Mensaje de espera visible al agente (Baja).**
- Anexo del brief: «El `Message` del progreso se ve en la interfaz de Claude Code y puede explicar por qué espera la llamada.»
- Brief, A quién sirve (Agente): «entender por qué se le detiene».
- PRD: FR-12 cubre los errores, pero no que el agente (y quien lo usa) sepa que la llamada está retenida mientras espera. Está en el anexo del PRD solo como pista del camino A.
- **Propuesta:** consecuencia en FR-16: «Mientras espera, el agente recibe una indicación de que la llamada está pendiente de aprobación, si el camino elegido lo permite.» Mantiene la decisión en la arquitectura.

### Contradicciones

**B-C1. Más de un servidor real (Baja).**
- Brief, Fuera del MVP: «Más de un servidor real: uno de ejemplo, un gestor de tareas.»
- PRD FR-5, Fuera de alcance: «más de un servidor real en la demo (el MVP admite varios, pero solo se prueba con el de ejemplo)». Además §7.2 ya no lo lista.
- No es caro, pero «admite varios» es una promesa que nadie probará. **Propuesta:** quitar el paréntesis o dejarlo en «el modelo de datos no limita a uno; solo se prueba con el de ejemplo», y devolver la línea a §7.2 para que la lista de fuera de alcance coincida con la del brief.

**B-C2. Permiso de sesión «para que no vuelva a preguntar».** No es contradicción: FR-15 («El supervisor las sigue evaluando») está decidido en la memlog del PRD («el permiso de sesión ahorra la aprobación, no la supervisión»). Sin acción.

### Alcance colado

Nada del PRD contradice el alcance del brief en lo grande. Lo colado menor se trata en la sección 4 (FR-5, FR-6, FR-7).

---

## 2. Visión de producto (docs/vision/vision-producto.md)

### Principios de diseño 1-8

| Principio | Dónde está en el PRD | Estado |
| --- | --- | --- |
| 1. La pasarela es la única con llaves | §3 (Pasarela), FR-3, NFR-1, NFR-2 | Cubierto |
| 2. La persona es la excepción | FR-7, FR-8, §4.5, SM-C2 | Cubierto, con la ambigüedad V-C1 |
| 3. Espera con tiempo máximo | FR-16 (5 min por defecto, decisión de la memlog) | Cubierto; ver V-C2 |
| 4. Todo registrado, sin secretos | FR-21, FR-3, FR-13 | Cubierto |
| 5. Objetivo declarado | FR-9 | Cubierto |
| 6. Sin cuentas externas | NFR-3, FR-20 | Cubierto; ver observación O-3 |
| 7. Claude Code con catálogo aprobado | §7.1 (fichero de ejemplo) y anexo del brief | Cubierto como documentación |
| 8. Multiplataforma | NFR-4 | Parcial: ver V-H1 |

### Huecos

**V-H1. CI multiplataforma (Baja).**
- Visión, principio 8: «la integración continua compila y pasa los tests unitarios en Linux y en Windows, y el E2E en Linux.»
- PRD NFR-4: «Funciona con Docker en Linux y en Windows con Docker Desktop.» El anexo del brief tampoco recoge la CI.
- **Propuesta:** no es un requisito de producto, pero se perdería por el camino. Añadirlo al anexo del PRD como pista para la arquitectura («CI: compilación y tests unitarios en Linux y Windows; E2E en Linux»), no al cuerpo.

**V-H2. «Sin decisión, caduca y el agente recibe un error claro»: cubierto.** Sin acción.

**V-H3. Matices de las líneas futuras (Baja).**
- Visión, Fuera de alcance: credenciales de usuario «se saltaría a la persona, nunca al supervisor **ni al freno por volumen**»; torre local: «daría aprobación y auditoría, **no una garantía**».
- PRD §7.3 conserva lo del supervisor pero pierde el freno por volumen y el aviso de la torre local.
- **Propuesta:** completar las dos líneas de §7.3 con esos incisos (una subordinada cada una).

**V-H4. Orden de recorte del calendario (Alta).** Ver E-H1; lo recogen la visión (alcance y deseables) y, con detalle, `entrada-bmad.md`.

### Contradicciones

**V-C1. Clasificar frente a cambiar la política de una herramienta sin anotar (Media).**
- Visión, principio 2: «Una herramienta sin anotar pide aprobación **hasta que el administrador la clasifica**, una sola vez.»
- PRD FR-8: «Una herramienta sin anotar deja de pedir aprobación por defecto en cuanto se clasifica.» Pero FR-6 y FR-7 tratan la política como un dato propio de la herramienta, propuesto una vez «al leer una herramienta nueva». No se dice si al cambiar la clasificación se recalcula la política propuesta. Si no se recalcula, FR-8 no se cumple; si se recalcula, puede pisar una política que el administrador ya cambió.
- PRD UJ-1: «Lucía acepta la propuesta y **cambia una herramienta sin anotar a «permitir»**.» El recorrido no usa FR-8, que es lo que pide la visión, y además la herramienta sin anotar no aparece antes en el recorrido (solo `listar_tareas` y `borrar_tarea`).
- **Propuesta:** (a) en FR-8, consecuencia: «Al cambiar la clasificación, la política se recalcula según FR-7 si el administrador no la había cambiado a mano; si la había cambiado, se mantiene.» (b) En UJ-1: «…y ve una tercera, `mover_tarea`, sin anotar, con «pedir aprobación». Lucía la clasifica como normal y su política pasa a «permitir, con el supervisor».»

**V-C2. Espera con la llamada abierta (Alta).** Es la contradicción E-C1, que se trata en la sección 3: la visión (principio 3: «La llamada retenida se mantiene abierta») y el PRD §4.6 suponen la llamada abierta, pero el PRD deja abierto el camino C.

### Alcance colado

Ninguno frente a la visión aparte de lo de la sección 4. Las incorporaciones sin cobertura en la visión (roles y acceso, FR-1 y FR-2; credencial de agente, FR-10; volver a leer, FR-5; idioma, NFR-5; sin objetivo, retener; supervisor caído, retener; espera de 5 min) están decididas en la memlog.

### Criterios de éxito

Los cinco criterios de la visión están en SM-1 a SM-5. SM-3 añade el umbral del 90 % y SM-C1 la contramétrica del 20 %: decididos en la memlog. Sin huecos.

---

## 3. Entrada de BMAD (docs/entrada-bmad.md)

### Huecos

**E-H1. Orden de recorte y prioridad entre historias (Alta).**
- `entrada-bmad.md` §3: «**Orden de recorte si hay riesgo:** (1) las deseables fuera del todo; (2) la UX como listado de pantallas…; (3) la historia 5 como listado de la sesión, no reproducción paso a paso; (4) la historia 2 con políticas manuales, sin propuesta inicial por riesgo; (5) la historia 3 y el supervisor (historia 4) no se recortan.»
- PRD: las deseables ya están en §7.3 (paso 1 aplicado), pero no hay nada sobre qué FR se recortan primero. Las épicas y la arquitectura no sabrán que FR-7 (propuesta por riesgo) y FR-23 (recorrer evento a evento) son los primeros candidatos, ni que FR-11 y FR-13 a FR-20 son el núcleo.
- **Propuesta:** añadir §7.4 «Prioridad y recorte»: «Núcleo, no se recorta: FR-11 a FR-20 (historias 3 y 4). Si hay riesgo, se recorta en este orden: FR-23 pasa a un listado de la sesión (FR-22 basta para SM-5 si muestra los eventos); FR-7 y FR-8 se sustituyen por políticas manuales con «pedir aprobación» por defecto.»

**E-H2. Requisitos de la entrega 1 (sin acción en el PRD).** Modelo de datos, API, tickets con etiquetas `backend`/`frontend`/`bd`, IA en 4 de 6 fases: son de la entrega, no del producto. No son hueco del PRD; corresponden a arquitectura, épicas y `README.md`.

### Contradicciones

**E-C1. Llamada abierta frente a camino C (Alta).**
- `entrada-bmad.md` §4: tres caminos posibles, entre ellos «C. Respuesta inmediata «pendiente de aprobación» con un identificador y una herramienta de la pasarela para consultar el estado».
- PRD §4.6: «El agente espera **con la llamada abierta** hasta la decisión o hasta la espera máxima.» FR-17: «Si el agente **corta la llamada** mientras está pendiente…». FR-16: «Mientras espera, el agente no corta por su propio límite de tiempo.» Las tres frases solo tienen sentido con los caminos A o B.
- PRD §9.1 y FR-16: «La forma de conseguirlo la decide la arquitectura (caminos A, B y C…)».
- Si la arquitectura elige C, el PRD queda incumplido; si el PRD manda, C ya no es opción y la pregunta abierta 1 sobra en parte.
- **Propuesta (una de dos, a elegir por Francisco):**
  1. Neutral: §4.6 «El agente recibe el resultado cuando el responsable decide o cuando se cumple la espera máxima.» FR-17: «Si el agente abandona la llamada pendiente (corta la conexión o, según el camino, lo indica), la llamada pasa a cancelada por el agente.» Mantener §9.1.
  2. Decidir ya el camino A (el único probado en la prueba de concepto, hasta 300 s) como requisito y dejar B y C como alternativas de la arquitectura si un cliente no manda `progressToken`.

**E-C2. Principio 3 («por ejemplo 60 segundos»).** Resuelto: `entrada-bmad.md` dice que «ya no tiene por qué ser 60» y la memlog fija 5 min. Sin acción.

### Alcance colado

Nada frente a `entrada-bmad.md` aparte de lo de la sección 4.

---

## 4. Alcance colado sin respaldo en entradas ni memlog

| Elemento del PRD | Cita | Por qué es colado | Propuesta |
| --- | --- | --- | --- |
| FR-6, consecuencia | «Cada cambio queda registrado con quién lo hizo y cuándo.» | La historia 2 no lo pide y la historia 5 audita sesiones, no la configuración. El glosario de «Evento» no incluye cambios de política, así que nadie lo consume: ni FR-22 ni FR-23 lo muestran | Quitarlo, o pedir el visto bueno de Francisco y añadir dónde se ve. Si se quita, va a §7.3 («auditoría de cambios de configuración») |
| FR-7, consecuencia | «El panel distingue las políticas propuestas que el administrador aún no ha revisado.» | Añade un estado «revisada/no revisada» al modelo de datos y a la UX. El brief solo dice que el administrador «solo tiene que revisar» la propuesta | Confirmar con Francisco. Alternativa mínima: quitarlo; FR-4 ya muestra la política de cada herramienta |
| FR-5, Fuera de alcance | «el MVP admite varios» | Ver B-C1 | Ver B-C1 |
| UJ-3 | «cambiar la fecha de entrega de una tarea» | No es colado de producto, pero obliga a que el servidor de ejemplo tenga más herramientas que las de la prueba de concepto (`listar_tareas`, `borrar_tarea`): una de búsqueda y otra de modificación | Dejarlo y anotarlo en el anexo: «El servidor de ejemplo necesita al menos: listar o buscar (solo lectura), modificar (normal), borrar (destructiva) y una sin anotar para UJ-1» |

---

## 5. Otras observaciones (fuera del contraste estricto)

- **O-1. Definición de «aprobación humana» (Baja).** FR-22, SM-5 y SM-C2 hablan del «porcentaje que necesitó aprobación humana». No queda claro si cuenta las retenidas (aprobadas, rechazadas, caducadas y canceladas) o solo las decididas, ni si el denominador incluye las de solo lectura. **Propuesta:** en el glosario: «Porcentaje de llamadas retenidas sobre el total de llamadas de la sesión, incluidas las de solo lectura.»
- **O-2. Valor por defecto de `destructiveHint` (Baja).** En la especificación de MCP, `destructiveHint` vale `true` por defecto cuando `readOnlyHint` es `false`. La clasificación «normal (con anotaciones, ni de solo lectura ni destructiva)» de FR-7 debería exigir `destructiveHint: false` explícito. **Propuesta:** una nota técnica en el anexo del PRD; conviene comprobarlo en la especificación antes de la arquitectura.
- **O-3. Modo del supervisor por defecto (Baja).** SM-4 exige arrancar sin preguntar nada; si el `.env.example` arranca con Ollama, hay que descargar un modelo. **Propuesta:** consecuencia en FR-20: «El `.env.example` arranca en modo simulado.»
- **O-4. Fecha del PRD.** La cabecera dice `updated: 2026-11-26`; la memlog llega al 27. Actualizar al cerrar.

## 6. Diferencias revisadas que son decisiones de la memlog (no huecos)

Tres roles con usuarios de prueba (FR-1, FR-2); sin objetivo, se retiene; supervisor caído, «no disponible» y se retiene; espera máxima de 5 min configurable; solo lectura sin supervisor; §2.2 sin aislamiento entre equipos; permiso de sesión con supervisión (FR-15); umbrales de SM-3 y SM-C1; idioma e i18n (NFR-5); agentes fijos en configuración (FR-10) y su gestión como línea futura; FR-5, FR-9, FR-13 (<2 s) y FR-21 aceptados; NFR de retardo eliminado; detección automática de cambios y exportar el registro como «Fuera de alcance» dentro de los FR; deseables (freno por bucle y hook) como líneas futuras (memlog del brief).
