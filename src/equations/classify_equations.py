import os
import cv2
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean

# =============================================================================
# CONFIGURACIÓN DE RUTAS
# =============================================================================

eq_base_folder = "../../data/equations/processed/"
prototipos_csv = "classify_digits/promedios_por_digito.csv"
output_csv = "test_analysis/ecuaciones_clasificadas.csv"

# =============================================================================
# FUNCIONES PARA CLASIFICACIÓN DE OPERANDOS
# =============================================================================

def cargar_vectores_promedio(csv_path):
    df = pd.read_csv(csv_path)
    return {
        int(row["Digito"]): row[[f"P. Cuadrante {i}" for i in range(1, 10)]].values.astype(float)
        for _, row in df.iterrows()
    }

def calcular_vector_tinta(img, size=(3, 3)):
    h, w = img.shape
    dh, dw = h // size[0], w // size[1]
    vector = []
    for i in range(size[0]):
        for j in range(size[1]):
            block = img[i*dh:(i+1)*dh, j*dw:(j+1)*dw]
            tinta = np.count_nonzero(block < 128)
            vector.append(tinta)
    return np.array(vector, dtype=float)

def clasificar_operando(img, vectores_promedio):
    vector = calcular_vector_tinta(img)
    distancias = {d: euclidean(vector, prototipo) for d, prototipo in vectores_promedio.items()}
    return min(distancias, key=distancias.get)

# =============================================================================
# FUNCIONES PARA CLASIFICACIÓN DE OPERADORES
# =============================================================================

def compute_projection_histogram(img, axis=0):
    return np.sum(img, axis=axis)

def count_peaks(hist, threshold=0.5):
    if np.max(hist) == 0:
        return 0
    normalized_hist = hist / np.max(hist)
    peaks = 0
    in_peak = False
    for value in normalized_hist:
        if value < threshold and not in_peak:
            peaks += 1
            in_peak = True
        elif value >= threshold:
            in_peak = False
    return peaks

def rotate_image_45(img):
    h, w = img.shape
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
    cos, sin = np.abs(matrix[0, 0]), np.abs(matrix[0, 1])
    new_w, new_h = int(h * sin + w * cos), int(h * cos + w * sin)
    matrix[0, 2] += (new_w / 2) - center[0]
    matrix[1, 2] += (new_h / 2) - center[1]
    rotated = cv2.warpAffine(img, matrix, (new_w, new_h), borderValue=255)
    _, thresh = cv2.threshold(rotated, 250, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)
    return rotated[y:y+h, x:x+w]

def clasificar_operador(img):
    h_proj = compute_projection_histogram(img, axis=1)
    v_proj = compute_projection_histogram(img, axis=0)
    h_peaks = count_peaks(h_proj, 0.8)
    v_peaks = count_peaks(v_proj, 0.8)

    rotated = rotate_image_45(img)
    h_proj_rot = compute_projection_histogram(rotated, axis=1)
    h_peaks_rot = count_peaks(h_proj_rot, 0.8)

    if h_peaks == 0 and v_peaks == 0 and (h_peaks_rot > 2 or h_peaks_rot == 0):
        return "div"
    elif h_peaks == 2 and v_peaks == 0:
        return "equals"
    elif h_peaks == 1 and v_peaks == 0:
        return "sub"
    elif h_peaks == 1 and v_peaks == 1:
        return "sum"
    elif h_peaks == 0 and v_peaks == 0 and h_peaks_rot <= 2:
        return "times"
    else:
        return "Desconocido"

# =============================================================================
# EVALUADOR DE OPERACIÓN
# =============================================================================

def evaluar_operacion(op1, op2, operador):
    try:
        if operador == "sum":
            return op1 + op2
        elif operador == "sub":
            return op1 - op2
        elif operador == "times":
            return op1 * op2
        elif operador == "div":
            return op1 // op2 if op2 != 0 else None
        else:
            return None
    except Exception:
        return None

# =============================================================================
# PROCESAMIENTO GENERAL
# =============================================================================

def procesar_todas_las_ecuaciones():
    print("🔎 Cargando vectores promedio de operandos...")
    vectores_prom = cargar_vectores_promedio(prototipos_csv)
    resultados = []

    total_eq = 0

    for resultado in sorted(os.listdir(eq_base_folder)):
        resultado_path = os.path.join(eq_base_folder, resultado)
        if not os.path.isdir(resultado_path):
            continue

        print(f"\n📁 Procesando ecuaciones con resultado esperado = {resultado}")

        for imagen_id in sorted(os.listdir(resultado_path)):
            imagen_path = os.path.join(resultado_path, imagen_id)

            for eq_folder in sorted(os.listdir(imagen_path)):
                eq_path = os.path.join(imagen_path, eq_folder)
                eq_id = f"{resultado}_{imagen_id}_{eq_folder}"
                total_eq += 1

                print(f"🔧 Clasificando {eq_id}...")

                try:
                    op1_img = cv2.imread(os.path.join(eq_path, "0.png"), cv2.IMREAD_GRAYSCALE)
                    oper_img = cv2.imread(os.path.join(eq_path, "1.png"), cv2.IMREAD_GRAYSCALE)
                    op2_img = cv2.imread(os.path.join(eq_path, "2.png"), cv2.IMREAD_GRAYSCALE)

                    if op1_img is None or oper_img is None or op2_img is None:
                        print(f"⚠️ Archivos faltantes en {eq_id}, se omite.")
                        continue

                    op1 = clasificar_operando(op1_img, vectores_prom)
                    operador = clasificar_operador(oper_img)
                    op2 = clasificar_operando(op2_img, vectores_prom)
                    resultado_esperado = int(resultado)
                    resultado_calculado = evaluar_operacion(op1, op2, operador)
                    es_correcta = resultado_calculado == resultado_esperado

                    resultados.append([
                        eq_id, op1, operador, op2,
                        resultado_esperado, resultado_calculado, es_correcta
                    ])

                except Exception as e:
                    print(f"❌ Error en {eq_id}: {e}")
                    continue

    df = pd.DataFrame(
        resultados,
        columns=[
            "Eq_ID", "Operando_1", "Operador", "Operando_2",
            "Resultado_Esperado", "Resultado_Calculado", "Es_Correcta"
        ]
    )

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"\n✅ Proceso completado. Resultados guardados en: {output_csv}")
    print(f"🔢 Total de ecuaciones procesadas: {len(df)}")

# =============================================================================
# EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    procesar_todas_las_ecuaciones()
