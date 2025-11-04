import cv2
import numpy as np
import os
import json

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (1920, 1920))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )
    return img, gray, thresh

def find_circles(gray):
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=60,
        param1=50, param2=30, minRadius=30, maxRadius=50
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles
    return []

def group_circles(circles):
    # Agrupa círculos por filas y columnas usando clustering simple
    circles = sorted(circles, key=lambda c: (c[1], c[0]))  # primero por Y, luego por X
    rows = []
    current_row = []
    last_y = None
    for c in circles:
        if last_y is None or abs(c[1] - last_y) < 50:
            current_row.append(c)
        else:
            rows.append(sorted(current_row, key=lambda x: x[0]))
            current_row = [c]
        last_y = c[1]
    if current_row:
        rows.append(sorted(current_row, key=lambda x: x[0]))
    return rows

def detect_filled(thresh, circles, fill_threshold=0.3):
    filled = []
    for row in circles:
        row_filled = []
        for (x, y, r) in row:
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.circle(mask, (x, y), r-5, 255, -1)
            total = cv2.countNonZero(mask)
            filled_pixels = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
            ratio = filled_pixels / float(total)
            row_filled.append(ratio > fill_threshold)
        filled.append(row_filled)
    return filled

def get_answers(filled, options=['A', 'B', 'C', 'D']):
    answers = []
    for i, row in enumerate(filled):
        try:
            idx = row.index(True)
            answers.append({"question": i+1, "response": options[idx]})
        except ValueError:
            answers.append({"question": i+1, "response": None})
    return answers

def visualize_circles(img, rows, filled, output_path):
    for i, row in enumerate(rows):
        for j, (x, y, r) in enumerate(row):
            color = (0, 255, 0) if filled[i][j] else (0, 0, 255)
            cv2.circle(img, (x, y), r, color, 3)
            cv2.putText(img, f"{chr(65+j)}", (x-10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imwrite(output_path, img)

def detect_answers(image_path, vis_output_path=None):
    img, gray, thresh = preprocess_image(image_path)
    circles = find_circles(gray)
    if len(circles) == 0:
        print(f"No se detectaron círculos en {image_path}.")
        return []
    rows = group_circles(circles)
    filled = detect_filled(thresh, rows, fill_threshold=0.3)
    answers = get_answers(filled)
    if vis_output_path:
        visualize_circles(img.copy(), rows, filled, vis_output_path)
    return answers

if __name__ == "__main__":
    images_dir = os.path.join("dataset", "images")

    outputs_dir = "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for img_name in image_files:
        img_path = os.path.join(images_dir, img_name)
        vis_output_path = os.path.join(outputs_dir, f"vis_{os.path.splitext(img_name)[0]}.png")
        # json_output_path = os.path.join(outputs_dir, f"{os.path.splitext(img_name)[0]}.json")
        answers = detect_answers(img_path, vis_output_path)
        # with open(json_output_path, "w", encoding="utf-8") as f:
        #     json.dump(answers, f, ensure_ascii=False, indent=2)
        print(f"Procesado: {img_name} -> , {vis_output_path}")