"""
===============================================================================
Proyecto: Inksolver
Archivo: visualize_operands.py
Descripcion: Visualiza ejemplos de operandos manuscritos agrupados por dígito 
             en una cuadrícula y guarda la imagen resultante.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-03
Ultima modificacion: 2025-04-03
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, cv2, matplotlib, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python visualize_operands.py
===============================================================================
Notas:
- El script selecciona 5 imágenes por cada dígito (0 al 9) desde la carpeta 
  de dataset de operandos y las organiza visualmente en una cuadrícula.
- La imagen generada se guarda en la carpeta 'operand_analysis'.
===============================================================================
"""

import os
import cv2
import matplotlib.pyplot as plt
import warnings

# Suprimir advertencias innecesarias de matplotlib
warnings.simplefilter("ignore", category=UserWarning)

# Definir ruta del dataset de operandos (entrada) y carpeta de salida
input_folder = "../../data/operands/raw/dataset/"
output_folder = "operand_analysis"
os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe

# Definir ruta del archivo de salida (imagen)
output_image_path = os.path.join(output_folder, "operand_samples.png")

# Lista de dígitos del 0 al 9
digits = [str(i) for i in range(10)]
samples_per_digit = 5  # Número de ejemplos a mostrar por dígito

# Crear diccionario para almacenar las imágenes de cada dígito
operand_samples = {digit: [] for digit in digits}

print("\n\033[91m🔴 Cargando ejemplos de operandos...\033[0m")

# Recorrer cada carpeta por dígito y cargar hasta 5 imágenes
for digit in digits:
    digit_path = os.path.join(input_folder, digit)
    if os.path.isdir(digit_path):
        images = sorted(os.listdir(digit_path))[:samples_per_digit]  # Tomar las primeras imágenes
        for img_name in images:
            img_path = os.path.join(digit_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                operand_samples[digit].append(img)

# Verificar si se cargaron imágenes
if not any(operand_samples.values()):
    print("\033[91m⚠️ No se encontraron imágenes de operandos en la carpeta de dataset.\033[0m")
    exit()

# Calcular el tamaño de la cuadrícula para visualización
rows = len(digits)  # 10 filas (una por dígito)
cols = samples_per_digit  # 5 columnas por ejemplo

# Crear figura con subplots organizados en grilla
fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
fig.subplots_adjust(top=0.92)  # Ajustar espacio superior para el título
fig.suptitle("Operand Samples (0-9)", fontsize=16, fontweight="bold", y=1)  # Título superior

# Mostrar cada imagen en su respectiva posición
for i, (digit, images) in enumerate(operand_samples.items()):
    for j in range(cols):
        ax = axes[i, j] if rows > 1 else axes[j]
        ax.axis("off")  # Ocultar ejes
        if j < len(images):
            ax.imshow(images[j], cmap="gray")

# Ajustar diseño y guardar la imagen resultante
plt.tight_layout()
plt.savefig(output_image_path, dpi=300, bbox_inches="tight")

# Mostrar la figura sin bloquear ejecución
try:
    plt.show(block=False)
except:
    pass

# 🔹 Mensaje final
print("\n\033[92m✅ VISUALIZACIÓN COMPLETADA: IMAGEN GENERADA.\033[0m")
print(f"\033[93m📂 Imagen guardada en: {output_image_path}\033[0m")
