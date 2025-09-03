<<<<<<< HEAD
import pymongo
=======
import random
from pymongo import MongoClient

def respuesta_multiple(documento):
    for orden, opcion in enumerate(documento["opciones"], 1):
        print(f"{orden}. {opcion}")

try:
    cliente = MongoClient("mongodb+srv://Cranicfes:Nikolas200605@cranicfes.f5idx6n.mongodb.net/?retryWrites=true&w=majority&appName=CranICFES")
    
    base_datos = cliente["CranICFES"]
    coleccion = base_datos["preguntas"]

    documentos = list(coleccion.find())

    documento_aleatorio = random.choice(documentos)

    print("\nPregunta:")
    print(documento_aleatorio["pregunta"])

    respuesta_multiple(documento_aleatorio)   

except Exception as ex:
    print("Error durante la conexion: {}".format(ex))
finally:
    cliente.close()

>>>>>>> c5327b4e0fda55ad1f60966d4f4099ede3926a4a
