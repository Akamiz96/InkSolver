"""
===============================================================================
Proyecto: Inksolver
Archivo: piechart_operators.py
Descripcion: Genera un diagrama de pastel del numero de imagenes por categoria de operadores matematicos.
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
    python piechart_operators.py
===============================================================================
Notas:
- El dataset debe estar en '../../data/operators/raw/'.
- La grafica generada se guarda en 'operator_analysis/operator_piechart.png'.
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
dataset_path = "../../data/operators/raw/"

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
    
    # Generar colores para cada seccion
    colors = [plt.cm.Paired(i) for i in range(len(df_counts))]

    # Configurar "explode" para separar mas las categorias pequenas
    explode = [0.2 if count < 5 else 0 for count in df_counts["Image Count"]]

    # Funcion para ocultar valores menores al 1%
    def autopct_format(pct):
        return f"{pct:.1f}%" if pct >= 1 else ""

    # Crear la figura del diagrama de pastel
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        df_counts["Image Count"], labels=df_counts["Category"], autopct=autopct_format,
        colors=colors, startangle=90, wedgeprops={"edgecolor": "black"}, 
        explode=explode, pctdistance=0.85
    )

    # Ajustar tamanio de los textos
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight("bold")

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color("black")
        autotext.set_fontweight("bold")
        autotext.set_bbox(dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))

    # Titulo del grafico
    plt.title("Percentage of Operator Images", fontsize=14, fontweight="bold")

    # Guardar la imagen
    output_path = os.path.join(output_dir, "operator_piechart.png")
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

    print(f"\033[93m📂 Pie chart saved at: {output_path}\033[0m")
