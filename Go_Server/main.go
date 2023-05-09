package main


//Importacion de las dependencias necesarias

import (
	"encoding/json"
	"log"
	"net/http"
	"github.com/gorilla/mux"
	"github.com/gorilla/handlers"
)

//Objeto donde almacenaremos la respuesta del endpoint
type Objeto struct{
	Icon_Url string `json:"icon_url"`
	ID    string `json:"id"`
	URL   string `json:"url"`
	Value string `json:"value"`
}


//Constante del endpoint de donde obtendremos los objetos
const ENDPOINT string = "https://api.chucknorris.io/jokes/random"


//Endpoint root de prueba para verificar que la api corra correctamente
func root(w http.ResponseWriter, r *http.Request){

	json.NewEncoder(w).Encode("Listening on port 3000")
}

//Funcion auxiliar para la verificación de la existencia del objeto para que no se repita
func exists(Objetos []Objeto, objeto Objeto) bool {
	for _, i := range Objetos {
		if i.ID == objeto.ID {
			return true
		}
	}
	return false
}

//Endpoint tipo get para la obtención de objetos
func getObjects(w http.ResponseWriter, r *http.Request){

	//Arreglo de tipo Objeto para almacenar los 25 objetos a obtener
	Objetos := []Objeto{}

	//Iteracion para obtener los 25 objetos que contendrá el arreglo
	for len(Objetos) < 25 {

		//#Objeto recivido por el enpoint anteriormente declarado
		response, err := http.Get(ENDPOINT)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		//Cerramos el body
		defer response.Body.Close()

		//Declaramos la variable donde será almacenado el objeto
		var objeto Objeto
		
		/*Obtenemos el objeto y lo almacenamos en la variable antes declarada
		y nos aseguramos que no haya ningun error en el proceso*/
		if err := json.NewDecoder(response.Body).Decode(&objeto); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		//Verificamos la existencia del objeto dentro del arreglo Objetos
		if !exists(Objetos, objeto) {
			//Aqui se agrega el nuevo objeto al arreglo
			Objetos = append(Objetos, objeto)
		}
	}
	json.NewEncoder(w).Encode(Objetos)
}

func main(){

	router := mux.NewRouter()
	
	router.HandleFunc("/", root).Methods("GET")
	router.HandleFunc("/getObjects", getObjects).Methods("GET")
	log.Fatal(http.ListenAndServe(":3000", handlers.CORS(handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"}),
	 handlers.AllowedMethods([]string{"GET", "POST", "PUT", "HEAD", "OPTIONS"}), handlers.AllowedOrigins([]string{"*"}))(router)))
}