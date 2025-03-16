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

def load_images(category, max_samples=3):  # Ahora solo 3 imágenes
    """Carga imágenes de una categoría específica."""
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

# Cargar imágenes por categoría
operation_images = {category: load_images(category) for category in operation_categories}

def compute_projection_histogram(img, axis=0):
    """Calcula el histograma de proyección en la dirección especificada."""
    projection = np.sum(img, axis=axis)
    return projection / np.max(projection)  # Normalización

# Procesar cada operador y generar las gráficas
for category in operation_categories:
    images = operation_images[category]
    if not images:
        continue

    fig, axes = plt.subplots(len(images), 3, figsize=(12, len(images) * 3))
    fig.suptitle(f"Proyección Normalizada - {category}", fontsize=14, fontweight="bold")

    for i, img in enumerate(images):
        hist_horizontal = compute_projection_histogram(img, axis=1) 
        hist_vertical = compute_projection_histogram(img, axis=0)

        # Mostrar imagen original
        axes[i, 0].imshow(img, cmap='gray')
        axes[i, 0].set_title("Imagen Original")
        axes[i, 0].axis("off")
        
        # Mostrar histograma horizontal
        axes[i, 1].plot(hist_horizontal, color="blue")
        axes[i, 1].set_title("Proyección Horizontal")
        axes[i, 1].set_xlim([0, len(hist_horizontal)])

        # Mostrar histograma vertical
        axes[i, 2].plot(hist_vertical, color="red")
        axes[i, 2].set_title("Proyección Vertical")
        axes[i, 2].set_xlim([0, len(hist_vertical)])

    plt.tight_layout()

    # Guardar la figura en la carpeta 'operator_analysis'
    output_path = os.path.join(output_dir, f"projection_{category}.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    # Intentar mostrar la imagen sin warnings
    try:
        plt.show(block=False)
    except:
        pass  # Si hay un error, continuar sin mostrar warning

    # Verificar si la figura realmente se mostró
    if not plt.get_fignums():
        print("\n\033[91m" + "=" * 50)
        print(f"⚠️  WARNING: Interactive display is not available for {category} ⚠️")
        print("=" * 50 + "\033[0m\n")

    print(f"\033[93m📂 Projection image saved at: {output_path}\033[0m")
