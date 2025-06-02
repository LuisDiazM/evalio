# Procesamiento de la imagen
Dentro de la etapa de procesamiento es necesario transformar la imagen para aplicar un pipeline que inicia con estandarizar la imagen a unas dimensiones establecidas; convertir todo a escala de grises ya que no se necesitan hacer procesamientos por color; hacer una limpieza de ruido por condiciones de iluminación, cámara; el principio de análisis se basa en que la prueba tiene sus opciones de respuesta tipo circulos, entonces intenta encontrar circulos por aproximación HoughCircles pueden existir ovalos, o circulos nor perfectos por ello se aproxima para encontrar todas las opciones de respuesta; con las opciones de respuesta identificadas en sus coordenadas se evalúa si su área corresponde a un umbral de llenado de pixeles; se comparan los circulos que superan el umbral y su posición para determinar la respuesta y generarla en una lista de diccionario.

A continuación se describirá cada etapa del procesamiento para mayor información.

## 1. Redimensionamiento
Estandarizar la imagen a una dimensión fija esto es debido a que en el navegador se está usando la cámara como si fuese una webcam por lo tanto la dimesion no es fija y podría variar.

## 2. Escala de grises
Dado que se iniciará un proceso de OMR (Optical Mark Recognition) la identificación de colores no aplica para este caso de uso por lo tanto convertirla a grises ayudará dentro del proceso y se tendrá unicamente un canal.

## 3. Aplicación de umbral
La aplicación del umbral permite eliminar el ruido y unificar la imagen únicamente a dos colores blanco o negro, sin tonalidades de gris, esto se hace con el fin de tener una imagen más limpia como podemos ver:
![black](/cv-grader-analyzer/docs/umbral.png)

Imagen original

![original](/cv-grader-analyzer/docs/original.jpeg)

## 4. Detección de posibles circulos
La idea es poder detectar las coordenadas de posibles circulos para saber donde están las opciones de respuesta, ya que sabemos que tienen 4 posibles opciones y cada fila de 4 circulos representaría 1 pregunta, la aproximación se realizó usando la transformación [Hough](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)

en nuestra imagen podemos ver lo siguiente con los circulos detectados:

![circulos](/cv-grader-analyzer/docs/circulos.png)

Como se observa no todos los circulos están centrados o tienen el mismo tamaño, pero tienen algo en comun y es que comparten cercanía con las opciones de respuesta.

## 5. Evaluación de circulos rellenos
Como se tienen los circulos detectados se evalúa circulo por circulo si su área tiene pixeles y acá es importante la imagen con el umbral ya que como tenemos posibles valores blanco o negro una respuesta rellena va a tener una densidad de pixeles más grande que una sin contestar donde se aplicará un umbral debido a que dentro de las opciones están las letras A,B,C,D y el sistema podría interpretar esa densidad de pixeles como opción válida por ello el umbral reduce esa probabilidad y podemos obtener la siguiente imagen:

![relleno](/cv-grader-analyzer/docs/respuesta.png)

## 6. Generar respuestas
Con los circulos detectados como rellenos se evalúa la pregunta para saber si es 1, 2, 3, ... con base en las filas y sus posiciones para finalmente traducir la respuesta a una lista de diccionarios donde se identifica el número de pregunta y su respuesta, por ejemplo:
```
[{"question":1, "response":"A"},{"question":2, "response":"B"},{"question":3, "response":"C"},{"question":4, "response":"D"},...]
``` 

El objetivo de la identificación es saber lo que respondió el estudiante, luego el caso de uso evalúa si la respuesta es correcta basado en una plantilla.