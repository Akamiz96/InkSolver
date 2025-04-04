"""
===============================================================================
Proyecto: Inksolver
Archivo: analyze_operands.py
Descripcion: Analiza las imágenes de operandos escritas a mano y genera
             un histograma y un gráfico de pastel con la cantidad por dígito.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-03
Ultima modificacion: 2025-04-03
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, matplotlib, seaborn, warnings, numpy
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python analyze_operands.py
===============================================================================
Notas:
- Este script analiza las imágenes del dataset de operandos almacenadas en
  subcarpetas numeradas del 0 al 9, correspondientes a cada dígito.
- Genera dos gráficas en la carpeta de salida:
    1. Histograma de cantidad de imágenes por dígito
    2. Gráfico de pastel con el porcentaje de imágenes por dígito
===============================================================================
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np

# Suprimir advertencias innecesarias de la librería matplotlib
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta de entrada (dataset de operandos) y de salida para los gráficos
input_folder = "../../data/operands/raw/dataset/"
output_folder = "operand_analysis"
os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe

# Definir rutas donde se guardarán las imágenes generadas
histogram_path = os.path.join(output_folder, "operand_histogram.png")
piechart_path = os.path.join(output_folder, "operand_piechart.png")

# 🔹 Contar imágenes por dígito en la carpeta del dataset
print("\n\033[91m🔴 Contando imágenes en la carpeta de operandos...\033[0m")
image_counts = {}

for digit in range(10):  # Para cada dígito del 0 al 9
    digit_folder = os.path.join(input_folder, str(digit))  # Ruta a cada subcarpeta
    if os.path.isdir(digit_folder):
        num_images = len(os.listdir(digit_folder))  # Cantidad de archivos en la carpeta
        image_counts[str(digit)] = num_images       # Guardar el conteo en el diccionario

# Si no se encontró ninguna imagen, se termina el script
if not image_counts:
    print("\033[91m⚠️ No se encontraron imágenes de operandos en la carpeta de dataset.\033[0m")
    exit()

# Ordenar las categorías para visualización
categories, counts = zip(*sorted(image_counts.items(), key=lambda x: int(x[0])))

# Definir una paleta de colores personalizada (10 colores distintos para 10 dígitos)
custom_colors = sns.color_palette("tab10", 10)

# 🔹 Generar Histograma
print("\033[91m🔴 Generando histograma de imágenes extraídas...\033[0m")
plt.figure(figsize=(10,6))

# Crear las barras del histograma
bars = plt.bar(categories, counts, color=custom_colors, edgecolor="black", linewidth=2)

# Añadir etiquetas numéricas encima de cada barra
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
             f"{count:,}", ha='center', va='bottom', fontsize=12, fontweight='bold')

# Personalización de los ejes y título
plt.xlabel("Digit Categories", fontsize=14, fontweight='bold')
plt.ylabel("Number of Images", fontsize=14, fontweight='bold')
plt.title("Histogram of Operand Image Counts", fontsize=16, fontweight='bold')
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.ylim(0, max(counts) * 1.1)  # Extensión vertical del gráfico
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Guardar el histograma en un archivo
plt.savefig(histogram_path, dpi=300, bbox_inches="tight")
try:
    plt.show(block=False)
except:
    pass

# 🔹 Generar gráfico de pastel (pie chart)
print("\033[91m🔴 Generando gráfico de pastel de distribución...\033[0m")

# Separar visualmente las categorías con menos de 5 imágenes
explode = [0.1 if count < 5 else 0 for count in counts]

# Mostrar etiquetas solo si representan ≥1% del total
def autopct_format(pct):
    return f"{pct:.1f}%" if pct >= 1 else ""

# Crear la figura del gráfico de pastel
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    counts, labels=categories, autopct=autopct_format,
    colors=custom_colors, startangle=90, wedgeprops={"edgecolor": "black"}, 
    explode=explode, pctdistance=0.85
)

# Personalización del texto de etiquetas
for text in texts:
    text.set_fontsize(12)
    text.set_fontweight("bold")

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_color("black")
    autotext.set_fontweight("bold")
    autotext.set_bbox(dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

# Título del gráfico
plt.title("Percentage of Operand Images", fontsize=14, fontweight="bold")

# Guardar el gráfico de pastel
plt.savefig(piechart_path, dpi=300, bbox_inches="tight")
try:
    plt.show(block=False)
except:
    pass

# 🔹 Mensajes finales al usuario
print("\n\033[92m✅ ANÁLISIS COMPLETADO: GRÁFICOS GENERADOS.\033[0m")
print(f"\033[93m📂 Histograma guardado en: {histogram_path}\033[0m")
print(f"\033[93m📂 Gráfico de pastel guardado en: {piechart_path}\033[0m")
