import cv2
import numpy as np
import os

THRESHOLD_UMBRAL = 0.6
def correct_perspective(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Encuentra el contorno más grande con 4 lados (el hoja de respuestas)
    max_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.1 * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)
    
    if len(approx) == 4:  # Asegura que sea un cuadrilátero
        corners = approx.reshape(4, 2).astype(np.float32)
        # Ordena las esquinas: top-left, top-right, bottom-right, bottom-left
        rect = np.zeros((4, 2), dtype="float32")
        s = corners.sum(axis=1)
        rect[0] = corners[np.argmin(s)]  # top-left
        rect[2] = corners[np.argmax(s)]  # bottom-right
        diff = np.diff(corners, axis=1)
        rect[1] = corners[np.argmin(diff)]  # top-right
        rect[3] = corners[np.argmax(diff)]  # bottom-left
        
        # Define las dimensiones deseadas (e.g., 1000x1000)
        dst_pts = np.array([[0, 0], [999, 0], [999, 999], [0, 999]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst_pts)
        corrected = cv2.warpPerspective(image, M, (1000, 1000))
        return corrected
    else:
        raise Exception("No se pudo detectar el hoja de respuestas con 4 esquinas.")
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("No se pudo cargar la imagen.")
    corrected_image = correct_perspective(image)
    img_resize = cv2.resize(corrected_image, (1000, 1000))  # Tamaño estándar más grande
    gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return img_resize, gray, thresh

def find_circles(gray):
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
                               param1=50, param2=20, minRadius=10, maxRadius=25)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # Filtra círculos por tamaño predominante
        radii = circles[:, 2]
        median_radius = np.median(radii)
        filtered_circles = [c for c in circles if abs(c[2] - median_radius) <= 3]
        return filtered_circles
    else:
        print("No se detectaron círculos con HoughCircles.")
        return []


def find_filled_circles(circles, thresh):
    proportions = []
    for (x, y, r) in circles:
        mask = np.zeros_like(thresh)
        cv2.circle(mask, (x, y), r, (255,0,0), -1)
        roi = cv2.bitwise_and(thresh, mask)
        white_pixels = cv2.countNonZero(roi)
        total_pixels = cv2.countNonZero(mask)
        proportion = white_pixels / total_pixels if total_pixels > 0 else 0
        proportions.append((x, y, r, proportion))

def group_questions(circles):
    if not circles:
        return []
    centers = [(x, y, r) for x, y, r in circles]
    centers.sort(key=lambda c: c[1])  # Ordenar por Y
    
    # Agrupar en filas
    rows = []
    current_row = []
    previous_y = None
    for center in centers:
        x, y, r = center
        if previous_y is None or abs(y - previous_y) < 50:  # Tolerancia aumentada
            current_row.append((x, y, r))
        else:
            rows.append(current_row)
            current_row = [(x, y, r)]
        previous_y = y
    if current_row:
        rows.append(current_row)
    
    # Asignar columnas (A, B, C, D)
    column_positions = []
    for row in rows:
        x_coords = sorted([x for x, _, _ in row])
        if len(x_coords) == 4:  # Solo filas completas
            column_positions.append(x_coords)
    if column_positions:
        avg_column_positions = np.mean(column_positions, axis=0)
    else:
        avg_column_positions = None
    
    grouped_rows = []
    for row in rows:
        row.sort(key=lambda r: r[0])  # Ordenar por X
        if avg_column_positions is not None:
            assigned_row = []
            for x, y, r in row:
                # Asigna a la columna más cercana
                col_idx = np.argmin([abs(x - pos) for pos in avg_column_positions])
                assigned_row.append((x, y, r, col_idx))
            grouped_rows.append(assigned_row)
        else:
            grouped_rows.append([(x, y, r, i) for i, (x, y, r) in enumerate(row)])
    
    return grouped_rows

def calculate_question_response(rows_with_proportions):
    responses = []
    columns = ["A", "B", "C", "D"]
    for row_index, row in enumerate(rows_with_proportions, start=1):
        # Obtener proporciones de llenado
        proportions = [(x, y, r, prop, col_idx) for x, y, r, col_idx, prop in row]
        if len(proportions) != 4:
            print(f"Pregunta {row_index}: Número incorrecto de círculos ({len(proportions)}).")
            continue
        
        # Encontrar la proporción máxima y la segunda mayor
        sorted_props = sorted(proportions, key=lambda p: p[4], reverse=True)
        p_max, p_second = sorted_props[0][4], sorted_props[1][4]
        
        # Criterios para seleccionar respuesta
        if p_max > 0.4 and (p_max - p_second) > 0.2:
            x, y, r, prop, col_idx = sorted_props[0]
            responses.append({"question": row_index, "response": columns[col_idx]})
        else:
            print(f"Pregunta {row_index}: Respuesta incierta (p_max={p_max}, p_second={p_second}).")
    return responses

def grade_exam(image_path, output_prefix):
    try:
        image, gray, thresh = preprocess_image(image_path)
        circles = find_circles(gray)
        if circles:
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 0, 255), 2)  # Círculos en rojo
            circles_with_proportions = find_filled_circles(circles, thresh)
            rows = group_questions(circles)
            # Asocia proporciones a las filas
            rows_with_proportions = []
            for row in rows:
                row_with_props = []
                for x, y, r, col_idx in row:
                    for cx, cy, cr, prop in circles_with_proportions:
                        if np.sqrt((x - cx)**2 + (y - cy)**2) < 10:
                            row_with_props.append((x, y, r, col_idx, prop))
                            break
                rows_with_proportions.append(row_with_props)
            
            responses = calculate_question_response(rows_with_proportions)
            for response in responses:
                q, r = response["question"], response["response"]
                col_idx = ["A", "B", "C", "D"].index(r)
                for x, y, r, idx, prop in rows_with_proportions[q-1]:
                    if idx == col_idx:
                        cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Círculos llenos en verde
            
            output = os.path.join(os.path.dirname(image_path), f"{output_prefix}_resultado.png")
            cv2.imwrite(output, image)
            return {"responses": responses, "output": output}
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    path = os.path.join("./", "images", "exam-6840373eb4a896fcb04dcabe-1102518280.jpeg")
    result = grade_exam(path, "output")
    print("Respuestas detectadas:", result.get("responses", []))