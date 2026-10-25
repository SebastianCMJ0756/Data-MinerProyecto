# Análisis Exploratorio de Datos (EDA)

**Autores:** José Camilo Rodríguez Ortegón · Juan Sebastian Calderón Martínez  
**NRC:** 95400 – Esteban Ernesto Morales Castro  
**Facultad:** Ingeniería, Programa de Ingeniería de Sistemas (ISUM) – Universidad Minuto de Dios  
**Fecha:** Octubre 2026

> 📄 **Descargar el informe original en PDF:** [DataminerProyectoEDA.pdf](./DataminerProyectoEDA.pdf)

---

## Tabla de contenido

- [Contexto](#contexto)
- [Objetivos](#objetivos)
- [Calidad de datos](#calidad-de-datos)
- [Análisis univariado](#análisis-univariado)
- [Análisis bivariado / multivariado](#análisis-bivariado--multivariado)
- [Hallazgos y recomendaciones](#hallazgos-y-recomendaciones)
- [Árbol de decisiones (prototipo)](#árbol-de-decisiones-prototipo)

---

## Contexto

Mediante el proyecto wearable se busca desarrollar un prototipo orientado a la gestión de datos biométricos y de comportamiento del paciente mediante el análisis de variables capturadas por dispositivos electrónicos compactos que se llevan puestos en el cuerpo (wearables).

En el ámbito clínico, la inmovilidad prolongada y la alteración de los patrones de sueño son indicadores críticos del deterioro funcional; la ingesta continua de series de tiempo provenientes de los sensores inteligentes permite transformar observaciones pasivas en alertas analíticas oportunas.

---

## Objetivos

**Objetivo general:**  
Preprocesar, depurar y estructurar los patrones de actividad física, sedentarismo y sueño registrados por sensores para alimentar el prototipo.

**Objetivos específicos:**
- Construir un pipeline de limpieza modular en Python (`SensoresDataCleaner`) que garantice la calidad de los datos resolviendo registros nulos, columnas fantasma de exportación y días sin uso del dispositivo.
- Consolidar fuentes de datos heterogéneas (actividad diaria y registros de sueño) utilizando claves únicas compuestas.
- Vectorizar y escalar la matriz final de datos (`SensoresDataTransformer`) aplicando `RobustScaler`, `MinMaxScaler` y One-Hot Encoding para asegurar su lectura óptima por algoritmos predictivos.

---

## Calidad de datos

Durante la fase de diagnóstico inicial sobre el dataset crudo (`SENSORES(sucio).xlsx`) y la fuente de sueño (`sleepDay_merged.csv`), se identificaron y trataron cuatro problemas principales de calidad de datos:

### Columnas fantasma
Presencia de columnas sin nombre (`Unnamed: 15`, `Unnamed: 16`) generadas por la exportación de Excel, sumando 1.879 celdas nulas. Se aplicó una limpieza automática de columnas sin encabezado válido en la fase de ingesta del script `Sensores_limpios.py`.

### Días de "No uso" del dispositivo
Se detectaron 72 registros donde `TotalSteps = 0` y `SedentaryMinutes = 1440` (24 horas completas de inmovilidad). Esto corresponde a días en los que el usuario no portó el reloj. Se removieron estos registros para evitar distorsionar los promedios de sedentarismo real y no sesgar los algoritmos de recomendación.

### Registros duplicados en sueños
Se identificaron duplicados exactos en la tabla de sueño para una misma fecha e identificador de usuario (`Id + SleepDay`). Se ejecutó desduplicación con `.drop_duplicates()` previo al cruce relacional.

### Outliers extremos
Presencia de picos extremos en pasos totales, calorías y minutos de alta actividad producidos por errores puntuales de lectura del acelerómetro. Se aplicó Winsorización basada en el Rango Intercuartílico (IQR con factor 1.5), acotando los valores al límite superior sin eliminar la información del registro.

Al final, el dataset pasó de **940 filas y 17 columnas** a una matriz limpia de **868 filas y 18 columnas**.

---

## Análisis univariado

| Variable | Media | Desv. Estándar | Mínimo | Mediana (Q2) | Máximo |
|---|---|---|---|---|---|
| TotalSteps | 8.312,4 | 3.410,2 | 8,0 | 8.025,0 | 20.400,4 |
| Calories | 2.361,5 | 682,1 | 388,6 | 2.210,0 | 4.295,6 |
| VeryActiveMinutes | 23,4 | 21,8 | 0,0 | 20,0 | 87,5 |
| TotalMinutesAsleep | 419,2 | 118,3 | 58,0 | 433,0 | 796,0 |
| Eficiencia_Sueño | 0,91 | 0,08 | 0,45 | 0,93 | 1,00 |

### Gráficas

> Las gráficas del análisis univariado (distribuciones de pasos, calorías, minutos de alta actividad y eficiencia del sueño) se encuentran en el [PDF original](./DataminerProyectoEDA.pdf).

**Pasos Totales (TotalSteps):** Muestra una distribución aproximadamente normal con un promedio de 8.312 pasos. La winsorización permitió acotar los registros que superaban los 20.400 pasos, estabilizando la varianza.

**Calorías Quemadas (Calories):** Presenta una distribución unimodal centrada en torno a las 2.200–2.400 kcal/día, lo cual coincide con el gasto calórico basal de un adulto promedio en actividad moderada.

**Minutos de Alta Actividad (VeryActiveMinutes):** Presenta un fuerte sesgo a la izquierda. La mayoría de los registros se concentran entre 0 y 30 minutos diarios, demostrando que la actividad intensa ocurre en ráfagas cortas.

**Eficiencia del Sueño (Eficiencia_Sueño):** Muestra una concentración alta en valores superiores a 0,90 (90%). La mediana se sitúa en 0,93, lo que indica que la mayoría de los usuarios duermen la mayor parte del tiempo que permanecen en cama.

---

## Análisis bivariado / multivariado

El análisis cruzado entre el volumen de pasos y la eficiencia del descanso demostró que dar más pasos no incrementa de forma lineal la eficiencia del sueño. Sin embargo, las personas categorizadas dentro de **Alto Sedentarismo** registraron caídas críticas en la eficiencia del sueño (valores inferiores al 70%), aumentando sustancialmente la dispersión del descanso.

**Heatmap (correlaciones):**
- **TotalSteps vs. Calories (r = 0,59):** Existe una correlación positiva moderada-alta; a mayor cantidad de pasos registrados, mayor es el consumo energético diario.
- **VeryActiveMinutes vs. Calories (r = 0,62):** Es la correlación positiva más fuerte con el gasto calórico, lo que confirma que la intensidad del movimiento tiene un impacto superior por unidad de tiempo que la caminata ligera.
- **TotalTimeInBed vs. TotalMinutesAsleep (r = 0,93):** Correlación lineal directa casi perfecta. Esta relación fundamentó la creación de la variable sintética `Eficiencia_Sueño`.

---

## Hallazgos y recomendaciones

### Hallazgo 1
Se identificaron jornadas con más de 1.000 minutos acumulados de sedentarismo en pacientes sin registros de ejercicio intenso.  
**Recomendación:** Programar alertas automáticas de inmovilidad (push notifications) en la aplicación cuando el sensor detecte más de 90 minutos continuos de sedentarismo en horario diurno, sugiriendo pausas activas o caminatas breves.

### Hallazgo 2
Los usuarios del segmento "Alto Sedentarismo" mostraron una variabilidad 2,5 veces mayor en la eficiencia de su descanso nocturno.  
**Recomendación:** Diseñar un módulo de recomendación médica en la app que prescriba metas mínimas de 15 a 20 minutos de actividad física moderada antes de las 6:00 PM para pacientes que registren eficiencias de sueño inferiores al 75%.

### Hallazgo 3
Se detectaron 72 días sin mediciones válidas debido a que el usuario se quitó el reloj o no cargó la batería.

---

## Árbol de decisiones (prototipo)

> El prototipo del árbol de decisiones se encuentra documentado en el [PDF original](./DataminerProyectoEDA.pdf) (página 11).

---

## Enlaces

- **Repositorio del proyecto:** https://github.com/SebastianCMJ0756/Data-MinerProyecto.git
- **Descargar este informe en PDF:** [DataminerProyectoEDA.pdf](./DataminerProyectoEDA.pdf)