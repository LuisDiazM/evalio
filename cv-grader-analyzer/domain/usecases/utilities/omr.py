import cv2
import numpy as np
import os


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    img_resize = cv2.resize(image, (540, 720))

    gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 121, 10)
    return img_resize, thresh

def detect_edges(thresh):
    edges = cv2.Canny(thresh, 120, 10)
    return edges

def find_option_contours(edges):
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    option_contours = []
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        # Calcular el perímetro
        perimeter = cv2.arcLength(contour, True)
        # Aproximar el contorno a un polígono
        approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
        # Si tiene muchos lados (más de 8), asumimos que es un círculo
        if cv2.contourArea(contour) > 300: # este valor se debe ajustar
            if len(approx) >= 4:
                option_contours.append(contour)

    return option_contours


def find_contours_filled(option_contours, thresh):
    contours_filled = []
    for contour in option_contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = thresh[y:y+h, x:x+w]
        intensidad_media = cv2.mean(roi)[0]
        if intensidad_media > 100:
            contours_filled.append(contour)
    return contours_filled


def group_questions(contours):
    """
    Obtiene las coordenadas de los circulos agrupados por filas
    """
    circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # se debe ajustar esta area
            (x, y), radius = cv2.minEnclosingCircle(contour)
            # Verificar si el contorno es un círculo (comparar área real vs. área del círculo)
            if abs(1 - (area / (np.pi * radius ** 2))) < 0.3:
                circles.append((int(x), int(y)))

    circles.sort(key=lambda c: c[1])  # Ordenar por coordenada Y
    rows = []
    current_row = []
    previous_y = None
    for circle in circles:
        x, y = circle
        # Ajusta el umbral según el espaciado
        if previous_y is None or abs(y - previous_y) < 50:
            current_row.append(circle)
        else:
            current_row.sort(key=lambda r: r[0])
            rows.append(current_row)
            current_row = [circle]
        previous_y = y
    if current_row:  # Agregar la última fila
        current_row.sort(key=lambda r: r[0])
        rows.append(current_row)
    return rows


def calculate_question_response(contour, rows):
    (x, y), _ = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    columns = ["A", "B", "C", "D", "E"] # se debe ajustar ya que son 4 opciones de respuesta

    for row_index, row in enumerate(rows, start=1):
        for column_index, column in enumerate(row):
            x_center, y_center = center
            x_column, y_column = column
            distance = abs(x_center - x_column) + abs(y_center - y_column)
            if distance <= 5:
                return {"question": row_index, "response": columns[column_index], "center": center}


# 7. Función principal
def grade_exam(image_path, output_prefix) -> dict:
    try:
        image, thresh = preprocess_image(image_path)
        edges = detect_edges(thresh)
        option_contours = find_option_contours(edges)
        contours_filled = find_contours_filled(option_contours, thresh)
        rows = group_questions(option_contours)
        responses = []
        for c in contours_filled:
            response = calculate_question_response(c, rows)
            if response is not None:
                responses.append(response)
        cv2.drawContours(image, contours_filled, -1, (0, 255, 0), 2)

        for res in responses:
            cv2.putText(image, f"{res.get('question')}", (res.get("center")[
                        0]-50, res.get("center")[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, f"{res.get('response')}", (res.get("center")[
                        0]-30, res.get("center")[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        output = os.path.join(
            os.path.dirname(image_path), f"{output_prefix}_result.png")
        cv2.imwrite(output, image)
        return {"responses": responses, "output": output}
    except Exception:
        return {}


# Ejecutar el programa
if __name__ == "__main__":
    path = os.path.join("./", "images", "test_04.png")

    grade_exam(path,"output")
