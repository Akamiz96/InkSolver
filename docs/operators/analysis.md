# Análisis de Operadores en Inksolver

## 🔢 Definición de los Operadores
El sistema **Inksolver** trabaja con los siguientes operadores matemáticos básicos:

- **Suma** (`+`) → Identificado como `sum`
- **Resta** (`-`) → Identificado como `sub`
- **Multiplicación** (`×`) → Identificado como `times`
- **División** (`/`) → Identificado como `div`
- **Igual** (`=`) → Identificado como `equals`

Estos nombres estandarizados facilitan el manejo de los operadores dentro del sistema y evitan ambigüedades en la detección y procesamiento.

---

## 📃 Fuente de los Datos
Las imágenes de los operadores utilizados en **Inksolver** provienen del conjunto de datos público **[Handwritten Math Symbols](https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols?select=data.rar)** de Kaggle.

- **Preprocesamiento de Datos:** No se realizó ningún tipo de preprocesamiento o limpieza de datos en las imágenes originales del conjunto de datos.

A continuación, se muestran varias representaciones gráficas del conjunto de datos utilizadas en el análisis.

### 📌 Ejemplo de imágenes de operadores
![Ejemplos de operadores matemáticos](images/operator_samples.png)

Esta imagen ilustra cómo se ven las muestras de operadores en el dataset. Se pueden observar variaciones en la escritura de cada operador, lo que representa un desafío para su detección y clasificación.

### 📊 Distribución de las Imágenes en el Dataset
El siguiente histograma muestra la cantidad de imágenes disponibles para cada operador en el conjunto de datos:

![Distribución de imágenes por operador](images/operator_histogram.png)

En este histograma se observa la cantidad de imágenes disponibles para cada uno de los operadores utilizados en **Inksolver**. Se pueden destacar los siguientes puntos clave:

- **El operador `sub` (resta) es el más representado**, con un total de **33,997 imágenes**, seguido de `sum` (suma) con **25,112 imágenes**.
- **El operador `equals` (=) cuenta con 13,104 imágenes**, lo que también le da una representación considerable en el dataset.
- **El operador `times` (multiplicación, ×) tiene una cantidad significativamente menor de imágenes, con solo 3,251**.
- **El operador `div` (división, /) es el menos representado en el conjunto de datos, con solo 199 imágenes**, lo que podría impactar en la precisión del modelo para este caso.

### 📊 Proporción de operadores en el dataset
Además del histograma, el siguiente gráfico de pastel muestra la proporción relativa de cada operador en el conjunto de datos:

![Distribución proporcional de operadores](images/operator_piechart.png)

Este gráfico permite visualizar la participación relativa de cada operador dentro del dataset. Se puede observar que:

- **Los operadores `sub` (resta) y `sum` (suma) representan la mayoría de los datos**, con una distribución dominante.
- **El operador `times` (multiplicación) y `equals` (=) tienen una presencia considerablemente menor** en comparación con los anteriores.
- **El operador `div` (división) tiene menos del 1% de los datos disponibles, razón por la cual no aparece en el gráfico**.

La baja representación del operador de división (`/`) puede significar un reto en su análisis. Esto sugiere que, en futuras versiones del proyecto, sería recomendable evaluar cómo afecta esta distribución al desempeño del reconocimiento de operadores y considerar si se requieren ajustes en el procesamiento.

---

### 🖥️ Generación de las Gráficas
Todas las gráficas presentadas en esta sección han sido generadas mediante **scripts en Python** que forman parte del repositorio de **Inksolver**. Estos scripts se encuentran en la carpeta `src/operators/` y permiten visualizar y analizar los datos del conjunto de operadores.

Los archivos disponibles en esta carpeta son:

- **`histogram_operators.py`** → Genera el histograma de distribución de operadores (`operator_histogram.png`).
- **`piechart_operators.py`** → Genera el gráfico de pastel con la proporción de operadores (`operator_piechart.png`).
- **`visualize_operators.py`** → Genera una muestra de imágenes de operadores (`operator_samples.png`).

Para ejecutar cada uno de estos scripts correctamente, sigue los siguientes pasos:

1. **Abrir una terminal** y navegar a la carpeta de los scripts con el siguiente comando:
   ```bash
   cd src/operators/
   ```

2. **Ejecutar el script deseado** con el intérprete de Python:
   ```bash
   python histogram_operators.py
   ```
   ```bash
   python piechart_operators.py
   ```
   ```bash
   python visualize_operators.py
   ```

Esto generará automáticamente las imágenes en la carpeta de salida definida en cada script.

