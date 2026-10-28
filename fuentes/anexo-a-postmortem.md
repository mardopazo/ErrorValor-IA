# Anexo A. Plantilla de post-mortem sin culpa

**Nota para quien facilita:** iniciar la reunión leyendo en voz alta la Directiva Primaria (sección 1). El objetivo es entender **cómo el sistema permitió que ocurriera el error**, no quién apretó el botón.

---

## Reporte de post-mortem: [nombre corto del incidente]

| Campo | Valor |
|---|---|
| Fecha del incidente | DD/MM/AAAA |
| Líder de la investigación | [nombre] |
| Estado | En revisión / Completado |

## 1. Directiva Primaria

> "Independientemente de lo que descubramos hoy, se parte de la premisa de que todos hicieron el mejor trabajo posible con la información, las herramientas, el tiempo y los recursos disponibles en ese momento."

*Adaptada de la "Directiva Primaria" de las retrospectivas (Norm Kerth, 2001).*

## 2. Resumen ejecutivo

Breve descripción de qué pasó, qué impacto tuvo en usuarios o sistema y cómo se resolvió a grandes rasgos.

- **¿Qué falló?**
- **Impacto:** (ej.: el 15 % de las transacciones falló durante 2 horas).

## 3. Cronología de los hechos

Línea de tiempo objetiva. Evitar nombres propios: usar roles o acciones del sistema.

- 14:00 – Se despliega la versión X en producción.
- 14:05 – El sistema de alertas detecta un pico de errores 500 en el módulo de pagos.
- 14:12 – El equipo de guardia recibe la notificación e inicia el triaje.
- 14:30 – Se identifica que el cambio en la variable de entorno `DB_TIMEOUT` causó el bloqueo.
- 14:45 – Se realiza rollback a la versión anterior. Sistema estable.

## 4. Análisis de causa raíz (los 5 ¿por qué?)

Método para llegar al problema sistémico. Sirve como guía, no como regla: un incidente suele tener **varias** causas, que se recogen en la sección 6.

1. ¿Por qué fallaron los pagos? *Porque la base de datos no respondió a tiempo.*
2. ¿Por qué no respondió a tiempo? *Porque el parámetro de timeout se redujo drásticamente.*
3. ¿Por qué se redujo? *Porque se unificó la configuración con el entorno de testing.*
4. ¿Por qué se unificó sin validar el impacto? *Porque la revisión de variables de entorno es manual y no está documentada en el pipeline.*
5. ¿Por qué es manual? *Porque no hay una herramienta de gestión de configuración que valide límites según el entorno.*

## 5. Participación de IA en el cambio

*Completar si el código involucrado fue generado o asistido por IA. Esta sección no busca atribuir culpa a la herramienta ni a la persona: busca entender qué parte del proceso quedó sin comprensión humana.*

- **Herramienta y contexto:** ¿qué herramienta se usó y qué contexto (archivos, requisitos, restricciones) recibió?
- **Prompt o instrucción:** ¿qué se pidió exactamente? ¿Faltaba información de la regla de negocio?
- **Qué se revisó realmente:** ¿hubo lectura línea por línea, tests propios, prueba manual? ¿Quién aprobó?
- **Comprensión:** ¿el equipo hoy puede explicar qué hace ese cambio y qué casos no cubre?
- **Casos no contemplados:** ¿qué situaciones borde o de excepción no se consideraron?

## 6. Factores contribuyentes (el entorno)

¿Qué elementos del entorno o de las herramientas facilitaron que el error ocurriera?

- **Falta de visibilidad:** el monitoreo no reflejó la saturación de conexiones de inmediato.
- **Documentación desactualizada:** el manual de despliegue no mencionaba las dependencias de esa variable.
- **Presión de plazos o de métricas:** (completar si corresponde).

## 7. Dónde tuvimos suerte y qué todavía no sabemos

- **Suerte:** ¿qué pudo haber salido peor y no salió? (ej.: el incidente ocurrió fuera de la hora pico).
- **Incógnitas:** ¿qué preguntas quedan abiertas? ¿Qué no podemos explicar todavía?

## 8. Plan de acción y mitigación

Tareas concretas, **con responsable y fecha**, para que el sistema sea más robusto. **Ninguna acción puede ser "que el desarrollador tenga más cuidado".**

| Acción preventiva o correctiva | Dueño | Prioridad (Alta / Media / Baja) | Fecha objetivo | Ticket |
|---|---|---|---|---|
| Automatizar la validación de variables en el pipeline de CI/CD | [rol o nombre] | Alta | DD/MM | PROD-1234 |
| Configurar alertas específicas para el pool de conexiones de la base de datos | [rol o nombre] | Media | DD/MM | PROD-1235 |
| Actualizar la documentación de arquitectura del módulo de pagos | [rol o nombre] | Baja | DD/MM | PROD-1236 |

## 9. Aprendizaje a compartir

Una o dos frases que el equipo pueda llevarse, redactadas sin nombres propios y publicables.

---

*Un post-mortem sin acciones cerradas es un ritual vacío. Revisar el estado de la tabla de la sección 8 en la siguiente retrospectiva.*
