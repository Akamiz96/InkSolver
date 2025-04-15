"""
===============================================================================
Proyecto: Inksolver
Archivo: operands_test_ink_density_avg.py
Descripcion: Calcula el promedio del porcentaje de tinta en cada cuadrante 
             (3x3) para todos los dígitos, y genera un único CSV resumen de las
             imagenes de test
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-14
Ultima modificacion: 2025-04-14
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, pandas
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python operands_test_ink_density_avg.py
===============================================================================
Notas:
- Este script espera que ya existan archivos CSV individuales por dígito,
  generados previamente por el script de extracción de cuadrantes.
- Calcula los promedios de los porcentajes de tinta en los 9 cuadrantes
  para cada dígito (0 al 9) y los guarda en un único archivo CSV.
===============================================================================
"""

import os
import pandas as pd

def generar_csv_promedios(input_path="csv_por_digito_test", output_file="csv_por_digito_test/promedios_por_digito.csv"):
    """
    Calcula el promedio de tinta por cuadrante para cada dígito y guarda los
    resultados en un único archivo CSV.

    Parámetros:
    - input_path: carpeta que contiene los CSV por dígito
    - output_file: ruta donde se guardará el CSV resumen de promedios
    """
    resultados = []

    print(f"\n\033[94m📊 Generando promedios de tinta por cuadrante para cada dígito...\033[0m")

    for digito in range(10):
        file_path = os.path.join(input_path, f"digito_{digito}.csv")
        
        # Verificar que exista el archivo para el dígito actual
        if not os.path.exists(file_path):
            print(f"\033[93m⚠️ No se encontró el archivo CSV para el dígito {digito}\033[0m")
            continue
        
        # Leer archivo CSV correspondiente al dígito
        df = pd.read_csv(file_path)

        # Calcular el promedio de los porcentajes por cada cuadrante
        columnas_cuadrantes = [f"P. Cuadrante {i}" for i in range(1, 10)]
        promedios = df[columnas_cuadrantes].mean()

        # Crear fila con dígito y sus promedios
        fila = [digito] + list(promedios)
        resultados.append(fila)

        print(f"\033[92m✔ Promedios calculados para dígito {digito}\033[0m")

    # Armar DataFrame final con todos los promedios
    columnas = ["Digito"] + [f"P. Cuadrante {i}" for i in range(1, 10)]
    df_resultado = pd.DataFrame(resultados, columns=columnas)

    # Guardar archivo CSV con todos los promedios
    df_resultado.to_csv(output_file, index=False)
    print(f"\n\033[1;32m✅ CSV de promedios guardado en: {output_file}\033[0m")

# Punto de entrada principal
if __name__ == "__main__":
    generar_csv_promedios()
