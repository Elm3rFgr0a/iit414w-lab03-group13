# Hito 1 — Problem Framing + Baseline

**Módulo:** Module 5 — Unit IV — Capstone: F1 Race Strategy Advisor  
**Tipo:** Entrega grupal (equipos de 2–3)  
**Peso:** 5% de NP (20% de la nota del Capstone)  
**Deadline:** Miércoles 6 de mayo de 2026 — 16:20 CLT (firme)

---

## Resumen

Subir un paquete Hito 1 al repositorio GitHub del equipo y enviar la URL por Canvas antes de las 16:20 del miércoles 6 de mayo. La entrega ocurre durante la sesión de clase (studio + clínica de entrega con TA).

---

## Decisiones bloqueadas (aplican a todos los equipos)

| Decisión | Valor fijo |
|---|---|
| Target | `is_top10` |
| Split temporal | Train 2019–2021 · Calibración 2022 · Test 2023–2024 |
| Baseline de referencia | Brier 0.132 y ROC-AUC 0.892 (modelo calibrado del docente) |

---

## Archivos a entregar

### 1. `framing.md` (2–3 páginas)
Debe cubrir las **7 secciones** del Team Decision Sheet:

1. **Decision context:** ¿Qué decisión de estrategia se apoya? ¿Quién? ¿Cuándo en el fin de semana de carrera?
2. **Target & primary metric:** target = `is_top10`, justificar la métrica elegida
3. **Baseline plan** con justificación defendible desde lógica F1
4. **What-if comparison plan** con al menos 2 escenarios específicos (valores concretos de features)
5. **Acknowledgment de al menos 2 de las 5 limitaciones conocidas del dataset**
6. **3 experimentos planificados para Hito 2** con hipótesis
7. **Workflow del equipo** (quién hace qué entre lunes y miércoles)

---

### 2. `hito1_baseline.ipynb`
Notebook ejecutable que:

- Carga `f1_strategy_race_level.csv`
- Implementa el split temporal bloqueado: train 2019–2021, calibración 2022, test 2023–2024
- Implementa al menos **un baseline** (heurístico O modelo simple)
- Reporta **Brier score, log loss y curva de calibración** en el test set vs `is_top10`
- Incluye una **celda de auditoría de leakage** que documenta: features pre-carrera vs inputs de escenario vs columnas de auditoría
- Corre end-to-end desde un clone limpio (Run All funciona)

---

### 3. `PROMPTS.md`
Al menos **2 interacciones con IA documentadas** usando el estándar de 6 campos:

| Campo | Descripción |
|---|---|
| Context | Situación en que se usó la IA |
| Prompts | El prompt exacto enviado |
| Output | La respuesta de la IA |
| Validation | Cómo se validó la respuesta |
| Adaptations | Qué se modificó o rechazó |
| Final Decision | Qué se decidió usar al final |

---

### 4. `README.md`
Runbook mínimo: instalación, cómo correr, dónde encontrar cada cosa.

---

## Split temporal

| Bloque | Temporadas | Uso |
|---|---|---|
| Train | 2019, 2020, 2021 | Ajustar el modelo |
| Calibración | 2022 | Ajustar el mapeo de calibración (Platt o isotónico). **Nunca usar para selección de modelos.** |
| Test | 2023, 2024 | Intocable hasta evaluación final. Ver solo una vez. |

---

## Baseline de referencia del docente

| Referencia | Brier (test) | ROC-AUC (test) |
|---|---|---|
| Grid-rule baseline | 0.208 | — |
| Modelo calibrado del docente | 0.132 | 0.892 |

- Superar grid-rule es el **mínimo aceptable**.
- Igualar o superar al modelo del docente — o explicar honestamente por qué no — es lo que lleva sobre 5.5 en Hito 1.

---

## 5 Limitaciones conocidas del dataset

Debe reconocerse **al menos 2** en `framing.md` con sus consecuencias:

1. Cobertura desde 2019 (no antes) — el artefacto de lap-level recuperado es 2019–2024.
2. `qualifying_position` es un proxy de `grid_position`; `qualifying_time_s` está vacío. **Tratar qualifying como señal real es un error calificado.**
3. `safety_car_periods` es un indicador binario por driver-carrera, no un conteo de intervalos completo.
4. Las features de estrategia son **observadas post-carrera** — son inputs de escenario, no señales pre-carrera.
5. La elección de estrategia **no es independiente** del ritmo del auto, piloto, clima e incidentes. Debe discutirse el confounding.

---

