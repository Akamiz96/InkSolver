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

# Definir la carpeta donde se guardarán las gráficas
output_dir = "operator_analysis"
os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

def load_single_image(category):
    """Carga una única imagen de una categoría específica."""
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        image_files = os.listdir(category_path)
        if image_files:
            img_path = os.path.join(category_path, image_files[0])
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            return img
    return None

def rotate_image_45(img):
    """Rota la imagen 45 grados y recorta los bordes blancos innecesarios."""
    h, w = img.shape
    center = (w // 2, h // 2)

    # Matriz de rotación para 45 grados
    rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)

    # Calcular el tamaño de la nueva imagen para evitar recortes
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Ajustar la matriz de transformación para el centro de la nueva imagen
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    # Aplicar la rotación con interpolación NEAREST para evitar difuminado
    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_w, new_h), borderValue=255, flags=cv2.INTER_NEAREST)

    # Recortar la imagen para eliminar los bordes blancos
    _, thresh = cv2.threshold(rotated_img, 250, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)
    cropped_img = rotated_img[y:y+h, x:x+w]

    return cropped_img

def compute_projection_histogram(img, axis=0):
    """Calcula el histograma de proyección en la dirección especificada y lo normaliza."""
    projection = np.sum(img, axis=axis)
    return projection / np.max(projection)  # Normalización

# Crear una figura grande para mostrar todas las imágenes en una sola
fig, axes = plt.subplots(len(operation_categories), 4, figsize=(16, len(operation_categories) * 3))
fig.suptitle("Análisis de Proyección - Imagen Original y Rotada 45°", fontsize=16, fontweight="bold")

# Procesar cada operador
for i, category in enumerate(operation_categories):
    img = load_single_image(category)
    if img is None:
        continue

    # Calcular histogramas para la imagen original
    hist_horizontal_orig = compute_projection_histogram(img, axis=1)
    hist_vertical_orig = compute_projection_histogram(img, axis=0)

    # Rotar la imagen 45 grados y recortar
    rotated_img = rotate_image_45(img)

    # Calcular histogramas después de la rotación
    hist_horizontal_rot = compute_projection_histogram(rotated_img, axis=1)
    hist_vertical_rot = compute_projection_histogram(rotated_img, axis=0)

    # Mostrar imagen original
    axes[i, 0].imshow(img, cmap='gray')
    axes[i, 0].set_title(f"{category.upper()} - Imagen Original")
    axes[i, 0].axis("off")

    # Mostrar histogramas de la imagen original
    axes[i, 1].plot(hist_horizontal_orig, color="blue", label="Horizontal")
    axes[i, 1].plot(hist_vertical_orig, color="red", label="Vertical")
    axes[i, 1].set_title("Proyección Original")
    axes[i, 1].legend()

    # Mostrar imagen rotada
    axes[i, 2].imshow(rotated_img, cmap='gray')
    axes[i, 2].set_title("Imagen Rotada 45°")
    axes[i, 2].axis("off")

    # Mostrar histogramas de la imagen rotada
    axes[i, 3].plot(hist_horizontal_rot, color="blue", label="Horizontal")
    axes[i, 3].plot(hist_vertical_rot, color="red", label="Vertical")
    axes[i, 3].set_title("Proyección Rotada")
    axes[i, 3].legend()

plt.tight_layout()

# Guardar la figura en la carpeta 'operator_analysis'
output_path = os.path.join(output_dir, "projection_rotated_cropped.png")
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

print(f"\033[93m📂 Projection image saved at: {output_path}\033[0m")
