import cv2
import os
from imutils.perspective import four_point_transform


path = os.path.join("./", "images", "IMG_20250316_165910.jpg")

image = cv2.imread(path)
print(image.shape)
img_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img_gray_resize = cv2.resize(img_grayscale, (540, 720))
img_resize = cv2.resize(image, (540, 720))

# ret, thresh1 = cv2.threshold(img_gray_resize, 150, 255, cv2.THRESH_BINARY)
thresh2 = cv2.adaptiveThreshold(
    img_gray_resize, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 121, 10)

edges = cv2.Canny(thresh2, 120, 10)
cnts, hierarchy = cv2.findContours(
    edges, cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)
docCnt = None

contours = sorted(cnts, key=cv2.contourArea, reverse=True)
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1 * peri, True)
    if cv2.contourArea(c) > 300:
        if len(approx) == 4:
            cv2.drawContours(img_resize, c, -1, (0,255,0))





cv2.imshow("thresh", thresh2)
cv2.imshow("edges", edges)
cv2.imshow("resize", img_resize)
cv2.waitKey(0)