📌 **Nota:** Asegúrate de tener instaladas las dependencias necesarias ejecutando:
```bash
pip install -r src/requirements.txt
```
Si los scripts requieren modificaciones o ajustes en la visualización, puedes editarlos directamente en la carpeta `src/operators/`.

---

## 🤖 Método de Reconocimiento de Operadores
El reconocimiento de operadores en **Inksolver** se basa en un análisis de proyecciones en diferentes ejes, lo que permite detectar los picos característicos en los histogramas normalizados. El proceso se lleva a cabo en los siguientes pasos:

---

### 📌 1. Proyección en los Ejes Horizontal y Vertical + Cálculo Normalizado  

Para analizar la estructura de los operadores, se genera una proyección de la imagen en los ejes **horizontal** y **vertical**. Esto permite visualizar la distribución de los píxeles y detectar patrones característicos en cada operador. La proyección se normaliza para mantener la escala uniforme y facilitar la comparación entre diferentes operadores.

A continuación, se presentan las proyecciones de cada operador con su respectivo análisis:

#### ➗ Proyección del Operador `div` (División)  
![Proyección Normalizada - División](images/projection_div.png)

**Análisis:**  
- La imagen original muestra una línea diagonal, característica del operador `/`.
- En la **proyección horizontal** (gráfico azul), se observa una fluctuación en la densidad de píxeles, con picos y valles que reflejan la inclinación de la línea.
- La **proyección vertical** (gráfico rojo) tiene una caída pronunciada en el centro, indicando que la mayor parte de los píxeles están distribuidos en los extremos superior e inferior.

---

#### 🔗 Proyección del Operador `equals` (Igual)  
![Proyección Normalizada - Igual](images/projection_equals.png)

**Análisis:**  
- La imagen original muestra dos líneas horizontales, características del operador `=`.
- En la **proyección horizontal**, se pueden notar valles bien definidos que representan la separación entre ambas líneas.
- En la **proyección vertical**, se observa una distribución más estable con menor variabilidad, indicando que la mayor parte de los píxeles están concentrados a lo largo del eje horizontal.

---

#### ➖ Proyección del Operador `sub` (Resta)  
![Proyección Normalizada - Resta](images/projection_sub.png)

**Análisis:**  
- La imagen original muestra una única línea horizontal, representando el operador `-`.
- En la **proyección horizontal**, se observa un valle pronunciado en la región donde se encuentra la línea.
- La **proyección vertical** es prácticamente constante, ya que la mayor parte de los píxeles están concentrados en una única franja horizontal.

---

#### ➕ Proyección del Operador `sum` (Suma)  
![Proyección Normalizada - Suma](images/projection_sum.png)

**Análisis:**  
- La imagen original muestra dos líneas perpendiculares que forman el símbolo `+`.
- En la **proyección horizontal**, se observan dos valles bien definidos, correspondientes a la presencia de la línea vertical en el centro.
- En la **proyección vertical**, se presentan dos caídas similares, reflejando la distribución de los píxeles en la línea horizontal.

---

#### ✖️ Proyección del Operador `times` (Multiplicación)  
![Proyección Normalizada - Multiplicación](images/projection_times.png)

**Análisis:**  
- La imagen original muestra dos líneas diagonales cruzadas formando el operador `×`.
- En la **proyección horizontal**, se observan múltiples variaciones, reflejando la intersección de ambas líneas.
- En la **proyección vertical**, se aprecian picos irregulares, indicando la presencia de líneas diagonales en distintos puntos del eje.

---

### 🖥️ Código para la Generación de Proyecciones  

El código utilizado para generar estas proyecciones se encuentra en el archivo **`projection_operators.py`**, ubicado en la carpeta `src/operators/`. Este script permite calcular las proyecciones horizontal y vertical de los operadores y normalizarlas para su análisis.

Para ejecutar el script correctamente, sigue estos pasos:

1. **Abrir una terminal** y navegar a la carpeta de los scripts con el siguiente comando:
   ```bash
   cd src/operators/
   ```

2. **Ejecutar el script con el intérprete de Python**:
   ```bash
   python projection_operators.py
   ```

Esto generará automáticamente las imágenes de proyección en la carpeta de salida definida en el script.

📌 **Nota:** Asegúrate de tener instaladas las dependencias necesarias ejecutando:
```bash
pip install -r src/requirements.txt
```
Si el script requiere ajustes o mejoras, puedes modificarlo directamente en la carpeta `src/operators/`.

---

### 📌 2. Rotación de 45 Grados + Nueva Proyección y Normalización  

Para mejorar la identificación de ciertos operadores, se aplica una **rotación de 45 grados** antes de realizar nuevamente el cálculo de la proyección normalizada. Esta técnica permite resaltar características clave que pueden ser difíciles de distinguir en la proyección estándar.

