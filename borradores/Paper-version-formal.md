# Gestionar el error en la era de la IA: del panóptico a la cultura del aprendizaje

*Título de trabajo. Ver alternativas en `00-NotasDeRevision.md`.*

**Autor:** Martín [apellido]
**Versión:** borrador v2 — 28/10/2026

---

## Resumen

El desarrollo asistido por IA acelera la producción de código por encima de la capacidad humana de revisarlo, comprenderlo y hacerse cargo de él. El análisis que antes ocurría antes de producción (caminos posibles, situaciones borde, reglas de negocio) se traslada a las aplicaciones ya en uso. Este trabajo sostiene que la respuesta de la gestión no puede ser más control, sino un entorno donde el error sea visible, discutible y valorado como fuente de conocimiento. Se analiza cómo los dispositivos habituales de monitoreo del trabajo de desarrollo empujan a ocultar los errores, se propone un marco que distingue culpa de responsabilidad, y se ofrecen tres líneas de acción con dos herramientas concretas: una plantilla de post-mortem sin culpa (Anexo A) y pautas para dailys sin vigilancia (Anexo B).

---

## 1. El problema: el código viaja más rápido que la comprensión

El código se produce a una velocidad mayor que la que permite evaluarlo, analizarlo y revisarlo. Esto ocurre en todas las instancias de control:

- **En el debug del propio desarrollador**, que acepta lo que "parece funcionar".
- **En los tests**, que las IAs tienden a orientar al camino feliz.
- **En los Pull Requests**, que muchas veces no se revisan de forma exhaustiva: se hace una lectura en diagonal y se verifica que compile.

El resultado es que el momento de análisis previo (caminos posibles, situaciones borde, reglas de negocio) se traslada a producción. Los problemas aparecen con el sistema ya en uso, frente a los usuarios.

Ariel Fabian (2026) denomina a este fenómeno **"efecto bullet"**, por analogía con el ajedrez de ritmo ultrarrápido, donde el tiempo disponible anula el cálculo profundo. Su tesis es que el problema no es la herramienta sino el ritmo: una persona necesita tiempo para entender la lógica de un software y no puede hacerlo a la velocidad con la que un modelo genera texto. Cuando eso ocurre se acumula **deuda cognitiva**: sistemas que funcionan, pero que nadie en el equipo sabe modificar con seguridad, y cuyas fallas pueden llegar directo a producción. Fabian respalda el diagnóstico con evidencia reciente que él cita:

- En 196.000 Pull Requests, la tasa de revisión humana profunda cayó del 48 % al 21 % (He y Vasilescu, 2026).
- En organizaciones con adopción masiva y sin reglas de IA, los cambios aprobados sin revisión previa subieron un 76,3 % y los incidentes críticos en producción un 125,4 % (Faros AI, 2026; patrón observacional).
- En un ensayo controlado con desarrolladores, quienes delegaron en la IA mostraron 17 puntos porcentuales menos de comprensión conceptual (Shen y Tamkin, 2025).

Propone cinco reglas de trabajo adaptadas del ajedrez (control de ritmo, la regla del 10 + 10, un "peaje cognitivo" antes del commit, auditoría preventiva y el modelo centauro) y reconoce expresamente una limitación que este trabajo toma como punto de partida: *ninguna regla técnica funciona de forma aislada si los indicadores de seguimiento solo contemplan el volumen de entrega inmediato*; cuando el apuro del calendario desplaza el espacio de análisis, cualquier control corre el riesgo de convertirse en un paso formal que se completa por cumplir.

Este trabajo toma ese diagnóstico como punto de partida y se concentra en **la otra mitad del problema**: qué le pasa a un equipo cuando, además de la presión de velocidad, opera en un entorno donde equivocarse tiene consecuencias. Las reglas de ritmo y asimilación (el peaje cognitivo, el 10 + 10) solo funcionan si el equipo puede decir "no entiendo esto" sin costo y si lo que se mide no premia la velocidad aparente. Esa condición no la garantiza ninguna regla técnica: es una decisión de gestión.

## 2. Hipótesis

> Los equipos que hacen visible, analizable y valorado el error comprenden mejor lo que entregan; esa comprensión es la principal mitigación disponible frente a la deuda cognitiva del código generado con IA.

