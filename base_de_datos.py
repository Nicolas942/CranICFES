from pymongo import MongoClient
import random

# === Conexión a la base de datos ===
cliente = None
coleccion = None

try:
    cliente = MongoClient("mongodb+srv://Cranicfes:Nikolas200605@cranicfes.f5idx6n.mongodb.net/?retryWrites=true&w=majority&appName=CranICFES")
    base_datos = cliente["CranICFES"]
    coleccion = base_datos["preguntas"]
    print("✅ Conexión exitosa a la base de datos")
except Exception as ex:
    print("❌ Error al conectar a MongoDB:", ex)

# === Función que devuelve una pregunta aleatoria con formato usable ===
def obtener_pregunta_aleatoria():
    if coleccion is None:
        print("⚠️  Colección no disponible")
        return None

    try:
        documentos = list(coleccion.find())
        if not documentos:
            print("⚠️  No hay preguntas en la base de datos")
            return None

        documento = random.choice(documentos)
        return {
            "pregunta": documento["pregunta"],
            "opciones": documento["opciones"],
            "correcta": documento.get("correcta")  # opcional: índice de la correcta
        }
    except Exception as ex:
        print("❌ Error al obtener pregunta:", ex)
        return None

# === Función auxiliar para usar en consola (opcional) ===
def mostrar_en_consola(pregunta_data):
    if pregunta_data:
        print("\nPregunta:")
        print(pregunta_data["pregunta"])
        for i, opcion in enumerate(pregunta_data["opciones"], 1):
            marca = "✅" if i - 1 == pregunta_data.get("correcta") else ""
            print(f"{i}. {opcion} {marca}")

