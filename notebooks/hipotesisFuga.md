# Si tuviéramos que adivinar quién fuga solo con 3 preguntas, ¿cuáles elegiríamos y por qué?

## Nuestras 3 hipótesis (preguntas)

1. **¿El cliente tiene contrato mes a mes (Month-to-month)?**  
   *Por qué:* los contratos mensuales no tienen barrera de salida; la fuga se concentra en este segmento. Es la variable con mayor poder discriminante individual.

2. **¿Lleva menos de 12 meses como cliente (tenure bajo)?**  
   *Por qué:* el riesgo de fuga es mayor en los primeros meses, antes de que se forme el hábito de uso y la lealtad. A mayor antigüedad, menor probabilidad de fuga.

3. **¿Paga con cheque electrónico (Electronic check) y/o tiene cargos mensuales altos?**  
   *Por qué:* el cheque electrónico se asocia a clientes con menor compromiso y mayor fricción en el pago; combinado con cargos altos, aumenta la propensión a cancelar.

## Por qué estas 3 y no otras

- Son variables **disponibles al momento de la campaña** (no requieren datos futuros).
- Son **accionables**: podemos ofrecer descuentos, migración a contrato anual, o cambio de método de pago.
- Cubren las 3 dimensiones clave del churn: **compromiso contractual**, **madurez de la relación** y **fricción/costo**.
- Variables descartadas (p. ej., género, servicio de teléfono) mostraron bajo poder predictivo en el EDA.

## Conexión con el Avance 2

Estas 3 hipótesis se convierten en las 3 primeras divisiones del árbol de decisión (sesión 7): primero el tipo de contrato, luego la antigüedad, luego el método de pago/cargos. El resultado son 2 reglas de negocio exportables a una campaña de retención.

---
*Entregable Avance 1 – "3 preguntas para adivinar quién fuga".*