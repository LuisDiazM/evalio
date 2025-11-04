import cv2
import numpy as np
from tensorflow import keras
import os

IMG_SIZE = 40
MODEL_PATH = "circle_cnn_model.h5"
model = keras.models.load_model(MODEL_PATH)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {image_path}")
    img = cv2.resize(img, (1920, 1920))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Mejorar contraste con CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    return img, blurred

def find_circles(gray):
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.1, minDist=65,
        param1=50, param2=25, minRadius=30, maxRadius=55
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles
    return []

def find_contour_candidates(thresh, expected_y, y_tol=30):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500 or area > 4000:
            continue
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if abs(y - expected_y) < y_tol:
            candidates.append((int(x), int(y), int(radius)))
    return candidates

def group_circles_force(circles, n_rows=10, n_cols=4, img_shape=(1920,1920), gray=None, thresh=None):
    # Agrupa círculos por filas y columnas, y si faltan, busca candidatos por contorno
    circles = sorted(circles, key=lambda c: (c[1], c[0]))
    rows = []
    height = img_shape[0]
    row_height = height // n_rows
    for i in range(n_rows):
        y_center = int((i + 0.5) * row_height)
        row = [c for c in circles if abs(c[1] - y_center) < row_height//2]
        # Si faltan círculos, busca por contornos
        if len(row) < n_cols and thresh is not None:
            needed = n_cols - len(row)
            contour_cands = find_contour_candidates(thresh, y_center, y_tol=row_height//2)
            # Evita duplicados (por posición x)
            xs = [c[0] for c in row]
            for cand in contour_cands:
                if all(abs(cand[0] - x) > 20 for x in xs):
                    row.append(cand)
                    xs.append(cand[0])
                if len(row) == n_cols:
                    break
        row = sorted(row, key=lambda x: x[0])
        rows.append(row)
    return rows

def crop_circle(img, x, y, r, out_size=40):
    x1 = max(x - r, 0)
    y1 = max(y - r, 0)
    x2 = min(x + r, img.shape[1])
    y2 = min(y + r, img.shape[0])
    crop = img[y1:y2, x1:x2]
    crop = cv2.resize(crop, (out_size, out_size))
    mask = np.zeros((out_size, out_size), dtype=np.uint8)
    cv2.circle(mask, (out_size//2, out_size//2), out_size//2-2, 255, -1)
    crop_bgr = crop.copy()
    for c in range(3):
        crop_bgr[:,:,c] = np.where(mask==255, crop_bgr[:,:,c], 255)
    return crop_bgr

def predict_filled(crop):
    crop = crop.astype("float32") / 255.0
    crop = np.expand_dims(crop, axis=0)
    prob = model.predict(crop, verbose=0)[0][0]
    return prob

def detect_answers(image_path, options=['A', 'B', 'C', 'D'], threshold=0.5, vis_output_path=None, debug_circles_path=None):
    img, gray = preprocess_image(image_path)
    # Para contornos
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    circles = find_circles(gray)
    rows = group_circles_force(circles, n_rows=10, n_cols=4, img_shape=img.shape, gray=gray, thresh=thresh)
    answers = []
    img_vis = img.copy()
    img_debug = img.copy()
    for i, row in enumerate(rows):
        best_prob = 0
        best_option = None
        for j, (x, y, r) in enumerate(row):
            crop = crop_circle(img, x, y, r, out_size=IMG_SIZE)
            prob = predict_filled(crop)
            color = (0, 255, 0) if prob > threshold else (0, 0, 255)
            cv2.circle(img_vis, (x, y), r, color, 3)
            cv2.putText(img_vis, f"{chr(65+j)}", (x-10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            # Azul si viene de HoughCircles, naranja si viene de contorno
            if circles is not None and any(abs(x-c[0])<5 and abs(y-c[1])<5 for c in circles):
                cv2.circle(img_debug, (x, y), r, (255, 0, 0), 2)
            else:
                cv2.circle(img_debug, (x, y), r, (0, 140, 255), 2)
            if prob > threshold and prob > best_prob:
                best_prob = prob
                best_option = options[j] if j < len(options) else chr(65+j)
        answers.append({"question": i+1, "response": best_option})
    if vis_output_path:
        cv2.imwrite(vis_output_path, img_vis)
    if debug_circles_path:
        cv2.imwrite(debug_circles_path, img_debug)
    return answers

if __name__ == "__main__":
    images_dir = os.path.join("dataset", "images")
    outputs_dir = "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for img_name in image_files:
        path = os.path.join(images_dir, img_name)
        vis_output_path = os.path.join(outputs_dir, f"vis_{os.path.splitext(img_name)[0]}.png")
        debug_circles_path = os.path.join(outputs_dir, f"debug_circles_{os.path.splitext(img_name)[0]}.png")
        answers = detect_answers(path, vis_output_path=vis_output_path, debug_circles_path=None)
        print(f"{img_name}: {answers}")
    
    # path = os.path.join(images_dir, image_files[0])
    # anwsers = detect_answers(path, vis_output_path="output.png", debug_circles_path="debug.png")
