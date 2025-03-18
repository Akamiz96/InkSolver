"""
===============================================================================
Proyecto: Inksolver
Archivo: analyze_test_images.py
Descripcion: Analiza las imagenes de prueba en la carpeta 'test' y genera un histograma de conteo por categoria.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-17
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: os, matplotlib, seaborn, warnings, numpy
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python analyze_test_images.py
===============================================================================
Notas:
- El script cuenta la cantidad de imagenes en la carpeta de prueba y genera un histograma.
- Las imagenes deben estar organizadas en subcarpetas por categoria dentro de 'test/'.
===============================================================================
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np

# Suprimir warnings innecesarios
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset y la carpeta de salida
input_folder = "../../data/operators/processed/test/"
output_folder = "test_analysis"
os.makedirs(output_folder, exist_ok=True)

# Definir la ruta del archivo de salida
histogram_path = os.path.join(output_folder, "test_image_histogram.png")

# Obtener la cantidad de imagenes por categoria
print("\n\033[91m🔴 Contando imagenes en la carpeta de test...\033[0m")
image_counts = {}

for category in os.listdir(input_folder):
    category_path = os.path.join(input_folder, category)
    if os.path.isdir(category_path):
        num_images = len(os.listdir(category_path))
        image_counts[category] = num_images

# Verificar si hay datos
if not image_counts:
    print("\033[91m❌ No se encontraron imagenes en la carpeta de test.\033[0m")
    exit()

# Ordenar los datos por categoria
categories, counts = zip(*sorted(image_counts.items(), key=lambda x: x[0]))

# Definir colores especificos para cada barra
custom_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]  # Colores para el histograma

# 🔹 **Generar Histograma con Formato Ajustado**
print("\033[91m🔴 Generando histograma de imagenes extraidas...\033[0m")
def generate_histogram(categories, counts, save_path):
    """
    Genera un histograma de la cantidad de imagenes por categoria y lo guarda en un archivo.

    Args:
        categories (list): Lista con los nombres de las categorias.
        counts (list): Lista con la cantidad de imagenes por categoria.
        save_path (str): Ruta donde se guardara el histograma.
    """
    plt.figure(figsize=(8,5))
    bars = plt.bar(categories, counts, color=custom_colors, edgecolor="black")
    
    # Añadir los numeros sobre las barras
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(int(height)), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')
    
    # Etiquetas y titulo
    plt.xlabel("Operator Categories", fontsize=12)
    plt.ylabel("Number of Images", fontsize=12)
    plt.title("Histogram of Operator Image Counts", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Ajustar limites y grid
    plt.ylim(0, max(counts) * 1.1)  # Un poco mas arriba del maximo
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Guardar la imagen
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    try:
        plt.show(block=False)
    except:
        pass
    
    # Verificar si la figura realmente se mostro
    if not plt.get_fignums():
        print("\n\033[91m" + "=" * 50)
        print("⚠️  WARNING: Interactive display is not available ⚠️")
        print("=" * 50 + "\033[0m\n")

# Llamar a la funcion para generar el histograma
generate_histogram(categories, counts, histogram_path)

# 🔹 **Mensaje Final**
print("\n\033[92m✅ ANALISIS COMPLETADO: HISTOGRAMA GENERADO.\033[0m")
print(f"\033[93m📂 Histograma guardado en: {histogram_path}\033[0m")