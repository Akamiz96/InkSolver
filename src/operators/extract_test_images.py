import cv2
import numpy as np
import os
import re

# Definir rutas de entrada y salida
input_folder = "../../data/operators/raw/test/"
output_base_folder = "../../data/operators/processed/test/"

# Crear la carpeta de salida si no existe
os.makedirs(output_base_folder, exist_ok=True)

def extract_black_boxes_from_image(image_path, operator, image_id):
    """Extrae cuadros negros de una imagen y los guarda en la carpeta correspondiente."""
    
    # Definir carpeta de salida para el operador
    output_folder = os.path.join(output_base_folder, operator)
    os.makedirs(output_folder, exist_ok=True)

    print(f"\n\033[91m🔴 Procesando imagen: {image_path}...\033[0m")

    # Cargar la imagen
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral para detectar cuadros negros
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos de los cuadros
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar y ordenar los cuadros detectados
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))  # Ordenar por fila y columna

    # Identificar filas y columnas
    row_dict = {}
    for x, y, w, h in bounding_boxes:
        if 50 < w < 200 and 50 < h < 200:  # Filtrar ruido
            row = y // 80  
            col = x // 80
            if row not in row_dict:
                row_dict[row] = []
            row_dict[row].append((x, y, w, h))

    image_count = 0
    for row in sorted(row_dict.keys()):
        for col_index, (x, y, w, h) in enumerate(sorted(row_dict[row], key=lambda b: b[0])):
            # Extraer la región del cuadro
            border_margin = 10  
            cropped = gray[y+border_margin:y+h-border_margin, x+border_margin:x+w-border_margin]

            # Convertir a blanco y negro
            _, bw_cropped = cv2.threshold(cropped, 145, 255, cv2.THRESH_BINARY)

            # Guardar imagen con formato [id imagen]_[id consecutivo].png
            output_filename = f"{image_id}_{image_count}.png"
            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, bw_cropped)

            image_count += 1

    # Mensaje final por imagen
    print(f"\033[92m✔ Se extrajeron {image_count} cuadros de la imagen {image_path}.\033[0m")
    print(f"\033[93m📂 Imágenes guardadas en: {output_folder}\033[0m")

# Procesar todas las imágenes en la carpeta de prueba
for filename in os.listdir(input_folder):
    match = re.match(r"([a-zA-Z]+)_(\d+)\.png", filename)
    if match:
        operator, image_id = match.groups()
        image_path = os.path.join(input_folder, filename)
        extract_black_boxes_from_image(image_path, operator, image_id)

print("\n\033[92m✅ PROCESO COMPLETO: TODAS LAS IMÁGENES FUERON EXTRAÍDAS Y GUARDADAS.\033[0m")
