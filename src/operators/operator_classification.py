"""
===============================================================================
Proyecto: Inksolver
Archivo: operator_classification.py
Descripcion: Clasifica imagenes de operadores matematicos segun sus histogramas de proyeccion.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-03-16
Ultima modificacion: 2025-03-18
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerias externas: OpenCV (cv2), NumPy, Pandas, os, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python operator_classification.py
===============================================================================
Notas:
- El dataset debe estar en '../../data/operators/raw/'.
- Los resultados de la clasificacion se guardaran en 'operator_results/operator_classification_results.csv'.
===============================================================================
"""

import os
import cv2
import numpy as np
import pandas as pd
import warnings

# Suprimir warnings innecesarios
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de operadores
dataset_path = "../../data/operators/raw/dataset/"
operation_categories = ["div", "equals", "sub", "sum", "times"]

# Definir la carpeta donde se guardara el CSV con los resultados
output_dir = "operator_results"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

# Ruta del archivo CSV
csv_path = os.path.join(output_dir, "operator_classification_results.csv")

# Tamano del bloque de procesamiento
BLOCK_SIZE = 50  # Numero de imagenes a procesar por bloque

def load_image_paths(category):
    """
    Carga las rutas de todas las imagenes en una categoria especifica.

    Args:
        category (str): Nombre de la categoria a cargar.

    Returns:
        list: Lista de rutas de imagenes en la categoria.
    """
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        return [os.path.join(category_path, img_file) for img_file in os.listdir(category_path)]
    return []

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
    Calcula el histograma de proyeccion en la direccion especificada.

    Args:
        img (numpy.ndarray): Imagen en escala de grises.
        axis (int): Direccion del histograma (0=vertical, 1=horizontal).

    Returns:
        numpy.ndarray: Histograma de proyeccion de la imagen.
    """
    return np.sum(img, axis=axis)

def count_peaks(hist, threshold=0.5):
    """
    Cuenta los picos en un histograma de proyeccion basado en un umbral relativo.

    Args:
        hist (numpy.ndarray): Histograma de proyeccion.
        threshold (float): Umbral relativo para contar picos.

    Returns:
        int: Numero de picos detectados en el histograma.
    """
    if np.max(hist) == 0:
        return 0
    normalized_hist = hist / np.max(hist)
    peaks = 0
    in_peak = False
    for value in normalized_hist:
        if value < threshold and not in_peak:
            peaks += 1
            in_peak = True
        elif value >= threshold:
            in_peak = False
    return peaks

def classify_operation(horizontal_peaks, vertical_peaks, horizontal_peaks_rot):
    """
    Clasifica la operacion matematica basada en la cantidad de picos detectados.

    Args:
        horizontal_peaks (int): Picos en el histograma horizontal original.
        vertical_peaks (int): Picos en el histograma vertical original.
        horizontal_peaks_rot (int): Picos en el histograma horizontal de la imagen rotada.

    Returns:
        str: Tipo de operador clasificado.
    """
    if horizontal_peaks == 0 and vertical_peaks == 0 and (horizontal_peaks_rot > 2 or horizontal_peaks_rot == 0):
        return "div"
    elif horizontal_peaks == 2 and vertical_peaks == 0:
        return "equals"
    elif horizontal_peaks == 1 and vertical_peaks == 0:
        return "sub"
    elif horizontal_peaks == 1 and vertical_peaks == 1:
        return "sum"
    elif horizontal_peaks == 0 and vertical_peaks == 0 and horizontal_peaks_rot <= 2:
        return "times"
    else:
        return "Desconocido"

# Crear archivo CSV con encabezados antes de procesar los datos
df_columns = ["Categoria", "Nombre_Imagen", "Picos_Horizontal_Original", "Picos_Vertical_Original", "Picos_Horizontal_Rotado", "Prediccion"]
pd.DataFrame(columns=df_columns).to_csv(csv_path, index=False)

# Procesar imágenes en bloques
for category in operation_categories:
    image_paths = load_image_paths(category)
    
    if not image_paths:
        continue

    total_images = len(image_paths)
    print(f"\033[94mProcesando {total_images} imágenes de la categoría '{category}'...\033[0m")

    # Procesar en bloques
    for i in range(0, total_images, BLOCK_SIZE):
        batch_paths = image_paths[i:i + BLOCK_SIZE]
        batch_data = []

        for img_path in batch_paths:
            img_file = os.path.basename(img_path)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue  # Saltar imágenes corruptas

            # Obtener histogramas de la imagen original
            hist_horizontal = compute_projection_histogram(img, axis=1)
            hist_vertical = compute_projection_histogram(img, axis=0)
            
            # Contar picos en la imagen original
            horizontal_peaks = count_peaks(hist_horizontal, threshold=0.8)
            vertical_peaks = count_peaks(hist_vertical, threshold=0.8)

            # Rotar la imagen 45 grados
            rotated_img = rotate_image_45(img)

            # Obtener histogramas de la imagen rotada
            hist_horizontal_rot = compute_projection_histogram(rotated_img, axis=1)
            
            # Contar picos en la imagen rotada
            horizontal_peaks_rot = count_peaks(hist_horizontal_rot, threshold=0.8)

            # Clasificar la operación
            prediction = classify_operation(horizontal_peaks, vertical_peaks, horizontal_peaks_rot)

            # Almacenar en lista de datos
            batch_data.append({
                "Categoria": category,
                "Nombre_Imagen": img_file,
                "Picos_Horizontal_Original": horizontal_peaks,
                "Picos_Vertical_Original": vertical_peaks,
                "Picos_Horizontal_Rotado": horizontal_peaks_rot,
                "Prediccion": prediction
            })

        # Guardar bloque en el CSV
        df_batch = pd.DataFrame(batch_data)
        df_batch.to_csv(csv_path, mode="a", header=False, index=False)

        print(f"\033[92m✔ {min(i + BLOCK_SIZE, total_images)}/{total_images} imágenes procesadas...\033[0m")

# Mensajes finales
print("\n\033[92m" + "=" * 50)
print("✅ PROCESO FINALIZADO: RESULTADOS GUARDADOS")
print("=" * 50 + "\033[0m")
print(f"\033[93m📂 Archivo CSV guardado en: {csv_path}\033[0m")
