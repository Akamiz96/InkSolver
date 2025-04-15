"""
===============================================================================
Proyecto: Inksolver
Archivo: generate_test_ink_density_csv.py
Descripcion: Genera archivos CSV individuales por dígito con los porcentajes de
             tinta (píxeles negros) por cuadrante (3x3) para cada imagen de test.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-14
Ultima modificacion: 2025-04-14
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, cv2, numpy, pandas, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python generate_test_ink_density_csv.py
===============================================================================
Notas:
- Las imágenes deben estar organizadas en carpetas por dígito (0 a 9).
- Cada CSV contiene una fila por imagen, con los porcentajes de tinta en
  los 9 cuadrantes ordenados de izquierda a derecha, de arriba hacia abajo.
- Los CSV generados se almacenan en la carpeta 'csv_por_digito'.
===============================================================================
"""

import os
import cv2
import numpy as np
import pandas as pd
import warnings

# Suprimir advertencias innecesarias (por ejemplo de matplotlib)
warnings.simplefilter("ignore", category=UserWarning)

def compute_tinta_por_cuadrante(image, grid_size=(3, 3)):
    """
    Calcula el porcentaje de píxeles negros (tinta) en cada uno de los 9 cuadrantes de la imagen.

    Parámetros:
    - image: imagen en escala de grises (numpy array)
    - grid_size: tamaño de la cuadrícula (por defecto 3x3)

    Retorna:
    - Lista con 9 valores (ordenados de izquierda a derecha, de arriba hacia abajo)
    """
    h, w = image.shape
    gh, gw = grid_size
    step_h, step_w = h // gh, w // gw

    # Invertir imagen: fondo blanco, tinta negra (valor 255)
    _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)

    porcentajes = []
    for i in range(gh):  # Fila
        for j in range(gw):  # Columna
            block = binary[i*step_h:(i+1)*step_h, j*step_w:(j+1)*step_w]
            total = block.size
            tinta = np.sum(block > 0)
            porcentaje = tinta / total
            porcentajes.append(round(porcentaje, 4))  # Redondear a 4 decimales
    return porcentajes

def generar_csv_por_digito(base_path="../../data/operands/processed/test", output_path="csv_por_digito_test", grid_size=(3,3), block_size=100):
    """
    Recorre todas las carpetas de dígitos y genera un CSV por cada una,
    donde se almacena el porcentaje de tinta por cuadrante por imagen.

    Parámetros:
    - base_path: ruta base con carpetas por dígito
    - output_path: carpeta de salida para los CSV
    - grid_size: tamaño de la grilla (por defecto 3x3)
    - block_size: cada cuántas imágenes imprimir avance
    """
    os.makedirs(output_path, exist_ok=True)

    for digit in range(10):
        digit_path = os.path.join(base_path, str(digit))
        if not os.path.exists(digit_path):
            print(f"\033[91m🚫 Carpeta no encontrada para dígito {digit}\033[0m")
            continue

        image_files = sorted(os.listdir(digit_path))
        total_images = len(image_files)

        print(f"\n\033[94m📁 Procesando {total_images} imágenes del dígito {digit}...\033[0m")

        rows = []
        for idx, img_name in enumerate(image_files):
            img_path = os.path.join(digit_path, img_name)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue

            # Calcular porcentajes y armar fila
            porcentajes = compute_tinta_por_cuadrante(image, grid_size)
            row = [digit, img_name] + porcentajes
            rows.append(row)

            # Imprimir cada cierto bloque de imágenes
            if (idx + 1) % block_size == 0 or (idx + 1) == total_images:
                print(f"\033[92m✔ {idx + 1}/{total_images} imágenes procesadas...\033[0m")

        # Guardar CSV si hay datos
        if rows:
            columns = ["Digito", "Nombre Imagen"] + [f"P. Cuadrante {i}" for i in range(1, 10)]
            df = pd.DataFrame(rows, columns=columns)
            csv_path = os.path.join(output_path, f"digito_{digit}.csv")
            df.to_csv(csv_path, index=False)
            print(f"\033[92m💾 CSV guardado en: {csv_path}\033[0m")
        else:
            print(f"\033[93m⚠️ No se procesaron imágenes para el dígito {digit}\033[0m")

    print("\n\033[1;32m✅ Generación de archivos CSV finalizada.\033[0m")

# Punto de entrada principal
if __name__ == "__main__":
    generar_csv_por_digito()
