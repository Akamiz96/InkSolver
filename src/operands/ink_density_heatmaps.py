import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suprimir advertencias innecesarias
warnings.simplefilter("ignore", category=UserWarning)

def visualizar_huellas_promedio(csv_path="csv_por_digito/promedios_por_digito.csv",
                                 output_path="operand_analysis/huella_promedio.png"):
    if not os.path.exists(csv_path):
        print(f"\033[91m🚫 Archivo no encontrado: {csv_path}\033[0m")
        return

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"\033[94m📊 Cargando datos desde '{csv_path}'...\033[0m")
    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    axes = axes.flatten()

    for idx, row in df.iterrows():
        digit = int(row["Digito"])
        valores = row[[f"P. Cuadrante {i}" for i in range(1, 10)]].values
        matriz = valores.reshape((3, 3))

        ax = axes[digit]
        im = ax.imshow(matriz, cmap='Reds', vmin=0, vmax=0.2)

        for i in range(3):
            for j in range(3):
                valor = matriz[i, j]
                ax.text(j, i, f"{valor:.2f}", ha='center', va='center',
                        color='black' if valor < 0.1 else 'white', fontsize=10)

        ax.set_title(f'Dígito {digit}')
        ax.axis('off')

    fig.suptitle("Huella digital promedio por dígito (ajustada para 20% máximo)", fontsize=14)
    plt.tight_layout()

    # Guardar figura
    fig.savefig(output_path)
    print(f"\n\033[92m💾 Figura guardada como: {output_path}\033[0m")

    plt.show()
    print("\n\033[1;32m✅ Visualización completa.\033[0m")

if __name__ == "__main__":
    visualizar_huellas_promedio()
