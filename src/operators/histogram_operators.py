"""
===============================================================================
Proyecto: Inksolver
Archivo: histogram_operators.py
Descripcion: Genera un histograma de conteo de imagenes de operadores matematicos.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-15
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: Matplotlib, Pandas, os, warnings, collections
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python histogram_operators.py
===============================================================================
Notas:
- El dataset debe estar en '../../data/operators/raw/'.
- El histograma generado se guarda en 'operator_analysis/operator_histogram.png'.
===============================================================================
"""

import os
import matplotlib.pyplot as plt
import warnings
import pandas as pd
from collections import defaultdict

# Suprimir warnings de Matplotlib
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de operadores
dataset_path = "../../data/operators/raw/dataset/"

# Definir la carpeta donde se guardaran las graficas
output_dir = "operator_analysis"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

# Obtener las categorias de operadores
categories = sorted(os.listdir(dataset_path))

# Contar el numero de imagenes por categoria
image_counts = defaultdict(int)

for category in categories:
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        image_counts[category] = len(os.listdir(category_path))

# Verificar si hay datos para graficar
if not image_counts:
    print("\033[91m❌ No image data found in the dataset path.\033[0m")
else:
    # Crear DataFrame con los conteos
    df_counts = pd.DataFrame(list(image_counts.items()), columns=["Category", "Image Count"])
    
    # Generar colores aleatorios para cada barra
    colors = [plt.cm.Paired(i) for i in range(len(df_counts))]

    # Crear la figura del histograma
    plt.figure(figsize=(8, 5))
    bars = plt.bar(df_counts["Category"], df_counts["Image Count"], color=colors, edgecolor="black")

    # Etiquetas y titulo
    plt.xlabel("Operator Categories", fontsize=12)
    plt.ylabel("Number of Images", fontsize=12)
    plt.title("Histogram of Operator Image Counts", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Agregar los valores encima de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(int(height)), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

    # Guardar el histograma
    output_path = os.path.join(output_dir, "operator_histogram.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    # Intentar mostrar la imagen sin warnings
    try:
        plt.show(block=False)
    except:
        pass  # Si hay un error, continuar sin mostrar warning

    # Verificar si la figura realmente se mostro
    if not plt.get_fignums():
        print("\n\033[91m" + "=" * 50)
        print("⚠️  WARNING: Interactive display is not available ⚠️")
        print("=" * 50 + "\033[0m\n")

    print(f"\033[93m📂 Histogram saved at: {output_path}\033[0m")
