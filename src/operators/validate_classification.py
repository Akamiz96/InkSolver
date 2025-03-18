"""
===============================================================================
Proyecto: Inksolver
Archivo: validate_classification.py
Descripcion: Valida el proceso de clasificacion de operadores matematicos utilizando una matriz de confusion.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-16
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: Pandas, NumPy, Matplotlib, Seaborn, os, warnings, scikit-learn
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python validate_classification.py
===============================================================================
Notas:
- El dataset de clasificacion debe estar en 'operator_results/operator_classification_results.csv'.
- Los resultados de validacion se guardaran en 'operator_validation/'.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.metrics import confusion_matrix

# Suprimir warnings innecesarios
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de clasificación
csv_path = "operator_results/operator_classification_results.csv"

# Definir la carpeta donde se guardarán los resultados de validación
output_dir = "operator_validation"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

# Cargar los datos del archivo CSV
print("\n\033[91m🔴 Cargando datos desde el archivo CSV...\033[0m")
df = pd.read_csv(csv_path)

# Extraer las etiquetas reales y las predicciones del dataset
print("\033[91m🔴 Extrayendo etiquetas reales y predichas...\033[0m")
y_true = df["Categoria"]  # Etiquetas reales
y_pred = df["Prediccion"]  # Etiquetas predichas por el modelo

# Definir las clases presentes en el dataset, incluyendo "Desconocido" en caso de errores
print("\033[91m🔴 Definiendo clases y asegurando la presencia de 'Desconocido'...\033[0m")
classes = sorted(set(y_true.unique()) | set(y_pred.unique()) | {"Desconocido"})

# Construir la matriz de confusión
print("\033[91m🔴 Construyendo la matriz de confusion...\033[0m")
conf_matrix = confusion_matrix(y_true, y_pred, labels=classes)

# Guardar la matriz de confusión en un archivo CSV
print("\033[91m🔴 Guardando la matriz de confusion en CSV...\033[0m")
conf_matrix_df = pd.DataFrame(conf_matrix, index=classes, columns=classes)
conf_matrix_csv_path = os.path.join(output_dir, "confusion_matrix.csv")
conf_matrix_df.to_csv(conf_matrix_csv_path)

# Generar y guardar la imagen de la matriz de confusión
print("\033[91m🔴 Generando y guardando la imagen de la matriz de confusion...\033[0m")
plt.figure(figsize=(8,6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicción")
plt.ylabel("Etiqueta Real")
plt.title("Matriz de Confusión")

conf_matrix_img_path = os.path.join(output_dir, "confusion_matrix.png")
plt.savefig(conf_matrix_img_path, dpi=300, bbox_inches="tight")

# Intentar mostrar la imagen sin errores
try:
    plt.show(block=False)
except:
    pass

# Calcular la precisión global del modelo
print("\033[91m🔴 Calculando precisión global del modelo...\033[0m")
total_correct_predictions = np.sum(np.diag(conf_matrix))
total_predictions = np.sum(conf_matrix)
accuracy_percentage = (total_correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0.0

# Diccionario para almacenar métricas de cada clase
metrics_per_class = {}

# Calcular métricas para cada clase: Precisión, Recall, Especificidad y F1-Score
print("\033[91m🔴 Calculando métricas por clase...\033[0m")
for i, class_label in enumerate(classes):
    TP = conf_matrix[i, i]  # Verdaderos Positivos
    FN = np.sum(conf_matrix[i, :]) - TP  # Falsos Negativos
    FP = np.sum(conf_matrix[:, i]) - TP  # Falsos Positivos
    TN = total_predictions - (TP + FN + FP)  # Verdaderos Negativos

    precision = (TP / (TP + FP)) * 100 if (TP + FP) > 0 else 0.0
    recall = (TP / (TP + FN)) * 100 if (TP + FN) > 0 else 0.0
    specificity = (TN / (TN + FP)) * 100 if (TN + FP) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    metrics_per_class[class_label] = {
        "Precisión (%)": precision,
        "Recall (%)": recall,
        "Especificidad (%)": specificity,
        "F1-Score (%)": f1_score
    }

# Generar el reporte de validación
print("\033[91m🔴 Generando reporte de validación...\033[0m")
report_txt_path = os.path.join(output_dir, "classification_report.txt")
with open(report_txt_path, "w", encoding="utf-8") as f:
    f.write("📊 VALIDACIÓN DEL PROCESO DE CLASIFICACIÓN 📊\n\n")
    f.write(f"✅ Precisión Global del Modelo: {accuracy_percentage:.2f}%\n\n")
    for class_label, metrics in metrics_per_class.items():
        f.write(f"🔹 Clase '{class_label}':\n")
        f.write(f"   🎯 Precisión: {metrics['Precisión (%)']:.2f}%\n")
        f.write(f"   🔍 Recall: {metrics['Recall (%)']:.2f}%\n")
        f.write(f"   🚀 Especificidad: {metrics['Especificidad (%)']:.2f}%\n")
        f.write(f"   ⚖️ F1-Score: {metrics['F1-Score (%)']:.2f}%\n\n")

# Mensaje final de validación
print("\n\033[92m✅ VALIDACIÓN COMPLETADA: RESULTADOS GUARDADOS\033[0m")
print(f"\033[93m📂 Matriz de Confusión guardada en: {conf_matrix_csv_path}\033[0m")
print(f"\033[93m📂 Imagen de Matriz de Confusión guardada en: {conf_matrix_img_path}\033[0m")
print(f"\033[93m📂 Reporte de Validación guardado en: {report_txt_path}\033[0m")