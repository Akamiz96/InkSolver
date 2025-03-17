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

print("\n\033[91m🔴 Cargando datos desde el archivo CSV...\033[0m")
df = pd.read_csv(csv_path)

print("\033[91m🔴 Extrayendo etiquetas reales y predichas...\033[0m")
y_true = df["Categoria"]
y_pred = df["Prediccion"]

print("\033[91m🔴 Definiendo clases y asegurando la presencia de 'Desconocido'...\033[0m")
classes = sorted(set(y_true.unique()) | set(y_pred.unique()) | {"Desconocido"})

print("\033[91m🔴 Construyendo la matriz de confusión...\033[0m")
conf_matrix = confusion_matrix(y_true, y_pred, labels=classes)

print("\033[91m🔴 Guardando la matriz de confusión en CSV...\033[0m")
conf_matrix_df = pd.DataFrame(conf_matrix, index=classes, columns=classes)
conf_matrix_csv_path = os.path.join(output_dir, "confusion_matrix.csv")
conf_matrix_df.to_csv(conf_matrix_csv_path)

print("\033[91m🔴 Generando y guardando la imagen de la matriz de confusión...\033[0m")
plt.figure(figsize=(8,6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicción")
plt.ylabel("Etiqueta Real")
plt.title("Matriz de Confusión")

conf_matrix_img_path = os.path.join(output_dir, "confusion_matrix.png")
plt.savefig(conf_matrix_img_path, dpi=300, bbox_inches="tight")

try:
    plt.show(block=False)
except:
    pass

print("\033[91m🔴 Calculando precisión global del modelo...\033[0m")
total_correct_predictions = np.sum(np.diag(conf_matrix))
total_predictions = np.sum(conf_matrix)
accuracy_percentage = (total_correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0.0

metrics_per_class = {}

print("\033[91m🔴 Calculando métricas por clase...\033[0m")
for i, class_label in enumerate(classes):
    TP = conf_matrix[i, i]
    FN = np.sum(conf_matrix[i, :]) - TP
    FP = np.sum(conf_matrix[:, i]) - TP
    TN = total_predictions - (TP + FN + FP)

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

print("\033[91m🔴 Generando reporte de validación...\033[0m")
report_text_file = f"""
📊 VALIDACIÓN DEL PROCESO DE CLASIFICACIÓN 📊

✅ 1. Precisión Global del Modelo:
   📌 El modelo logró una precisión global del {accuracy_percentage:.2f}%.
   📌 Representa el porcentaje de predicciones correctas sobre el total de clasificaciones.

📊 2. Precisión por Clase:
"""

for class_label, metrics in metrics_per_class.items():
    report_text_file += f"""
   🔹 Clase '{class_label}':
      - 🎯 Precisión: {metrics["Precisión (%)"]:.2f}%
      - 🔍 Recall: {metrics["Recall (%)"]:.2f}%
      - 🚀 Especificidad: {metrics["Especificidad (%)"]:.2f}%
      - ⚖️ F1-Score: {metrics["F1-Score (%)"]:.2f}%
"""

report_txt_path = os.path.join(output_dir, "classification_report.txt")
with open(report_txt_path, "w", encoding="utf-8") as f:
    f.write(report_text_file)

report_text_terminal = f"""
\033[94m📊 VALIDACIÓN DEL PROCESO DE CLASIFICACIÓN 📊\033[0m

\033[92m✅ 1. Precisión Global del Modelo:\033[0m
   📌 El modelo logró una precisión global del \033[93m{accuracy_percentage:.2f}%\033[0m.
   📌 Representa el porcentaje de predicciones correctas sobre el total de clasificaciones.

\033[94m📊 2. Precisión por Clase:\033[0m
"""

for class_label, metrics in metrics_per_class.items():
    report_text_terminal += f"""
   🔹 \033[96mClase '{class_label}':\033[0m
      - 🎯 Precisión: \033[93m{metrics["Precisión (%)"]:.2f}%\033[0m
      - 🔍 Recall: \033[93m{metrics["Recall (%)"]:.2f}%\033[0m
      - 🚀 Especificidad: \033[93m{metrics["Especificidad (%)"]:.2f}%\033[0m
      - ⚖️ F1-Score: \033[93m{metrics["F1-Score (%)"]:.2f}%\033[0m
"""

print(report_text_terminal)

print("\n\033[92m" + "=" * 50)
print("✅ VALIDACIÓN COMPLETADA: RESULTADOS GUARDADOS")
print("=" * 50 + "\033[0m")
print(f"\033[93m📂 Matriz de Confusión guardada en: {conf_matrix_csv_path}\033[0m")
print(f"\033[93m📂 Imagen de Matriz de Confusión guardada en: {conf_matrix_img_path}\033[0m")
print(f"\033[93m📂 Reporte de Validación guardado en: {report_txt_path}\033[0m")
