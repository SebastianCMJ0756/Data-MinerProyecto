# Limpieza del dataset de sedentarismo

**Autores:** José Camilo Rodríguez Ortegón · Juan Sebastián Calderón Martínez  
**Docente:** Esteban Ernesto Morales Castro  
**Curso:** Minería de Datos  
**NRC:** 87473  
**Facultad:** Ingeniería, Programa de Ingeniería de Sistemas – Corporación Universitaria Minuto de Dios (UNIMINUTO), Vicerrectoría Regional Centro Sur  
**Ciudad:** Ibagué, Tolima  
**Año:** 2026

> 📄 **Descargar el documento original en PDF:** [Limpieza_Datos_Sedentarismo.pdf](./Limpieza_Datos_Sedentarismo.pdf)

---

## Documento de Especificación Técnica y Limpieza de Datos: Proyecto MIMETIC

### Contexto

MIMETIC es un gemelo digital enfocado a la medicina que aborda la problemática de la detección tardía de hábitos de riesgo, centrando su atención en el perfil conocido como **"sedentarios activos"**. Este grupo de usuarios se caracteriza por cumplir con metas diarias de ejercicio físico pero, de manera paralela, mantener jornadas prolongadas de inmovilidad.

Para solucionar este sesgo de diagnóstico, el sistema procesa datos numéricos crudos provenientes de sensores fotopletismográficos (PPG) para frecuencia cardíaca y acelerómetros triaxiales, transformándolos en etiquetas cualitativas.

---

## Objetivos

**Objetivo General:**  
Desarrollar un modelo de minería de datos integrado al Gemelo Digital de MIMETIC para detectar oportunamente patrones de riesgo en "sedentarios activos", transformando datos numéricos de wearables en etiquetas cualitativas para la emisión de alertas preventivas en tiempo real.

**Objetivos Específicos:**
- **Analizar y preparar la data:** Extraer y transformar los datos crudos recolectados por sensores PPG y acelerómetros triaxiales (del dataset de Fitbit en Kaggle), limpiando y categorizando variables clave como `TotalSteps` y `SedentaryMinutes`.
- **Identificar patrones y reglas:** Aplicar técnicas de minería de datos (como reglas de asociación) para clasificar el comportamiento del usuario y detectar la coexistencia de metas de ejercicio con jornadas prolongadas de inmovilidad.
- **Integrar alertas preventivas:** Validar e integrar los resultados del modelo predictivo en la arquitectura del Gemelo Digital de MIMETIC para posibilitar la notificación automatizada de hábitos de riesgo en tiempo real.

---

## 2. Paso a Paso de la limpieza del Dataset (dfClean)

El proceso de preparación de datos se enmarcó en la **fase 3 de la metodología CRISP-DM (Preparación de Datos)**, ejecutada en el cuaderno interactivo `MIMETICSEC3.ipynb`. Para garantizar la trazabilidad académica, mantenibilidad y calidad de software, el procedimiento se empaquetó dentro de una arquitectura orientada a objetos mediante la clase `MIMETICDataCleaner`, respaldada por los principios **SOLID** (Responsabilidad Única y Principio de Abierto/Cerrado).

### Paso 1: Ingesta Multi-fuente e Integración Contextual

Se unificaron dos fuentes de datos complementarias dentro del pipeline:

- **Fuente primaria (wearable):** archivo `dailyActivity_mergedMIMETIC (version 1).xlsx` con 940 registros y 17 columnas iniciales, compuestas por métricas de fotopletismografía (PPG) y acelerometría triaxial (`TotalSteps`, `SedentaryMinutes`, `VeryActiveMinutes`, `Calories`).
- **Fuente secundaria (clima):** peticiones HTTP en tiempo real a la API de OpenWeatherMap para extraer variables meteorológicas (`Temperatura_C`, `Humedad_Pct`, `Velocidad_Viento`, `Estado_Clima`) en ciudades principales. Esto permite correlacionar factores ambientales externos con el nivel de sedentarismo o cumplimiento de actividad física.

### Paso 2: Diagnóstico, Depuración de Artefactos y Tratamiento de MNAR

En el diagnóstico inicial de calidad de datos se ejecutaron las siguientes acciones de saneamiento:

- **Eliminación de Columnas Fantasma:** Extirpación de las columnas `Unnamed: 15` y `Unnamed: 16` generadas por desbordamiento de delimitadores en Excel (1.879 celdas vacías).
- **Estandarización Temporal:** Aplicación de la función `normalizar fechas` para convertir `ActivityDate` a tipo de dato `datetime`, garantizando 0 registros inválidos (NaT) y permitiendo el análisis cronológico.
- **Depuración de Datos Faltantes No Aleatorios (MNAR):** Se identificaron 72 registros con `TotalSteps = 0` y `SedentaryMinutes = 1440` (24 horas continuas de inmovilidad). Dado que representaban días en los que el usuario no portó el dispositivo de medición, se utilizó el método `filtrarDiasSinUso` para eliminarlos en lugar de imputar valores artificiales que sesgarían el modelo, ajustando la muestra útil a 868 registros.

