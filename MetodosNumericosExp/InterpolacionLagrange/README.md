# Interpolación de Lagrange

## ¿Qué es?
La interpolación de Lagrange es un método matemático que construye un **polinomio** \(P_n(x)\) de grado \(\le n\) que pasa **exactamente** por \(n+1\) puntos conocidos \((x_i, y_i)\). Se usa para estimar el valor de una función en un punto intermedio cuando solo conoces la función en algunos puntos.

La fórmula es:
$$P_n(x) = \sum_{i=0}^{n} y_i \cdot L_i(x)$$

donde

$$L_i(x) = \prod_{\substack{j=0 \\ j \ne i}}^{n} \frac{x - x_j}{x_i - x_j}$$

- \(L_i(x_i) = 1\) (se "enciende" en su nodo).
- \(L_i(x_j) = 0\) para \(j \ne i\) (se "apaga" en los demás nodos).
- \(\sum L_i(x) = 1\) en cualquier punto (sirve para verificar).

## ¿Para qué sirve? (en general)
- Estimar valores intermedios entre mediciones conocidas.
- Cuando confías en que los datos son **exactos** (sin ruido).
- Ejemplos: estimar temperatura entre mediciones, completar datos faltantes de un sensor, generar curvas suaves a partir de puntos discretos.

## ¿Para qué sirve en el proyecto?
- Tienes mediciones de calorías quemadas para ciertos niveles de actividad intensa (ej. 0 min, 30 min, 87.5 min).
- Quieres estimar las calorías para un nivel intermedio (ej. 45 min) sin tener que medirlo directamente.
- Útil para **completar datos faltantes** o **generar alertas** basadas en estimaciones exactas.

## De dónde salieron los datos

Los datos se tomaron **directamente del archivo `Sensores_limpio.csv`** (la capa intermedia del proyecto, después de la limpieza). Se seleccionaron 3 filas reales:

| Fila original | Id | ActivityDate | VeryActiveMinutes | Calories |
|---|---|---|---|---|
| 1 | 1624580081 | 2016-04-13 | 0 | 1344 |
| 2 | 1503960366 | 2016-04-13 | 30 | 1776 |
| 3 | 1503960366 | 2016-04-21 | 87.5 | 2690 |

**Cómo se obtuvieron:**
1. Se abrió el archivo `Sensores_limpio.csv` en Python (pandas).
2. Se filtraron las filas donde `VeryActiveMinutes` era 0, 30 y 87.5 (valores extremos y uno intermedio).
3. Se leyó el valor de `Calories` de cada fila.
4. Se formó la tabla de puntos \((x_i, y_i)\).

Estos son **datos reales de sensores wearable** (Fitbit), no inventados.

## Paso a paso (con explicación para no expertos)

**Paso 1 – Identificar los puntos que conoces:**
Tienes 3 puntos: \((0, 1344)\), \((30, 1776)\), \((87.5, 2690)\). Donde \(x\) = minutos de actividad intensa e \(y\) = calorías quemadas.

**Paso 2 – Construir los "polinomios base" \(L_i(x)\):**
Cada \(L_i(x)\) es una fórmula que vale **1** en su punto \(x_i\) y **0** en los demás puntos. Es como un "interruptor" que se enciende solo en su punto.

$$L_0(x) = \frac{(x - 30)(x - 87.5)}{(0 - 30)(0 - 87.5)} = \frac{(x-30)(x-87.5)}{2625}$$

$$L_1(x) = \frac{(x - 0)(x - 87.5)}{(30 - 0)(30 - 87.5)} = \frac{x(x-87.5)}{-1725}$$

$$L_2(x) = \frac{(x - 0)(x - 30)}{(87.5 - 0)(87.5 - 30)} = \frac{x(x-30)}{5075}$$

**Paso 3 – Verificar que los interruptores funcionan:**
- \(L_0(0) = \frac{(-30)(-87.5)}{2625} = 1\) ✓ (se enciende en su punto)
- \(L_0(30) = 0\) ✓ (se apaga en los demás)
- \(L_1(30) = \frac{30(30-87.5)}{-1725} = 1\) ✓
- \(L_1(0) = 0\) ✓

**Paso 4 – Construir el polinomio interpolante:**
Multiplica cada \(L_i(x)\) por su \(y_i\) y suma:

$$P_2(x) = 1344 \cdot L_0(x) + 1776 \cdot L_1(x) + 2690 \cdot L_2(x)$$

**Paso 5 – Estimar para un valor intermedio (ej. 45 minutos de actividad intensa):**

$$L_0(45) = \frac{(45-30)(45-87.5)}{2625} = \frac{15 \cdot (-42.5)}{2625} = -0.2429$$

$$L_1(45) = \frac{45(45-87.5)}{-1725} = \frac{45 \cdot (-42.5)}{-1725} = 1.1087$$

$$L_2(45) = \frac{45(45-30)}{5075} = \frac{45 \cdot 15}{5075} = 0.1330$$

$$P_2(45) = 1344(-0.2429) + 1776(1.1087) + 2690(0.1330) = 2003.54 \text{ kcal}$$

**Resultado:** Con 45 minutos de actividad intensa, se estiman ~2003 kcal quemadas.

**Verificación:** \(-0.2429 + 1.1087 + 0.1330 = 0.9988 \approx 1\) ✓ (los pesos suman 1).

## ¿Qué significa para no expertos?
"Si un usuario tiene 0, 30 y 87.5 minutos de actividad intensa, y quemó 1344, 1776 y 2690 kcal respectivamente, podemos estimar que con 45 minutos quema ~2003 kcal. La curva pasa exactamente por los 3 puntos que medimos."


