# Proyecto Wearable: Gemelo Digital y Minería de Datos en Sensores de Sedentarismo

## Contexto del Proyecto
Este proyecto esta enfocado especificamente en la detección temprana de hábitos de riesgo en "sedentarios activos" utilizando datos de wearables (acelerometría triaxial y fotopletismografía - PPG), integrando además condiciones climáticas (API OpenWeatherMap) y registros de sueño (`sleepDay_merged.csv`).

## Estructura del Repositorio

```text
Data-MinerProyecto/
├── Datacrude/
│   ├── 01NoProcessData/                 # Datos crudos originales
│   │   ├── SENSORES(sucio).xlsx
│   │   └── sleepDay_merged.csv
│   ├── 02IntermediateData/              # Datos limpios e integrados
│   │   └── Sensores_limpio.csv
│   └── 03DatafinalProcessed/            # Matriz final transformada para ML
│       └── Sensores_transformado.csv
├── Docs/
|   ├── DatamineProyectoEDA.md
|   └── LimpiezaSedentarismo.md
|
├── notebooks/                           # Cuadernos Jupyter del proyecto
|   ├── arbol_de_decisiones.md           # Imagen del arbol + las dos discutas (con respuestas) sesion 7
|   ├── decisionesEscalado.md            # La matriz de Features (dataset wearable)
|   ├── hipotesisFuga.md                 # Las 3 preguntas 
|   ├── informeEDA.md                    # Informe inicial del EDA   
│   ├── Sensores.ipynb                   # Cuaderno de diagnóstico, limpieza y EDA
│   └── SensoresTransformacion.ipynb     # Cuaderno de vectorización y transformación
|   
├── src/                                 # Código fuente modular (Python)
│   ├── Limpieza/
│   │   └── Sensores_limpios.py          # Clase SensoresDataCleaner
│   └── Transformacion/
│       └── transformaciones.py          # Clase SensoresDataTransformer
└── README.md                            # Documentación principal del proyecto
```

## Estructura y Arquitectura de Datos (`Datacrude/`)
Esta primera parte implementa una arquitectura de procesamiento de datos por capas (*Data Lakehouse local*) estructurada en tres niveles de madurez, con el objetivo de garantizar la **inmutabilidad, trazabilidad y reproducibilidad** del pipeline de análisis de datos sin editar manualmente los archivos fuente.

---


## Antes y Después de la Limpieza del Dataset

| Métrica | Antes (Crudo: `SENSORES(sucio).xlsx`) | Después (Limpio: `Sensores_limpio.csv`) |
|---|---|---|
| **Filas** | 940 | 868 (−72 días de "no uso" del tracker) |
| **Columnas** | 17 (incluye 2 fantasma `Unnamed`) | 18 (sin fantasma + 3 de sueño) |
| **Nulos totales** | 1.879 | 1.815 (solo en variables de sueño) |
| **Duplicados exactos** | 0 | 0 |
| **Columnas fantasma** | 2 (`Unnamed: 15`, `Unnamed: 16`) | 0 (eliminadas) |
| **Fechas (`ActivityDate`)** | Mixtas (datetime y texto) | Normalizadas a `datetime` |
| **Fuente de sueño** | No integrada | Integrada (`sleepDay_merged.csv`) |
| **Cobertura de sueño** | — | ~30.3% de los días |
| **Nuevas columnas** | — | `TotalMinutesAsleep`, `TotalTimeInBed`, `Eficiencia_Sueño` |
| **Outliers** | Sin tratar | Winsorizados (IQR, factor 1.5) en `TotalSteps`, `Calories`, `VeryActiveMinutes` |
| **Categorías** | Con espacios inconsistentes | Limpias (`str.strip()`) en `Nivel_Pasos`, `Nivel_Sedentarismo` |
| **Valores únicos (categóricas)** | — | `Nivel_Pasos`: Baja 565 / Alta 303; `Nivel_Sedentarismo`: Alto 690 / Bajo 178 |

### Etapa posterior (transformación)
| Métrica | Matriz final (`Sensores_transformado.csv`) |
|---|---|
| **Filas** | 868 |
| **Columnas** | 17 (tras eliminar 2 categóricas originales y agregar 2 dummies One-Hot) |
| **Escalado** | `RobustScaler` (pasos, calorías, min. muy activos) + `MinMaxScaler` (sueño, sedentarios, eficiencia) |
| **Codificación** | One-Hot (`drop_first=True`) → `Nivel_Pasos_Baja Actividad`, `Nivel_Sedentarismo_Bajo Sedentarismo` |

