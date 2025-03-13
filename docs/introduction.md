# Introducción a Inksolver

## 🔍 Contexto y Motivación
La digitalización de expresiones matemáticas escritas a mano sigue siendo un desafío en diversos ámbitos, desde la educación hasta la investigación científica. La transcripción manual de ecuaciones puede ser tediosa y propensa a errores, lo que afecta la eficiencia de estudiantes, docentes e investigadores. 

Con la creciente disponibilidad de dispositivos móviles y tabletas, el reconocimiento de escritura manuscrita ha tomado mayor relevancia. En este contexto, **Inksolver** surge como una solución que permite interpretar y resolver operaciones matemáticas simples a partir de imágenes, sin el uso de técnicas avanzadas de inteligencia artificial.

## 🌟 Objetivo del Proyecto
### Objetivo General
Desarrollar un sistema basado en reconocimiento de patrones que permita interpretar y resolver expresiones matemáticas simples a partir de imágenes, facilitando la digitalización y automatización de operaciones básicas.

### Objetivos Específicos
- Implementar un módulo de reconocimiento óptico de caracteres (OCR) para identificar ecuaciones matemáticas en imágenes.
- Desarrollar un algoritmo de procesamiento que convierta la ecuación detectada en una expresión interpretable.
- Implementar un módulo de cálculo que resuelva operaciones matemáticas básicas (suma, resta, multiplicación y división) con dos operandos.
- Evaluar el rendimiento y precisión del sistema en distintos tipos de escritura y formatos de imagen.

## 🔄 Antecedentes y Estado del Arte
El reconocimiento de caracteres aplicado a ecuaciones matemáticas tiene una historia que se remonta a mediados del siglo XX, cuando comenzaron a desarrollarse los primeros sistemas de OCR (Reconocimiento Óptico de Caracteres). Inicialmente, estos sistemas solo podían procesar texto impreso con formatos estrictamente definidos. Durante la década de 1960, se exploró el reconocimiento de caracteres manuscritos, lo que derivó en los primeros sistemas de interpretación de ecuaciones matemáticas.

A lo largo de los años, los métodos tradicionales para el reconocimiento de caracteres han incluido:
- **Métodos basados en características geométricas:** Detección de líneas, curvas y ángulos característicos.
- **Análisis de patrones y reducción de dimensionalidad:** Uso de algoritmos como PCA y clasificadores como k-NN.
- **Sistemas basados en reglas heurísticas:** Identificación de caracteres mediante relaciones espaciales y patrones predefinidos.
- **Métodos basados en plantillas:** Comparación de imágenes con bases de datos de patrones predefinidos.

Si bien estos métodos han demostrado ser efectivos en entornos controlados, su aplicabilidad en contextos de escritura manual variada es limitada. **Inksolver** busca retomar enfoques tradicionales de reconocimiento de patrones sin recurrir a redes neuronales o modelos de aprendizaje profundo, enfatizando técnicas de procesamiento de imágenes y análisis geométrico.

## 📖 Metodología
El sistema de **Inksolver** se compone de cuatro módulos principales:
1. **Segmentación de la Operación:** Separa la expresión matemática en tres imágenes: primer operando, operador matemático y segundo operando.
2. **Reconocimiento del Operador:** Identifica la operación a realizar (*+, -, ×, ÷*).
3. **Reconocimiento de los Operandos:** Interpreta los números manuscritos y los convierte en valores numéricos.
4. **Cálculo del Resultado:** Aplica la operación matemática y devuelve el resultado al usuario.

## 💪 Entregables y Avances
### Avance 1: Preprocesamiento e Identificación de Caracteres Aislados (Marzo 2025)
- Implementación del módulo de OCR para extraer números y operadores matemáticos de imágenes.
- Desarrollo de técnicas de preprocesamiento de imágenes (binarización, eliminación de ruido, segmentación).
- Identificación y clasificación de caracteres solitarios (0-9 y operadores básicos).
- Documento con avances, métricas de precisión y ejemplos.

### Avance 2: Procesamiento de Expresiones y División en Componentes (Abril 2025)
- Implementación del módulo de procesamiento para interpretar estructuras matemáticas.
- Desarrollo de algoritmos de segmentación para dividir expresiones en operandos y operadores.
- Integración de reconocimiento de patrones para validar estructuras matemáticas.
- Pruebas con imágenes de ecuaciones en escritura impresa y manuscrita.

### Entrega Final: Implementación del Motor de Cálculo y Versión Funcional (Mayo - Junio 2025)
- Implementación del módulo de cálculo para resolver operaciones básicas.
- Optimización del sistema de OCR y procesamiento de ecuaciones.
- Ajustes en la detección de diferentes estilos de escritura manuscrita.
- Validación con un conjunto de datos más amplio para evaluar la precisión y confiabilidad.
- Documento final con resultados, conclusiones y mejoras futuras.

## 📜 Referencias
1. Smith, R. (2007). *An overview of the Tesseract OCR engine.* International Conference on Document Analysis and Recognition.
2. Zanibbi, R., Blostein, D., & Cordy, J. R. (2002). *Recognizing mathematical notation.* Handbook of Character Recognition and Document Image Analysis.
3. Mouchère, H., Viard-Gaudin, C., Zanibbi, R., & Kim, D. (2016). *Pattern recognition approaches in handwritten mathematical expressions: An overview.* International Journal on Document Analysis and Recognition.