A continuación, se presentan las proyecciones después de la rotación junto con un análisis de cada operador:

#### ➗ Proyección del Operador `div` (División) después de la rotación  
![Proyección Rotada - División](images/projection_rotated_div.png)

**Análisis:**  
- La imagen original muestra una línea diagonal (`/`), y al rotarla 45° se vuelve más vertical, lo que permite una mejor diferenciación en los ejes.
- En la **proyección horizontal** (gráfico azul), se observa una mayor variabilidad debido a la inclinación del trazo.
- En la **proyección vertical** (gráfico rojo), se generan picos más pronunciados, resaltando la estructura alargada de la línea.

---

#### 🔗 Proyección del Operador `equals` (Igual) después de la rotación  
![Proyección Rotada - Igual](images/projection_rotated_equals.png)

**Análisis:**  
- La imagen original con dos líneas horizontales se transforma en dos líneas diagonales tras la rotación.
- En la **proyección horizontal**, los valles característicos de la separación entre las líneas se vuelven más pronunciados.
- En la **proyección vertical**, la densidad de píxeles cambia, pero la estructura de los dos trazos sigue siendo visible.

---

#### ➖ Proyección del Operador `sub` (Resta) después de la rotación  
![Proyección Rotada - Resta](images/projection_rotated_sub.png)

**Análisis:**  
- Al rotar la línea horizontal (`-`) 45°, se inclina y su forma cambia drásticamente.
- En la **proyección horizontal**, se observan cambios menos abruptos debido a la forma del operador.
- En la **proyección vertical**, la estructura se mantiene con una franja de densidad central clara.

---

#### ➕ Proyección del Operador `sum` (Suma) después de la rotación  
![Proyección Rotada - Suma](images/projection_rotated_sum.png)

**Análisis:**  
- La imagen del `+` se transforma en una `X` tras la rotación.
- En la **proyección horizontal**, se observan caídas más pronunciadas debido a la intersección de las líneas.
- En la **proyección vertical**, se generan múltiples valles, reflejando la estructura cruzada del operador.

---

#### ✖️ Proyección del Operador `times` (Multiplicación) después de la rotación  
![Proyección Rotada - Multiplicación](images/projection_rotated_times.png)

**Análisis:**  
- La imagen original del `×` cambia su orientación tras la rotación de 45°.
- En la **proyección horizontal**, la estructura se vuelve más simétrica.
- En la **proyección vertical**, se observan picos bien definidos que corresponden a la intersección de las líneas diagonales.

---

### 🖥️ Código para la Generación de Proyecciones Rotadas  

El código utilizado para generar estas proyecciones después de la rotación se encuentra en el archivo **`projection_rotated_operators.py`**, ubicado en la carpeta `src/operators/`. Este script permite calcular la proyección normalizada después de aplicar una rotación de 45 grados.

Para ejecutar el script correctamente, sigue estos pasos:

1. **Abrir una terminal** y navegar a la carpeta de los scripts con el siguiente comando:
   ```bash
   cd src/operators/
   ```

2. **Ejecutar el script con el intérprete de Python**:
   ```bash
   python projection_rotated_operators.py
   ```

Esto generará automáticamente las imágenes de proyección rotada en la carpeta de salida definida en el script.

📌 **Nota:** Asegúrate de tener instaladas las dependencias necesarias ejecutando:
```bash
pip install -r src/requirements.txt
```
Si el script requiere ajustes o mejoras, puedes modificarlo directamente en la carpeta `src/operators/`.

---

### 📌 3. Reglas de Detección  

Con base en los patrones obtenidos de las proyecciones, se establecen **reglas de detección** que permiten identificar cada operador de manera precisa. Estas reglas se basan en la comparación de los valles y picos de las proyecciones, así como en la simetría y distribución de los píxeles.

---

---

## 📌 Conclusiones del Análisis
- La detección de operadores mediante análisis de proyecciones e histogramas normalizados ha demostrado ser una solución eficiente y funcional.
- La técnica de rotación de 45 grados mejoró significativamente la detección del operador de multiplicación (`×`).
- La baja cantidad de imágenes para el operador de división (`/`) podría representar un reto en la detección precisa de este operador.
- La evaluación en el conjunto de datos ha permitido validar el método, aunque futuras pruebas en escritura manuscrita real podrían refinar el sistema.
- La distribución de datos en el conjunto de operadores no es uniforme, lo que podría afectar la precisión de reconocimiento de ciertos operadores, en especial `div`.

Este análisis establece una base sólida para la correcta interpretación de operadores en **Inksolver** y sienta las bases para mejoras futuras en su detección y clasificación.
