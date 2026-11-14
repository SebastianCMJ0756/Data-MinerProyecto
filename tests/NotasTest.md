# Tests del Pipeline de Datos – Data-MinerProyecto

Este directorio contiene las **pruebas automatizadas** del pipeline de limpieza y transformación del proyecto, implementadas con **pytest**.

## ¿Qué se hizo?

Se crearon 2 archivos de tests que validan automáticamente cada paso del pipeline:

| Archivo | Tests | Qué valida |
|---|---|---|
| `test_limpieza.py` | 6 | Reducción de filas (940→868), 18 columnas, sin duplicados, sin columnas fantasma, `ActivityDate` datetime, CSV exportado coincide |
| `test_transformacion.py` | 4 | Dimensiones de la matriz (868×18), existencia de columnas One-Hot, dummies binarias (0/1), CSV de la matriz coincide |

**Total: 10 tests automatizados.**

## ¿Para qué sirve?

- Verificar que el pipeline funciona correctamente después de cualquier cambio en el código.
- Detectar regresiones (si alguien modifica `Sensores_limpios.py` o `transformaciones.py` y rompe algo).
- Dar evidencia visible para la sustentación: "Tenemos 10 tests automatizados con pytest; todos pasan en 4.74 segundos."

## ¿Cómo ejecutar?

Desde la **raíz del proyecto** (`Data-MinerProyecto/`):

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar solo limpieza
python -m pytest tests/test_limpieza.py -v

# Ejecutar solo transformación
python -m pytest tests/test_transformacion.py -v
```

> **Nota:** Si `pytest` no está en el PATH, usa `python -m pytest` (no `pytest` directamente).

## Resultado esperado

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\...\Data-MinerProyecto
collected 10 items

tests/test_limpieza.py::test_pipeline_reduces_rows PASSED       [ 10%]
tests/test_limpieza.py::test_pipeline_columns PASSED            [ 20%]
tests/test_limpieza.py::test_no_duplicates PASSED               [ 30%]
tests/test_limpieza.py::test_no_ghost_columns PASSED            [ 40%]
tests/test_limpieza.py::test_activity_date_is_datetime PASSED   [ 50%]
tests/test_limpieza.py::test_exported_csv_matches PASSED        [ 60%]
tests/test_transformacion.py::test_transformacion_dimensions PASSED [ 70%]
tests/test_transformacion.py::test_one_hot_columns_exist PASSED  [ 80%]
tests/test_transformacion.py::test_dummies_are_binary PASSED     [ 90%]
tests/test_transformacion.py::test_exported_matrix_matches PASSED [100%]

============================== 10 passed in 4.74s ==============================
```

## Señales de éxito vs. error

| Señal | Significado |
|---|---|
| `PASSED` (verde) | El test pasó correctamente |
| `FAILED` (rojo) | El test falló (revisa el mensaje de error) |
| `ERROR` (rojo) | Error de importación o sintaxis |
| `10 passed` al final | Todo funciona correctamente |

## Dependencias

- `pytest>=7.0` (agregado a `requirements.txt`)
- El proyecto debe ejecutarse desde la raíz (`Data-MinerProyecto/`) para que las rutas relativas funcionen.

## Nota sobre warnings
Si aparece un `PytestCacheWarning` (permisos de OneDrive al crear `.pytest_cache/`), **no es un error**. Los tests igual pasan. Para evitarlo, `.pytest_cache/` está ignorado por Git (ver `.gitignore`).
