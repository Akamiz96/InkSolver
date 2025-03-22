# Análisis de Operandos en Inksolver

## 🔢 Definición de los Operandos

En el sistema **Inksolver**, los operandos corresponden a los **números de una sola cifra del 0 al 9**. Estos dígitos son fundamentales para la representación de las operaciones matemáticas que el sistema debe interpretar y resolver.

Cada dígito es tratado como una clase independiente y debe ser identificado correctamente a partir de su representación escrita a mano.

---

## 📃 Fuente de los Datos

Las imágenes de operandos utilizadas en **Inksolver** provienen de un subconjunto seleccionado del dataset **[Handwritten Math Symbols](https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols)** alojado en Kaggle. Este conjunto contiene miles de imágenes escritas a mano que incluyen tanto símbolos matemáticos como dígitos numéricos.

Para el caso de los operandos, se utilizaron exclusivamente las imágenes etiquetadas con los dígitos del **0 al 9**, sin realizar modificaciones en el contenido original ni aplicar filtros adicionales. Esto asegura una representación variada y realista de la escritura manuscrita de cada número.

### 🖼️ Ejemplo de Imágenes de Operandos

A continuación, se presenta una muestra visual con ejemplos de operandos para cada una de las 10 clases disponibles (del 0 al 9), que refleja la variabilidad de la escritura manuscrita:

![Ejemplos de operandos](images/operand_samples.png)

Esta imagen permite observar cómo cambia la forma de un mismo número dependiendo de la persona que lo escribió. Esta variación justifica la necesidad de aplicar técnicas robustas para su análisis y clasificación.

### 📊 Distribución de las Imágenes en el Dataset

Para entender mejor la composición del dataset, se generó un histograma con la cantidad de imágenes disponibles para cada dígito. Esto permite detectar posibles desequilibrios en el número de ejemplos por clase.

![Distribución de imágenes por operando](images/operand_histogram.png)

En este histograma se observa la cantidad de imágenes disponibles para cada uno de los operadores utilizados en **Inksolver**. Se pueden destacar los siguientes puntos clave:

- **Los dígitos `1` y `2` son los más representados**, con más de 26,000 imágenes cada uno, lo cual puede influir positivamente en la precisión del modelo para estas clases.

- **El dígito `3` también cuenta con una buena representación (10,909 imágenes)**, seguido por `4` con 7,396 y `0` con 6,914 ejemplos.

- **Los dígitos `5`, `6`, `7`, `8` y `9` tienen una representación significativamente menor**, con menos de 4,000 ejemplos cada uno. Esta diferencia podría afectar negativamente el rendimiento del modelo en estas clases debido a la menor cantidad de muestras para aprender sus características.

- **El dígito `7` es el menos representado**, con apenas 2,909 imágenes disponibles en el conjunto de datos.

Este análisis resalta un **desequilibrio evidente en la distribución de clases**, lo cual es importante tener en cuenta para etapas posteriores de entrenamiento, evaluación y validación del modelo.

### 📈 Proporción de Operandos en el Dataset

Además del conteo absoluto, se analizó la proporción relativa de cada dígito dentro del conjunto total de operandos. Esto se visualiza mediante un gráfico de pastel que muestra cómo se distribuyen los datos entre las distintas clases.

![Distribución proporcional de operandos](images/operand_piechart.png)

Este gráfico permite visualizar la participación relativa de cada operando dentro del dataset. Se puede observar que:

- **Los dígitos `1` y `2` dominan el conjunto de datos**, representando juntos más del **55%** del total de imágenes (`1` con 28.1% y `2` con 27.7%). Esto puede facilitar la clasificación de estos dígitos, pero también generar un sesgo del modelo hacia ellos.

- **El dígito `3` ocupa el tercer lugar**, con un 11.6% de participación, aún con una representación considerable.

- **Los dígitos `0` y `4` tienen una representación intermedia**, con un 7.3% y 7.8% respectivamente.

- **Los dígitos `5` al `9` están poco representados**, con porcentajes que van del **3.1% al 4.0%**, lo cual podría impactar negativamente la capacidad del modelo para aprender patrones confiables para estas clases.

Este desequilibrio en la distribución de clases refuerza la necesidad de considerar técnicas de compensación o balanceo si se desea entrenar un modelo robusto que funcione bien en todos los operandos por igual.

---

### 🖥️ Generación de las Gráficas

Todas las gráficas presentadas en esta sección han sido generadas mediante **scripts en Python** que forman parte del repositorio de **Inksolver**. Estos scripts se encuentran en la carpeta `src/operands/` y permiten visualizar y analizar los datos del conjunto de operadores.

Los archivos disponibles en esta carpeta son:

- **`histogram_operators.py`** → Genera el histograma de distribución de operadores (`operator_histogram.png`).
- **`piechart_operators.py`** → Genera el gráfico de pastel con la proporción de operadores (`operator_piechart.png`).
- **`visualize_operators.py`** → Genera una muestra de imágenes de operadores (`operator_samples.png`).

Para ejecutar cada uno de estos scripts correctamente, sigue los siguientes pasos:

1. **Abrir una terminal** y navegar a la carpeta de los scripts con el siguiente comando:
   ```bash
   cd src/operands/
   ```

2. **Ejecutar el script deseado** con el intérprete de Python:
   ```bash
   python visualize_operands.py
   ```
   ```bash
   python analyze_operands.py
   ```

Esto generará automáticamente las imágenes en la carpeta de salida definida en cada script.

📌 **Nota:** Asegúrate de tener instaladas las dependencias necesarias ejecutando:
```bash
pip install -r src/requirements.txt
```
Si los scripts requieren modificaciones o ajustes en la visualización, puedes editarlos directamente en la carpeta `src/operands/`.

---
