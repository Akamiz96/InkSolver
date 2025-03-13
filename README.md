# Inksolver  

📄 **Solucionador de Operaciones Matemáticas Manuscritas**  

## 📌 Descripción  
**Inksolver** es una herramienta diseñada para resolver pequeñas operaciones matemáticas básicas (*suma, resta, multiplicación y división*) donde los operandos, de una sola cifra cada uno, han sido escritos a mano. El programa procesa la operación manuscrita y devuelve el resultado al usuario sin el uso de técnicas avanzadas de inteligencia artificial.  

## 🎯 Objetivo del Proyecto  
Este proyecto tiene como finalidad explorar métodos tradicionales de reconocimiento de patrones para interpretar y solucionar operaciones matemáticas simples, sin depender de redes neuronales u otras técnicas de aprendizaje profundo.  

## ⚙️ Funcionamiento General  
El sistema se compone de cuatro módulos principales:  
1. **Segmentación de la Operación** → Separa la operación en tres imágenes: primer operando, operador matemático y segundo operando.  
2. **Reconocimiento del Operador** → Identifica qué operación se debe aplicar (*+, -, ×, ÷*).  
3. **Reconocimiento de los Operandos** → Interpreta los números manuscritos para convertirlos en valores numéricos.  
4. **Cálculo del Resultado** → Aplica la operación matemática y devuelve el resultado.

## 📊 Datos  
Para el desarrollo de **Inksolver**, se utilizaron datos provenientes de conjuntos de datos públicos en Kaggle:  
- **[Handwritten Digits (0-9)](https://www.kaggle.com/datasets/olafkrastovski/handwritten-digits-0-9)** → Utilizado para el reconocimiento de los operandos escritos a mano.  
- **[Handwritten Math Expressions Dataset](https://www.kaggle.com/datasets/govindaramsriram/handwritten-math-expressions-dataset)** → Fuente de inspiración para el proyecto y referencia para la segmentación de expresiones matemáticas.  
  

## 🛠️ Tecnologías Utilizadas  
El proyecto está desarrollado en **Python** y utiliza las siguientes librerías:  
- **OpenCV** → Procesamiento de imágenes y segmentación.  
- **NumPy** → Manipulación de datos numéricos.  
- **Pandas** → Organización y estructuración de datos.  

## 📂 Estructura del Proyecto  
```
Inksolver/
│── README.md              # Explicación básica del proyecto
│
│── src/                   # Código fuente principal
│   ├── operators/         # Identificación del operador matemático
│   ├── operands/          # Reconocimiento de los operandos
│   ├── equations/         # Solución de la ecuación matemática
│   ├── requirements.txt   # Dependencias necesarias para el proyecto
│
│── data/                  # Conjunto de datos utilizados
│   ├── operators/         # Datos de operadores
│   │   ├── raw/          # Datos sin procesar
│   │   ├── processed/    # Datos procesados
│   ├── operands/          # Datos de operandos
│   │   ├── raw/          # Datos sin procesar
│   │   ├── processed/    # Datos procesados
│   ├── equations/         # Datos de ecuaciones
│   │   ├── raw/          # Datos sin procesar
│   │   ├── processed/    # Datos procesados
│
│── docs/                  # Documentación
│   ├── introduction.md    # Introducción general al proyecto
│   ├── operators/         # Documentación sobre operadores
│   │   ├── analysis.md   # Documento de análisis
│   │   ├── process.md    # Documento de proceso
│   │   ├── results.md    # Documento de resultados
│   ├── operands/          # Documentación sobre operandos
│   │   ├── analysis.md   # Documento de análisis
│   │   ├── process.md    # Documento de proceso
│   │   ├── results.md    # Documento de resultados
│   ├── equations/         # Documentación sobre ecuaciones
│   │   ├── analysis.md   # Documento de análisis
│   │   ├── process.md    # Documento de proceso
│   │   ├── results.md    # Documento de resultados
```

## 🚀 Instalación  
Para instalar las dependencias del proyecto, ejecuta el siguiente comando:  

```bash
pip install -r src/requirements.txt
```

## 📝 Estado del Proyecto  
Inksolver está en desarrollo activo. Próximamente se agregará un ejemplo práctico de uso.  

## 📜 Licencia  
Este proyecto está licenciado bajo la **MIT License**. Puedes ver más detalles en el archivo [LICENSE](LICENSE).  

---
