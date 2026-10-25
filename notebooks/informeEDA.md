# Informe EDA – Dataset Wearable (Sedentarismo Activo)

**Proyecto:** Data-MinerProyecto · Wearable: Minería de Datos en Sensores de Sedentarismo  
**Dataset analizado:** `Datacrude/02IntermediateData/Sensores_limpio.csv` (capa intermedia, post-limpieza)  
**Fuente cruda:** `Datacrude/01NoProcessData/SENSORES(sucio).xlsx` + `sleepDay_merged.csv`  
**Registros:** 868 · **Variables:** 18 · **Usuarios únicos:** 33 · **Periodo:** 2016-01-05 a 2016-12-05 (31 fechas distintas)

---

## Sección 1. Introducción y objetivo del análisis

Este informe presenta el Análisis Exploratorio de Datos (EDA) del dataset alternativo del equipo, construido a partir de registros de wearables (acelerometría triaxial + PPG) y enriquecido con métricas de sueño (`sleepDay_merged.csv`). El objetivo es entender la distribución, calidad y relaciones de las variables de actividad física y sueño, para fundamentar las decisiones de transformación (escalado/codificación) y las hipótesis que se convertirán en el árbol de decisión del Avance 2.

Variable objetivo implícita del proyecto: **riesgo sedentario** (`Nivel_Sedentarismo`: Alto/Bajo) y **nivel de actividad** (`Nivel_Pasos`: Alta/Baja Actividad).

## Sección 2. Descripción del dataset y fuentes

| Fuente | Archivo | Rol |
|---|---|---|
| Sensores wearable | `SENSORES(sucio).xlsx` | Actividad diaria (pasos, distancia, minutos por intensidad, calorías) |
| Sueño | `sleepDay_merged.csv` | Minutos dormidos, tiempo en cama, eficiencia de sueño |
| Derivadas | calculadas en pipeline | `Nivel_Pasos`, `Nivel_Sedentarismo`, `Eficiencia_Sueño` |

**Variables (18):** `Id`, `ActivityDate`, `TotalSteps`, `TotalDistance`, `VeryActiveDistance`, `ModeratelyActiveDistance`, `LightActiveDistance`, `SedentaryActiveDistance`, `VeryActiveMinutes`, `FairlyActiveMinutes`, `LightlyActiveMinutes`, `SedentaryMinutes`, `Calories`, `Nivel_Pasos`, `Nivel_Sedentarismo`, `TotalMinutesAsleep`, `TotalTimeInBed`, `Eficiencia_Sueño`.

**Composición categórica:**
- `Nivel_Pasos`: Baja Actividad = 565 (65.1%), Alta Actividad = 303 (34.9%).
- `Nivel_Sedentarismo`: Alto Sedentarismo = 690 (79.5%), Bajo Sedentarismo = 178 (20.5%).

## Sección 3. Calidad de los datos

- **Nulos:** 0 en las 15 variables de actividad; **605 nulos (69.7%)** en `TotalMinutesAsleep`, `TotalTimeInBed` y `Eficiencia_Sueño` (sueño solo se registró en ~30.3% de los días). Se tratará como MNAR: ausencia de registro de sueño.
- **Duplicados exactos:** 0.
- **Columnas fantasma (Unnamed):** eliminadas en el pipeline de limpieza.
- **Días de "no uso" del tracker** (0 pasos y 1440 min sedentarios): filtrados del dataset.
- **Outliers:** winsorización IQR (factor 1.5) aplicada a `TotalSteps`, `Calories`, `VeryActiveMinutes`.
- **Inconsistencia detectada:** las variables de distancia (`TotalDistance`, `VeryActiveDistance`, etc.) presentan magnitudes anómalas (≈10¹⁴), indicando un error de escala/parseo decimal en la fuente cruda. **Acción recomendada:** revisar conversión de unidades antes del modelado; no usar estas columnas tal cual.
- **Codificación:** el nombre de `Eficiencia_Sueño` presenta mojibake en el CSV (se recomienda renombrar a `Eficiencia_Sueno` o corregir encoding UTF-8).

## Sección 4. Análisis univariado

Estadísticos clave (dataset limpio):

| Variable | Media | Mediana | Desv. Est. | Min | Max |
|---|---|---|---|---|---|
| TotalSteps | 8,212 | 7,969 | 4,566 | 0 | 20,400 |
| VeryActiveMinutes | 21.0 | 7.0 | 27.6 | 0 | 87.5 |
| LightlyActiveMinutes | 208.8 | 206.5 | 97.8 | 0 | 518 |
| SedentaryMinutes | 954.0 | 1,020 | 283.2 | 0 | 1,440 |
| Calories | 2,353 | 2,219 | 702.5 | 389 | 4,296 |
| TotalMinutesAsleep | 415.9 | 428.0 | 120.4 | 59 | 775 |
| Eficiencia_Sueño | 0.92 | 0.94 | 0.09 | 0.50 | 1.00 |

Observaciones:
- `TotalSteps` es asimétrica a la derecha (media > mediana), con cola de días de alta actividad.
- `SedentaryMinutes` domina el día (≈66% del tiempo), coherente con la población "sedentaria activa".
- La eficiencia de sueño es alta (mediana 0.94), pero con valores mínimos de 0.50 (sueño fragmentado).
- `VeryActiveMinutes` tiene muchos ceros (mediana 7): la mayoría de días no incluyen actividad vigorosa.

## Sección 5. Análisis bivariado y correlaciones

Correlaciones de Pearson (variables clave):

| Par | r |
|---|---|
| TotalSteps ↔ VeryActiveMinutes | 0.69 |
| TotalSteps ↔ Calories | 0.57 |
| VeryActiveMinutes ↔ Calories | 0.59 |
| SedentaryMinutes ↔ TotalMinutesAsleep | -0.67 |
| LightlyActiveMinutes ↔ SedentaryMinutes | -0.28 |
| Calories ↔ Eficiencia_Sueño | 0.34 |

Hallazgos:
- La actividad vigorosa (`VeryActiveMinutes`) es el mejor predictor de pasos y calorías.
- Mayor sedentarismo se asocia con **menos sueño** (r = -0.67): los días más sedentarios son también los de peor descanso.
- `Nivel_Pasos = Alta Actividad` se asocia con ~13,167 pasos/día y ~2,738 kcal, vs ~5,555 pasos y ~2,146 kcal en Baja Actividad.
- `Nivel_Sedentarismo = Alto` promedia ~1,053 min sedentarios/día vs ~569 en Bajo.

## Sección 6. Conclusiones y próximos pasos

1. El dataset describe adecuadamente el fenómeno de "sedentario activo": alto sedentarismo coexistiendo con actividad ligera.
2. Variables más informativas para modelado: `TotalSteps`, `VeryActiveMinutes`, `SedentaryMinutes`, `Calories`, `TotalMinutesAsleep`, `Eficiencia_Sueño`.
3. Se recomienda **no usar** las columnas de distancia hasta corregir el error de escala.
4. El sueño tiene 69.7% de missing; se propone imputación por usuario o indicador de "sin registro de sueño".
5. Hipótesis para el árbol de decisión (Avance 2): un día se clasifica como "alto riesgo sedentario" si `SedentaryMinutes` es alto **y** `VeryActiveMinutes` es bajo **y** `TotalSteps` es bajo.
6. Próximo paso: aplicar el árbol de decisión sobre estas variables y validar con las 2 reglas generadas.

---
*Informe EDA – borrador completo (6 secciones).*