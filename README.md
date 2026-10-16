# Proyecto Wearable: Gemelo Digital y Minería de Datos en Sensores de Sedentarismo

## Contexto del Proyecto
Este proyecto esta enfocado especificamente en la detección temprana de hábitos de riesgo en "sedentarios activos" utilizando datos de wearables (acelerometría triaxial y fotopletismografía - PPG), integrando además condiciones climáticas (API OpenWeatherMap) y registros de sueño (`sleepDay_merged.csv`). 

## Estructura del Repositorio
Data-MinerProyecto/
├── README.md                          # <-- Puerta de entrada al proyecto
├── requirements.txt                   # <-- Las dependencias del proyecto
├── data/
│   ├── 01NoProcessData/                        # Datos crudos inmutables
│   │   ├── SENSORES(sucio).xlsx
│   │   └── sleepDay_merged.csv
│   ├── 02IntermediateData/                    # Datos limpios intermedios
│   │   └── Sensores_limpio.csv
│   └── 03DatafinalProcessed/                  # Matrices finales para modelado
│       └── Sensores_transformado.csv

# Estructura y Arquitectura de Datos (`Datacrude/`)

Esta primera parte implementa una arquitectura de procesamiento de datos por capas (*Data Lakehouse local*) estructurada en tres niveles de madurez, con el objetivo de garantizar la **inmutabilidad, trazabilidad y reproducibilidad** del pipeline de análisis de datos sin editar manualmente los archivos fuente.

---






