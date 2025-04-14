"""
===============================================================================
Proyecto: InkSolver
Archivo: extract_test_operands.py
Descripción: Extrae cuadros negros de imágenes de prueba que contienen dígitos 
             escritos a mano y guarda las imágenes individuales en carpetas organizadas.
Autor: Alejandro Castro Martínez
Fecha de creación: 2025-04-14
Última modificación: 2025-04-14
Versión: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: OpenCV (cv2), NumPy, os, re
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python extract_test_operands.py
===============================================================================
Notas:
- Las imágenes de entrada deben estar en la carpeta '../../data/operands/raw/test/'.
- Las imágenes extraídas se guardarán en '../../data/operands/processed/test/' organizadas por nombre de archivo.
===============================================================================
"""

import cv2
import numpy as np
import os
import re

# Definir rutas de entrada y salida
input_folder = "../../data/operands/raw/test/"
output_base_folder = "../../data/operands/processed/test/"

# Crear la carpeta de salida si no existe
os.makedirs(output_base_folder, exist_ok=True)

def extract_black_boxes_from_image(image_path, image_label, image_id):
    """
    Extrae cuadros negros de una imagen de prueba que contiene múltiples dígitos escritos
    y guarda cada uno como imagen individual en la carpeta correspondiente.

    Args:
        image_path (str): Ruta de la imagen a procesar.
        image_label (str): Etiqueta o nombre base de la imagen.
        image_id (str): Identificador único de la imagen de entrada.
    
    Returns:
        None
    """
    # Definir carpeta de salida
    output_folder = os.path.join(output_base_folder, image_label)
    os.makedirs(output_folder, exist_ok=True)

    print(f"\n\033[91m🔴 Procesando imagen: {image_path}...\033[0m")

    # Cargar imagen en escala de grises
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral para aislar dígitos en negro
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extraer y ordenar cuadros
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))

    # Agrupar por filas y columnas
    row_dict = {}
    for x, y, w, h in bounding_boxes:
        if 50 < w < 200 and 50 < h < 200: # Filtrar ruido
            row = y // 80 # Agrupar por filas
            col = x // 80 # Agrupar por columnas
            row_dict.setdefault(row, []).append((x, y, w, h))

    # Extraer cuadros y guardar imágenes
    image_count = 0 # Contador de imagenes extraidas
    for row in sorted(row_dict.keys()):
        for col_index, (x, y, w, h) in enumerate(sorted(row_dict[row], key=lambda b: b[0])):
            # Extraer la region del cuadro con margen para evitar bordes
            border_margin = 10
            cropped = gray[y+border_margin:y+h-border_margin, x+border_margin:x+w-border_margin]

            # Convertir a imagen binaria
            _, bw_cropped = cv2.threshold(cropped, 145, 255, cv2.THRESH_BINARY)

            # Guardar imagen con formato [id imagen]_[id consecutivo].png
            output_filename = f"{image_id}_{image_count}.png"
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, bw_cropped)
            image_count += 1

    # Mensajes finales
    print(f"\033[92m✔ Se extrajeron {image_count} cuadros de la imagen {image_path}.\033[0m")
    print(f"\033[93m📂 Imágenes guardadas en: {output_folder}\033[0m")

# Procesar todas las imágenes en la carpeta de entrada
for filename in os.listdir(input_folder):
    match = re.match(r"(\d+)_(\d+)\.png", filename)
    if match:
        digit_class, image_id = match.groups()
        image_path = os.path.join(input_folder, filename)
        extract_black_boxes_from_image(image_path, digit_class, image_id)

print("\n\033[92m✅ PROCESO COMPLETO: TODAS LAS IMÁGENES FUERON EXTRAÍDAS Y GUARDADAS.\033[0m")
