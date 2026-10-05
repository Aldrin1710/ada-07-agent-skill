# Third-Party Skill Pre-Install Audit

Repository: https://github.com/addyosmani/agent-skills
Selected skill: code-review-and-quality
Version / commit inspected: main (latest via npx skills add)

## Purpose
Proporciona un proceso profesional para realizar revisiones de código y calidad (Code Review) antes de aprobar o fusionar cambios. Evalúa corrección, legibilidad, arquitectura, seguridad y rendimiento.

## Trigger / Description
Se activa cuando se solicita revisar código, un diff, o un PR. La descripción indica: "Use when the user asks to review code, assess PR quality, or verify changes against engineering standards."
*Límites:* No escribe comentarios en GitHub automáticamente ni hace merge sin confirmación explícita.

## Supporting References
Utiliza referencias compartidas a nivel de repositorio y plantillas específicas de revisión:
- `references/quality_gates.md`
- `references/security_checklist.md`
- `references/performance_guidelines.md`

## Tools / Commands / Permissions
- **Herramientas de lectura:** Utiliza herramientas MCP o CLI (como `gh pr diff` o `git diff`) para extraer los cambios.
- **Permisos requeridos:** Acceso de lectura al sistema de archivos local y acceso de solo lectura al repositorio remoto (GitHub MCP o GH CLI).
- **Ejecución:** Puede sugerir la ejecución de linters o pruebas unitarias estandarizadas.

## Supply-Chain Review
Antes de proceder con la instalación e inclusión en nuestro proyecto, se documenta la siguiente auditoría de cadena de suministro:

- **Pinning / Versión Inspeccionada:** Commit principal (main) de `addyosmani/agent-skills` al 5 de Octubre de 2026.
- **Permisos Requeridos:** Acceso de lectura al sistema de archivos local y lectura del repositorio remoto. No solicita escalación de privilegios de escritura en GitHub.
- **Scripts:** La Skill se instala vía `npx skills add addyosmani/agent-skills`, el cual clona el repositorio localmente. No ejecuta scripts de post-instalación destructivos (`postinstall`).
- **Secretos:** El análisis del código estático no muestra ofuscación de código, filtración de credenciales (API keys) ni tracking invasivo hacia servidores de terceros. Todo el procesamiento se hace a nivel del agente local.
- **Decisión de Confianza:** El repositorio es una fuente académica y reconocida en la comunidad. Las mitigaciones técnicas (lectura de diff en vez de escritura) avalan que el riesgo es sumamente bajo.

## Decision
[x] Install
[ ] Do not install
Reason: Supera la evaluación de supply-chain, no representa un riesgo para la base de código y es la herramienta indicada para cumplir la comparativa requerida en ADA-07.
