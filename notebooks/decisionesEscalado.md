# Decisiones de Escalado y Codificación – Matriz de Features (Dataset Wearable)

**Archivo fuente:** `src/Transformacion/transformaciones.py` · **Salida:** `Datacrude/03DatafinalProcessed/Sensores_transformado.csv`

## 1. Variables y transformación aplicada

| Grupo | Variables | Técnica | Justificación |
|---|---|---|---|
| Outliers residuales / sesgo | `TotalSteps`, `Calories`, `VeryActiveMinutes` | **RobustScaler** | Distribuciones con cola derecha y outliers; la mediana y el IQR son robustos a valores extremos. |
| Rangos acotados / eficiencias | `TotalMinutesAsleep`, `TotalTimeInBed`, `SedentaryMinutes`, `Eficiencia_Sueño` | **MinMaxScaler** | Valores con límites naturales (tiempo ≤ 1440 min, eficiencia ∈ [0,1]); se preserva la escala [0,1] para modelos sensibles a magnitud. |
| Categóricas ordinales | `Nivel_Pasos`, `Nivel_Sedentarismo` | **One-Hot Encoding** (`drop_first=True`) | Evita multicolinealidad; genera `Nivel_Pasos_Baja Actividad` y `Nivel_Sedentarismo_Bajo Sedentarismo`. |
| Identificadores / fecha | `Id`, `ActivityDate` | **Passthrough** | Se conservan para trazabilidad; no se escalan. |
| No transformadas (pendiente) | `TotalDistance`, `VeryActiveDistance`, `ModeratelyActiveDistance`, `LightActiveDistance`, `SedentaryActiveDistance`, `FairlyActiveMinutes`, `LightlyActiveMinutes` | — | Se dejaron sin escalar por el error de escala detectado en el EDA; deben corregirse antes de modelar. |

## 2. Decisiones clave

- **Escalado selectivo** (no global): se eligió la técnica según la distribución y el significado de cada variable, no se aplicó un único scaler a todo.
- **RobustScaler antes que StandardScaler** porque los datos de actividad tienen colas largas y outliers (días de muy alta actividad).
- **MinMaxScaler para sueño** porque la eficiencia ya está en [0,1] y los minutos tienen cota superior física (1440).
- **One-Hot con `drop_first=True`** para evitar la trampa de las variables dummy.
- **Codificación a enteros (0/1)** para compatibilidad directa con scikit-learn.

## 3. Validación de la matriz resultante

- Dimensiones finales: **868 filas × 17 columnas** (tras eliminar 2 categóricas originales y agregar 2 dummies).
- Sin nulos introducidos por la transformación.
- Variables numéricas en rangos acotados (robustas o [0,1]); categóricas en {0,1}.

## 4. Pendientes

- Corregir escala de las columnas de distancia.
- Imputar o indicar missing de sueño (69.7%).
- Renombrar `Eficiencia_Sueño` (mojibake) a `Eficiencia_Sueno`.

---
*Documentación de decisiones de escalado/codificación (complemento al notebook SensoresTransformacion.ipynb).*