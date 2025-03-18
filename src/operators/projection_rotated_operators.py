"""
===============================================================================
Proyecto: Inksolver
Archivo: projection_rotated_operators.py
Descripcion: Genera graficas de histogramas de proyeccion de imagenes de operadores matematicos tras rotarlas 45°.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-16
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: OpenCV (cv2), NumPy, Matplotlib, os, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python projection_rotated_operators.py
===============================================================================
Notas:
- El dataset debe estar en '../../data/operators/raw/'.
- Las graficas generadas se guardaran en 'operator_analysis/'.
===============================================================================
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suprimir warnings innecesarios de Matplotlib
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de operadores
dataset_path = "../../data/operators/raw/"
operation_categories = ["div", "equals", "sub", "sum", "times"]

# Definir la carpeta donde se guardaran las graficas
output_dir = "operator_analysis"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

def load_images(category, max_samples=3):
    """
    Carga imagenes de una categoria especifica.

    Args:
        category (str): Nombre de la categoria.
        max_samples (int, opcional): Numero maximo de imagenes a cargar. Por defecto, 3.

    Returns:
        list: Lista de imagenes en escala de grises.
    """
    category_path = os.path.join(dataset_path, category)
    images = []
    if os.path.isdir(category_path):
        image_files = os.listdir(category_path)[:max_samples]
        for img_file in image_files:
            img_path = os.path.join(category_path, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
    return images

def rotate_image_45(img):
    """
    Rota la imagen 45 grados manteniendo el tamano original.

    Args:
        img (numpy.ndarray): Imagen en escala de grises.

    Returns:
        numpy.ndarray: Imagen rotada.
    """
    h, w = img.shape
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]
    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_w, new_h), borderValue=255)
    return rotated_img

def compute_projection_histogram(img, axis=0):
    """
    Calcula el histograma de proyeccion en la direccion especificada y lo normaliza.

    Args:
        img (numpy.ndarray): Imagen en escala de grises.
        axis (int): Direccion del histograma (0=vertical, 1=horizontal).

    Returns:
        numpy.ndarray: Histograma de proyeccion normalizado.
    """
    projection = np.sum(img, axis=axis)
    return projection / np.max(projection)

# Cargar imagenes por categoria
operation_images = {category: load_images(category) for category in operation_categories}

# Procesar cada operador y generar las graficas
for category in operation_categories:
    images = operation_images[category]
    if not images:
        continue

    fig, axes = plt.subplots(len(images), 3, figsize=(12, len(images) * 3))
    fig.suptitle(f"Proyeccion Normalizada (Rotado 45°) - {category}", fontsize=14, fontweight="bold")

    for i, img in enumerate(images):
        rotated_img = rotate_image_45(img)
        hist_horizontal_rot = compute_projection_histogram(rotated_img, axis=1)
        hist_vertical_rot = compute_projection_histogram(rotated_img, axis=0)
        
        axes[i, 0].imshow(rotated_img, cmap='gray')
        axes[i, 0].set_title("Imagen Rotada 45°")
        axes[i, 0].axis("off")
        
        axes[i, 1].plot(hist_horizontal_rot, color="blue")
        axes[i, 1].set_title("Proyeccion Horizontal")
        axes[i, 1].set_xlim([0, len(hist_horizontal_rot)])
        
        axes[i, 2].plot(hist_vertical_rot, color="red")
        axes[i, 2].set_title("Proyeccion Vertical")
        axes[i, 2].set_xlim([0, len(hist_vertical_rot)])

    plt.tight_layout()
    output_path = os.path.join(output_dir, f"projection_rotated_{category}.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    print(f"\033[93m📂 Rotated projection image saved at: {output_path}\033[0m")
