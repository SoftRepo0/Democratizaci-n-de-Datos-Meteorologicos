# Probando con aislar tablas una vez identificada la pagina de interes-
import sys
import os
from PIL import Image
import pytesseract
import cv2
from pdf2image import convert_from_path
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Convertir pdf's en imagenes
filePath = input("Ingrese el nombre del archivo \n") #pedimos el nombre del archivo a revisar al correr el archivo

doc = convert_from_path(filePath)
#img = np.array(doc[0])
path, fileName = os.path.split(filePath)
fileBaseName, fileExtension = os.path.splitext(fileName)



for page_number, page_data in enumerate(doc):

	### Comenzamos identificando las tablas en la pagina##

	#escala de grises
	gray = cv2.cvtColor(np.array(page_data), cv2.COLOR_BGR2GRAY) #se coloca en escalas de grises

	# Threshold e inversion
	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

	# Aplicamos filtros de cv2 para indentificar lineas verticales y horizontales. Esto lo hacemos con los kernel
	# Defining a kernel lengt
	kernel_length = np.array(thresh1).shape[1]//80
	 
	# lineas verticales
	verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
	# lineas horizontales
	hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
	# A kernel of (3 X 3) ones.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	# Morphological operation to detect vertical lines from an image
	img_temp1 = cv2.erode(thresh1, verticle_kernel, iterations=2)
	verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=5)
	#cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
	# Morphological operation to detect horizontal lines from an image
	img_temp2 = cv2.erode(thresh1, hori_kernel, iterations=2)
	horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=5)
	#cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

	#unimos lineas verticales y horizontales
	# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
	#img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
	img_final_bin = cv2.add(horizontal_lines_img,verticle_lines_img)
	#img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=1)
	thresh, img_final_bin = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	#cv2.imwrite("img_final_bin.jpg",img_final_bin)

	#mascara de las lineas obtenidas

	h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
	# contains only the horizontal lines
	h_mask = cv2.morphologyEx(horizontal_lines_img, cv2.MORPH_OPEN, h_kernel, iterations=1)

	# performing repeated iterations to join lines
	h_mask = cv2.dilate(h_mask, h_kernel, iterations=7)

	v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
	v_mask = cv2.morphologyEx(verticle_lines_img, cv2.MORPH_OPEN, v_kernel, iterations=1)
	v_mask =  cv2.dilate(v_mask, v_kernel, iterations=1)

	joined_lines = cv2.bitwise_or(v_mask, h_mask)
	#cv2.imwrite("joined_lines.jpg",joined_lines)


	#Buscamos el mayor recuadro (para conseguir la tabla completa)

	contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	c = max(contours, key = cv2.contourArea)           # contour with largest area
	black = np.zeros((img_final_bin.shape[0], img_final_bin.shape[1]), np.uint8)
	mask = cv2.drawContours(black, [c], 0, 255, -1)    # --> -1 to fill the contour

	fin = cv2.bitwise_and(joined_lines, joined_lines, mask = mask)
	#identificamos celdas utilizando esto



	#aislamos la tabla del resto de la pagina
	im=thresh1.copy()
	x, y, w, h = cv2.boundingRect(c)
	isolated = im[y:y + h, x:x + w]
	fin=fin[y:y + h, x:x + w]
	imagename = "Tabla.jpg"
	cv2.imwrite("Tabla.jpg",255-isolated)
	#cv2.imwrite("fin.jpg",fin)

	### A partir de aca utilizamos cv2 para limpiar la imagen y poder extraer la informacion de las celdas##
	#Quitamos los bordes de la tabla
	tt =  cv2.subtract(isolated,fin) 
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
	tt = cv2.erode(tt, kernel, iterations=1)
	tt = cv2.dilate(tt, kernel, iterations=1)

	#cv2.imwrite("tt.jpg",tt)
	#Mas grande a ver si lee mejor
	bigger=cv2.resize(tt, (0,0), fx=2, fy=2)
	#Identificamos los contornos para separar las celdas
	contours, hierarchy = cv2.findContours(cv2.resize(fin, (0,0), fx=2, fy=2), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#bigger = cv2.threshold(bigger, 128, 255, cv2.THRESH_BINARY)[1]
	#cv2.imwrite("bigger.jpg",bigger)
	
	
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	
	#identificamos los bloques de texto en la imagen

	dilated_image = cv2.dilate(bigger, rect_kernel, iterations=5)
	simple_kernel = np.ones((5,5), np.uint8)
	dilated_image = cv2.dilate(bigger, simple_kernel, iterations=2)
	#cv2.imwrite("dilated_image.jpg",dilated_image)
	contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	bigger=255-bigger
	#sharp = cv2.Laplacian(bigger,cv2.CV_64F) #filtro para mejorar los bordes
	#cv2.imwrite("work.jpg",bigger)

	image_with_contours_drawn = bigger.copy()
	
	cnt_list = []
	heights = []
	#cmin = min(contours, key = cv2.contourArea) #identificar las cajas con menor area (que probablemente sean ruido)
	mx, ym, wm, hm = cv2.boundingRect(c)
	#print(minarea)
	for contour in contours:
		x, y, w, h = cv2.boundingRect(contour)
		#heights.append(h) #encontraremos la altura promeido de los recuadros
		cropped = bigger[y:y + h, x:x + w]
		#descartamos los cuadros del ancho o largo de la tabla, para tener solo las celdas
		#considerar combinar con las celdas de la tabla encontradas a partir de las lineas
		if w<2*wm and h<2*hm:
			text = pytesseract.image_to_string(cropped, lang='spa')
			text = text.replace("\n", " ")
			cnt_list.append([x,y,h,text])
			rect = cv2.rectangle(image_with_contours_drawn, (x, y), (x + w, y + h), (0, 255, 0), 5)
			cv2.circle(image_with_contours_drawn,(x,y),8,(255,255,0),8)
			#mean_height = np.mean(heights)
	cv2.imwrite("contornos detectados.jpg",image_with_contours_drawn)

	
	sorted_list = sorted(cnt_list, key=lambda x: x[1]) #ordenamos los recuadros en Y

	#ordenamos por filas para escribir los datos en formato csv
	#agrupamos por filas
	rows=[]
	this_row=[cnt_list[0]]
	for cnt in sorted_list:
		if abs(cnt[1] - this_row[0][1])<cnt[2]: #si la separacion en y de las celdas es menor que su altura
			this_row.append(cnt)
		else: #si la separacion es mayor que la altura, estamos en una fila diferente
			rows.append(this_row) #agrego las celdas de la fila hasta ahora
			this_row=[cnt]
	rows.append(this_row)



	for row in rows:
		row.sort(key=lambda x: x[0]) #ordenaos de izquierda a derecha cada fila

	#archivo csv
	# Archivo de texto para guardar el output de cada pagina
	file = open("Tabla.txt", "w")
	for row in rows:
		for item in row:
			if item[3]!="": #no imprimimos las celdas vacias
				file.write(item[3] + ' , ')
		file.write("\n")
	file.close()

print("Los datos han sido democratizados :) \n")








