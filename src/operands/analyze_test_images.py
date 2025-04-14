"""
===============================================================================
Proyecto: Inksolver
Archivo: analyze_test_images.py
Descripcion: Analiza las imagenes de prueba en la carpeta 'test' y genera un histograma de conteo por categoria.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-14
Ultima modificacion: 2025-04-14
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
input_folder = "../../data/operands/processed/test/"
output_folder = "test_analysis"
os.makedirs(output_folder, exist_ok=True)

# Definir las rutas de los archivos de salida
histogram_path = os.path.join(output_folder, "test_image_histogram.png")
piechart_path = os.path.join(output_folder, "test_image_piechart.png")

# Obtener la cantidad de imágenes por categoría
print("\n\033[91m🔴 Contando imágenes en la carpeta de test...\033[0m")
image_counts = {}

for category in os.listdir(input_folder):
    category_path = os.path.join(input_folder, category)
    if os.path.isdir(category_path):
        num_images = len(os.listdir(category_path))
        image_counts[category] = num_images

# Verificar si hay datos
if not image_counts:
    print("\033[91m⚠️ No se encontraron imágenes en la carpeta de test.\033[0m")
    exit()

# Ordenar los datos por categoría
categories, counts = zip(*sorted(image_counts.items(), key=lambda x: x[0]))

# Definir colores específicos para cada barra (mismo orden para ambos gráficos)
custom_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

# 🔹 **Generar Histograma**
print("\033[91m🔴 Generando histograma de imágenes extraídas...\033[0m")
plt.figure(figsize=(10,6))

bars = plt.bar(categories, counts, color=custom_colors, edgecolor="black", linewidth=2)

# Añadir los números sobre las barras en negrita
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f"{count:,}", ha='center', va='bottom', fontsize=12, fontweight='bold')

# Personalizar el estilo del gráfico
plt.xlabel("Operand Categories", fontsize=14, fontweight='bold')
plt.ylabel("Number of Images", fontsize=14, fontweight='bold')
plt.title("Histogram of Operand Image Counts", fontsize=16, fontweight='bold')
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')

# Ajustar límites y grid
plt.ylim(0, max(counts) * 1.1)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Guardar la imagen del histograma
plt.savefig(histogram_path, dpi=300, bbox_inches="tight")
try:
    plt.show(block=False)
except:
    pass

# 🔹 **Generar Pie Chart**
print("\033[91m🔴 Generando gráfico de pastel de distribución...\033[0m")

# Configurar "explode" para separar más las categorías pequeñas
explode = [0.2 if count < 5 else 0 for count in counts]

# Función para ocultar valores menores al 1%
def autopct_format(pct):
    return f"{pct:.1f}%" if pct >= 1 else ""

# Crear la figura del diagrama de pastel
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    counts, labels=categories, autopct=autopct_format,
    colors=custom_colors, startangle=90, wedgeprops={"edgecolor": "black"}, 
    explode=explode, pctdistance=0.85
)

# Ajustar tamaño de los textos
for text in texts:
    text.set_fontsize(12)
    text.set_fontweight("bold")

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_color("black")
    autotext.set_fontweight("bold")
    autotext.set_bbox(dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

# Título del gráfico
plt.title("Percentage of Operator Images", fontsize=14, fontweight="bold")

# Guardar la imagen del pie chart
plt.savefig(piechart_path, dpi=300, bbox_inches="tight")
try:
    plt.show(block=False)
except:
    pass

# 🔹 **Mensajes Finales**
print("\n\033[92m✅ ANÁLISIS COMPLETADO: GRÁFICOS GENERADOS.\033[0m")
print(f"\033[93m📂 Histograma guardado en: {histogram_path}\033[0m")
print(f"\033[93m📂 Gráfico de pastel guardado en: {piechart_path}\033[0m")
