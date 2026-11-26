# Revisión de calidad del PRD — Holdpoint

## Veredicto global

Es un PRD sólido para lo que debe hacer: tiene una tesis clara (política + supervisor + persona, con cierre por defecto), el alcance es honesto y está bien acotado, y los FR casi siempre traen consecuencias comprobables. El riesgo está en dos sitios: las métricas no comprueban de verdad las dos apuestas técnicas del producto (que el agente aguante la espera más allá de los 60 s y que el supervisor real, no el simulado, acierte), y algunos FR dejan sin fijar límites que la arquitectura y las historias necesitan: el tiempo del supervisor, dónde empieza y acaba una sesión y la clasificación «normal» frente a los valores por defecto de MCP. Nada de esto pide más alcance; son precisiones de una línea dentro de los FR y las SM que ya existen.

## Decisión — strong

Las decisiones están escritas como decisiones, no como «consideraciones»: el orden de evaluación de §4.5 es explícito, el cierre por defecto ante el fallo del supervisor (FR-19), la retención en sesiones sin objetivo (FR-11), que el permiso de sesión «ahorra la aprobación, no la supervisión» (FR-15) y la espera máxima de 5 min (FR-16). Las preguntas abiertas de §9 lo son de verdad, y cada una dice quién la cierra y cuándo. La nota de FR-7 («"Solo lectura" no quiere decir "inofensiva"…») reconoce una objeción real en lugar de esquivarla.

Falta nombrar dos costes de decisiones ya tomadas. El cierre por defecto hace que, con Ollama caído o lento, toda llamada que no sea de solo lectura dependa de una persona. Y el supervisor añade su latencia a cada llamada que no es de solo lectura. El memlog retira a propósito el NFR de retardo, y eso está bien, pero el PRD no dice en ninguna parte lo que se acepta a cambio.

### Hallazgos
- **medium** Coste del cierre por defecto y de la latencia del supervisor sin nombrar (§4.5, FR-19) — Quien lea «el veredicto es "no disponible" y la llamada queda retenida» no sabe que se acepta, a cambio, más carga para el responsable y más espera en cada llamada supervisada. *Fix:* una frase en las notas de FR-19 que diga lo que se cede (disponibilidad y latencia) y por qué (la seguridad manda en el MVP).

## Sustancia frente a relleno — strong

No hay relleno. La visión (§1) es específica del producto: describe el flujo de decisión, no una promesa genérica. Los cuatro trabajos por hacer de §2.1 se usan: el agente justifica FR-12 y el auditor, FR-21 a FR-23. Los NFR traen umbrales y hechos propios del producto (Docker Compose, `.env.example`, español con los textos separados), no adjetivos. El detalle de Claude Code («60 s por defecto» en FR-16) es justo el tipo de dato que se gana en la prueba de concepto.

### Hallazgos
- **low** NFR-4 sin comprobación (§5) — «Funciona con Docker en Linux y en Windows con Docker Desktop» no lo valida ninguna SM. *Fix:* decir que SM-4 se ejecuta en las dos plataformas, o dejarlo como intención declarada.

## Coherencia estratégica — strong

La tesis está clara y todo cuelga de ella: una sola pasarela que combina la política por herramienta, el supervisor contra el objetivo declarado y la decisión humana, y que registra cada evento. Las funcionalidades siguen el flujo de §4.5, y el alcance del MVP es de tipo «resolver el problema»: el recorrido completo con un solo servidor de ejemplo. Hay contramétricas (SM-C1 y SM-C2) bien pensadas: la de SM-C1 impide que el supervisor «mejore» a fuerza de no retener nunca.

El punto débil está en que las métricas principales no prueban las dos apuestas que sostienen la tesis (ver Done-ness: SM-1 y SM-3).

## Done-ness — adequate

La mayoría de los FR tienen consecuencias comprobables y precisas: FR-11, FR-13 («menos de 2 segundos»), FR-14 (la primera decisión gana), FR-15 y FR-19. Los huecos están justo en las piezas en que se apoyan la arquitectura y las historias 3 y 4.

