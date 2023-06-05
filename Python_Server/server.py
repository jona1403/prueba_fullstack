from flask import Flask, make_response
from waitress import serve
import requests
import concurrent.futures

#la api está hecha con flask
app = Flask(__name__)

#constante del enpoint donde obtendremos los objetos
ENDPOINT = 'https://api.chucknorris.io/jokes/random'

#Funcion auxiliar para la verificacion de la existencia del objeto por el id
def exists(objects, obj):
    #Iteracion del arreglo
    for object in objects:
        #Condicion de existencia del objeto por el ID
        if object["id"] == obj["id"]:
            #Doble chequeo al encontrar un objeto con el mimos ID
            for ob in objects:
                if ob["id"] == obj["id"]:
                    return True
    return False

#Endpoint root de prueba para verificar que la api corra correctamente
@app.route('/', methods = {'GET'})
def root():
    #Retornamos una etiqueta html para la verificación 
    return '<h1>Listening on port 3000</h1>'


# Función para obtener un objeto a partir de una URL
def peticionObjeto(url):
    response = requests.get(url)
    return response.json()


#Endpoint tipo get para la obtención de objetos
@app.route('/getObjects', methods= {'GET'})
def getObjects():
    #Arreglo donde almacenaremos los 25 objetos
    objects = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while len(objects) < 25:
            # Crear una lista de futures para las solicitudes de objetos faltantes
            futures = [executor.submit(peticionObjeto, ENDPOINT) for _ in range(25 - len(objects))]

            # Esperar a que se completen las solicitudes y obtener los resultados
            for future in concurrent.futures.as_completed(futures):
                json_object = future.result()
                 #Condición para que sea un objeto no existente dentro del arreglo 
                if not exists(objects ,json_object):
                    #Se agrega un objeto mas al arreglo
                    objects.append(json_object)

    #Se establece la respuesta que envieremos con el codigo de ok
    response = make_response(objects, 200)
    return response


if __name__ == '__main__':
    serve(app, host = '0.0.0.0', port = 3000)
