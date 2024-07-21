# Democratizaci-n-de-Datos-Meteorologicos
Proyecto de Hackathon
#  [2024.07.21]	D.N.D
<autores>
Raffaella Martinez
David Bellorin
Mauricio Rojas
Marcell Adams
Elkin Montoya
</autores>
<objetivos>
Este programa tiene como objetivo extraer data de scans de documentos con datos meteorológicos. Fue realizado durante el evento Hackathon CoAfina 2024 por el grupo D.N.D.
</objetivos>

El programa tambien es adaptable para buscar otros textos o caracteres en documentos con distinta precision.

<implementacion>
El programa implementa Tesseract OCR e implementa ideas de John Scanella [1]
Fue probado con las siguientes dependencias:

  pytesseract  0.3.10 
  pdf2image    1.17.0 
  openCV       4.10.0.84 
  Pillow       10.4.0 
  NumPy        2.0.0
	
</implementacion>
<requerimientos>
Es necesario un compilador de C++ 17. El programa escaneará el archivo con el motor Tesseract implementado por Pytesseract, convertirlo en un archivo de texto, busca las coincidencias de éste con un diccionario 

Al correr el programa es necesario especificar el archivo a analizar y el diccionario de palabras a buscar en formato txt: "Palabras.txt". El programa distingue entre mayusculas y minusculas.

El diccionario debe estar escrito en el siguiente formato:

		palabra1 a
		palabra2 b
		palabra3 c
  
y sucesivamente. 'a', 'b', 'c', etc. son los umbrales de precisión, separados de las palabras por un espacio precisamente y sin espacio al final. Dado que no es factible esperar que el OCR traduzca fielmente todas las palabras es posible que "temperatura", se capture como "tempora+ura", por lo tanto es necesario especificar cuantos caracteres se espera que coincidan. Documentos de menor calidad son más probables en resultar en transducciones erroneas pero al mismo tiempo un unbrál muy bajo resultaría en falso positivos que dependiendo de la palabra pueden obviar el objetivo del programa. 

El programa creará un archivo llamado "nombre del archivo"_Resultado.txt con el siguiente formato:

		Archivo: nombre del archivo
		  Palabra: palabra1
		    Fila  Columna
          n1    n2
          n3    n4
  		Palabra:  palabra2
		    Fila   Columna
		      n5     n6   
</requerimientos>

https://medium.com/@blacksmithforlife/better-ocr-for-newspapers-c7c1e2788b7a

## Programa
1) El programa consta de un directorio llamado Proyecto el cual contiene:
- Dos directorios, Program y zchaff.
- Tres archivos bash, Creador, Solver y Automatico.
- Dos archivos de textos, Instancia e InstanciasSudokus.

2) El directorio Program es el que contiene los traductores de Sudoku a CNF (TSB), de CNF a Sudoku (TBS) y el proceso de automatizaciÃ³n.

3) El directorio zchaff es el que contiene el resolvedor de SAT proporcionado por [[1]](https://www.princeton.edu/~chaff/zchaff.html).

4) El bash Creador es el que se encarga de compilar todas las rutinas necesarias, el bash Solver es el que se encarga de reportar la soluciÃ³n. El bash Automatico se encarga de reportar varias soluciones.

5) El archivo de texto Instancia es el que contiene el sudoku a resolver, mientras que el archivo InstanciasSudokus es el que contiene varios sudokus para resolverse de forma automÃ¡tica.
### Instrucciones
1) (Opcional) Cambie los permisos de los archivos bash para que sean ejecutables por el usuario:

		chmod u+x Creador.sh
		chmod u+x Solver.sh
		chmod u+x Automatico.sh

2) Ejecute el archivo Creador.sh.

	

El primer nÃºmero es el orden del sudoku. Seguido de un espacio, se encuentran los nÃºmeros de las casillas del tablero de sudoku separados por guiones, siguiendo el orden de izquierda a derecha y arriba hacia abajo, donde los 0 representan las casillas con espacios vacÃ­os.

chivo Automatico.sh para resolverlos todos: 

		./Automatico.sh

Las soluciones se encontrarÃ¡n en un directorio llamado Soluciones. Adicionalmente, en el directorio llamado Tiempos, encontrara un archivo con el tiempo que tomo resolver cada sudoku.
### Notas
1) El archivo Instancia solo puede contener **un** sudoku a la vez, este tiene que estar en el formato anteriormente mencionado y todo en una sola lÃ­nea. Si desea resolver varios sudokus, siga el paso 6) de las instrucciones.

2) EL programa zchaff usado fue la versiÃ³n de 32-bits, dicho programa **no** puede ser reemplazado por otra versiÃ³n.
