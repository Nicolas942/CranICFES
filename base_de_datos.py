from pymongo import MongoClient
import random

# === Conexión a MongoDB ===
cliente = None
coleccion = None

try:
    # Usa tu URL de conexión
    cliente = MongoClient("mongodb+srv://Cranicfes:Nikolas200605@cranicfes.f5idx6n.mongodb.net/?retryWrites=true&w=majority&appName=CranICFES")
    
    # Selecciona la base de datos y colección
    base_datos = cliente["CranICFES"]
    coleccion = base_datos["preguntas"]
    
    # Prueba de conexión
    cliente.admin.command('ping')
    print("✅ Conexión exitosa a la base de datos")
except Exception as ex:
    print("Error durante la conexion: {}".format(ex))
finally:
    cliente.close()

