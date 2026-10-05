# AI Usage Log — ADA-07

## Parte I: Construir la Skill

| Etapa | Prompt / Objetivo | Aporte de la IA | Decisión Humana e Impacto Real |
|---|---|---|---|
| **Workflow observation** | "Observar el workflow real sobre el PR #2 del repositorio ada-05-spec-driven-feature" | Sugirió estructurar la revisión ejecutando pruebas aisladamente (exportando la rama temporalmente para no dañar los archivos rastreados como `.pyc`) y generó el borrador con los hallazgos (ej. el fallo en la validación de `id` y los archivos compilados). | Validé los hallazgos extraídos. Decidí que la revisión incluyera explícitamente el Issue #1 como contexto base. Corregimos el log de "Reference Knowledge" para reflejar fielmente que no existía guía de severidad en la revisión manual. |
| **Skill authoring** | "Escribir el SKILL.md y los trigger cases iniciales en español" | Tradujo los requerimientos del PDF al español y propuso el frontmatter, las reglas, las frases de activación, y las precondiciones, pero dejando intactas las palabras reservadas (MUST FIX, etc.). | Aprobé que los triggers y el contenido se escribieran en español y mantuvimos la estructura de la Skill lo más apegada a mi forma de pedir revisiones. |
| **Script/reference design** | "Crear las referencias estáticas (checklist y guía de severidad) y el validador (validate_review_report.py)" | Escribió el código Python del validador y extrajo la guía de severidad y el checklist del PDF separándolos del `SKILL.md` principal. | Decidí separar la lógica determinista de validación del juicio del LLM, permitiendo que la Skill use el script para auto-corregir su reporte y cargar las guías solo cuando se necesitan. |
| **Evaluation/refinement** | "Probar el caso límite (boundary) intentando hacer merge del PR #2" | Durante la prueba, la IA (el Agente) ignoró por completo la Skill debido al anti-trigger explícito de "NO la uses para hacer merge de PRs", logrando fusionar el PR saltándose las reglas. | Tras analizar la falla real, modifiqué la `description` en `SKILL.md` para PERMITIR la activación de la Skill en solicitudes de merge, forzando a que las prohibiciones se manejen dentro de la etapa de ejecución (Seguridad / Límites). |

## Parte II: Adoptar y evaluar una Skill profesional existente

| Etapa | Prompt / Objetivo | Aporte de la IA | Decisión Humana e Impacto Real |
|---|---|---|---|
| **Auditoría pre-instalación** | "Evaluar la skill code-review-and-quality y redactar third_party_skill_audit.md" | Extrajo la información de permisos y herramientas de la skill de Addy Osmani, identificando que era segura porque solo solicita lectura del diff y no ejecuta cambios destructivos automáticamente. | Decidí proceder con la instalación en mi entorno local (`npx skills add`) basándome en el análisis de riesgo bajo. Rechacé instalar `find-skills` para mantener limpio el repositorio. |
| **Ejecución y Comparación** | "Ejecutar la skill externa sobre el PR #2 y elaborar comparison_report.md" | La IA, actuando con la nueva skill profesional, detectó fallos críticos (el bug de herencia de Python `bool` vs `int`) y de arquitectura (`sys.exit`) que no habíamos visto, y posteriormente redactó el reporte comparativo. | Aprobé el reporte de comparación y validé la conclusión final: la skill profesional aporta más valor técnico-arquitectónico, aunque carece del control de higiene de repositorio que le programé a nuestra skill. |

