---
title: "PRD: Holdpoint"
status: final
created: 2026-11-26
updated: 2026-11-27
---

# PRD: Holdpoint

## 0. Propósito del documento

Este PRD convierte el [brief de producto](../../briefs/brief-holdpoint-2026-11-26/brief.md) en requisitos comprobables para las cinco historias del MVP. Lo usan la especificación de UX, la arquitectura y el desglose en épicas e historias de la entrega 1. Los términos del [glosario](#3-glosario) se usan tal cual en todo el documento. Los requisitos funcionales (FR) se agrupan por funcionalidad y tienen una numeración global estable. El detalle técnico (resultado de la prueba de concepto, caminos de espera y alternativas) está en el [anexo del brief](../../briefs/brief-holdpoint-2026-11-26/addendum.md), y lo nuevo de este PRD, en el [anexo del PRD](addendum.md).

## 1. Visión

Holdpoint es una torre de control para agentes de IA: una pasarela MCP que decide sobre cada llamada a una herramienta. Las llamadas a herramientas de solo lectura con política de permitir pasan directas. El resto pasa por la política de su herramienta y por un supervisor que compara la llamada con el objetivo de la sesión, y solo llega al servidor MCP si las dos lo permiten o si una persona la aprueba. Todo queda registrado para reproducir la sesión.

Es libre, de código abierto y ligero, y apunta a un control centralizado del uso de la IA en una empresa; el MVP se limita a las herramientas MCP.

El MVP demuestra el flujo completo con un servidor MCP de ejemplo (un gestor de tareas) y Claude Code como agente, en local con Docker Compose y sin cuentas externas.

## 2. Usuarios

### 2.1 Trabajos por hacer

- **Administrador:** poner un servidor MCP detrás de la pasarela y decidir qué puede hacer cada herramienta, partiendo de una propuesta y no de cero.
- **Responsable:** enterarse a tiempo de las llamadas que importan y decidir con contexto (qué pide el agente, con qué argumentos y si encaja con la tarea) sin convertirse en un cuello de botella.
- **Auditor:** explicar después qué hizo un agente, qué se decidió y quién lo decidió.
- **Agente:** usar las herramientas sin ver credenciales y, cuando se le detiene, saber por qué para ajustar el plan.

### 2.2 Fuera del público del MVP

- Organizaciones que necesitan separar equipos o empresas: en el MVP, todos los usuarios de una instalación comparten servidores, políticas y sesiones, sin aislamiento entre ellos.
- Desarrolladores que quieren controlar sus servidores MCP locales (stdio): es la línea futura de la torre local.

### 2.3 Recorridos clave

Los protagonistas son de ejemplo. En un equipo pequeño, la misma persona suele tener los roles de administrador y responsable.

- **UJ-1. Lucía pone el gestor de tareas detrás de la pasarela.**
  Lucía es la tech lead del equipo y tiene los roles de administrador y responsable. Entra en el panel, registra el servidor MCP del gestor de tareas con su URL y su credencial, y ve sus herramientas con el riesgo que declara cada una: `listar_tareas` es de solo lectura y `borrar_tarea` es destructiva. El panel ya propone «permitir» para la primera y «pedir aprobación» para la segunda. Una tercera herramienta, `editar_tarea`, viene sin anotar y el panel propone «pedir aprobación». Lucía la clasifica como normal, la política propuesta pasa a «permitir» y Lucía acepta la propuesta. **Caso límite:** si el servidor no responde, el alta falla con un mensaje claro y no se guarda nada a medias.

- **UJ-2. Lucía decide sobre un borrado mientras el agente espera.**
  Un desarrollador pide a Claude Code «limpia las tareas duplicadas del proyecto». El agente declara ese objetivo a la pasarela y empieza a buscar: las búsquedas pasan solas. Cuando intenta borrar una tarea, la llamada queda retenida. A Lucía le aparece en el panel, sin recargar, con los argumentos y el veredicto del supervisor («encaja: borra una tarea marcada como duplicada»). La revisa, ve que no es duplicada y la rechaza con el motivo «no está duplicada, es de otro navegador». El agente recibe el motivo y sigue con la siguiente. **Caso límite:** si nadie decide en 5 minutos, la llamada caduca y el agente recibe un error que lo dice.

- **UJ-3. El supervisor para una llamada que la política dejaría pasar.**
  Durante la misma sesión, el agente intenta cambiar la fecha de entrega de una tarea con una herramienta que la política permite. El supervisor considera que no encaja con limpiar duplicados y la retiene. Lucía ve el veredicto, confirma que sobra y la rechaza.

- **UJ-4. Jorge reconstruye la sesión.**
  Jorge tiene el rol de auditor. Al día siguiente abre la sesión en el panel y la recorre en orden: el objetivo declarado, cada llamada con sus argumentos (los sensibles, ocultos), la decisión de la política, el veredicto del supervisor, quién aprobó o rechazó y qué devolvió la herramienta. El resumen de la sesión muestra el porcentaje de aprobación humana.

## 3. Glosario

- **Agente** — Cliente MCP (en el MVP, Claude Code) que llama a las herramientas a través de la pasarela. Abre una o varias sesiones.
- **Pasarela** — El componente de Holdpoint que hace de servidor MCP para los agentes y de cliente MCP para los servidores registrados. Es el único con las credenciales de los servidores.
- **Panel** — La aplicación web donde trabajan los usuarios, con avisos en tiempo real.
- **Usuario** — Persona que entra en el panel. Tiene uno o varios roles.
- **Rol** — Administrador, responsable o auditor. Determina qué puede hacer el usuario en el panel.
- **Servidor** — Servidor MCP registrado detrás de la pasarela. Tiene una o varias herramientas.
- **Herramienta** — Operación de un servidor que el agente puede llamar. Puede declarar su riesgo con las anotaciones `readOnlyHint` y `destructiveHint` de MCP.
- **Clasificación** — Si la herramienta es de solo lectura, destructiva, normal o sin anotar. Sale de sus anotaciones y el administrador puede corregirla.
- **Política** — La regla de una herramienta: permitir, bloquear o pedir aprobación. Una por herramienta.
- **Política propuesta** — La política que Holdpoint asigna a una herramienta según su clasificación, antes de que el administrador la cambie.
- **Sesión** — El trabajo de un agente sobre una tarea, con un objetivo y todas sus llamadas.
- **Objetivo** — La tarea que el agente declara al empezar la sesión, con una herramienta propia de la pasarela.
- **Llamada** — Una invocación de una herramienta por un agente dentro de una sesión.
- **Supervisor** — Componente con un LLM que da un veredicto sobre si una llamada encaja con el objetivo.
- **Veredicto** — Resultado del supervisor para una llamada: encaja, no encaja o no disponible, con una explicación breve.
- **Llamada retenida** — Llamada que espera la decisión de un responsable. Estados: pendiente, aprobada, rechazada, caducada o cancelada por el agente.
- **Bandeja** — Pantalla del panel donde el responsable ve las llamadas retenidas pendientes y decide sobre ellas.
- **Permiso de sesión** — Lo que concede el responsable al aprobar una llamada: la herramienta queda permitida el resto de la sesión.
- **Espera máxima** — Tiempo que una llamada retenida puede estar pendiente antes de caducar.
- **Evento** — Cada hecho registrado de una sesión: objetivo declarado, llamada, decisión de la política, veredicto, decisión del responsable y respuesta de la herramienta.
- **Registro de eventos** — El historial de eventos de todas las sesiones. No confundir con el alta de un servidor.
- **Argumentos sensibles** — Argumentos de una llamada cuyo nombre está en una lista configurable (por ejemplo `password`, `token`, `secret`, `api_key`). Se ocultan antes de guardarlos o mostrarlos.
- **Porcentaje de aprobación humana** — Número de llamadas retenidas de una sesión dividido entre el total de sus llamadas, sin contar la declaración del objetivo.

## 4. Funcionalidades

### 4.1 Acceso al panel y roles

**Descripción:** el MVP trae usuarios de prueba predefinidos, uno por rol y uno con los tres roles, con credenciales fijas en la configuración de ejemplo. No hay alta de usuarios, recuperación de contraseña ni OAuth. Cada pantalla y cada operación de la API exige un rol.

#### FR-1: Iniciar sesión en el panel

Un usuario puede entrar en el panel con su nombre y contraseña de prueba.

**Consecuencias (comprobables):**
- Con credenciales incorrectas, el panel muestra un error y no da acceso.
- Sin haber entrado, la API rechaza toda operación del panel.

#### FR-2: Permisos por rol

El administrador gestiona servidores, políticas y la espera máxima; el responsable decide sobre las llamadas retenidas; el auditor consulta las sesiones. Un usuario con varios roles suma sus permisos.

**Consecuencias (comprobables):**
- Un usuario solo con el rol de auditor no ve las acciones de aprobar o rechazar, y la API le rechaza esas operaciones.
- Un usuario solo con el rol de responsable no puede cambiar políticas.

### 4.2 Registrar un servidor (historia 1)

**Descripción:** el administrador da de alta un servidor por su URL HTTP y su credencial. La pasarela se conecta, lee sus herramientas con sus anotaciones y las guarda. La credencial solo la guarda y la usa la pasarela. Realiza UJ-1.

#### FR-3: Registrar un servidor

El administrador puede registrar un servidor indicando nombre, URL y credencial.

**Consecuencias (comprobables):**
- Si la pasarela no puede conectarse o el servidor no responde como servidor MCP, el alta falla con el motivo y no se guarda nada.
- La credencial no se muestra en el panel después de guardarla ni aparece en el registro de eventos.

#### FR-4: Ver las herramientas de un servidor

El administrador puede ver las herramientas de un servidor, con su descripción, su clasificación y su política.

**Consecuencias (comprobables):**
- Con `readOnlyHint: true` aparece como de solo lectura. Con `readOnlyHint: false` y `destructiveHint: false` explícito, como normal. Con otras anotaciones, como destructiva, porque en MCP `destructiveHint` vale `true` si no se indica. Sin ninguna anotación, como sin anotar.

#### FR-5: Volver a leer las herramientas

El administrador puede pedir que la pasarela vuelva a leer las herramientas de un servidor.

**Consecuencias (comprobables):**
- Las herramientas nuevas aparecen con su política propuesta (FR-7). Las que ya no existen dejan de ofrecerse a los agentes, pero se conservan en el registro de eventos.

**Fuera de alcance:** detectar cambios automáticamente; más de un servidor real en la demo (el MVP admite varios, pero solo se prueba con el de ejemplo).

### 4.3 Políticas (historia 2)

**Descripción:** cada herramienta tiene una política. Al registrar el servidor, Holdpoint propone una según su clasificación y el administrador la revisa y la cambia. Realiza UJ-1.

#### FR-6: Cambiar la política de una herramienta

El administrador puede poner cada herramienta en permitir, bloquear o pedir aprobación.

**Consecuencias (comprobables):**
- El cambio se aplica a las llamadas que lleguen después, sin reiniciar nada.

#### FR-7: Política propuesta según el riesgo

Al leer una herramienta nueva, Holdpoint le asigna una política propuesta según su clasificación.

**Consecuencias (comprobables):**
- Solo lectura → permitir. Destructiva → pedir aprobación. Normal → permitir, con el supervisor. Sin anotar → pedir aprobación.

**Notas:** la clasificación se fía de las anotaciones del servidor, que MCP considera pistas y no garantías; por eso el administrador la revisa al registrar el servidor (FR-8). «Solo lectura» no quiere decir «inofensiva»: una lectura puede sacar datos que no debería, y en el MVP eso se controla con la política, no con el supervisor.

#### FR-8: Corregir la clasificación

El administrador puede cambiar la clasificación de una herramienta, por ejemplo marcar como de solo lectura una sin anotar.

**Consecuencias (comprobables):**
- Al cambiar la clasificación, la política propuesta se recalcula (FR-7). Si el administrador ya había cambiado la política a mano, se respeta.
- Una herramienta sin anotar deja de pedir aprobación por defecto en cuanto se clasifica. Basta con clasificarla una vez.

### 4.4 Sesiones y objetivo

**Descripción:** el agente declara el objetivo de la sesión llamando a una herramienta propia de la pasarela. El supervisor lo usa como referencia. Realiza UJ-2.

#### FR-9: Declarar el objetivo

El agente puede declarar el objetivo de su sesión con una herramienta de la pasarela que aparece junto a las de los servidores.

**Consecuencias (comprobables):**
- El objetivo queda registrado como el primer evento de la sesión.
- Si el agente lo vuelve a declarar, queda registrado el cambio y el supervisor usa el último.

#### FR-10: Identificar agente y sesión

La pasarela identifica qué agente hace cada llamada y a qué sesión pertenece.

**Consecuencias (comprobables):**
- Cada agente se conecta con una credencial de prueba propia. Los agentes, con su nombre y su credencial, vienen definidos en la configuración de ejemplo: no hay pantalla ni API para darlos de alta.
- Un agente sin credencial válida no ve ninguna herramienta.
- El panel muestra el nombre del agente en la bandeja y en las sesiones.

### 4.5 Decisión sobre cada llamada

**Descripción:** este es el corazón de la pasarela. Realiza UJ-2 y UJ-3. Para cada llamada se aplica, en este orden:

1. **Bloquear:** si la política es bloquear, el agente recibe un error con el motivo y la llamada no llega al servidor.
2. **Solo lectura:** si la herramienta es de solo lectura y su política es permitir, la llamada pasa directa, sin supervisor.
3. **Supervisor:** cualquier otra llamada pasa por el supervisor.
4. **Permitir:** si la política es permitir (o hay permiso de sesión) y el veredicto es «encaja», la llamada pasa.
5. **Retener:** en cualquier otro caso (política de pedir aprobación, veredicto «no encaja» o «no disponible», o sesión sin objetivo) la llamada queda retenida, con el veredicto adjunto.

#### FR-11: Aplicar la decisión

La pasarela decide cada llamada con las reglas anteriores.

**Consecuencias (comprobables):**
- Una herramienta bloqueada nunca recibe la llamada y el agente recibe un error que dice que está bloqueada por política.
- Una llamada a una herramienta que no es de solo lectura, con política de permitir y veredicto «no encaja», queda retenida.
- En una sesión sin objetivo, toda llamada a una herramienta que no sea de solo lectura queda retenida.

#### FR-12: Errores comprensibles para el agente

Cada vez que una llamada no llega al servidor, el agente recibe un error con el motivo: bloqueada por política, rechazada (con el motivo del responsable), caducada o servidor no disponible.

**Consecuencias (comprobables):**
- El error se marca como error de herramienta en MCP, de forma que el agente no lo confunda con un resultado.

### 4.6 Aprobación en tiempo real (historia 3)

**Descripción:** las llamadas retenidas aparecen en una bandeja del panel en cuanto se producen. El agente queda a la espera de la decisión o de la caducidad. Realiza UJ-2.

#### FR-13: Bandeja de llamadas retenidas

El responsable ve las llamadas pendientes en tiempo real, con agente, sesión, objetivo, herramienta, argumentos, veredicto del supervisor y tiempo restante.

**Consecuencias (comprobables):**
- Una llamada retenida aparece en la bandeja en menos de 2 segundos, sin recargar la página.
- Los argumentos sensibles aparecen ocultos (FR-21).

#### FR-14: Aprobar o rechazar

El responsable puede aprobar o rechazar una llamada pendiente. Al rechazar puede escribir un motivo.

**Consecuencias (comprobables):**
- Al aprobar, la llamada llega al servidor y el agente recibe su resultado.
- Al rechazar, el agente recibe el motivo; si no se escribió ninguno, uno genérico.
- Si dos responsables deciden a la vez, vale la primera decisión y el segundo ve que ya estaba resuelta.

#### FR-15: Permiso de sesión

Al aprobar, el responsable puede conceder permiso de sesión para esa herramienta.

**Consecuencias (comprobables):**
- Las siguientes llamadas a esa herramienta en la misma sesión se tratan como si su política fuera permitir.
- El supervisor las sigue evaluando: si una no encaja, se retiene igual.
- El permiso no afecta a otras sesiones.

#### FR-16: Caducidad

Una llamada pendiente caduca al cumplir la espera máxima, de 5 minutos por defecto, que el administrador puede cambiar.

**Consecuencias (comprobables):**
- Al caducar, el agente recibe el error de caducada y la llamada sale de la bandeja como caducada.
- El agente no recibe un error por tiempo agotado antes de la decisión o de la caducidad, aunque su cliente tenga un límite menor (en Claude Code, 60 s por defecto). La forma de conseguirlo la decide la arquitectura (caminos A, B y C del anexo del brief).

#### FR-17: Cancelación por el agente

Si el agente abandona la espera mientras la llamada está pendiente, la llamada pasa a cancelada por el agente.

**Consecuencias (comprobables):**
- La bandeja la muestra como cancelada por el agente y ya no se puede aprobar.

### 4.7 Supervisor de intención (historia 4)

**Descripción:** el supervisor recibe el objetivo de la sesión y la llamada (herramienta, descripción y argumentos) y devuelve un veredicto con una explicación breve. Funciona en modo simulado o con un modelo local vía Ollama, sin claves de API. Realiza UJ-3.

#### FR-18: Evaluar la llamada

El supervisor da un veredicto «encaja» o «no encaja», con una explicación de una o dos frases, para cada llamada a una herramienta que no es de solo lectura.

**Consecuencias (comprobables):**
- El veredicto acompaña a la llamada en la bandeja y en el registro de eventos.
- En el conjunto de casos de prueba se cumple SM-3.

#### FR-19: Fallo del supervisor

Si el supervisor falla o no responde en su tiempo máximo (30 s por defecto, configurable), el veredicto es «no disponible» y la llamada queda retenida.

**Consecuencias (comprobables):**
- Con el supervisor apagado, ninguna llamada a una herramienta que no sea de solo lectura llega al servidor sin una aprobación.

#### FR-20: Modo simulado

El supervisor se puede configurar en modo simulado, con veredictos deterministas para las pruebas y la demo.

**Consecuencias (comprobables):**
- El sistema arranca y funciona de extremo a extremo sin Ollama.

### 4.8 Registro y reproducción de sesiones (historia 5)

**Descripción:** cada evento queda registrado, con los argumentos sensibles ocultos. El auditor recorre una sesión en orden. Realiza UJ-4.

#### FR-21: Registrar con los argumentos sensibles ocultos

La pasarela registra cada evento de cada sesión con fecha y hora, y oculta los argumentos sensibles antes de guardarlos.

**Consecuencias (comprobables):**
- Las llamadas que pasan directas también se registran.
- El registro de eventos normaliza el resultado de error: si el servidor no lo marca, se guarda como no error.

#### FR-22: Lista de sesiones

El auditor puede ver las sesiones con su agente, objetivo, inicio, número de llamadas y porcentaje de aprobación humana.

#### FR-23: Recorrer una sesión

El auditor puede recorrer una sesión evento a evento, en orden: qué pidió el agente, qué decidió la política, qué dijo el supervisor, quién aprobó o rechazó y qué devolvió la herramienta.

**Consecuencias (comprobables):**
- La sesión de la demo se puede recorrer entera desde el panel.

**Fuera de alcance:** exportar el registro de eventos, buscar texto dentro de las respuestas y borrar sesiones.

## 5. Requisitos no funcionales

- **NFR-1. La pasarela es el único camino.** En el despliegue con Docker Compose, el servidor de ejemplo solo es accesible desde la red de la pasarela; una llamada directa falla (SM-2). Con servidores reales, aislarlos es responsabilidad de quien los despliega.
- **NFR-2. Sin secretos.** El repositorio solo contiene un `.env.example` con valores de prueba. Las credenciales de los servidores no salen de la pasarela.
- **NFR-3. Arranque en un paso.** Todo el sistema (panel, API, pasarela, base de datos, supervisor y servidor de ejemplo) arranca con Docker Compose y datos de prueba, sin cuentas externas (SM-4).
- **NFR-4. Multiplataforma.** Funciona con Docker en Linux y en Windows con Docker Desktop.
- **NFR-5. Idioma.** El panel y los mensajes al agente están en español. Los textos del panel van separados del código para poder traducirlos después, sin traducciones en el MVP.

## 6. No objetivos

- Holdpoint no es un filtro de contenido: no inspecciona lo que devuelven las herramientas.
- No sustituye a los permisos de cada cliente; se suma a ellos.
- No gestiona usuarios, organizaciones ni facturación.
- No es un producto para producción en el MVP: sin alta disponibilidad ni despliegue en la nube.

## 7. Alcance del MVP

### 7.1 Dentro

- Las cinco historias: registrar un servidor, políticas, aprobación en tiempo real, supervisor de intención y reproducción de sesiones (FR-1 a FR-23).
- Tres roles con usuarios de prueba fijos.
- Un servidor de ejemplo (gestor de tareas) y Claude Code como agente de referencia.
- La configuración gestionada de Claude Code (`managed-settings.json`), solo documentada con un fichero de ejemplo.

### 7.2 Fuera

- Transporte stdio: solo HTTP.
- Recursos y prompts de MCP: solo herramientas.
- OAuth y gestión de usuarios: credenciales fijas de prueba.
- Separación por equipos o empresas, nube y alta disponibilidad.

### 7.3 Líneas futuras

- Freno automático cuando un agente entra en bucle.
- Hook de Claude Code para las herramientas propias del agente (terminal, edición de ficheros).
- Gestión de agentes desde el panel: alta, baja y rotación de sus credenciales. En el MVP, cada agente usa una credencial de prueba fija de la configuración (FR-10).
- Credenciales por usuario: la política depende de quién pide; puede ahorrar la aprobación de una persona, nunca la revisión del supervisor.
- Inspección de lo que devuelven las herramientas.
- Torre local para los servidores MCP del portátil.
- Comunidad: abrir el proyecto a contribuciones, con adaptadores para más servidores y clientes MCP.

### 7.4 Prioridad y recorte

Si el calendario aprieta, se recorta en este orden:

1. La historia 5 se simplifica: un listado de la sesión (FR-22) en lugar de recorrerla evento a evento (FR-23).
2. La historia 2 se simplifica: políticas manuales (FR-6), sin política propuesta según el riesgo (FR-7 y FR-8).
3. La aprobación en tiempo real (FR-13 a FR-17) y el supervisor (FR-18 a FR-20) no se recortan: son el núcleo del producto.

## 8. Métricas de éxito

**Principales**
- **SM-1. Flujo completo:** un agente con guion fijo intenta borrar una tarea, la llamada queda retenida, se aprueba desde el panel pasados más de 60 s y el agente recibe el resultado. Prueba de extremo a extremo en verde, más la misma comprobación a mano con Claude Code en la demo. Valida FR-11, FR-13, FR-14 y FR-16.
- **SM-2. Sin atajos:** una llamada directa al servidor MCP falla. Prueba de seguridad en verde. Valida NFR-1.
- **SM-3. Supervisor útil:** con el modelo de Ollama (no en modo simulado), el supervisor marca como «no encaja» al menos el 90 % de las llamadas contrarias al objetivo. Se mide con un conjunto de casos de prueba «objetivo + llamada» que incluye al menos 10 de esas llamadas. Valida FR-18.
- **SM-4. Arranque sin preguntas:** quien evalúa lo arranca con Docker Compose y el `.env.example` sin pedir ayuda. Valida NFR-3.
- **SM-5. Sesión reproducible:** la sesión de la demo se recorre entera desde el panel y muestra su porcentaje de aprobación humana. Valida FR-22 y FR-23.

**Contramétricas (no optimizar)**
- **SM-C1. Falsas alarmas del supervisor:** porcentaje de llamadas que encajan y que el supervisor marca como «no encaja». Se mide como SM-3, con el modelo de Ollama. Debe quedarse por debajo del 20 %, pero no a costa de SM-3: un supervisor que nunca retiene no sirve.
- **SM-C2. Porcentaje de aprobación humana:** no se busca reducirlo a cualquier precio. Bajarlo relajando políticas o el supervisor anula el producto.

## 9. Preguntas abiertas

1. **Camino de espera** (A, B o C): lo decide la arquitectura, con el requisito de FR-16. Solo el A está probado.
2. **Modelo del supervisor con Ollama:** qué modelo local da veredictos aceptables en un portátil sin GPU. Se decide al preparar los casos de prueba.
3. **Conjunto de casos de prueba del supervisor:** cuántos casos y quién los escribe. Propuesta: unos 20 pares «objetivo + llamada» sobre el gestor de tareas, al menos 10 contrarios al objetivo (SM-3).
4. **Límite de la sesión:** si una sesión corresponde a una conexión del agente (`Mcp-Session-Id`) o a otra cosa. Lo decide la arquitectura.
