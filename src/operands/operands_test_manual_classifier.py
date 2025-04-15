"""
===============================================================================
Proyecto: Inksolver
Archivo: operands_test_manual_classifier.py
Descripcion: Clasificador simple basado en distancia Euclidiana entre vectores
             de tinta por cuadrante y los vectores promedio por dígito de test.
Autor: Alejandro Castro Martinez
Fecha de creacion: 2025-04-14
Ultima modificacion: 2025-04-14
Version: 1.0
===============================================================================
Dependencias:
- Python 3.10
- Librerías externas: os, pandas, numpy, scipy
===============================================================================
Uso:
Ejecutar el script con el siguiente comando:
    python operands_test_manual_classifier.py
===============================================================================
Notas:
- El script clasifica cada imagen manuscrita comparándola con los promedios
  de cada dígito (vectores prototipo), utilizando distancia Euclidiana.
- Requiere que previamente existan los CSV con los cuadrantes individuales
  y el archivo de promedios por dígito.
- Los resultados se guardan en un único archivo CSV con predicciones.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

def clasificador_manual(csv_prototipos="csv_por_digito_test/promedios_por_digito.csv",
                        csv_individuales_path="csv_por_digito_test",
                        salida="test_analysis/clasificacion_resultados_test.csv",
                        block_size=100):
    """
    Clasifica cada imagen de operandos utilizando distancia Euclidiana
    a los vectores promedio de cada dígito (prototipos).

    Parámetros:
    - csv_prototipos: ruta al archivo CSV con vectores promedio por dígito.
    - csv_individuales_path: carpeta con los CSV individuales por imagen.
    - salida: ruta de salida para guardar el CSV con predicciones.
    - block_size: frecuencia de impresión del progreso.
    """
    # Verificar existencia del archivo de prototipos
    if not os.path.exists(csv_prototipos):
        print(f"\033[91m🚫 Archivo de prototipos no encontrado: {csv_prototipos}\033[0m")
        return

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    print(f"\033[94m🧠 Clasificando imágenes con prototipos desde: {csv_prototipos}\033[0m")

    # Cargar los vectores promedio (prototipos)
    df_protos = pd.read_csv(csv_prototipos)
    vectores_promedio = {
        int(row["Digito"]): row[[f"P. Cuadrante {i}" for i in range(1, 10)]].values.astype(float)
        for _, row in df_protos.iterrows()
    }

    resultados = []

    # Procesar cada CSV de imágenes por dígito
    for digito in range(10):
        archivo = os.path.join(csv_individuales_path, f"digito_{digito}.csv")
        if not os.path.exists(archivo):
            print(f"\033[93m⚠️ CSV no encontrado para dígito {digito}\033[0m")
            continue

        df = pd.read_csv(archivo)
        total = len(df)

        print(f"\n\033[94m📁 Clasificando {total} imágenes del dígito {digito}...\033[0m")

        for i, (_, row) in enumerate(df.iterrows()):
            # Extraer vector de la imagen actual
            vector = row[[f"P. Cuadrante {i}" for i in range(1, 10)]].values.astype(float)

            # Calcular distancias a cada prototipo
            distancias = {
                protodig: euclidean(vector, v)
                for protodig, v in vectores_promedio.items()
            }

            # Elegir el dígito con menor distancia
            digito_predicho = min(distancias, key=distancias.get)

            # Guardar resultado
            resultados.append(
                [row["Digito"], row["Nombre Imagen"]] +
                list(vector) +
                [digito_predicho]
            )

            # Mostrar progreso
            if (i + 1) % block_size == 0 or (i + 1) == total:
                print(f"\033[92m✔ {i + 1}/{total} clasificadas...\033[0m")

    # Guardar resultados en un DataFrame
    columnas = ["Digito Real", "Nombre Imagen"] + [f"P. Cuadrante {i}" for i in range(1, 10)] + ["Digito Predicho"]
    df_resultado = pd.DataFrame(resultados, columns=columnas)
    df_resultado.to_csv(salida, index=False)

    print(f"\n\033[1;32m✅ Clasificación finalizada. Resultados guardados en: {salida}\033[0m")
    print(f"\033[90m🔢 Total de imágenes clasificadas: {len(df_resultado)}\033[0m")

# Punto de entrada
if __name__ == "__main__":
    clasificador_manual()
