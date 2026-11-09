# Veredicto Técnico – Torneo de Clasificadores (Dataset Wearable)

**Proyecto:** Data-MinerProyecto · Wearable: Gemelo Digital y Minería de Datos en Sensores de Sedentarismo

## Contexto

Se compararon tres clasificadores (Árbol de Decisión, Naive Bayes y KNN) sobre el dataset wearable (sedentarismo) para predecir `Nivel_Sedentarismo` (Alto/Bajo), siguiendo la metodología de la Sesión 8.

- **Features (sin fuga de datos):** `VeryActiveMinutes`, `LightlyActiveMinutes`, `FairlyActiveMinutes`, `Calories`, `Nivel_Pasos` (one-hot).
- **Partición:** `train_test_split(test_size=0.25, random_state=42, stratify=y)` → Train: 651 | Test: 217.

## 1. Árbol de Decisión (max_depth=4)

**Qué se usó:** `DecisionTreeClassifier(max_depth=4, random_state=42)`.

**Resultados:**
- Accuracy train: **0.842**
- Accuracy test: **0.816**
- Tiempo de entrenamiento: 0.0025 s

**Veredicto:** Accuracy moderado (0.816) con cierto sobreajuste (brecha train/test de 0.026). Su principal ventaja es la **interpretabilidad**: genera reglas legibles (ej. "si VeryActiveMinutes bajo y Calories bajo → riesgo alto"), ideales para explicar decisiones a médicos o pacientes. Recomendado si el negocio exige transparencia.

## 2. Naive Bayes (GaussianNB)

**Qué se usó:** `GaussianNB()` (variante para variables numéricas, asume distribución gaussiana por clase).

**Resultados:**
- Accuracy train: **0.779**
- Accuracy test: **0.774**
- Tiempo de entrenamiento: 0.0014 s (el más rápido)

**Veredicto:** El accuracy más bajo (0.774), pero el más **estable** (brecha train/test de solo 0.005) y el más rápido. Funciona como **línea base honesta**: si un modelo más complejo no supera a Naive Bayes, sobra complejidad. No ofrece reglas interpretables.

## 3. K-Vecinos (KNN, k=5)

**Qué se usó:** `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))`.

**Resultados:**
- Accuracy train: **0.856**
- Accuracy test: **0.825** (el mejor de los 3)
- Tiempo de entrenamiento: 0.0026 s
- KNN **sin escalar**: accuracy test **0.811** (baja 0.014) → confirma que la escala importa.

**Efecto de k:**

| k | acc_train | acc_test | Diagnóstico |
|---|---|---|---|
| 1 | 1.000 | 0.779 | Sobreajuste (memoriza) |
| 5 | 0.856 | 0.825 | Buen equilibrio |
| 11 | 0.828 | 0.788 | Empeora en test |
| 31 | 0.797 | 0.793 | Subajuste |
| 101 | 0.796 | 0.793 | Subajuste (tiende a la clase mayoritaria) |

**KNN con `weights='distance'`:** accuracy test 0.816 (no mejora respecto al uniforme).

**Veredicto:** Mejor accuracy en test (0.825) con k=5 y escalado. Sin embargo, es **lento en predicción** (busca vecinos en toda la historia) y no es interpretable. Recomendado si solo importa la precisión.

## Tabla comparativa final

| Criterio | Árbol (prof=4) | Naive Bayes | KNN (k=5, escalado) |
|---|---|---|---|
| Accuracy test | 0.816 | 0.774 | **0.825** |
| Interpretabilidad | **Alta** (reglas legibles) | Baja | Baja-media |
| Velocidad predicción | Rápida | Instantánea | Lenta (busca vecinos) |
| ¿Requiere escalar? | No | No | Sí (crítico) |
| Riesgo sobreajuste | Moderado (brecha 0.026) | Mínimo | Moderado (brecha 0.031) |

## Conclusión: ¿qué modelo usar para el proyecto?

**Recomendación final:**
- Si el negocio exige **explicar decisiones** (alertas a médicos/pacientes, regulación): elegir el **Árbol** (0.816), con reglas legibles.
- Si solo importa la **precisión** y no hay restricción de explicabilidad: elegir **KNN k=5** (0.825), asumiendo el costo de predicción.
- Usar **Naive Bayes (0.774)** como **línea base permanente** para detectar sobrecomplejidad.

> La decisión final la definen la **interpretabilidad y la operación**, no solo el accuracy.

---
*Veredicto Técnico – Torneo de Clasificadores (Sesión 8).*