Se deriva un desafío para quienes gestionan equipos: generar un entorno de **revisión, replanteo, cooperación y transparencia** (disclosure) sobre lo que se sabe y lo que no se sabe del modelo, la arquitectura y las funcionalidades en desarrollo.

Se trata a la vez de evitar la deuda cognitiva de usar código que no se comprende o no se revisó, que produce **ausencia de propósito arquitectónico**: equipos que desarrollan y dan soporte a sistemas construidos muy rápido pero que nadie comprende y de los que nadie es dueño.

## 3. Por qué los equipos ocultan el error

### 3.1 Estilos de conducción

Existen distintos estilos de conducción de equipos de desarrollo. Algunos buscan al responsable del error. Otros no le dan relevancia, pero miden la "productividad" de cada desarrollador a partir, justamente, de los errores que comete.

También hay que desconfiar de una tercera actitud, aparentemente sana: *"no importa quién se equivocó, no busco responsables sino soluciones"*. Sin quererlo, esa postura **vela el error en función de la solución**: se arregla, pero no se enseña ni se explica nada sobre el desarrollo ni sobre el porqué del error. El problema se resuelve y el aprendizaje se pierde.

### 3.2 El panóptico como metáfora de gestión

Los excesos de control (reuniones permanentes donde hay que dar cuenta de avances y demoras) producen un efecto contrario al buscado: se *esconden* los problemas o se escribe código que "salva" lo que se ve sin que se sepa con precisión qué hace ni qué otros inconvenientes puede traer.

Michel Foucault, en *Vigilar y castigar*, describe el panóptico como un dispositivo que se aplica a escuelas, hospitales, fábricas y cuarteles para ordenar, corregir y normalizar conductas. Su eficacia está en que el control se **internaliza**: como nunca se sabe con certeza si se está siendo observado en ese momento, se termina actuando como si siempre se estuviera.

Byung-Chul Han (*Psicopolítica*; *La sociedad del cansancio*) sostiene que el poder contemporáneo ya no funciona principalmente por disciplina externa sino por exposición voluntaria y autoexplotación: el panóptico digital es más sutil y más eficaz porque no necesita un vigilante. Esa diferencia importa para este trabajo: en los equipos de desarrollo, la presión no suele venir de un jefe que mira, sino de un tablero que se actualiza y de una disponibilidad que se exhibe.

> **Alcance de la metáfora.** No se afirma que Jira, las dailys o el pair programming sean vigilancia en sí mismos. Se afirma que, **usados como instrumento de control de la persona y no como herramienta de coordinación del trabajo**, producen los efectos descriptos aquí. Ver sección 8.

### 3.3 Las herramientas como parte del dispositivo

| Herramienta o práctica | Propósito declarado | Efecto real posible |
|---|---|---|
| Aplicaciones en segundo plano (Teams, Discord) | Facilitar la comunicación inmediata y resolver bloqueos | Monitoreo del tiempo de inactividad |
| Canales de voz permanentes | Simular la cercanía de la oficina física en remoto | Pérdida de privacidad y de espacio de concentración |
| Métricas de repositorio (commits, líneas, PRs) | Medir la estabilidad y el avance del proyecto | Cuantificación del esfuerzo humano como si fuera rendimiento |

Tres ejemplos de cómo se concreta:

- **Presencia constante.** Los indicadores de estado ("Disponible", "Ausente", "En una reunión") funcionan como las ventanas iluminadas de las celdas de Bentham. Quien trabaja sabe que su disponibilidad es visible en tiempo real, y eso crea la presión de estar "siempre activo".
- **Reuniones y voz permanente.** Las dailys extendidas, el pair programming forzado y los canales de voz abiertos todo el día se justifican como "colaboración orgánica", pero exponen el tiempo y el ritmo de pensamiento de quien programa y, con ellos, sus posibles errores.
- **El panóptico en el código.** El historial de commits (frecuencia, líneas, hora de entrega) y las métricas de gestión (tiempo por tarea, burndown) actúan como registros del rendimiento. Importa más la cantidad de commits o PRs que la decisión arquitectónica de organizarlos para que sean comprensibles y revisables.

**El agravante de la IA.** La generación asistida infla exactamente las métricas de actividad: más commits, más líneas, más PRs en menos tiempo. Si esas métricas sirven para evaluar, miden cada vez más ruido, y cada vez menos comprensión. Además, las métricas de *uso* de la IA (aceptación de sugerencias, volumen generado) empiezan a convertirse en un nuevo tablero de control. [PENDIENTE: fuente o ejemplo concreto.]

