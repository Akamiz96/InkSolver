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

1. **Proyección en el eje horizontal y en el eje vertical**  
   - Se calcula la distribución de los píxeles en cada uno de estos ejes.

2. **Rotación de 45 grados**  
   - Para mejorar la diferenciación, especialmente en operadores como `×` (multiplicación), se realiza una rotación de 45 grados antes de aplicar una nueva proyección en el eje horizontal.

3. **Cálculo del histograma normalizado**  
   - A partir de las proyecciones obtenidas, se genera un histograma normalizado que refleja los picos característicos de cada operador.

4. **Reglas de detección**  
   - Basado en los picos del histograma y reglas predefinidas, se determina qué operador está presente en la imagen analizada.

---

## 📌 Conclusiones del Análisis
- La detección de operadores mediante análisis de proyecciones e histogramas normalizados ha demostrado ser una solución eficiente y funcional.
- La técnica de rotación de 45 grados mejoró significativamente la detección del operador de multiplicación (`×`).
- La baja cantidad de imágenes para el operador de división (`/`) podría representar un reto en la detección precisa de este operador.
- La evaluación en el conjunto de datos ha permitido validar el método, aunque futuras pruebas en escritura manuscrita real podrían refinar el sistema.
- La distribución de datos en el conjunto de operadores no es uniforme, lo que podría afectar la precisión de reconocimiento de ciertos operadores, en especial `div`.

Este análisis establece una base sólida para la correcta interpretación de operadores en **Inksolver** y sienta las bases para mejoras futuras en su detección y clasificación.