### Hallazgos
- **high** SM-1 no prueba la espera larga (§8 SM-1, FR-16) — SM-1 dice que valida FR-16, pero su guion («la llamada queda retenida, se aprueba desde el panel») no obliga a que la aprobación llegue después de 60 s, ni usa Claude Code («un agente con guion fijo»). El mayor riesgo técnico del producto, que el agente no corte la espera (anexo del brief, caminos A, B y C), puede quedar sin probar con la prueba en verde. *Fix:* en SM-1, aprobar pasados más de 60 s y, al menos en la demo, con Claude Code; y añadir el caso de caducidad (5 min o una espera máxima reducida para la prueba).
- **high** SM-3 no fija con qué supervisor se mide (§8 SM-3, FR-18, FR-20) — Con el modo simulado (FR-20), cuyos veredictos son deterministas, SM-3 se cumple por construcción. La pregunta abierta 2 deja sin elegir el modelo de Ollama. Así, la métrica del componente que diferencia el producto puede quedarse vacía. *Fix:* decir que SM-3 y SM-C1 se miden con el modelo de Ollama elegido y no en modo simulado, y que el conjunto de unos 20 casos (pregunta 3) incluye un número mínimo de llamadas contrarias al objetivo para que el 90 % tenga sentido (por ejemplo, 10 o más).
- **medium** El tiempo máximo del supervisor no tiene cifra (FR-19) — «falla o no responde a tiempo» es un adjetivo. El anexo del PRD dice que necesita un tiempo máximo propio, menor que la espera máxima, pero no da ninguno. Sin él no se puede probar FR-19 y el retardo de cada llamada supervisada no tiene tope. *Fix:* un valor por defecto configurable (por ejemplo, 30 s) en FR-19.
- **medium** El porcentaje de aprobación humana no está definido (FR-22, UJ-4, SM-5, SM-C2) — No se dice sobre qué total se calcula (¿también las de solo lectura?) ni qué cuenta como «necesitó» (¿las caducadas?, ¿las canceladas?, ¿las que pasan por un permiso de sesión?). Lo usan tres secciones y una contramétrica. *Fix:* una línea en FR-22 que diga «llamadas retenidas / total de llamadas de la sesión, sin contar la declaración del objetivo», o la definición que se elija.
- **medium** FR-22 y FR-23 son débiles como criterio de aceptación (§4.8) — FR-22 no tiene consecuencias, y la de FR-23 («se puede recorrer entera») no dice qué debe verse en cada evento. Es la historia 5, la que la orden de recorte simplifica primero, así que conviene que su «hecho» sea nítido en cualquiera de sus dos versiones. *Fix:* en FR-23, una consecuencia del tipo «cada llamada muestra la política aplicada, el veredicto, quién decidió y el resultado; los argumentos sensibles, ocultos».
- **low** FR-4 no cubre la clasificación «normal» (FR-4) — Las consecuencias tratan tres de las cuatro clasificaciones. *Fix:* añadir el caso «normal».

## Honestidad del alcance — strong

Los límites son explícitos y están en varios niveles: §2.2 (público fuera), §6 (no objetivos), §7.2 (fuera), §7.3 (líneas futuras, donde están las dos deseables) y un «Fuera de alcance» dentro de FR-5 y FR-23. La frase de FR-5 («el MVP admite varios, pero solo se prueba con el de ejemplo») es un buen ejemplo de honestidad. No hay supuestos sueltos: el memlog explica que se eliminó el índice porque ya no quedaban pendientes, y no queda ningún `[SUPUESTO]` en el texto.

### Hallazgos
- **medium** NFR-1 promete más de lo que Holdpoint controla (§5 NFR-1, SM-2) — «Los servidores MCP solo aceptan conexiones de la pasarela» solo puede garantizarse para el servidor de ejemplo, dentro de la red de Docker Compose. Con un servidor real registrado, lo único que pone Holdpoint es que la credencial no sale de la pasarela. *Fix:* acotarlo: «el servidor de ejemplo solo es accesible desde la pasarela; con otros servidores, la garantía es que solo la pasarela tiene la credencial».
- **medium** El límite de la sesión queda sin decidir y sin señalar (glosario «Sesión», FR-10, anexo del PRD) — El glosario define la sesión como «el trabajo de un agente sobre una tarea», mientras que el anexo propone «una sesión por conexión» (`Mcp-Session-Id`, «a confirmar»). De ese límite dependen el permiso de sesión (FR-15), la regla de la sesión sin objetivo (FR-11) y la lista de sesiones (FR-22), pero no aparece en las preguntas abiertas de §9 y FR-10 no tiene ninguna consecuencia sobre la sesión. *Fix:* añadirlo como pregunta abierta 4 (lo decide la arquitectura) o fijar en FR-10 «una sesión por conexión MCP del agente; volver a declarar el objetivo no abre una sesión nueva».