---

## Informacion / Documentacion (`notebooks/`)
Aca esta la informacion necesaria sobre el proyecto, se manejan en el formado .md (*Markdown*) y en .ipynb (*Jupyter Notebook*).

---

## Codigo fuente despues de ser procesado (`src/`)
Codigo fuente modular, en resumen, es el motor del pipeline de datos.
### `src/Limpieza/Sensores_limpios.py`
Clase `SensoresDataCleaner` que ejecuta la **fase de limpieza (CRISP-DM)** sobre el dataset crudo:
- Diagnóstico inicial (nulos, duplicados, columnas fantasma, días de "no uso").
- Eliminación de columnas fantasma (`Unnamed`).
- Normalización de fechas (`ActivityDate`).
- Integración de la fuente de sueño (`sleepDay_merged.csv`) y cálculo de `Eficiencia_Sueño`.
- Filtrado de días sin uso del tracker.
- Winsorización de outliers (IQR) en `TotalSteps`, `Calories`, `VeryActiveMinutes`.
- Limpieza de categorías (`Nivel_Pasos`, `Nivel_Sedentarismo`).
- Validación y exportación a `Datacrude/02IntermediateData/Sensores_limpio.csv`.

### `src/Transformacion/transformaciones.py`
Clase `SensoresDataTransformer` que ejecuta la **fase de transformación/vectorización**:
- Carga del dataset limpio.
- Escalado selectivo: `RobustScaler` (variables con outliers) y `MinMaxScaler` (tiempos/eficiencias).
- Codificación categórica con One-Hot Encoding (`drop_first=True`).
- Exportación de la matriz final a `Datacrude/03DatafinalProcessed/Sensores_transformado.csv`.

## Dependencias e Instalación

El proyecto requiere las siguientes librerías de Python para ejecutar el pipeline y los notebooks:

| Librería | Uso en el proyecto |
|---|---|
| `pandas` | Carga y manipulación de CSV/Excel (`read_csv`, `read_excel`) |
| `numpy` | Operaciones numéricas |
| `scikit-learn` | `RobustScaler`, `MinMaxScaler`, `OneHotEncoder` (`src/Transformacion/transformaciones.py`) |
| `matplotlib` | Gráficos en los notebooks |
| `seaborn` | Temas y visualizaciones en los notebooks |
| `openpyxl` | Lectura de archivos `.xlsx` (`SENSORES(sucio).xlsx`) |
| `requests` | Importado en `src/Limpieza/Sensores_limpios.py` (uso opcional) |
| `jupyter` / `notebook` | Ejecución de los archivos `.ipynb` |

> `pathlib`, `sys` e `importlib` son parte de la biblioteca estándar de Python (no se instalan).

### Para qué sirve cada uno en el proyecto

- **pandas:** carga los datasets crudos (`SENSORES(sucio).xlsx`, `sleepDay_merged.csv`) y los datasets procesados (`Sensores_limpio.csv`, `Sensores_transformado.csv`); permite filtrar, agrupar y transformar columnas.
- **numpy:** soporta operaciones numéricas y el manejo de arreglos usados por scikit-learn y pandas.
- **scikit-learn:** proporciona los escaladores (`RobustScaler`, `MinMaxScaler`) y el codificador (`OneHotEncoder`) aplicados en `src/Transformacion/transformaciones.py` para construir la matriz de features.
- **matplotlib:** genera gráficos (histogramas, boxplots, etc.) en los notebooks de EDA y transformación.
- **seaborn:** mejora la estética de los gráficos y facilita visualizaciones estadísticas en los notebooks.
- **openpyxl:** permite leer el archivo Excel crudo `SENSORES(sucio).xlsx` con `pd.read_excel`.
- **requests:** habilita (de forma opcional) la integración con la API de OpenWeatherMap mencionada en el contexto del proyecto.
- **jupyter / notebook:** entorno para ejecutar y documentar los notebooks (`Sensores.ipynb`, `SensoresTransformacion.ipynb`).

### Para una instalación rápida

```bash
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl requests jupyter