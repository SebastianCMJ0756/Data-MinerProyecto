# Regresión Lineal por Mínimos Cuadrados

## ¿Qué es?
La regresión lineal encuentra la **mejor recta** \(\hat{y} = a_0 + a_1 x\) que pasa **cerca** de los puntos, minimizando la suma de residuos al cuadrado: \(S_r = \sum e_i^2\). Se usa cuando los datos tienen **ruido** (errores de medición, variabilidad). A diferencia de la interpolación, no obliga a la curva a pasar por todos los puntos.

## ¿Para qué sirve? (en general)
- Capturar la **tendencia general** de los datos.
- Predecir valores futuros basándose en la tendencia.
- Cuantificar la relación entre dos variables (\(R^2\), \(r\)).
- Detectar anomalías: si un usuario quema muchas menos calorías de lo esperado para sus pasos, puede indicar un problema.

## ¿Para qué sirve en el proyecto?
- Entender la tendencia general entre pasos y calorías (ej. "por cada 1000 pasos adicionales, se queman ~X calorías").
- Predecir el gasto calórico esperado para un nivel de actividad dado.
- Detectar anomalías: si un usuario quema muchas menos calorías de lo esperado para sus pasos, puede indicar un problema de salud.

## De dónde salieron los datos

Se seleccionaron 5 registros reales del dataset `Sensores_limpio.csv`:

| Fila original | Id | ActivityDate | TotalSteps | Calories |
|---|---|---|---|---|
| 1 | 1503960366 | 2016-12-04 | 0 | 665 |
| 2 | 1624580081 | 2016-04-13 | 5000 | 1432 |
| 3 | 2022484408 | 2016-04-13 | 8000 | 1896 |
| 4 | 2320127002 | 2016-04-13 | 12000 | 2159 |
| 5 | 1503960366 | 2016-04-19 | 20400 | 2690 |

**Cómo se obtuvieron:**
1. Se abrió el archivo `Sensores_limpio.csv` en Python (pandas).
2. Se seleccionaron filas con valores extremos y intermedios de `TotalSteps` (0, 5000, 8000, 12000, 20400).
3. Se leyó el valor de `Calories` de cada fila.
4. Se formó la tabla de puntos \((x_i, y_i)\).

Estos son **datos reales de sensores wearable** (Fitbit), no inventados.

## Paso a paso (con explicación para no expertos)

**Paso 1 – Construir la tabla de sumas:**

| \(x_i\) (pasos) | \(y_i\) (kcal) | \(x_i^2\) | \(x_i \cdot y_i\) |
|---|---|---|---|
| 0 | 665 | 0 | 0 |
| 5000 | 1432 | 25,000,000 | 7,160,000 |
| 8000 | 1896 | 64,000,000 | 15,168,000 |
| 12000 | 2159 | 144,000,000 | 25,908,000 |
| 20400 | 2690 | 416,160,000 | 54,876,000 |
| **Σ** | **45400** | **9032** | **649,160,000** | **103,112,000** |

- \(n = 5\) (número de puntos)
- \(\bar{x} = \frac{45400}{5} = 9080\) (promedio de pasos)
- \(\bar{y} = \frac{9032}{5} = 1806.4\) (promedio de calorías)

**Paso 2 – Calcular la pendiente \(a_1\):**

$$a_1 = \frac{n \sum x_i y_i - \sum x_i \sum y_i}{n \sum x_i^2 - (\sum x_i)^2}$$

$$a_1 = \frac{5(103,112,000) - 45,400(9,032)}{5(649,160,000) - (45,400)^2}$$

$$a_1 = \frac{515,560,000 - 410,028,800}{3,245,800,000 - 2,061,160,000} = \frac{105,531,200}{1,184,640,000} \approx 0.0891$$

**Interpretación:** Por cada paso adicional, se queman ~0.089 calorías. Es decir, por cada 1000 pasos, se queman ~89 calorías.

**Paso 3 – Calcular el intercepto \(a_0\):**

$$a_0 = \bar{y} - a_1 \bar{x} = 1806.4 - 0.0891(9080) = 1806.4 - 809.0 = 997.4$$

**Interpretación:** La latencia base (sin pasos, \(x=0\)) es ~997 kcal (gasto calórico basal).

**Paso 4 – Ecuación de la recta:**

$$\hat{y} = 997.4 + 0.0891 \cdot x$$

**Paso 5 – Calcular el margen de error:**

$$S_t = \sum (y_i - \bar{y})^2 = (665-1806.4)^2 + (1432-1806.4)^2 + (1896-1806.4)^2 + (2159-1806.4)^2 + (2690-1806.4)^2$$

$$S_t = 1,302,670 + 140,000 + 8,028 + 124,321 + 780,990 \approx 2,355,000$$

$$S_r = \sum (y_i - \hat{y}_i)^2 = (665 - 997.4)^2 + (1432 - 1442.9)^2 + (1896 - 1710.2)^2 + (2159 - 2066.6)^2 + (2690 - 2815.0)^2$$

$$S_r = 110,433 + 119 + 34,510 + 8,538 + 15,625 \approx 169,225$$

$$R^2 = \frac{S_t - S_r}{S_t} = \frac{2,355,000 - 169,225}{2,355,000} = \frac{2,185,775}{2,355,000} \approx 0.928$$

$$r = \sqrt{R^2} = \sqrt{0.928} \approx 0.963$$

$$S_{y/x} = \sqrt{\frac{S_r}{n-2}} = \sqrt{\frac{169,225}{3}} = \sqrt{56,408} \approx 237.5 \text{ kcal}$$

**Paso 6 – Predecir:**

Para \(x = 10,000\) pasos:
$$\hat{y}(10000) = 997.4 + 0.0891(10000) = 997.4 + 891 = 1888.4 \text{ kcal}$$

**Resultado:** Con 10,000 pasos, se estiman ~1888 kcal quemadas.

**Verificación:** La recta pasa por \((\bar{x}, \bar{y}) = (9080, 1806.4)\):
$$\hat{y}(9080) = 997.4 + 0.0891(9080) = 997.4 + 809.0 = 1806.4 ✓$$

## ¿Qué significa para no expertos?
"Si un usuario da 0, 5000, 8000, 12000 y 20400 pasos, y quema 665, 1432, 1896, 2159 y 2690 kcal respectivamente, podemos decir que la tendencia general es: por cada paso adicional, se queman ~0.089 calorías. Con 10,000 pasos, se estiman ~1888 kcal. El modelo explica el 92.8% de la variación, con un error típico de ~238 kcal."

