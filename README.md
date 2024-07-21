# Democratizaci-n-de-Datos-Meteorologicos
Proyecto de Hackathon
#  [2024.07.21]	D.N.D
##	D.N.D está conformado pro:
Raffaella Martinez

David Bellorin

Mauricio Rojas

Marcell Adam

Elkin Montoya
##	Objetivos
Este programa tiene como objetivo extraer data de scans de documentos con datos meteorológicos. Fue realizado durante el evento Hackathon CoAfina 2024 por el grupo D.N.D.

El programa tambien es adaptable para buscar otros textos o caracteres en documentos con distinta precision.

##	Implementacion
El programa implementa Tesseract OCR y aplica ideas de John Scancella [1]
Fue probado con las siguientes dependencias:

  pytesseract  0.3.10 
  pdf2image    1.17.0 
  openCV       4.10.0.84 
  Pillow       10.4.0 
  NumPy        2.0.0
	
##	Requerimientos
Es necesario un compilador de C++ 17, Tesseract OCR y Pytesseract. El programa escaneará el archivo con el motor Tesseract implementado por Pytesseract, convertirlo en un archivo de texto, busca las coincidencias de éste con un diccionario y escriba un archivo de resultados con una lista de las coincidencias y su posición en el archivo de texto.

### Instrucciones

Al correr el programa es necesario especificar el archivo a analizar y el diccionario de palabras a buscar en formato txt: "Palabras.txt". El programa distingue entre mayusculas y minusculas.

El diccionario debe estar escrito en el siguiente formato:

		palabra1 a
		palabra2 b
		palabra3 c
  
y sucesivamente. 'a', 'b', 'c', etc. son los umbrales de precisión, separados de las palabras por **un** espacio *precisamente* y *sin espacios o lineas al final*. Dado que no es factible esperar que el OCR traduzca fielmente todas las palabras es posible que "temperatura", se capture como "temp*o*ra*+*ura", por lo tanto es necesario especificar cuantos caracteres se espera que coincidan. Documentos de menor calidad son más probables en resultar en transducciones erroneas pero al mismo tiempo un unbrál muy bajo resultaría en falso positivos que dependiendo de la palabra pueden obviar el objetivo del programa. 

El programa creará un archivo llamado "nombre del archivo"_Resultado.txt con el siguiente formato:

	Archivo: nombre del archivo
		Palabra: palabra1
	    		Fila  Columna
        		n1    n2
       			n3    n4
  		Palabra:  palabra2
			Fila   Columna
			n5     n6   

##	Referencias

https://medium.com/@blacksmithforlife/better-ocr-for-newspapers-c7c1e2788b7a

### Notas

