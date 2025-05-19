"""
===============================================================================
Proyecto: InkSolver
Archivo: evaluate_equation_results.py
Descripción: Evalúa el desempeño de la clasificación de ecuaciones comparando
             si el resultado calculado es igual al esperado. Calcula métricas
             globales y guarda un resumen en un archivo .txt.
Autor: Alejandro Castro Martínez
Fecha: 2025-05-18
Dependencias: pandas
===============================================================================
"""

import pandas as pd

def evaluar_resultados(path_csv, path_salida_txt="resumen_resultados_ecuaciones.txt"):
    # Cargar el archivo con resultados de ecuaciones
    df = pd.read_csv(path_csv)

    # Verificar columna esperada
    if "Es_Correcta" not in df.columns:
        raise ValueError("La columna 'Es_Correcta' no se encuentra en el archivo CSV.")

    # Cálculo de métricas
    total = len(df)
    correctas = df["Es_Correcta"].sum()
    incorrectas = total - correctas
    accuracy = correctas / total if total > 0 else 0.0

    # Texto del resumen
    resumen = (
        "📊 Evaluación general de resultados de ecuaciones\n"
        "---------------------------------------------------\n"
        f"🔢 Total de ecuaciones evaluadas: {total}\n"
        f"✅ Correctas: {correctas}\n"
        f"❌ Incorrectas: {incorrectas}\n"
        f"🎯 Exactitud global: {accuracy:.2%}\n"
    )

    # Mostrar en consola
    print(resumen)

    # Guardar en archivo .txt
    with open(path_salida_txt, "w", encoding="utf-8") as f:
        f.write(resumen)

    return {
        "total": total,
        "correctas": correctas,
        "incorrectas": incorrectas,
        "accuracy": accuracy
    }

# Ejemplo de ejecución directa
if __name__ == "__main__":
    evaluar_resultados("test_analysis/ecuaciones_clasificadas.csv")