### Paso 3: Tratamiento de Outliers por Winsorización (Regla IQR de Tukey)

Para controlar la varianza sin reducir el volumen de la muestra, se implementó el método `tratarOutliersIqr`. Se aplicó una técnica de Winsorización que calcula los límites mediante el Rango Intercuartílico (IQR = Q3 − Q1):

- Límite Inferior = Q1 − 1,5 × IQR
- Límite Superior = Q3 + 1,5 × IQR

Cualquier valor ubicado fuera de estas cotas fue ajustado al límite permitido más cercano usando la función `.clip()`:

- **TotalSteps:** Se acotaron los valores extremos superiores para suavizar marchas atípicas sin perder el registro del usuario.
- **Calories y VeryActiveMinutes:** Se ajustaron los picos atípicos de gasto calórico e intensidad para evitar distorsión en los algoritmos de clasificación de "sedentarios activos".

### Paso 4: Normalización Categórica y Diseño Extensible

- **Limpieza de Cadenas:** Aplicación de `.str.strip()` en variables cualitativas como `Nivel_Pasos` y `Nivel_Sedentarismo` para eliminar espacios en blanco marginales y prevenir la creación de categorías duplicadas (ej. "Activo " vs "Activo").
- **Diseño Extensible (SOLID):** Toda la secuencia fue orquestada por `MIMETICDataCleaner.ejecutarPipeline()`, conservando el conjunto de datos original intacto mediante copia explícita (`self.dfOriginal.copy()`) y manteniendo listas de configuración dinámicas (`colsOutlier`, `colsCategoricas`).

---

## 3. Documentación de Cambios Realizados en el Dataset

La tabla a continuación consolida las transformaciones estructurales, estadísticas y de formato aplicadas entre la versión cruda (`dfMimetic`) y la versión depurada (`dfClean` / `MIMETIC_limpio.csv`):

| Contexto | Estado Inicial (Dataset Crudo) | Estado Final (Dataset Limpio) | Tipo de Cambio y Justificación |
|---|---|---|---|
| Dataset general | 940 filas × 17 columnas | 868 filas × 15 columnas | Reducción: eliminación de 2 columnas fantasma y descarte de 72 registros MNAR (días sin uso del wearable). |
| Columnas fantasma | 2 (`Unnamed: 15`, `Unnamed: 16`) | 0 columnas | Eliminación: extirpación de artefactos creados por desbordamiento de delimitadores en Excel. |
| Valores nulos totales | 1.879 celdas vacías | 0 celdas vacías | Saneamiento: remoción completa de nulos al eliminar las columnas fantasma. |
| Registros duplicados | 0 filas | 0 filas | Sin cambio: se verificó y confirmó la integridad muestral de los datos originales. |
| `ActivityDate` | Texto no estructurado (object) | Formato de fecha (datetime64) | Estandarización: conversión coercitiva para análisis de series de tiempo. |
| `TotalSteps` | Valores extremos atípicos presentes | Valorado y acotado por IQR | Winsorización: recorte con `.clip()` al límite superior (Q3 + 1,5 × IQR) para suavizar marchas atípicas. |
| `Calories` | Picos atípicos de gasto calórico | Valorado y acotado por IQR | Winsorización: ajuste de picos atípicos para evitar distorsión en algoritmos de clasificación. |
| `VeryActiveMinutes` | Valores extremos de alta intensidad | Valorado y acotado por IQR | Winsorización: control de varianza extrema manteniendo la muestra. |
| `SedentaryMinutes` | Incluía 72 días con 1440 min (24 hrs) | Filtrado sin registros de 1440 min con 0 pasos | Filtrado MNAR: eliminación de días en que el dispositivo no fue utilizado por el usuario. |
| `Nivel_Pasos` / `Nivel_Sedentarismo` | Cadenas con posibles espacios marginales | Cadenas limpias sin espacios | Normalización: aplicación de `str.strip()` para consistencia de etiquetas pre-One-Hot Encoding. |

---

## Enlaces

- **Repositorio del proyecto:** https://github.com/SebastianCMJ0756/Data-MinerProyecto.git
- **Descargar este documento en PDF:** [Limpieza_Datos_Sedentarismo.pdf](./Limpieza_Datos_Sedentarismo.pdf)