import os
import cv2
import matplotlib.pyplot as plt
import warnings

# Suprimir warnings innecesarios
warnings.simplefilter("ignore", category=UserWarning)

# Definir la ruta del dataset de operandos
input_folder = "../../data/operands/raw/dataset/"
output_folder = "operand_analysis"
os.makedirs(output_folder, exist_ok=True)

# Definir la ruta donde se guardará la imagen de salida
output_image_path = os.path.join(output_folder, "operand_samples.png")

# Definir los dígitos (0-9)
digits = [str(i) for i in range(10)]
samples_per_digit = 5  # Número de ejemplos a mostrar por dígito

# Almacenar imágenes por cada dígito
operand_samples = {digit: [] for digit in digits}

print("\n\033[91m🔴 Cargando ejemplos de operandos...\033[0m")

for digit in digits:
    digit_path = os.path.join(input_folder, digit)
    if os.path.isdir(digit_path):
        images = sorted(os.listdir(digit_path))[:samples_per_digit]  # Tomar hasta 3 imágenes
        for img_name in images:
            img_path = os.path.join(digit_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                operand_samples[digit].append(img)

# Verificar si hay datos
if not any(operand_samples.values()):
    print("\033[91m⚠️ No se encontraron imágenes de operandos en la carpeta de dataset.\033[0m")
    exit()

# Determinar el tamaño de la cuadrícula
rows = len(digits)
cols = samples_per_digit

fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
fig.subplots_adjust(top=0.92)  # Ajustar el espacio del título
fig.suptitle("Operand Samples (0-9)", fontsize=16, fontweight="bold", y=1)  # Separar más el título

for i, (digit, images) in enumerate(operand_samples.items()):
    for j in range(cols):
        ax = axes[i, j] if rows > 1 else axes[j]
        ax.axis("off")
        if j < len(images):
            ax.imshow(images[j], cmap="gray")

plt.tight_layout()
plt.savefig(output_image_path, dpi=300, bbox_inches="tight")

# Intentar mostrar la imagen sin warnings
try:
    plt.show(block=False)
except:
    pass

# 🔹 **Mensaje Final**
print("\n\033[92m✅ VISUALIZACIÓN COMPLETADA: IMAGEN GENERADA.\033[0m")
print(f"\033[93m📂 Imagen guardada en: {output_image_path}\033[0m")
