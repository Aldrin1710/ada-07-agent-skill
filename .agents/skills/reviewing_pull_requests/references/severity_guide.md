# Guía de severidad de hallazgos

## MUST FIX
Úsalo cuando el cambio:
- Viola un Requisito o Criterio de Aceptación.
- Introduce una regresión.
- Rompe pruebas exigidas por la especificación.
- Crea un problema de seguridad o de integridad de datos.
- Hace que aprobar el PR sea inseguro.

## SHOULD FIX
Úsalo cuando la funcionalidad puede operar, pero hay un problema significativo de mantenibilidad, capacidad de prueba, arquitectura o claridad.

## OPTIONAL
Úsalo para mejoras no bloqueantes que no afectan el comportamiento aprobado ni la seguridad.

Todo hallazgo debe incluir evidencia.
