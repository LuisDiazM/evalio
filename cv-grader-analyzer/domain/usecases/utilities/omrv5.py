import cv2
import numpy as np
import os

THRESHOLD_UMBRAL = 0.6

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("No se pudo cargar la imagen.")
    img_resize = cv2.resize(image, (720, 720))  # Mantener tamaño ajustado
    gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 121, 10)
    return img_resize, gray, thresh

def find_circles(gray):
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=0.5, minDist=32,  # minDist para evitar circulos muy cercanos
                               param1=30, param2=15,  # Reducidos para mayor sensibilidad
                               minRadius=8, maxRadius=13)  # Para que no ponga circulos muy grandes
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles 
    else:
        print("No se detectaron círculos con HoughCircles.")
        return []

def find_filled_circles(circles, thresh):
    filled_circles = []
    for (x, y, r) in circles:
        mask = np.zeros_like(thresh)
        cv2.circle(mask, (int(x), int(y)), int(r), (255,255,255), -1)  # Usar 255 para blanco
        roi = cv2.bitwise_and(thresh, mask)
        white_pixels = cv2.countNonZero(roi)
        total_pixels = cv2.countNonZero(mask)
        proportion = white_pixels / total_pixels if total_pixels > 0 else 0
        if proportion >THRESHOLD_UMBRAL:  # Umbral más bajo
            filled_circles.append((x, y, r))
    return filled_circles

def group_questions(circles):
    centers = [(x, y) for x, y, r in circles]
    centers.sort(key=lambda c: c[1])  # Ordenar por Y
    rows = []
    current_row = []
    previous_y = None
    for center in centers:
        x, y = center
        if previous_y is None or abs(y - previous_y) < 40:
            current_row.append(center)
        else:
            current_row.sort(key=lambda r: r[0])  # Ordenar por X
            rows.append(current_row)
            current_row = [center]
        previous_y = y
    if current_row:
        current_row.sort(key=lambda r: r[0])
        rows.append(current_row)
    return rows

def calculate_question_response(filled_circle, rows):
    x, y, _ = filled_circle
    columns = ["A", "B", "C", "D"]
    for row_index, row in enumerate(rows, start=1):
        for column_index, column in enumerate(row):
            x_column, y_column = column
            distance = np.sqrt((x - x_column)**2 + (y - y_column)**2)
            if distance <= 20:  # Tolerancia aumentada
                return {"question": row_index, "response": columns[column_index]}
    return None

def grade_exam(image_path, output_prefix):
    try:
        image, gray, thresh = preprocess_image(image_path)
        circles = find_circles(gray)
        if circles is not None:
            # for (x, y, r) in circles:
            #     cv2.circle(image, (x, y), r, (0, 0, 255), 2)
            filled_circles = find_filled_circles(circles, thresh)
            rows = group_questions(circles)
            responses = []
            for c in filled_circles:
                response = calculate_question_response(c, rows)
                if response:
                    responses.append(response)
            for (x, y, r) in filled_circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)  # Círculos rellenos en verde
        
            output = os.path.join(os.path.dirname(image_path), f"{output_prefix}_resultado.png")
            cv2.imshow("circiles",image)
            cv2.imshow("thresh", thresh)
            cv2.waitKey(0)
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