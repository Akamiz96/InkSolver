"""
===============================================================================
Proyecto: Inksolver
Archivo: matriz_distancia_digitos.py
Descripcion: Calcula y visualiza la matriz de distancia entre los vectores 
             promedio de tinta por cuadrante de cada dígito manuscrito.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-03
Ultima modificacion: 2025-04-03
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, pandas, numpy, matplotlib, scipy, warnings
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python matriz_distancia_digitos.py
===============================================================================
Notas:
- La distancia se calcula entre los vectores promedio de cada dígito 
  (extraídos de un archivo CSV con 9 cuadrantes por dígito).
- La métrica de distancia predeterminada es Euclidiana, pero puede cambiarse.
- El resultado se guarda como imagen PNG y se muestra como heatmap.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import warnings

# Suprimir advertencias innecesarias de matplotlib
warnings.simplefilter("ignore", category=UserWarning)

def matriz_distancia_digitos(csv_path="csv_por_digito/promedios_por_digito.csv",
                              metodo="euclidean",
                              output_dir="operand_analysis"):
    """
    Calcula y visualiza la matriz de distancia entre los vectores promedio de tinta por dígito.

    Parámetros:
    - csv_path: ruta del CSV que contiene los promedios por cuadrante para cada dígito.
    - metodo: métrica de distancia (por defecto "euclidean", también puede ser "cosine", etc.).
    - output_dir: carpeta donde se guardará la imagen generada.
    """
    if not os.path.exists(csv_path):
        print(f"\033[91m🚫 Archivo no encontrado: {csv_path}\033[0m")
        return

    print(f"\033[94m📐 Calculando matriz de distancia con el método '{metodo}'...\033[0m")

    # Leer el CSV con los vectores promedio
    df = pd.read_csv(csv_path)
    vectores = df[[f"P. Cuadrante {i}" for i in range(1, 10)]].values  # Solo columnas de cuadrantes
    digitos = df["Digito"].values  # Etiquetas (0 al 9)

    # Calcular matriz de distancias entre cada par de vectores promedio
    distancias = cdist(vectores, vectores, metric=metodo)

    # Crear figura para el heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(distancias, cmap="Blues")

    # Configurar ejes con etiquetas de los dígitos
    ax.set_xticks(np.arange(len(digitos)))
    ax.set_yticks(np.arange(len(digitos)))
    ax.set_xticklabels(digitos)
    ax.set_yticklabels(digitos)

    # Escribir los valores dentro de cada celda del heatmap
    for i in range(len(digitos)):
        for j in range(len(digitos)):
            valor = distancias[i, j]
            ax.text(j, i, f"{valor:.2f}",
                    ha="center", va="center",
                    color="white" if valor > distancias.max() * 0.5 else "black")

    # Título y etiquetas
    ax.set_title(f"Matriz de distancia entre vectores promedio ({metodo})")
    plt.xlabel("Dígito")
    plt.ylabel("Dígito")
    plt.colorbar(im, label="Distancia")
    plt.tight_layout()

    # Crear carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Guardar imagen
    output_path = os.path.join(output_dir, f"matriz_distancia_{metodo}.png")
    fig.savefig(output_path)
    print(f"\n\033[92m💾 Figura guardada como: {output_path}\033[0m")

    # Mostrar visualización
    plt.show()
    print("\n\033[1;32m✅ Visualización de matriz de distancias completa.\033[0m")

# Punto de entrada
if __name__ == "__main__":
    matriz_distancia_digitos()
