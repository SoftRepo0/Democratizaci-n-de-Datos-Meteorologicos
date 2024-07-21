import os
from PIL import Image
import pytesseract
import cv2
from pdf2image import convert_from_path
import numpy as np
import math
import glob
import subprocess
from inspect import getsourcefile
from os.path import abspath

pytesseract.pytesseract.tesseract_cmd  =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Convertir pdf's en imagenes

añoIni = 1854;
my_folder = abspath("")
numero = 0
for root, dirs, files in os.walk(my_folder):
    numero += len([fn for fn in files if fn.endswith(".pdf")])
añoFinal = añoIni+math.floor(numero/12.0)
mesesRest = numero % 12
meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']

for año in range(añoIni, añoFinal):
  for mes in range(12):
    filePath = 'bogota_gacetaoficial_{}_{}.pdf'.format(meses[mes],str(año))
    print(filePath)
    doc = convert_from_path(filePath)
    
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)

    # Archivo de texto para guardar el output
    #file = open(".txt", "a")
    #file.write('Lei el archivo de Gaceta del año {}, mes de {} \n'.format(str(año),str(meses[mes])))
    #file.close()
    pPath = 'bogota_gacetaoficial_{}_{}'.format(meses[mes],str(año))
    os.mkdir(pPath)

    for page_number, page_data in enumerate(doc):
      #filePath = 'bogota_gacetaoficial_{}_{}.txt'.format(meses[mes],str(año))
      image = cv2.rotate(np.array(page_data), cv2.ROTATE_90_CLOCKWISE)

      text = pytesseract.image_to_string(page_data,lang="spa")
      text_rot = pytesseract.image_to_string(np.array(image),lang="spa")
      # Guardar texto en documento

      file = open('{}/bogota_gacetaoficial_{}_{}_{}.txt'.format(pPath,meses[mes],str(añoFinal),str(page_number)), "w", encoding='utf-8')
      file.write(text)
      file.close()
      file = open('{}/bogota_gacetaoficial_{}_{}_{}_rot.txt'.format(pPath,meses[mes],str(añoFinal),str(page_number)), "w", encoding='utf-8')
      file.write(text_rot)
      file.close()
      # Close the file
     
      #subprocess.run([r"Hackaton2.exe", "your", "arguments", "comma", "separated"])

for mes in range(mesesRest):
  filePath = 'bogota_gacetaoficial_{}_{}.pdf'.format(meses[mes],str(añoFinal))
  print(filePath)
  doc = convert_from_path(filePath)
  path, fileName = os.path.split(filePath)
  fileBaseName, fileExtension = os.path.splitext(fileName)


  pPath = 'bogota_gacetaoficial_{}_{}'.format(meses[mes],str(añoFinal))
  os.mkdir(pPath)

  for page_number, page_data in enumerate(doc):
    filePath = 'bogota_gacetaoficial_{}_{}_{}.txt'.format(meses[mes],str(añoFinal),str(page_number))
    image = cv2.rotate(np.array(page_data), cv2.ROTATE_90_CLOCKWISE)

    text = pytesseract.image_to_string(page_data,lang="spa")
    text_rot = pytesseract.image_to_string(np.array(image),lang="spa")
    # Guardar texto en documento

    file = open('{}/bogota_gacetaoficial_{}_{}_{}.txt'.format(pPath,meses[mes],str(añoFinal),str(page_number)), "w", encoding='utf-8')
    file.write(text)
    file.close()
    file = open('{}/bogota_gacetaoficial_{}_{}_{}_rot.txt'.format(pPath,meses[mes],str(añoFinal),str(page_number)), "w", encoding='utf-8')
    file.write(text_rot)
    file.close()
    #subprocess.run([r"Hackaton2.exe", "your", "arguments", "comma", "separated"])