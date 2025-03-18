"""
===============================================================================
Proyecto: Inksolver
Archivo: validate_test_classification.py
Descripcion: Valida el proceso de clasificacion de operadores matematicos en pruebas utilizando una matriz de confusion.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-17
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: Pandas, NumPy, Matplotlib, Seaborn, os, warnings, scikit-learn
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python validate_test_classification.py
===============================================================================
Notas:
- El dataset de clasificacion de prueba debe estar en 'test_results/classified_test_images.csv'.
- Los resultados de validacion se guardaran en 'test_validation/'.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.metrics import confusion_matrix

# Suprimir warnings innecesarios
warnings.simplefilter("ignore", category=UserWarning)

# Definir rutas de entrada y salida
test_csv_path = "test_results/classified_test_images.csv"  # Archivo de clasificación de prueba
output_folder = "test_validation"  # Carpeta para guardar los resultados
os.makedirs(output_folder, exist_ok=True)

# Definir rutas de salida para los archivos generados
conf_matrix_img_path = os.path.join(output_folder, "confusion_matrix.png")
conf_matrix_csv_path = os.path.join(output_folder, "confusion_matrix.csv")
report_txt_path = os.path.join(output_folder, "classification_report.txt")

# Cargar el archivo CSV con los resultados de la clasificación de prueba
print("\n\033[91m🔴 Cargando datos desde el archivo de clasificación de prueba...\033[0m")
df = pd.read_csv(test_csv_path)

# Extraer etiquetas reales y predichas del dataset
print("\033[91m🔴 Extrayendo etiquetas reales y predichas...\033[0m")
y_true = df["Operador_Real"]  # Etiquetas reales
y_pred = df["Prediccion"]  # Etiquetas predichas

# Obtener clases únicas, asegurando incluir la categoría "Desconocido"
print("\033[91m🔴 Definiendo clases y asegurando la presencia de 'Desconocido'...\033[0m")
classes = sorted(set(y_true) | set(y_pred) | {"Desconocido"})

# Construcción de la matriz de confusión
print("\033[91m🔴 Generando matriz de confusión...\033[0m")
conf_matrix = confusion_matrix(y_true, y_pred, labels=classes)

# Guardar la matriz de confusión en un archivo CSV
print("\033[91m🔴 Guardando la matriz de confusión en CSV...\033[0m")
conf_matrix_df = pd.DataFrame(conf_matrix, index=classes, columns=classes)
conf_matrix_df.to_csv(conf_matrix_csv_path)

# Graficar la matriz de confusión
print("\033[91m🔴 Generando y guardando la imagen de la matriz de confusión...\033[0m")
plt.figure(figsize=(8,6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicción")
plt.ylabel("Etiqueta Real")
plt.title("Matriz de Confusión")
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

# Crear un diccionario para almacenar métricas por clase
metrics_per_class = {}

# Calcular métricas clave: Precisión, Recall, Especificidad y F1-Score
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
with open(report_txt_path, "w", encoding="utf-8") as f:
    f.write("📊 VALIDACIÓN DE CLASIFICACIÓN DE TEST 📊\n\n")
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