## Utilidad para los pasos siguientes — adequate

Hay glosario, los identificadores son contiguos y únicos (FR-1 a FR-23, NFR-1 a NFR-5, SM-1 a SM-5 y SM-C1 a SM-C2) y cada funcionalidad dice qué UJ realiza. Las SM apuntan a sus FR y NFR. Para la UX hay material suficiente: la bandeja (FR-13) y el recorrido de la sesión (FR-23) dicen qué datos muestran. Lo que resta es la ambigüedad de algunos términos que las historias van a usar tal cual (ver las notas mecánicas).

### Hallazgos
- **medium** La clasificación «normal» choca con los valores por defecto de MCP (glosario «Clasificación», FR-7) — En MCP, `destructiveHint` vale `true` por defecto cuando `readOnlyHint` es `false`. Una herramienta anotada solo con `readOnlyHint: false` es destructiva según el protocolo, pero «con anotaciones, ni de solo lectura ni destructiva» puede leerse como «normal» → permitir. Quien implemente lo hará al pie de la letra, justo en la regla por defecto de seguridad. *Fix:* en FR-7, «normal = `readOnlyHint: false` y `destructiveHint: false` explícito; las anotaciones que faltan toman el valor por defecto de MCP».
- **low** La reclasificación y la política propuesta no se relacionan (FR-8) — «deja de pedir aprobación por defecto en cuanto se clasifica» no dice si la política se recalcula solo cuando sigue siendo la propuesta sin revisar, o también cuando el administrador ya la había cambiado. *Fix:* «al cambiar la clasificación se recalcula la política propuesta si el administrador aún no la ha revisado; si la había cambiado, se mantiene».

## Ajuste a la forma — strong

La forma encaja con lo que es: una herramienta interna con tres roles, al principio de la cadena (alimenta UX, arquitectura y épicas) y para un TFM. Cuatro UJ con protagonistas de ejemplo y casos límite son lo justo: no sobra formalidad. Agrupar los FR por funcionalidad con la historia del MVP en el título facilita el desglose en épicas.

## Notas mecánicas

- **«Registro» con dos sentidos:** el registro de un servidor (FR-3, UJ-1: «el registro falla») y el registro de eventos (FR-21). En FR-5 («se conservan en el registro») no se sabe cuál es. Conviene reservar «registro» para los eventos y usar «alta» para los servidores.
- **Términos sin entrada en el glosario:** «bandeja» (FR-10, FR-13, FR-17), «política propuesta» (FR-5, FR-7) y «argumentos sensibles» o «lista de nombres sensibles» (FR-13, FR-21). §0 promete que los términos del glosario se usan tal cual; estos tres se usan como términos de dominio y no figuran en él.
- **Estado «cancelada por el agente»:** el glosario lo llama así y FR-17 y la bandeja dicen «cancelada». Es una deriva menor; conviene unificarlo.
- **§7.1 «(FR-1 a FR-23)» dentro de «las cinco historias»:** FR-1, FR-2 y FR-9 a FR-12 son soporte transversal, no de una historia concreta. Es correcto (el memlog recoge la decisión de los roles), pero conviene decir «las cinco historias y su soporte (FR-1 a FR-23)» para que la trazabilidad de las épicas no busque una historia que no existe.
- **SM-1 dice que valida FR-16**, pero hoy no lo hace (ver Done-ness).
- **Roles y bandeja:** FR-2 no dice si el responsable puede consultar las sesiones ni si el auditor ve la bandeja en modo lectura. Es menor, pero la UX lo preguntará.
- **Índice de supuestos:** no hay `[SUPUESTO]` en el texto y el índice se eliminó (memlog), así que no hay nada que cruzar.