### 3.4 Consecuencias: la autocensura

La consecuencia más profunda no es el castigo posible sino la **autocensura**. En el desarrollo de software se manifiesta en comportamientos específicos:

- **Teatralidad de la productividad.** Se priorizan las tareas visibles (mover tarjetas, escribir en canales públicos) por sobre el trabajo profundo (*deep work*) y la resolución de problemas complejos, que requieren tiempo de desconexión.
- **Ansiedad de disponibilidad.** El temor a figurar como "Ausente" fragmenta la atención: se interrumpe el flujo para responder alertas, sacrificando calidad de código para validar presencia.
- **Ilusión de autonomía.** Las metodologías ágiles se presentan como marcos de autoorganización, pero al depender de un monitoreo estricto de datos y de reuniones constantes, la autonomía se vuelve **autovigilancia coordinada**: el equipo se disciplina a sí mismo para cumplir con la métrica del tablero.

Programar requiere abstracción y, sobre todo, comprensión del problema. El panóptico digital exige, en cambio, visibilidad y ruido comunicativo. El resultado es código que hoy funciona y que mañana no sabemos explicar, además de un efecto de agotamiento (burnout) en los equipos.

## 4. El error como objeto de conocimiento

Para construir un entorno amigable con el error y con lo que se desconoce, se toman como referencia las actitudes metodológicas de los ambientes de aprendizaje. En las teorías del aprendizaje, el error forma parte del proceso de construcción del conocimiento. No es necesariamente una falla ni un fracaso: es, muy probablemente, **evidencia de una hipótesis en crisis**, la lógica que hay detrás del error.

La estrategia fundamental es **aceptar, valorar y discutir** el error: no justificarse ni defenderse, sino explicarlo. Y no solo en lo funcional, sino en **la lógica que llevó a producirlo**.

Los orígenes posibles del error son múltiples:

- un prompt mal formulado;
- un análisis deficiente de la regla de negocio que el software debe cumplir;
- situaciones borde no contempladas;
- entornos con condiciones de excepción (sin conectividad, caída de base de datos, etc.);
- una infraestructura que no soporta adecuadamente los requerimientos.

Solo valorando y aceptando el error se comprende el modelo y los flujos del software en acción. Eso permite, además, anticipar con más precisión problemas potenciales y diagnosticar con más eficacia los que aparezcan.

## 5. Responsabilidad sin culpa

La cultura sin culpa recibe una objeción previsible: si nadie es culpable, ¿quién se hace cargo? La respuesta de este trabajo es que **culpa y responsabilidad son cosas distintas**, y que una cultura del error necesita la segunda precisamente para poder prescindir de la primera.

| | Culpa | Responsabilidad |
|---|---|---|
| **Mira hacia** | Atrás: el daño ya causado | Adelante: la reparación y la prevención |
| **Pregunta** | ¿Quién lo hizo? ¿Qué merece? | ¿Qué pasó? ¿Quién necesita qué? ¿Qué cambiamos? |
| **Efecto en el equipo** | Se oculta información | Se comparte información |
| **Resultado** | Castigo | Aprendizaje y mejora del sistema |

Esta distinción tiene antecedentes. Sidney Dekker, en su trabajo sobre *cultura justa* (*Just Culture: Balancing Safety and Accountability*), contrapone una versión **retributiva**, que clasifica las conductas y pregunta qué castigo corresponde, con una versión **restaurativa**, que pregunta quién resultó afectado, qué necesita y a quién le corresponde atenderlo. John Allspaw, al introducir los post-mortems sin culpa en Etsy (2012), planteó la misma idea en términos de gestión: se trata de mirar los errores "con una perspectiva de aprendizaje" y de equilibrar seguridad y responsabilidad, no de eliminar esta última.

Aplicada al desarrollo con IA, la distinción produce una regla concreta:

> **Quien aprueba se hace responsable.** Debe poder explicar qué hace el cambio, por qué lo hace y qué casos no cubre, aunque no lo haya escrito. "Fue un error de la IA" no es una explicación válida, ni para quien desarrolla ni para quien gestiona.

La regla no castiga el error: **señala la opacidad**. Si alguien no puede explicar un cambio, la consecuencia esperable no es una sanción sino una acción de reparación: leerlo en conjunto, escribir la prueba que falta, o desandar el cambio. Lo que se cuida es la comprensión del equipo, no la reputación de nadie.

