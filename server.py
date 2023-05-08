from flask import Flask, make_response
from waitress import serve
import requests


#la api está hecha con flask
app = Flask(__name__)

#constante del enpoint donde obtendremos los objetos
ENDPOINT = 'https://api.chucknorris.io/jokes/random'


#Endpoint root de prueba para verificar que la api corra correctamente
@app.route('/', methods = {'GET'})
def root():
    #Retornamos una etiqueta html para la verificación 
    return '<h1>Listening on port 3000</h1>'


#Endpoint tipo get para la obtención de objetos
@app.route('/getObjects', methods= {'GET'})
def getObjects():
    #Arreglo donde almacenaremos los 25 objetos
    objects = []

    #Loop para iterar hasta que el arreglo objetos tenga una dimension de 25
    while len(objects) < 25:

        #Objeto recivido por el enpoint anteriormente declarado
        object_received = requests.get(ENDPOINT)
    
        #object_received en formato JSON
        json_object = object_received.json()
        
        #Condición para que sea un objeto no existente dentro del arreglo 
        if json_object not in objects:
            #Se agrega un objeto mas al arreglo
            objects.append(json_object)

    #Se establece la respuesta que envieremos con el codigo de ok
    response = make_response(objects, 200)

    return response


if __name__ == '__main__':
    serve(app, host = '0.0.0.0', port = 3000)