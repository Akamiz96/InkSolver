"""
===============================================================================
Proyecto: Inksolver
Archivo: visualize_operators.py
Descripcion: Muestra muestras de imagenes de operadores matematicos y las guarda como una imagen de referencia.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-15
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: OpenCV (cv2), Matplotlib, os, warnings, collections
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python visualize_operators.py
===============================================================================
Notas:
- El dataset debe estar en '../../data/operators/raw/'.
- La imagen generada se guarda en 'operator_analysis/operator_samples.png'.
===============================================================================
"""

import os
import cv2
import matplotlib.pyplot as plt
import warnings
from collections import defaultdict

# Suprimir todos los warnings de matplotlib
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de operadores
dataset_path = "../../data/operators/raw/dataset/"

# Definir la carpeta donde se guardarán las gráficas
output_dir = "operator_analysis"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

# Obtener las categorías de operadores (div, equals, sub, sum, times)
categories = sorted(os.listdir(dataset_path))

# Almacenar muestras limitadas por categoría
image_samples = defaultdict(list)

for category in categories:
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        images = os.listdir(category_path)

        # Tomar hasta 5 muestras por categoría para evitar demoras
        for img in images[:5]:
            img_path = os.path.join(category_path, img)
            image_samples[category].append(img_path)

# Verificar que haya imágenes para mostrar
if not image_samples:
    print("❌ No images found in the dataset path.")
else:
    # Crear la figura con un número dinámico de filas
    fig, axes = plt.subplots(len(image_samples), 5, figsize=(10, len(image_samples) * 2))
    fig.suptitle("Sample Images of Mathematical Operators", fontsize=14, y=1.0)

    for i, (category, images) in enumerate(image_samples.items()):
        for j in range(5):
            ax = axes[i, j] if len(image_samples) > 1 else axes[j]
            ax.axis("off")
            if j < len(images):
                img = cv2.imread(images[j], cv2.IMREAD_GRAYSCALE)
                ax.imshow(img, cmap='gray')

    plt.tight_layout()

    # Guardar la imagen en la carpeta 'operator_analysis'
    output_path = os.path.join(output_dir, "operator_samples.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    # Intentar mostrar la imagen sin warnings
    try:
        plt.show(block=False)
    except:
        pass  # Si hay un error, continuar sin mostrar warning

    # Verificar si la figura realmente se mostró
    if not plt.get_fignums():  
        print("\n\033[91m" + "=" * 50)
        print("⚠️  WARNING: Interactive display is not available ⚠️")
        print("=" * 50 + "\033[0m\n")

    print(f"\033[93m📂 Image saved at: {output_path}\033[0m")
