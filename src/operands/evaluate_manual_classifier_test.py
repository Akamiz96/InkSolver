"""
===============================================================================
Proyecto: Inksolver
Archivo: evaluate_manual_classifier_test.py
Descripcion: Evalúa el desempeño del clasificador manual generando la matriz
             de confusión, métricas por clase y precisión global.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-14
Ultima modificacion: 2025-04-14
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, pandas, numpy, matplotlib, sklearn
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python evaluate_manual_classifier_test.py
===============================================================================
Notas:
- Este script analiza el archivo generado por el clasificador manual y calcula:
    - Matriz de confusión
    - Precisión, recall, especificidad y F1-score por clase
    - Precisión global del modelo
- Todos los resultados se guardan en la carpeta 'evaluation_report'
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def evaluar_clasificador(csv_path="test_analysis/clasificacion_resultados_test.csv",
                          output_dir="evaluation_report_test"):
    """
    Evalúa el clasificador calculando matriz de confusión, métricas por clase
    y precisión global. Guarda los resultados como archivos.

    Parámetros:
    - csv_path: ruta del archivo de clasificación (resultados)
    - output_dir: carpeta donde se guardarán las métricas y figuras
    """
    if not os.path.exists(csv_path):
        print(f"\033[91m🚫 No se encontró el archivo de clasificación: {csv_path}\033[0m")
        return

    os.makedirs(output_dir, exist_ok=True)

    print(f"\033[94m📊 Evaluando clasificador usando datos en '{csv_path}'...\033[0m")

    # Leer archivo con clasificaciones
    df = pd.read_csv(csv_path)
    y_true = df["Digito Real"].astype(int)
    y_pred = df["Digito Predicho"].astype(int)
    etiquetas = sorted(y_true.unique())

    # Calcular matriz de confusión
    cm = confusion_matrix(y_true, y_pred, labels=etiquetas)

    # Crear figura del heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(np.arange(len(etiquetas)))
    ax.set_yticks(np.arange(len(etiquetas)))
    ax.set_xticklabels(etiquetas)
    ax.set_yticklabels(etiquetas)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de Confusión")

    # Anotar valores dentro del heatmap
    for i in range(len(etiquetas)):
        for j in range(len(etiquetas)):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() * 0.5 else "black")

    plt.colorbar(im)
    plt.tight_layout()

    # Guardar matriz de confusión
    cm_path = os.path.join(output_dir, "matriz_confusion.png")
    fig.savefig(cm_path)
    plt.close(fig)
    print(f"\033[92m💾 Matriz de confusión guardada en: {cm_path}\033[0m")

    # Calcular métricas por clase
    metricas = []
    total = len(y_true)

    for i, clase in enumerate(etiquetas):
        TP = cm[i, i]  # Verdaderos positivos
        FP = sum(cm[:, i]) - TP  # Falsos positivos
        FN = sum(cm[i, :]) - TP  # Falsos negativos
        TN = total - TP - FP - FN  # Verdaderos negativos

        # Métricas clásicas
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0
        especificidad = TN / (TN + FP) if (TN + FP) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        metricas.append([
            clase,
            round(precision, 4),
            round(recall, 4),
            round(especificidad, 4),
            round(f1, 4)
        ])

    # Crear DataFrame con las métricas por dígito
    df_metricas = pd.DataFrame(metricas, columns=["Dígito", "Precisión", "Recall", "Especificidad", "F1-Score"])

    # Guardar métricas en CSV
    metricas_path = os.path.join(output_dir, "metricas_por_clase.csv")
    df_metricas.to_csv(metricas_path, index=False)
    print(f"\033[92m💾 Métricas por clase guardadas en: {metricas_path}\033[0m")

    # Calcular y guardar precisión global
    accuracy = np.mean(y_true == y_pred)
    resumen_path = os.path.join(output_dir, "resumen.txt")
    with open(resumen_path, "w") as f:
        f.write(f"Precisión global del modelo: {accuracy:.4f}\n")
    print(f"\033[92m💾 Precisión global guardada en: {resumen_path}\033[0m")

    # Mostrar métricas por consola
    print("\n📈 Métricas por clase:")
    print(df_metricas)
    print(f"\n\033[1;32m✅ Precisión global del modelo: {accuracy:.4f}\033[0m")

# Punto de entrada
if __name__ == "__main__":
    evaluar_clasificador()
