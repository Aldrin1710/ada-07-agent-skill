# Workflow Observation

> Ejecución manual / agent-assisted del workflow "PR Readiness Review" sobre el
> PR #2 de `Aldrin1710/ada-05-spec-driven-feature` (rama `new-branch` -> `main`,
> "Resuelve el issue de validacion. Fixes #1"). Este documento describe lo que
> realmente se hizo; la Skill se diseña a partir de esto.

## Trigger
Cuando el usuario pide revisar un PR / rama / diff antes de la revisión humana:
"Review PR #N", "is this PR ready for review?", "check this PR against the spec
and tests". No aplica a: implementar un issue, hacer merge, comentar/aprobar en
GitHub, o explicar qué es un PR.

## Inputs
- Identificador del PR (#2) o rama (`new-branch`) y su base (`main`).
- Acceso de solo lectura al repo (GitHub MCP read-only y/o clon local).
- Documentos normativos del repo: `REQUERIMENTS.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `AGENTS.md` (todos existen en el repo revisado).
- Issue vinculado (#1) cuando el PR lo referencia (`Fixes #1`).

## Steps Performed
1. **Seleccionar el PR.** `list_pull_requests` (GitHub MCP read-only) devolvió un
   único PR abierto: #2, `new-branch` -> `main`.
2. **Leer el issue vinculado (#1).** Pide validar tipos de dato (null, tipos
   incorrectos) al leer `customers.json` en `storage.py` y agregar una prueba
   automatizada.
3. **Leer spec/requisitos.** Se buscó en `SPEC.md`, `REQUERIMENTS.md` y
   `ARCHITECTURE.md` reglas sobre carga/validación. Solo `SPEC.md` EH-02
   (archivo inexistente o corrupto -> mensaje + exit code 1).
4. **Inspeccionar el diff.** `git fetch` + `git diff main origin/new-branch`.
   Archivos relevantes: `src/storage.py` (+9) y `tests/test_storage.py` (+9),
   más `.pyc` binarios modificados.
5. **Identificar tests relevantes.** `tests/test_storage.py`; el PR agrega
   `test_load_customers_invalid_data_types`.
6. **Ejecutar pruebas.** Baseline en `main`: 18 passed. Rama del PR (exportada
   con `git archive` a una carpeta temporal para no tocar el clon): 19 passed.
7. **Clasificar hallazgos** (ver sección Decisions).
8. **Generar reporte para revisión humana** (pendiente de formalizar con la
   plantilla de la Skill).

### Hallazgos preliminares observados (insumo para el criterio de severidad)
| # | Hallazgo | Evidencia | Severidad tentativa |
|---|---|---|---|
| 1 | `isinstance(x, int)` acepta `True/False` como `id` válido. | `src/storage.py`, validación añadida | SHOULD FIX |
| 2 | La validación de tipos no está documentada en `SPEC.md`/`REQUERIMENTS.md` (regla no trazable a un requisito). | SPEC EH-02 solo cubre archivo inexistente/corrupto | SHOULD FIX |
| 3 | La prueba nueva cubre solo `name=None`; no cubre `email`, `last_name`, `id` con tipo incorrecto ni cada rama del `or`. | `tests/test_storage.py` | SHOULD FIX |
| 4 | Archivos `.pyc` y `.coverage` están versionados; no hay `.gitignore`. Ensucian el diff y bloquean `git checkout` si cambian localmente. | `git ls-files`; checkout falló con cambios locales en `.pyc` | SHOULD FIX |
| 5 | Líneas en blanco con espacios sobrantes tras el nuevo bloque. | `src/storage.py` | OPTIONAL |

## Decisions
Decisiones que requieren criterio del LLM (no automatizables):
- Decidir si un cambio de comportamiento está respaldado por un requisito o
  introduce una regla de negocio no documentada.
- Decidir si la cobertura de pruebas es suficiente para el riesgo del cambio.
- Clasificar severidad (MUST FIX / SHOULD FIX / OPTIONAL) con evidencia.
- Detectar ruido en el PR (artefactos compilados) y juzgar su impacto.
- Decidir qué queda como "Human decision required".

## Deterministic Work
Pasos que deben ser comandos/scripts, no juicio del LLM:
- Listar PRs / leer diff (GitHub MCP o `git diff`).
- Ejecutar la suite (`pytest -v`) y registrar el resultado.
- Listar archivos versionados que no deberían estarlo (`git ls-files`).
- **Validar la estructura del reporte** (`scripts/validate_review_report.py`):
  secciones obligatorias, conteos y línea "Human decision required".

## Reference Knowledge
Fuentes que realmente se consultaron en esta revisión manual:
- **Issue #1** (vía GitHub MCP read-only): define el comportamiento esperado.
- **`SPEC.md`**: se buscó por palabras clave (null, tipo, storage, carga);
  solo EH-02 aplica.
- **`REQUERIMENTS.md` y `ARCHITECTURE.md`**: se buscaron las mismas palabras
  clave; `ARCHITECTURE.md` solo describe el rol de Storage y sus tests.
- **Criterio propio del LLM** para clasificar severidad y juzgar cobertura de
  pruebas. No se usó un checklist ni una guía de severidad formal.

Observación: la revisión no tuvo un criterio escrito de severidad ni una lista
de verificación; esa falta es una candidata a convertirse en conocimiento de
referencia de la Skill, pero todavía no está definida.

## Output
Reporte local `results/pr-readiness-review.md` con: contexto, requisitos
revisados, evidencia de tests, hallazgos por severidad con evidencia, preguntas
abiertas y resumen final con conteos y "Human decision required: YES".

## Stop Conditions
Detenerse y pedir intervención humana si:
- `REQUERIMENTS.md` y `SPEC.md` se contradicen.
- No se puede acceder al PR/diff o a los tests.
- La petición incluye comentar, aprobar o hacer merge (fuera de alcance).
- Se detectan secretos/credenciales en el diff.
- Los tests no se pueden ejecutar y no hay evidencia alternativa.