Esto no implica desconocer que existen conductas que ninguna cultura sana ampara, como la negligencia deliberada o el sabotaje; el enfoque de este trabajo las da por fuera de su alcance. Lo que sí propone es una precaución previa a cualquier atribución individual: antes de señalar una conducta de riesgo en una persona, hay que preguntarse si el sistema la premia. Quien aprueba un PR sin leerlo en un entorno donde se miden los PRs cerrados por semana no está violando las reglas: las está cumpliendo.

Por último, hay una forma de irresponsabilidad que esta cultura sí busca eliminar: **ocultar el error**. Quien lo oculta no se hace cargo ni de la falla ni de lo que el equipo podría aprender de ella. Por eso la seguridad psicológica no es lo opuesto de la responsabilidad: es su condición de posibilidad.

## 6. Propuesta: tres líneas de acción

La gestión de los equipos debe pasar de una cultura del **monitoreo de presencia** a una cultura del **impacto y la seguridad psicológica**. En software, el error no es una falla del programador: es un subproducto inevitable de la exploración, de los intentos de resolver problemas y de la innovación. Al aplicar estas estrategias, la gestión deja de ser la torre central de vigilancia y se vuelve **facilitadora de infraestructura y confianza**, de modo que el desarrollo vuelva a ser una disciplina creativa e iterativa.

### 6.1 Reconfigurar la comunicación y la presencia

- **Soberanía sobre el estado de disponibilidad.** Una política explícita de "sin indicadores": normalizar que los desarrolladores cierren la mensajería o activen "No molestar" en bloques de 3 o 4 horas para el trabajo profundo.
- **Comunicación asincrónica por defecto.** Las respuestas a mensajes pueden demorar 1 o 2 horas sin que eso signifique falta de compromiso. Para lo urgente, se define un canal de escalamiento específico (por ejemplo, una llamada).
- **Sin salas de voz permanentes.** Reemplazarlas por "horas de oficina" acotadas (por ejemplo, 30 minutos al inicio o al final del día) o por salas de diseño puntuales. La colaboración debe ser un acto consciente, no una exposición continua.

### 6.2 Redefinir las métricas

- **Impacto, no actividad.** Evitar líneas de código, horas conectadas o cantidad de commits como evaluación de rendimiento. Medir el valor entregado al usuario, la estabilidad del sistema, el cumplimiento de los objetivos del sprint y, sobre todo, **la comprensión técnica de los aportes al sistema**.
- **El tablero como mapa, no como látigo.** Las herramientas de gestión sirven para que el equipo coordine dependencias, no para que se microgestione el tiempo de cada tarea. Si una tarjeta se retrasa, la pregunta de gestión es *"¿cómo te ayudo a destrabarla?"* y no *"¿por qué tardaste más?"*. Si la traba revela un dato relevante del sistema, se analiza a fondo y, una vez resuelta, se comparte el hallazgo con el equipo.

### 6.3 Institucionalizar el error como proceso natural

Para que el equipo deje de ocultar fallas por temor a la vigilancia, el error debe ser visible, analizado y entendido como fuente de mejora.

- **Post-mortems sin culpa.** Ante un fallo grave en producción o un bug crítico, la reunión de análisis se concentra en cómo y por qué falló el sistema, no en quién cometió el error. El objetivo es identificar fallas de proceso, falta de pruebas automatizadas o ambigüedad en los requerimientos. En equipos que usan IA, el análisis incluye el **prompt, el contexto entregado y qué se revisó realmente** (ver plantilla en el Anexo A).
- **Entornos de experimentación seguros.** Fomentar ambientes locales o de staging robustos donde romper el código sea barato y seguro. Si el desarrollador sabe que un error en su rama no tiene consecuencias punitivas ni exposición pública negativa, se anima a buscar mejores soluciones arquitectónicas.
- **Sesiones de aprendizaje compartido (FailFaire).** Espacios mensuales donde líderes técnicos y desarrolladores senior exponen sus peores errores recientes y lo que aprendieron. Ver vulnerables a los referentes desarma la ilusión panóptica de la perfección obligatoria.
- **Dailys sin vigilancia.** La daily deja de ser un reporte individual y pasa a ser una inspección del trabajo del equipo (ver pautas en el Anexo B).

