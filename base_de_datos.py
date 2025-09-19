# base_de_datos.py
import random
from pymongo import MongoClient

def respuesta_multiple():
    try:
        cliente = MongoClient("mongodb+srv://Cranicfes:Nikolas200605@cranicfes.f5idx6n.mongodb.net/?retryWrites=true&w=majority&appName=CranICFES")
        base_datos = cliente["CranICFES"]
        coleccion = base_datos["preguntas"]
        

        documento = random.choice(list(coleccion.find()))

        print(documento["pregunta"])
        for orden, opcion in enumerate(documento["opciones"], 1):
            print(f"{orden}. {opcion}")
        
    except Exception as ex:
        print("Error durante la conexion: {}".format(ex))
    finally:
        cliente.close()

