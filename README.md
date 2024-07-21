# Democraticemos la historia de los datos metereológicos de América Latina
Proyecto de Hackathon CoAfina2024 
# Grupo 7 D.N.D
## Integrantes
- Raffaella Martinez
- David Bellorin
- Mauricio Rojas
- Marcell Adam
- Elkin Montoya

##	Objetivos
Este programa tiene como objetivo extraer data de scans de documentos con datos meteorológicos. Fue realizado durante el evento Hackathon CoAfina 2024 por el grupo D.N.D.

El programa tambien es adaptable para buscar otros textos o caracteres en documentos con distinta precision.


# Visión General del Programa
Se implementan varias herramientas
1. Conversión de PDF a texto: Convierte los PDF de los repositorios de la [Biblioteca Digital de la Casa de las Culturas Ecuatorianas](http://repositorio.casadelacultura.gob.ec/handle/34000/9417) y  [Biblioteca Nacional de Colombia](http://repositorio.casadelacultura.gob.ec/handle/34000/1534). Ofrece un archivo .txt con el texto de las páginas de los PDF. 
2. Identifiación de Palabras y temas clave: A partir de un banco de palabras clave, identifica en qué partes del documento se mencionan las palabras claves y con qué frecuencia, permitiendo recopilar los documentos y las páginas en las que potencialmente se encuentra información relacionada al clima o datos meterológicos. Se incluye un banco de palabras sugeridas para esta aplicación, basándonos en el contenido de los documentos en el repositorio ya mencionado, pero puede ser mejorado para la identifiación relevante a otras disciplinas. 
3. Identifiación de tablas: Conocida(s) la(s) página(s) del documento en donde se encuentra la información de interés, identifica las tablas y obtiene: imagen con la tabla de interés, archivo .txt con el contenido de la tabla, imagen de referencia que permite distinguir si existen errores en las celdas del archivo.txt. Implementando las ideas en [2] y [3] para la identificación de tablas en las imágenes.

   

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
  
y sucesivamente. *'a'* , * 'b' * ,* 'c'* , etc. son los umbrales de precisión, separados de las palabras por **un** espacio *precisamente* y *sin espacios o lineas al final*. Dado que no es factible esperar que el OCR traduzca fielmente todas las palabras es posible que "temperatura", se capture como "temp*o*ra+ura", por lo tanto es necesario especificar cuantos caracteres se espera que coincidan. Documentos de menor calidad son más probables en resultar en transducciones erroneas pero al mismo tiempo un umbrál muy bajo resultaría en falso positivos que, dependiendo de la palabra, pueden obviar el objetivo del programa. 

El programa creará un archivo llamado * "nombre del archivo"_Resultado.txt * con el siguiente formato:

	Archivo: nombre del archivo
		Palabra: palabra1
	    		Fila  Columna
        		n1    n2
       			n3    n4
  		Palabra:  palabra2
			Fila   Columna
			n5     n6   

Donde los números **nx** son las posiciones en el archivo de texto resultante del OCR

Una vez identificadas los pdf con información de interés, utilizar el programa "Extract_Table.py" e indicarle el nombre del pdf con la página de la cual se quiere extraer información. Este devolverá 
1. imagen de la tabla extraída

2. imagen de la tabla extraída en la que se indican las regiones de las cuales se extrajo texto, a fin de poder cotejar si hubo celdas que no se identificaron correctamente

3. archivo con la información de la tabla, en formato separado por comas. 

##	Referencias

[1] https://medium.com/@blacksmithforlife/better-ocr-for-newspapers-c7c1e2788b7a
[2] https://stackoverflow.com/questions/71902322/complete-missing-lines-in-table-opencv
[3] https://medium.com/coinmonks/a-box-detection-algorithm-for-any-image-containing-boxes-756c15d7ed26


### Notas