## 7. Cómo saber si funciona

Una propuesta sobre métricas debería poder medirse, con cuidado de no reproducir el problema que critica. Indicadores posibles:

- **Estabilidad del delivery:** tasa de fallos por cambio y tiempo de recuperación (métricas DORA).
- **Aprendizaje:** cantidad de post-mortems realizados y de acciones preventivas efectivamente cerradas.
- **Comprensión:** porcentaje de cambios en los que quien aprueba pudo explicar el cambio, relevado por muestreo y no de forma individual.
- **Clima:** una encuesta breve y anónima de seguridad psicológica (por ejemplo, la escala de Edmondson).

Medir la adopción de una cultura sin culpa con instrumentos individuales y permanentes crearía un panóptico nuevo. Por eso los indicadores se relevan **a nivel de equipo, por muestreo y con propósito declarado**.

## 8. Límites y objeciones

Una propuesta de gestión debe poder discutirse. Estas son las objeciones más fuertes que reconocemos y cómo las respondemos o las dejamos abiertas.

### 8.1 No todo control es vigilancia

Un equipo necesita coordinarse, y los equipos remotos más todavía. La comunicación asincrónica ahorra interrupciones pero tiene costos: demoras, malentendidos, decisiones que esperan una respuesta. Algunos momentos (un incidente en curso, un diseño en disputa) requieren una conversación en tiempo real. Por eso la propuesta no es eliminar la sincronía sino **hacerla deliberada**: encuentros con propósito y duración acotados, y canales de escalamiento claros para lo urgente.

### 8.2 Las herramientas no son el problema

Ni Jira, ni las dailys, ni el pair programming son vigilancia en sí mismos. El mismo tablero puede ser un mapa que ayuda a coordinar o un látigo que mide minutos. La metáfora del panóptico describe un **uso** de las herramientas (control de la persona), no las herramientas.

### 8.3 Registro para auditar no es lo mismo que registro para evaluar

Muchos entornos, en especial los regulados, **exigen trazabilidad**: quién cambió qué y cuándo. La propuesta no pide renunciar a ese registro. Pide separar su finalidad: el historial puede servir para auditar y para reconstruir un incidente, pero no para medir el desempeño de las personas ni para armar rankings de errores.

### 8.4 Trazabilidad como responsabilidad, no como culpabilidad

Rastrear qué cambio originó un incidente y quién lo aprobó es una práctica legítima y necesaria. Los diseños experimentales sobre desarrollo con IA, como el protocolo propuesto por Fabian (2026), la contemplan al seguir el commit causante de una falla y registrar la autoría del código. Desde la perspectiva de este trabajo, esa auditoría se entiende como **responsabilidad** (la capacidad de reconstruir qué pasó, entender por qué y reparar) y no como **culpabilidad** (*blame*). La diferencia no está en el dato sino en su uso: el mismo historial sirve para aprender o para señalar. Para que siga siendo lo primero, los indicadores se agregan a nivel de equipo, se informan antes de empezar y no se utilizan para evaluar personas.

### 8.5 Un equipo no cambia solo

Un equipo puede adoptar dailys sin vigilancia y post-mortems sin culpa, pero si la organización que lo rodea evalúa por tickets cerrados, líneas generadas o velocidad de entrega, la cultura sin culpa se vuelve un barniz. Fabian (2026) hace una advertencia equivalente respecto de sus reglas: ningún control funciona de forma aislada si los indicadores solo premian el volumen inmediato. La propuesta exige entonces **coherencia entre niveles**: lo que dice el equipo, lo que mide la gestión y lo que recompensa la organización.

### 8.6 El riesgo del ritual vacío

Un post-mortem sin culpa que no produce acciones cerradas es una nueva forma de teatro. Lo mismo vale para una daily "sin vigilancia" que sigue siendo un reporte individual con otro nombre. Por eso los anexos incluyen acciones con dueño y fecha, y la revisión periódica de su cumplimiento.

### 8.7 Alcance y evidencia

La propuesta se apoya en teoría (aprendizaje, estudios sobre cultura justa y seguridad psicológica) y en experiencia profesional en la gestión de equipos de desarrollo. **Todavía no se contrastó con datos propios.** Tampoco hay una única medida de "cultura del error", y es probable que el contexto (tamaño del equipo, sector, grado de regulación, madurez) cambie su efecto.

