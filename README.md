# Proyecto Wearable: Minería de Datos en Sensores de Sedentarismo

## Contexto del Proyecto
Este proyecto está enfocado específicamente en la detección temprana de hábitos de riesgo en "sedentarios activos" utilizando datos de wearables (acelerometría triaxial y fotopletismografía - PPG), integrando además condiciones climáticas (API OpenWeatherMap) y registros de sueño (`sleepDay_merged.csv`).

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
│   ├── DataminerProyectoEDA.md          # Informe EDA (convertido desde PDF)
│   └── LimpiezaSedentarismo.md          # Documento de limpieza (convertido desde PDF)
├── notebooks/                           # Cuadernos Jupyter y documentos del proyecto
│   ├── Sensores.ipynb                   # Diagnóstico, limpieza y EDA
│   ├── SensoresTransformacion.ipynb     # Vectorización y transformación
│   ├── Clustering_Sedentarismo.ipynb    # Sesión 9: Clustering (K-means, codo, silueta dendrograma)
│   ├── comparacion_modelos.ipynb        # Sesión 8: Torneo Árbol vs Naive Bayes vs KNN
│   ├── arbol_de_decisiones_PyR.md       # Avance 2: Árbol + 2 reglas + discusión
│   ├── decisionesEscalado.md            # Decisiones de escalado/codificación
│   ├── doc_comparacion_modelos.md       # Veredicto técnico del torneo de modelos
│   ├── hipotesisFuga.md                 # 3 preguntas/hipótesis de fuga
│   ├── informeEDA.md                    # Informe EDA (6 secciones)
│   └── Pitch_Data-MinerProyecto.pptx    # Presentación del proyecto
├── src/                                 # Código fuente modular (Python)
│   ├── Limpieza/
│   │   └── Sensores_limpios.py          # Clase SensoresDataCleaner
│   └── Transformacion/
│       └── transformaciones.py          # Clase SensoresDataTransformer
├── .gitignore                           # Ignora __pycache__, checkpoints, entornos virtuales
├── requirements.txt                     # Dependencias del proyecto
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

## Información / Documentación (`notebooks/`)
Aquí está la información necesaria sobre el proyecto, manejada en formato `.md` (Markdown) y `.ipynb` (Jupyter Notebook).

---

## Código fuente después de ser procesado (`src/`)
Código fuente modular; en resumen, es el motor del pipeline de datos.

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
- **jupyter / notebook:** entorno para ejecutar y documentar los notebooks (`Sensores.ipynb`, `SensoresTransformacion.ipynb`, `Clustering_Sedentarismo.ipynb`, `comparacion_modelos.ipynb`).

### Instalación rápida

```bash
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl requests jupyter
```

O crea un archivo `requirements.txt` en la raíz del proyecto con:

```text
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
matplotlib>=3.7
seaborn>=0.12
openpyxl>=3.1
requests>=2.31
jupyter>=1.0
```

y ejecuta:

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar

1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar limpieza: abrir `notebooks/Sensores.ipynb` → **Run All**
3. Ejecutar transformación: `notebooks/SensoresTransformacion.ipynb` → **Run All**
4. Ejecutar torneo de modelos: `notebooks/comparacion_modelos.ipynb` → **Run All**
5. Ejecutar clustering: `notebooks/Clustering_Sedentarismo.ipynb` → **Run All**
6. Resultados esperados: accuracy test Árbol 0.816, NB 0.774, KNN 0.825; 3 clusters (silueta 0.235)

## Enlace del repositorio

https://github.com/SebastianCMJ0756/Data-MinerProyecto.git
