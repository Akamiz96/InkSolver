import cv2
import numpy as np
import os
import re

# Rutas base
input_folder = "../../data/equations/raw/"
output_base_folder = "../../data/equations/processed/"

os.makedirs(output_base_folder, exist_ok=True)

def extract_equations_from_image(image_path, resultado, image_id):
    """
    Extrae cuadros de una imagen que contiene dos ecuaciones por fila y los guarda
    como eq_0, eq_1, ..., eq_n en orden consecutivo.

    Args:
        image_path (str): Ruta de la imagen a procesar.
        resultado (str): Resultado correcto de las ecuaciones (0 a 9).
        image_id (str): Identificador único de la imagen.
    """
    print(f"\n🔴 Procesando imagen: {image_path}...")

    # Cargar y preprocesar imagen
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Detección de contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))  # por fila y columna

    # Agrupar cuadros por fila
    row_dict = {}
    for x, y, w, h in bounding_boxes:
        if 50 < w < 200 and 50 < h < 200:
            row = y // 80
            if row not in row_dict:
                row_dict[row] = []
            row_dict[row].append((x, y, w, h))

    eq_counter = 0  # contador global por imagen
    for row in sorted(row_dict.keys()):
        boxes = sorted(row_dict[row], key=lambda b: b[0])
        if len(boxes) != 10:
            print(f"⚠️ Advertencia: se esperaban 10 cuadros en la fila {row}, pero se detectaron {len(boxes)}")
            continue

        for eq_num in range(2):  # dos ecuaciones por fila
            eq_folder = os.path.join(output_base_folder, resultado, image_id, f"eq_{eq_counter}")
            os.makedirs(eq_folder, exist_ok=True)

            start = eq_num * 6  # ecuación 1: 0–3, ecuación 2: 6–9
            for i in range(4):  # solo 4 cuadros por ecuación
                x, y, w, h = boxes[start + i]
                border = 10
                cropped = gray[y+border:y+h-border, x+border:x+w-border]
                _, bw_cropped = cv2.threshold(cropped, 145, 255, cv2.THRESH_BINARY)
                output_filename = f"{i}.png"
                cv2.imwrite(os.path.join(eq_folder, output_filename), bw_cropped)

            eq_counter += 1  # avanzar al siguiente número de ecuación

    print(f"✅ Imagen procesada y ecuaciones extraídas: {image_id} ({eq_counter} ecuaciones)")

# Procesar todas las carpetas (0 a 9) dentro de raw
for resultado in os.listdir(input_folder):
    resultado_path = os.path.join(input_folder, resultado)
    if not os.path.isdir(resultado_path):
        continue

    for filename in os.listdir(resultado_path):
        match = re.match(rf"{resultado}_(\d+)\.png", filename)
        if match:
            image_id = match.group(1)
            image_path = os.path.join(resultado_path, filename)
            extract_equations_from_image(image_path, resultado, image_id)

print("\n✅ PROCESO COMPLETO: TODAS LAS ECUACIONES FUERON EXTRAÍDAS Y ORGANIZADAS.")