Como línea futura, el diseño factorial de Fabian (reserva de tiempo de asimilación y peaje cognitivo) podría ampliarse con un tercer factor: el clima del equipo respecto del error. La pregunta empírica sería si las reglas de ritmo y comprensión funcionan mejor, igual o peor en equipos con seguridad psicológica alta. Es una hipótesis, no un resultado.

## 9. Conclusión

El desarrollo con IA no creó el problema del error en los equipos de software, pero lo volvió más costoso. Cuando el código se produce más rápido de lo que se lo puede comprender, lo que no se revisó llega a producción, y lo que nadie entiende no tiene dueño. Las reglas de ritmo y asimilación, como las que propone Fabian, atacan esa velocidad. Este trabajo sostiene que esas reglas necesitan una condición previa: **un entorno donde decir "no entiendo esto" no tenga costo.**

Ese entorno no se logra con más control. Las herramientas de monitoreo, las reuniones permanentes y las métricas de actividad, usadas para vigilar a la persona y no para coordinar el trabajo, empujan a esconder los problemas y a producir código que funciona sin que nadie sepa por qué. La alternativa que se propone se apoya en tres ideas:

1. **El error es evidencia de una hipótesis en crisis**, y por lo tanto un objeto de análisis y de aprendizaje, no un motivo de vergüenza.
2. **Responsabilidad no es culpa.** Quien aprueba se hace responsable de entender lo que entrega; el análisis de un fallo se concentra en cómo el sistema lo permitió.
3. **Lo que se mide y se recompensa tiene que ser coherente con lo que se dice.** Sin eso, la cultura sin culpa es una declaración sin efecto.

Las herramientas concretas (post-mortems sin culpa, dailys centradas en el tablero, métricas de impacto, espacios para compartir errores) son un punto de partida para probar en equipos reales y ajustar con datos. Esta propuesta no tiene todavía evidencia propia, y reconocerlo es parte de su coherencia: un modelo que pide valorar el error debería poder equivocarse en público.

La velocidad de la IA no se va a detener. Lo que sí está en manos de quienes gestionan equipos es decidir qué pasa cuando alguien se equivoca: si se esconde o si se estudia. De esa decisión depende que el equipo siga comprendiendo lo que construye.

---

## Referencias

> Lista preliminar. **Verificar** cada ítem (año, edición, URL o DOI) antes de publicar.

- Fabian, A. (2026). *El Efecto Bullet: Deuda Cognitiva y la Ilusión de la Velocidad en la Era de la IA.* Zenodo. DOI 10.5281/zenodo.23641059. https://arfab.github.io/efectobullet/
- Faros AI (2026). *The Speed Trap: How Generative AI Impacts Software Quality and Production Incidents.* Faros Engineering Report. (Citado por Fabian; no consultado directamente.)
- He, H. y Vasilescu, B. (2026). *AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise "2x" Mandate.* https://arxiv.org/abs/2607.01904 (Citado por Fabian; no consultado directamente.)
- Shen, J. H. y Tamkin, A. (2025). *How AI Impacts Skill Formation.* Anthropic Research. https://arxiv.org/abs/2601.20245 (Citado por Fabian; no consultado directamente.)
- Foucault, M. *Vigilar y castigar: nacimiento de la prisión.*
- Foucault, M. *Microfísica del poder.*
- Han, B.-C. *Psicopolítica.*
- Han, B.-C. *La sociedad del cansancio.*
- Dekker, S. *Just Culture: Balancing Safety and Accountability.* [PENDIENTE: editorial, año y edición.]
- Allspaw, J. (2012). Blameless PostMortems and a Just Culture. Etsy, Code as Craft. [PENDIENTE: verificar URL.]
- Edmondson, A. (1999). Psychological safety and learning behavior in work teams. *Administrative Science Quarterly.*
- Kerth, N. (2001). *Project Retrospectives: A Handbook for Team Reviews.* (Directiva Primaria.)
- DORA / *Accelerate* (Forsgren, Humble y Kim).
- Schwaber, K. y Sutherland, J. *La Guía de Scrum* (2020).

## Anexos

- **Anexo A.** Plantilla de post-mortem sin culpa (`02-AnexoA-PostMortem.md`).
- **Anexo B.** Pautas para dailys sin vigilancia (`03-AnexoB-Dailys.md`).
