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
|   |   |   ├── dataset/   # Datos provenientes de Kaggle
|   |   |   ├── test/      # Datos realizados por el autor  
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
│   ├── operands/          # Documentación sobre operandos
│   │   ├── analysis.md   # Documento de análisis
│   ├── equations/         # Documentación sobre ecuaciones
│   │   ├── analysis.md   # Documento de análisis
```

## 🚀 Instalación
  
### 🏗️ Usando un Entorno Virtual (Opcional pero Recomendado)  
Para evitar conflictos con otras dependencias de Python, puedes crear un entorno virtual para este proyecto siguiendo estos pasos:

1. **Crear un entorno virtual**  
   ```bash
   python3 -m venv .venv
   ```

2. **Activar el entorno virtual**  
   ```bash
   source .venv/bin/activate
   ```

3. **Confirmar que el entorno virtual está activado**  
   ```bash
   which python
   ```
   Debería mostrar una ruta dentro de `.venv/`.

4. **Desactivar el entorno virtual (cuando termines de usarlo)**  
   ```bash
   deactivate
   ```

🔗 Más detalles sobre entornos virtuales en Python:  
[Python Packaging Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

### 📦 Instalación de Dependencias  
Una vez activado el entorno virtual (o sin él si decides no usarlo), instala las dependencias necesarias con:

```bash
pip install -r src/requirements.txt
```

## 📝 Estado del Proyecto  
Inksolver está en desarrollo activo. Próximamente se agregará un ejemplo práctico de uso.  

## 📜 Licencia  
Este proyecto está licenciado bajo la **MIT License**. Puedes ver más detalles en el archivo [LICENSE](LICENSE).  

---
