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
├── notebooks/                           # Cuadernos Jupyter del proyecto
│   ├── Sensores.ipynb                   # Cuaderno de diagnóstico, limpieza y EDA
│   └── SensoresTransformacion.ipynb     # Cuaderno de vectorización y transformación
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






