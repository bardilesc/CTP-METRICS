import os
from pymongo import MongoClient

class MongoDBManager:
    mongodb_host = os.environ.get('MONGODB_HOST')
    mongodb_port = int(os.environ.get('MONGODB_PORT'))  # Convertir la cadena a entero
    mongodb_user = os.environ.get('MONGODB_USER')
    mongodb_pass = os.environ.get('MONGODB_PASS')

    def __init__(self, host=None, port=None, username=None, password=None, database='CTP_METRICS' ,authSource='admin', coleccion="HITS_COUNT_PER_DAY"):
        # Accede a las variables de entorno dentro del método __init__
        self.host = host or MongoDBManager.mongodb_host
        self.port = port or MongoDBManager.mongodb_port
        self.username = username or MongoDBManager.mongodb_user
        self.password = password or MongoDBManager.mongodb_pass
        self.client = MongoClient(self.host, self.port, username=self.username, password=self.password, authSource=authSource)
        self.db = self.client[database]
        self.db_name = database
        self.coleccion = self.db[coleccion]

    def insertar_documento(self, documento):
        self.coleccion.insert_one(documento)

    def obtener_documentos(self):
        return list(self.coleccion.find())
    
    def obtener_filtro_documentos(self, filtro):
        return list(self.coleccion.find(filtro, {"_id": False}))

    def actualizar_documento(self, filtro, actualizacion):
        self.coleccion.update_many(filtro, {'$set': actualizacion})

    def cerrar_conexion(self):
        self.client.close()

    def validar_db(self):
        database_names = self.client.list_database_names()
        return True if self.db_name in database_names else False
    
    def obtener_documentos_filtrado(self, filtro):
        return self.coleccion.find(filtro)
    
    def insert_multiple(self, data):
        try:
            self.coleccion.insert_many(data)
            print("Documentos insertados exitosamente.")
        except Exception as e:
            print(f"Error al insertar múltiples documentos: {e}")


# if endTime is None:
#     filtro = {"date": {"$gte": startTime}}
# else:
#     filtro = {"date": {"$gte": startTime, "$lte": endTime}}

# manager = MongoDBManager()
# try:
#     data = manager.obtener_filtro_documentos(filtro)
#     return jsonify(data)

# except Exception as e:
#     print("Error al obtener datos:", e)
#     return jsonify({"error": "Error interno del servidor", "mensaje": e}), 500