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
    coleccion = base_datos["preguntas2"]
    
    # Prueba de conexión
    cliente.admin.command('ping')
    print("✅ Conexión exitosa a la base de datos")
except Exception as ex:
    print("❌ Error al conectar a MongoDB:", ex)

# === Función principal: obtener una pregunta aleatoria filtrada por materia ===
def obtener_pregunta_aleatoria(materia=None):
    if coleccion is None:
        print("⚠️  Colección no disponible. Revisa la conexión.")
        return None

    try:
        # Filtro por materia si se especifica
        filtro = {"materia": materia} if materia else {}
        
        # Obtener todos los documentos que coincidan
        documentos = list(coleccion.find(filtro))
        
        if not documentos:
            print(f"⚠️  No se encontraron preguntas para la materia: {materia}")
            return None

        # Elegir una pregunta al azar
        documento = random.choice(documentos)
        
        # Devolver datos estructurados
        return {
            "pregunta": documento["pregunta"],
            "opciones": documento["opciones"],
            "respuesta": documento.get("respuesta"),  
            "materia": documento["materia"],
            "actividad" : documento["actividad"],
            "imagen" : documento["imagen"]
        }
    except Exception as ex:
        print("❌ Error al obtener pregunta desde la base de datos:", ex)
        return None