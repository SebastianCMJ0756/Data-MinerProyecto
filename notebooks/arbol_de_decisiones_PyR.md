# Avance 2: Primer Artefacto

## Árbol de Decisiones

```mermaid
flowchart TD
    N1["¿Los pasos totales son iguales o menores a 4.200 pasos?"] --> S1((Si))
    N1 --> N1_NO((No))

    S1 --> N2["Actividad intensa <= 5 min?"]
    N2 --> S2((Si))
    N2 --> N2_NO((No))

    S2 --> D1[/Sedentarismo de alto riesgo/]
    N2_NO --> D2[/Persona activa sin riesgo/]

    N1_NO --> N3["Calorías <= 2100.0?"]
    N3 --> S3((Si))
    N3 --> N3_NO((No))

    N3_NO --> D3[/Paciente estable/]

    S3 --> R1["Riesgo moderado"]
    R1 --> N4["Horas de sueño <= 6h"]
    N4 --> S4((Si))
    N4 --> N4_NO((No))

    S4 --> D4[/Riesgo de sueño insuficiente/]
    N4_NO --> D5[/Riesgo moderado/]
```

### Discusión de las Reglas

#### ¿Estas reglas les sirven para un entorno real?
Sí, pueden ser altamente interpretables para cualquier médico o analista, ya que son fáciles y rápidas en calcular y permiten también automatizar alertas tempranas de forma directa.
Aunque el modelo actual está basado en umbrales estáticos y simples, y esto puede generar falsos positivos o simplemente ignorar la variabilidad individual de cada paciente.

#### ¿Qué variable falta?
* **Frecuencia cardiaca en reposo:** Indicador crítico de estrés cardiovascular y recuperación física.
* **Edad y antecedentes médicos del paciente:** El nivel de tolerancia al sedentarismo varía drásticamente según la edad o patologías previas.
* **Nivel de estrés:** Vital para cruzarlo con la eficiencia del sueño y detectar fatiga real.
* **Historial de medicación:** En la parte de fármacos que influyan directamente en el ritmo cardiaco o en los patrones de sueño.
