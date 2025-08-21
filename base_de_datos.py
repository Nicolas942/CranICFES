import random
from pymongo import MongoClient

try:
    cliente = MongoClient("mongodb+srv://Cranicfes:Nikolas200605@cranicfes.f5idx6n.mongodb.net/?retryWrites=true&w=majority&appName=CranICFES")
    
    base_datos = cliente["CranICFES"]
    coleccion = base_datos["preguntas"]

    documentos = list(coleccion.find())

    documento_aleatorio = random.choice(documentos)

    print(documento_aleatorio["pregunta"])

    respuesta = int(input("Ingrese su repuesta: "))

    if respuesta == documento_aleatorio["respuesta"]:
        print("la respuesta es correcta")
    else:
        print("mal")

except Exception as ex:
    print("Error durante la conexion: {}".format(ex))
