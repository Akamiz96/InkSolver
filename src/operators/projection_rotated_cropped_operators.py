"""
===============================================================================
Proyecto: Inksolver
Archivo: projection_rotated_cropped_operators.py
Descripcion: Genera graficas de histogramas de proyeccion de imagenes de operadores matematicos tras rotarlas y recortarlas.
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
    python projection_rotated_cropped_operators.py
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
dataset_path = "../../data/operators/raw/dataset/"
operation_categories = ["div", "equals", "sub", "sum", "times"]

# Definir la carpeta donde se guardaran las graficas
output_dir = "operator_analysis"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

def load_single_image(category):
    """
    Carga una unica imagen de una categoria especifica.

    Args:
        category (str): Nombre de la categoria.

    Returns:
        numpy.ndarray o None: Imagen en escala de grises si existe, None si no hay imagenes.
    """
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        image_files = os.listdir(category_path)
        if image_files:
            img_path = os.path.join(category_path, image_files[0])
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            return img
    return None

def rotate_image_45(img):
    """
    Rota la imagen 45 grados y recorta los bordes blancos innecesarios.

    Args:
        img (numpy.ndarray): Imagen en escala de grises.

    Returns:
        numpy.ndarray: Imagen rotada y recortada.
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
    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_w, new_h), borderValue=255, flags=cv2.INTER_NEAREST)
    _, thresh = cv2.threshold(rotated_img, 250, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)
    return rotated_img[y:y+h, x:x+w]

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

# Crear una figura grande para mostrar todas las imagenes en una sola
fig, axes = plt.subplots(len(operation_categories), 4, figsize=(16, len(operation_categories) * 3))
fig.suptitle("Analisis de Proyeccion - Imagen Original y Rotada 45°", fontsize=16, fontweight="bold")

# Procesar cada operador
for i, category in enumerate(operation_categories):
    img = load_single_image(category)
    if img is None:
        continue

    hist_horizontal_orig = compute_projection_histogram(img, axis=1)
    hist_vertical_orig = compute_projection_histogram(img, axis=0)
    rotated_img = rotate_image_45(img)
    hist_horizontal_rot = compute_projection_histogram(rotated_img, axis=1)
    hist_vertical_rot = compute_projection_histogram(rotated_img, axis=0)
    
    axes[i, 0].imshow(img, cmap='gray')
    axes[i, 0].set_title(f"{category.upper()} - Imagen Original")
    axes[i, 0].axis("off")
    
    axes[i, 1].plot(hist_horizontal_orig, color="blue", label="Horizontal")
    axes[i, 1].plot(hist_vertical_orig, color="red", label="Vertical")
    axes[i, 1].set_title("Proyeccion Original")
    axes[i, 1].legend()
    
    axes[i, 2].imshow(rotated_img, cmap='gray')
    axes[i, 2].set_title("Imagen Rotada 45°")
    axes[i, 2].axis("off")
    
    axes[i, 3].plot(hist_horizontal_rot, color="blue", label="Horizontal")
    axes[i, 3].plot(hist_vertical_rot, color="red", label="Vertical")
    axes[i, 3].set_title("Proyeccion Rotada")
    axes[i, 3].legend()

plt.tight_layout()
output_path = os.path.join(output_dir, "projection_rotated_cropped.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"\033[93m📂 Projection image saved at: {output_path}\033[0m")