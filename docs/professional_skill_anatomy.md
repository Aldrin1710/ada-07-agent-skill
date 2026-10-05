# Reverse Engineering: `code-review-and-quality`

## Estructura y Arquitectura General
La skill `code-review-and-quality` (de la colección `addyosmani/agent-skills`) adopta un enfoque mucho más extenso y doctrinario para la revisión de código que la skill construida en la Parte I. 
Su estructura principal no se basa en un flujo paso-a-paso estricto, sino en **reglas de ingeniería, principios de honestidad y checklist de dominios** (Arquitectura, Seguridad, Rendimiento, Legibilidad, Dependencias).

### Componentes Clave:
- **Jerarquía de Desacuerdos:** Establece reglas claras sobre qué tiene prioridad al resolver conflictos (1. Datos, 2. Guías de estilo, 3. Diseño de software, 4. Consistencia).
- **Reglas de Honestidad:** Instruye explícitamente al LLM a no ser un "sello de goma" (rubber-stamp) y a empujar en contra de enfoques con problemas claros ("sycophancy is a failure mode").
- **Disciplina de Dependencias:** Un proceso detallado de 5 pasos antes de añadir cualquier dependencia.
- **Checklist Centralizado:** Evalúa Corrección, Legibilidad, Arquitectura, Seguridad, Rendimiento y Verificación.
- **Referencias Externas:** Llama a otros archivos (ej. `security-checklist.md`, `performance-checklist.md`) para revisiones profundas.

## Comparación con Nuestra Skill (`reviewing-pull-requests`)

| Característica | Nuestra Skill (Parte I) | Skill Externa (`code-review-and-quality`) |
| :--- | :--- | :--- |
| **Enfoque de Revisión** | **Basado en Especificaciones (Spec-Driven)**. Se centra en verificar que el PR cumpla estrictamente los Requerimientos y las Pruebas locales definidas en el proyecto. | **Basado en Calidad y Estándares (Standard-Driven)**. Se centra en la calidad general del código, arquitectura, seguridad, legibilidad y disciplina de dependencias. |
| **Flujo de Trabajo** | Determinista (1 al 10). Ejecuta validación local (`validate_review_report.py`) para forzar un formato estricto. | Filosófico y guiado por checklists. Confía más en el razonamiento del LLM y en los principios de ingeniería documentados. |
| **Formato de Salida** | Plantilla obligatoria validada por un script externo. Clasifica por Severidad (MUST FIX, SHOULD FIX). | Checklist abierto de revisión, con veredictos (Approve o Request changes). |
| **Manejo de Dependencias** | No especificado; se delega a los requerimientos del proyecto. | Altamente prescriptivo (Evitar dependencias, leer changelogs, aislamiento, etc.). |
| **Integración con otros archivos** | `severity_guide.md`, `review_checklist.md`, `review_report_template.md`. | `security-checklist.md`, `performance-checklist.md`. |

## Aprendizajes Clave
1. **Instrucciones Anticomplacencia:** La skill externa incluye directivas brillantes como *"Push back on approaches with clear problems. Sycophancy is a failure mode"*. Esto es vital para LLMs, que tienden a ser complacientes y aprobar código mediocre.
2. **Tablas de Racionalizaciones (Red Flags):** Usa una tabla para enseñar al LLM a refutar excusas comunes (ej. "Lo limpio después" -> "El después nunca llega").
3. **Escalabilidad:** Mientras nuestra skill es ideal para asegurar que una feature específica cumpla un ticket, la skill externa es mejor como un **Quality Gate** global para cualquier Pull Request en cualquier proyecto.

**Conclusión:** Ambas skills son complementarias. Nuestra skill actúa como un verificador de cumplimiento funcional (Acceptance Criteria), mientras que la de Addy Osmani actúa como un auditor de ingeniería de software clásico.
