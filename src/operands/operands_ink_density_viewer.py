"""
===============================================================================
Proyecto: Inksolver
Archivo: visualize_colored_quadrants.py
Descripcion: Visualiza imágenes de dígitos manuscritos y colorea sus cuadrantes
             en función del porcentaje de tinta presente en cada bloque.
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
    python visualize_colored_quadrants.py
===============================================================================
Notas:
- Este script analiza imágenes de los operandos (0-9), calcula el porcentaje
  de píxeles negros por cuadrante (3x3 por defecto) y superpone un color rojo
  proporcional a la cantidad de tinta.
- Se genera una figura general y una imagen individual por cada dígito.
===============================================================================
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suprimir advertencias innecesarias de matplotlib
warnings.simplefilter("ignore", category=UserWarning)

def compute_tinta_por_cuadrante(image, grid_size=(3,3)):
    """
    Retorna una matriz con el porcentaje de píxeles negros (tinta) en cada cuadrante.

    Parámetros:
    - image: imagen en escala de grises.
    - grid_size: tamaño de la cuadrícula (por defecto 3x3).

    Retorna:
    - Matriz 2D de porcentajes (entre 0 y 1) por cuadrante.
    """
    h, w = image.shape
    gh, gw = grid_size
    step_h, step_w = h // gh, w // gw

    # Binarizar imagen: tinta negra será 255 (invertida)
    _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    
    porcentajes = np.zeros((gh, gw))
    for i in range(gh):
        for j in range(gw):
            bloque = binary[i*step_h:(i+1)*step_h, j*step_w:(j+1)*step_w]
            total = bloque.size
            tinta = np.sum(bloque > 0)
            porcentajes[i, j] = tinta / total
    return porcentajes

def mostrar_con_cuadrantes_coloreados(base_path="../../data/operands/raw/dataset", output_path="output_colored_grids", samples_per_digit=5, grid_size=(3,3)):
    """
    Visualiza y guarda imágenes con cuadrantes coloreados según porcentaje de tinta.

    - Cada imagen se recubre con rectángulos rojos con transparencia proporcional
      al porcentaje de tinta en cada celda de la grilla.
    - Se guarda un collage por dígito y una imagen general con todos los ejemplos.
    """
    os.makedirs(output_path, exist_ok=True)

    # Crear figura general con 10 filas (una por dígito)
    fig, axes = plt.subplots(10, samples_per_digit, figsize=(samples_per_digit * 2, 20))

    for digit in range(10):
        digit_path = os.path.join(base_path, str(digit))
        images = sorted(os.listdir(digit_path))[:samples_per_digit]

        print(f"\n\033[94m🖍️ Procesando dígito {digit} ({len(images)} imágenes)...\033[0m")

        for i, img_name in enumerate(images):
            img_path = os.path.join(digit_path, img_name)
            print(f"   📄 Cargando imagen: \033[92m{img_name}\033[0m")

            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            h, w = image.shape
            percent_tinta = compute_tinta_por_cuadrante(image, grid_size)
            gh, gw = grid_size
            step_h, step_w = h // gh, w // gw

            # Mostrar imagen base
            axes[digit, i].imshow(image, cmap='gray')

            # Dibujar rectángulos con transparencia según tinta
            for row in range(gh):
                for col in range(gw):
                    alpha = percent_tinta[row, col]
                    rect = plt.Rectangle(
                        (col * step_w, row * step_h),
                        step_w, step_h,
                        color='red',
                        alpha=alpha * 0.8,
                        linewidth=0
                    )
                    axes[digit, i].add_patch(rect)

            axes[digit, i].axis("off")
            if i == 0:
                axes[digit, i].set_ylabel(f'Dígito {digit}', fontsize=12)

        # Crear figura individual por dígito
        print(f"📸 Guardando collage de dígito {digit}...")
        digit_fig = plt.figure(figsize=(samples_per_digit * 2, 2))
        for i, img_name in enumerate(images):
            img_path = os.path.join(digit_path, img_name)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            percent_tinta = compute_tinta_por_cuadrante(image, grid_size)
            h, w = image.shape
            gh, gw = grid_size
            step_h, step_w = h // gh, w // gw

            ax = digit_fig.add_subplot(1, samples_per_digit, i + 1)
            ax.imshow(image, cmap='gray')
            for row in range(gh):
                for col in range(gw):
                    alpha = percent_tinta[row, col]
                    rect = plt.Rectangle(
                        (col * step_w, row * step_h),
                        step_w, step_h,
                        color='red',
                        alpha=alpha * 0.8,
                        linewidth=0
                    )
                    ax.add_patch(rect)
            ax.axis("off")

        digit_fig.tight_layout()
        digit_fig_path = os.path.join(output_path, f"{digit}.png")
        digit_fig.savefig(digit_fig_path)
        plt.close(digit_fig)
        print(f"   💾 Guardado en: \033[96m{digit_fig_path}\033[0m")
        print(f"\033[90m✅ Finalizado dígito {digit}\033[0m")

    # Guardar imagen general con todos los dígitos
    all_digits_path = os.path.join(output_path, "all_digits_colored.png")
    fig.tight_layout()
    fig.savefig(all_digits_path)
    print(f"\n\033[1;32m🎉 Visualización completa. Imagen general guardada en '{all_digits_path}'\033[0m")
    plt.show()

# Punto de entrada del script
if __name__ == "__main__":
    mostrar_con_cuadrantes_coloreados()
