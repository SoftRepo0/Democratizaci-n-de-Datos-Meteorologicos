#include <fstream>
#include <iostream>
#include <string>
#include <map>
#include <memory>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <iomanip>
#include <sys/stat.h>
#include <dirent.h> 
#include <iterator> 
using namespace std; 
using std::left;
using std::setw;
using std::right;

string Leer;
string archivo;
int fila = 1;

class Magnitud{
public:
	string nombre;
	mutable int x = 0;
	int treshold;
};
map<string, Magnitud> magnitudes; 

void Diccionario();
void Busqueda();
void Archivos();

int main(){
	cin >> archivo;
	Diccionario();
	Busqueda();
}

void Diccionario(){
	string Linea;
	string palabra;
	int tresh;
	ifstream input("Palabras.txt");
	while(input >> palabra >> tresh){
		magnitudes.emplace(palabra, Magnitud{});
		magnitudes[palabra].nombre = palabra;
		magnitudes[palabra].treshold = tresh;
	}
}

void Busqueda(){
	ifstream input(archivo);
	struct stat buffer;
	if(stat (archivo.c_str(), &buffer) == -1)
	{
		cout << "No existe " << "\"" << archivo << "\"" << endl;
		sleep(2);
		system("clear");
		exit(0);
	}
	input.close();
	ofstream output(archivo + "_" + "Resultado.txt"); 
	output << "Archivo: "<< archivo << endl; 
	decltype(magnitudes)::iterator it ;
	for(it = magnitudes.begin(); it != magnitudes.end(); ++it){
		ifstream input(archivo);
		output << "\t" << "Palabra: " << it->first << endl;
		output <<  "\t" << "\t" << setw(10) << left << "Fila" << setw(10) << left << "Columna" << endl;
		int i = 0;
		int aciertos = 0;
		fila = 1;
		while(getline(input,Leer)){
			it->second.x = 0;
			while(Leer.size() > 0){
				string copia;
				copia = Leer;
				string word = "";
				for (auto x : copia){
					if (x == ' '){
						break;

					}
					else{
						word = word + x;
					}
				}
				i = 0;
				aciertos = 0;
				while(i < it->second.nombre.size() && i < word.size()){
					if( it->second.nombre[i] == word[i] ){
						aciertos++;
					}
					i++;
				}
				if(aciertos >= it->second.treshold){
					output << "\t" << "\t" << setw(10) << left << fila << setw(10) << left << it->second.x + 1 << endl;
				}
				Leer = Leer.erase(0, word.size() + 1);
				it->second.x += word.size() + 1;
			}
			fila++;
		}
		input.close();
	}	
}
