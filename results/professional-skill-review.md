## Review: PR #2 - Validación de tipos de datos en la carga de clientes

### Context
- [x] Comprendo el propósito de este cambio (Añadir validación de tipos al cargar clientes según el NFR-02 y el manejo de errores).

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled (Falta manejar el caso de booleanos interpretados como enteros)
- [x] Error paths handled
- [x] Tests cover the change adequately

### Readability
- [x] Names are clear and consistent
- [ ] Logic is straightforward (Violación de DRY)
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows existing patterns (Sigue un antipatrón existente)
- [ ] No unnecessary coupling or dependencies (Fuerte acoplamiento con CLI)
- [ ] Appropriate abstraction level
- [ ] Refactors reduce complexity rather than relocate it
- [ ] No feature logic in shared modules

### Security
- [x] No secrets in code
- [x] Input validated at boundaries
- [x] No injection vulnerabilities
- [x] Auth checks in place
- [x] External data sources treated as untrusted

### Performance
- [x] No N+1 patterns
- [x] No unbounded operations
- [x] Pagination on list endpoints

### Verification
- [x] Tests pass
- [x] Build succeeds

### Findings

**Critical:** Validación de tipos errónea para enteros (booleanos)
- **File / Evidence**: `src/storage.py`, línea 33 (`isinstance(item['id'], int)`)
- **Engineering Rationale**: En Python, la clase `bool` hereda de `int`. Esto significa que si el archivo JSON contiene un valor booleano para el campo `id` (por ejemplo, `{"id": true}`), la función `json.load` lo parseará como `True`. Al evaluar `isinstance(True, int)`, Python retorna `True`. Esto permitiría que un tipo de dato incorrecto (booleano) se valide erróneamente como un número entero.
- **Recommended Action**: Modificar la validación para utilizar evaluación de tipo estricta o excluir los booleanos. Por ejemplo: `type(item['id']) is int` o `isinstance(item['id'], int) and not isinstance(item['id'], bool)`.

Violación de límites de arquitectura y repetición de código (DRY)
- **File / Evidence**: `src/storage.py`, líneas 37-38 (Uso repetido de `print("Error: No se...")` y `sys.exit(1)`)
- **Engineering Rationale**: El archivo `ARCHITECTURE.md` estipula claramente: "La validación pertenece al servicio; la CLI se encarga de atrapar los errores y mostrar mensajes claros al usuario", y su sección de decisiones de diseño dice "Mantener la lógica de negocio totalmente independiente de la CLI". Aunque este PR sigue el patrón previamente existente en el archivo de usar `print` y `sys.exit`, al hacerlo está consolidando un antipatrón arquitectónico que mezcla la capa de persistencia/datos con la de presentación de consola. Además, añade estas mismas dos líneas de código por quinta vez en la misma función, violando el principio DRY.
- **Recommended Action**: Abstenerse de usar `print` y `sys.exit` en la capa de persistencia. Refactorizar la función `load_customers` para que lance una excepción (ej. `ValueError` o `DataLoadError`) en caso de validación fallida, y permitir que la CLI la atrape para realizar la impresión y la salida del sistema. Si esta refactorización completa está fuera del alcance de este PR, como mínimo se debe agrupar la lógica de fallo (`print` + `sys.exit`) en una función interna para eliminar el código duplicado.

**Optional:** Verificación completa en las pruebas para asegurar el cumplimiento del requerimiento EH-02
- **File / Evidence**: `tests/test_storage.py`, líneas 69-74 (`test_load_customers_invalid_data_types`)
- **Engineering Rationale**: La prueba actual verifica correctamente que el sistema aborte y devuelva un código de estado 1 (`exc_info.value.code == 1`). Sin embargo, el requerimiento EH-02 (NFR-02) exige explícitamente que se muestre el mensaje estándar *"Error: No se pudo cargar la base de datos de clientes"*. Validar esto en la prueba garantiza que no se produzcan regresiones en la salida al usuario.
- **Recommended Action**: Extender la prueba agregando la validación del output capturado usando `capsys`:
  ```python
  captured = capsys.readouterr()
  assert "Error: No se pudo cargar la base de datos de clientes" in captured.out
  ```

### Verdict
- [ ] **Approve** — Ready to merge
- [x] **Request changes** — Issues must be addressed