## Reglas de Leakage

- Features como `n_stops`, `compound_sequence` y `stint_lengths` son observaciones post-carrera.
- En este capstone están **permitidas** porque el producto es una herramienta de comparación de escenarios (inputs controlados por el usuario).
- El `framing.md` **debe declarar explícitamente** esta distinción — es un ítem calificado.
- No usar columnas de incidentes de carrera (safety car, resultado del clima) como si fueran conocidas antes de la carrera. Si se usan, deben enmarcarse como slices de auditoría, stress tests de escenario, o limitaciones.

---

## Guía para el Baseline

**Debe ser:**
- Defendible desde lógica F1 (sin referenciar el test set)
- Evaluado con el mismo split temporal
- Direccionalmente correcto (score más alto = mayor P(top10))

**Opciones aceptables:**
- Regla heurística con 1–2 features (ej: "P(top10) = 0.85 si grid_position ≤ 5, 0.30 si no")
- Modelo simple con 2–4 features y mínimo tuning (ej: regresión logística con `grid_position` + `constructor_tier`)

**No cuenta como baseline:**
- Baseline con dirección invertida tras ver resultados del test
- Baseline con información post-carrera (target leakage)
- Baseline que agrega sobre todas las temporadas incluyendo datos de test

---

## Rúbrica

| Dimensión | Peso | Qué se evalúa |
|---|---|---|
| Business framing | 25% | Decisión · tomador de decisión · ventana temporal · unidad de predicción · target bloqueado reconocido · métrica justificada · distinción features-escenario-no-leakage declarada |
| Validación temporal + leakage | 25% | Split correcto (2019–2021 / 2022 / 2023–2024); auditoría de leakage completa; bloque de calibración usado solo para calibración; sin contaminación del test |
| Baseline ejecutable | 30% | Notebook corre end-to-end; métrica del baseline reportada; baseline es F1-defendible; comparación vs baseline del docente con reflexión honesta |
| Plan de experimentos | 20% | Al menos 3 experimentos con hipótesis + métrica; escenarios what-if con valores concretos; workflow del equipo claro |

---

## Lo que distingue un Hito 1 fuerte

✅ Supera grid-rule (Brier 0.208) y se acerca o iguala al modelo del docente (Brier 0.132)  
✅ Declara explícitamente la distinción features-de-estrategia-como-inputs-de-escenario  
✅ Divulga al menos 3 de las 5 limitaciones con sus consecuencias  
✅ Escenarios what-if con valores específicos de features (no frases genéricas)  
✅ `PROMPTS.md` documenta al menos un fallo o sugerencia rechazada de la IA  

---

## Errores comunes a evitar

❌ **Tuning en el test set.** Una vez visto 2023–2024, el modelo queda bloqueado.  
❌ **Baselines débiles.** "Predecir la clase mayoritaria" no sirve — el baseline debe reflejar lógica F1.  
❌ **Sobreestimación en el memo.** No afirmar que está listo para deployment si la evidencia es marginal.  
❌ **Escenarios what-if genéricos.** "Comparar 1-stop vs 2-stop" no es un escenario. "LEC, Mónaco 2024, n_stops=1 con M-H vs n_stops=2 con M-M-H" sí lo es.  

---

## Política de entrega y penalizaciones

| Estado de entrega | Observación TA | Resultado individual |
|---|---|---|
| Entregado ≤ 16:20 | Presente + trabajando activamente en 3+ de 4 rondas | Crédito completo del equipo, sin modificador |
| Entregado ≤ 16:20 | Presente pero sin trabajar en 2+ rondas | −1.0 de la nota individual del Hito 1 |
| Entregado ≤ 16:20 | Ausente sin justificación previa | −1.5 de la nota individual del Hito 1 |
| Entregado ≤ 16:20 | Ausencia justificada (enviada antes de las 13:50) + commits visibles en GitHub | Sin modificador |
| Entregado 16:21–23:59 con problema técnico registrado por TA | Cualquiera | Sin penalización |
| Entregado 16:21–23:59 sin problema registrado | Cualquiera | −10% a la nota del equipo |
| Sin entrega antes de las 23:59 | Cualquiera | Hito 1 = 1.0 para todo el equipo |

Los modificadores no pueden bajar la nota final por debajo de 1.0.

---

## Política de uso de IA

El curso es **open-AI**. El `PROMPTS.md` es obligatorio. Presentar trabajo que no coincida con los prompts documentados, copiar del repo de otro equipo, u ocultar el uso de IA son violaciones de integridad académica.
