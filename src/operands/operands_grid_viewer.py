"""
===============================================================================
Proyecto: Inksolver
Archivo: operands_grid_viewer.py
Descripcion: Visualiza ejemplos de dígitos manuscritos mostrando una cuadrícula
             sobre cada imagen para facilitar el análisis de distribución espacial.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-03
Ultima modificacion: 2025-04-03
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, cv2, numpy, matplotlib, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python operands_grid_viewer.py
===============================================================================
Notas:
- El script carga imágenes de los operandos (0 al 9) desde la ruta indicada,
  dibuja una cuadrícula sobre cada imagen y las visualiza organizadas por dígito.
- También guarda un collage por cada dígito y uno general con todos los dígitos.
===============================================================================
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suprimir advertencias innecesarias de matplotlib
warnings.simplefilter("ignore", category=UserWarning)

def draw_grid(image, grid_size=(3,3), color=128):
    """
    Dibuja una cuadrícula sobre la imagen sin modificar la original.
    
    Parámetros:
    - image: imagen en escala de grises (numpy array)
    - grid_size: tupla con número de filas y columnas (por defecto 3x3)
    - color: valor del gris para las líneas de la grilla (0=negro, 255=blanco)
    
    Retorna:
    - Imagen con líneas superpuestas representando la grilla
    """
    img = image.copy()
    h, w = img.shape
    gh, gw = grid_size
    step_h, step_w = h // gh, w // gw

    # Dibujar líneas horizontales
    for i in range(1, gh):
        y = i * step_h
        img[y-1:y+1, :] = color

    # Dibujar líneas verticales
    for j in range(1, gw):
        x = j * step_w
        img[:, x-1:x+1] = color

    return img

def show_digits_with_grid(base_path="../../data/operands/raw/dataset", output_path="output_with_grids", samples_per_digit=5, grid_size=(3,3)):
    """
    Visualiza y guarda imágenes de operandos con una cuadrícula superpuesta.
    
    - Muestra en pantalla una grilla 10xN con ejemplos por dígito.
    - Guarda una imagen por cada dígito y una imagen general.
    """
    os.makedirs(output_path, exist_ok=True)

    # Crear figura para mostrar todos los dígitos (10 filas)
    fig, axes = plt.subplots(10, samples_per_digit, figsize=(samples_per_digit * 2, 20))

    for digit in range(10):
        digit_path = os.path.join(base_path, str(digit))
        images = sorted(os.listdir(digit_path))[:samples_per_digit]

        print(f"\n\033[94m🔢 Procesando dígito {digit} ({len(images)} imágenes)...\033[0m")

        for i, img_name in enumerate(images):
            img_path = os.path.join(digit_path, img_name)
            print(f"   📄 Cargando imagen: \033[92m{img_name}\033[0m")

            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            image_with_grid = draw_grid(image, grid_size)

            # Mostrar en la figura principal (grilla 10xN)
            axes[digit, i].imshow(image_with_grid, cmap='gray')
            axes[digit, i].axis("off")
            if i == 0:
                axes[digit, i].set_ylabel(f'Dígito {digit}', fontsize=12)

        # Crear figura individual para el dígito actual
        print(f"📸 Guardando collage de dígito {digit}...")
        digit_fig = plt.figure(figsize=(samples_per_digit * 2, 2))
        for i, img_name in enumerate(images):
            img_path = os.path.join(digit_path, img_name)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            image_with_grid = draw_grid(image, grid_size)
            ax = digit_fig.add_subplot(1, samples_per_digit, i + 1)
            ax.imshow(image_with_grid, cmap='gray')
            ax.axis("off")
        
        # Guardar imagen individual por dígito
        digit_fig.tight_layout()
        digit_fig_path = os.path.join(output_path, f"{digit}.png")
        digit_fig.savefig(digit_fig_path)
        plt.close(digit_fig)

        print(f"   💾 Guardado en: \033[96m{digit_fig_path}\033[0m")
        print(f"\033[90m✅ Finalizado dígito {digit}\033[0m")

    # Guardar figura general con todos los dígitos
    all_digits_path = os.path.join(output_path, "all_digits.png")
    fig.tight_layout()
    fig.savefig(all_digits_path)

    print(f"\n\033[1;32m🎉 Visualización completa. Imagen general guardada en '{all_digits_path}'\033[0m")
    plt.show()

# Punto de entrada del script
if __name__ == "__main__":
    show_digits_with_grid()
