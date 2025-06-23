import cv2
import numpy as np
import os

# --- Copia de la función de preprocesamiento y detección de círculos ---
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
    circles = sorted(circles, key=lambda c: (c[1], c[0]))
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

def crop_circle(img, x, y, r, out_size=40):
    # Recorta un cuadrado centrado en (x, y) de tamaño 2*r, y aplica máscara circular
    x1 = max(x - r, 0)
    y1 = max(y - r, 0)
    x2 = min(x + r, img.shape[1])
    y2 = min(y + r, img.shape[0])
    crop = img[y1:y2, x1:x2]
    # Redimensiona a out_size x out_size
    crop = cv2.resize(crop, (out_size, out_size))
    # Aplica máscara circular
    mask = np.zeros((out_size, out_size), dtype=np.uint8)
    cv2.circle(mask, (out_size//2, out_size//2), out_size//2-2, 255, -1)
    crop_bgr = crop.copy()
    for c in range(3):
        crop_bgr[:,:,c] = np.where(mask==255, crop_bgr[:,:,c], 255)
    return crop_bgr

# --- Script de recorte y guardado ---
def crop_and_save_circles(image_path, crops_dir, options=['A', 'B', 'C', 'D']):
    img, gray, thresh = preprocess_image(image_path)
    circles = find_circles(gray)
    if len(circles) == 0:
        print(f"No se detectaron círculos en {image_path}.")
        return 0
    rows = group_circles(circles)
    base = os.path.splitext(os.path.basename(image_path))[0]
    count = 0
    for i, row in enumerate(rows):
        for j, (x, y, r) in enumerate(row):
            crop = crop_circle(img, x, y, r, out_size=40)
            crop_name = f"{base}_q{i+1}_{options[j] if j < len(options) else chr(65+j)}.png"
            crop_path = os.path.join(crops_dir, crop_name)
            cv2.imwrite(crop_path, crop)
            count += 1
    return count

if __name__ == "__main__":
    images_dir = "images"
    crops_dir = "crops"
    os.makedirs(crops_dir, exist_ok=True)
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    total = 0
    for img_name in image_files:
        img_path = os.path.join(images_dir, img_name)
        n = crop_and_save_circles(img_path, crops_dir)
        print(f"Procesado {img_name}: {n} círculos recortados.")
        total += n
    print(f"Total de círculos recortados: {total}") 