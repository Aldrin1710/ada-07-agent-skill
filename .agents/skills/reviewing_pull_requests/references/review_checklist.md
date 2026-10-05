# Checklist de revisión de PR

## Requisitos / Especificación
- El comportamiento modificado corresponde a un Requisito / Criterio de Aceptación existente.
- No se introduce ninguna regla de negocio no documentada.
- La SPEC y la implementación son consistentes.

## Código
- El cambio es enfocado y comprensible.
- El manejo de errores es apropiado.
- No se mezclan refactorizaciones no relacionadas en el PR.
- Las dependencias están justificadas.

## Pruebas
- El comportamiento nuevo tiene evidencia automatizada.
- Los casos borde importantes están cubiertos.
- El comportamiento existente no se debilita.
- Las pruebas verifican comportamiento, no solo detalles de implementación.

## Arquitectura
- El cambio respeta los límites documentados.
- `ARCHITECTURE.md` se actualiza si el diseño cambió.

## Seguridad
- No hay secretos ni credenciales.
- No hay permisos innecesarios.
- La entrada externa se valida donde se requiere.

## Evidencia
- Los hallazgos citan evidencia de archivo, prueba o requisito.
