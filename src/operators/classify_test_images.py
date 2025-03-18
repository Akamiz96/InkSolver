import os
import cv2
import numpy as np
import pandas as pd

# Definir rutas
input_folder = "../../data/operators/processed/test/"
output_folder = "test_results"
os.makedirs(output_folder, exist_ok=True)

output_csv = os.path.join(output_folder, "classified_test_images.csv")
BLOCK_SIZE = 50  # Número de imágenes a procesar por bloque

def load_image_paths(folder):
    """Carga las rutas de todas las imágenes organizadas por categoría."""
    image_paths = {}
    for category in os.listdir(folder):
        category_path = os.path.join(folder, category)
        if os.path.isdir(category_path):
            images = [(category, os.path.join(category_path, filename), filename) for filename in os.listdir(category_path)]
            image_paths[category] = images
    return image_paths

def rotate_image_45(img):
    """Rota la imagen 45 grados y recorta los bordes blancos innecesarios."""
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
    """Calcula el histograma de proyección en la dirección especificada."""
    return np.sum(img, axis=axis)

def count_peaks(hist, threshold=0.5):
    """Cuenta los picos en un histograma de proyección basado en un umbral relativo."""
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
    """Clasifica la operación matemática basada en la cantidad de picos detectados."""
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

# Crear el archivo CSV con encabezados antes de procesar los datos
df_columns = ["Operador_Real", "Nombre_Imagen", "Picos_Horizontal_Original", "Picos_Vertical_Original", "Picos_Horizontal_Rotado", "Prediccion"]
pd.DataFrame(columns=df_columns).to_csv(output_csv, index=False)

def process_images():
    """Carga, procesa y clasifica las imágenes en bloques por categoría."""
    print("\n\033[91m🔴 Cargando imágenes desde la carpeta de test...\033[0m")
    image_paths = load_image_paths(input_folder)

    if not image_paths:
        print("\033[91m⚠️ No se encontraron imágenes para procesar en la carpeta de test.\033[0m")
        return

    for category, images in image_paths.items():
        total_images = len(images)
        print(f"\n\033[94m📂 Procesando {total_images} imágenes de la categoría '{category}'...\033[0m")

        # Procesar en bloques de 50
        for i in range(0, total_images, BLOCK_SIZE):
            batch_paths = images[i:i + BLOCK_SIZE]
            batch_data = []

            for operator, img_path, img_file in batch_paths:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue  # Saltar imágenes corruptas

                hist_horizontal = compute_projection_histogram(img, axis=1)
                hist_vertical = compute_projection_histogram(img, axis=0)
                horizontal_peaks = count_peaks(hist_horizontal, threshold=0.8)
                vertical_peaks = count_peaks(hist_vertical, threshold=0.8)
                rotated_img = rotate_image_45(img)
                hist_horizontal_rot = compute_projection_histogram(rotated_img, axis=1)
                horizontal_peaks_rot = count_peaks(hist_horizontal_rot, threshold=0.8)
                prediction = classify_operation(horizontal_peaks, vertical_peaks, horizontal_peaks_rot)

                batch_data.append({
                    "Operador_Real": operator,
                    "Nombre_Imagen": img_file,
                    "Picos_Horizontal_Original": horizontal_peaks,
                    "Picos_Vertical_Original": vertical_peaks,
                    "Picos_Horizontal_Rotado": horizontal_peaks_rot,
                    "Prediccion": prediction
                })

            # Guardar el bloque en el CSV
            df_batch = pd.DataFrame(batch_data)
            df_batch.to_csv(output_csv, mode="a", header=False, index=False)

            print(f"\033[92m✔ {min(i + BLOCK_SIZE, total_images)}/{total_images} imágenes procesadas en '{category}'...\033[0m")

    print("\n\033[92m✅ PROCESO COMPLETADO: CLASIFICACIÓN FINALIZADA.\033[0m")
    print(f"\033[93m📂 Archivo de resultados guardado en: {output_csv}\033[0m")

if __name__ == "__main__":
    process_images()
