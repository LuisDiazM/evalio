# Conceptos clave

## Input/Output

Una imagen es una matriz (x,y,z) donde la profundidad son los canales
BGR, RGB, GrayScale: comercialmente son 3 canales más de tres canales
son multiespectrales que capturan información más allá del espectro

se representan mediante un objeto de numpy que en realidad es una matriz

```
path = os.path.join("./","images","galaxy.webp")
image = cv2.imread(path)
```

## Redimensionar
- Se puede aplicar un resize que mantiene la escencia de la imagen
```image_rez = cv2.resize(image, (700, 520))```
- Se puede cortar la imagen por posiciones x,y como manejo de matrices
```image[580:750,580:750]``` 


## Colores

con opencv se puede cambiar la escala por ejemplo de RGB a BGR, a escala de grises, estas transformaciones pueden impactar las dimensiones (z) por ejemplo, en escala de grises solo hay 1 canal
```
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

## Blurring
Concepto para remover ruido de imagenes, sin embargo, degrada la imagen porque toma regiones de pixeles y aplica promedios, existen diferentes funciones matemáticas:
- GaussianBlur
- blur

Entre más grande la región de pixeles la imagen va a ser más borrosa.


## Threshold
Aplica un limite a la imagen si supera ciertos valores le coloca un valor máximo.
Existen diferentes métodos simple y adaptativo.
El simple es por comparación y el adaptativo para aplicaciones donde las condiciones de ilumnación varían a lo largo de la imagen, tiene sus complejidad computacional por las operaciones matemáticas que realiza. 
https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html