import os
import sys
import json

##############################

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger #prueba

##############################

from controller.mongo_manager import MongoDBManager
from controller.HTTPRequest import HTTPRequest
from controller.Hits import get_last_hits, get_virtualization, get_hits_peer_dates
##############################

from flask import Flask, jsonify, request, make_response
app = Flask(__name__)

##############################

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

BASE_URL_CTP = os.environ.get('BASE_URL_CTP')


def get_hit_virts(startTime, endTime):
    requester = HTTPRequest(BASE_URL_CTP)
    data_hits = requester.get_json(endpoint=get_hits_peer_dates(startTime,endTime))
    data_virt_list = requester.get_json(endpoint="em/virtualizeservers/virtualassets")
    data_virts = get_virtualization(data_virt_list)
    # Iterar sobre los elementos de data_hits["items"]
    for item in data_hits["items"]:
        # Obtener el resourceId del elemento actual
        virt_name_hits = item.get("name")
        acum = 0
        for virt_data in data_virts:
            virt_name_asset =  virt_data["virt_name"]

            tribu =  virt_data["tribu"]
            celula =  virt_data["celula"]
            clan =  virt_data["clan"]

            if virt_name_hits == virt_name_asset:
                item.update({
                    "tribu": tribu ,
                    "celula": celula ,
                    "clan": clan
                })
                acum+=1
        
        
        if acum==0:
            # Si no se encuentra ninguna coincidencia, establecer los valores como "Na"
            item.update({
                "tribu": "Na",
                "celula": "Na",
                "clan": "Na",
            })

    return data_hits

def save_last_hits():
    manager = MongoDBManager()
    requester = HTTPRequest(BASE_URL_CTP)
    data = requester.get(endpoint=get_last_hits())
    data_json = json.loads(data)

    # Obtener la fecha y hora actual en formato datetime
    today = datetime.now()
    # Restar dos días a la fecha actual
    yesterday_2 = today - timedelta(days=1)
    # Convertir la fecha resultante a formato ISODate
    date_iso = yesterday_2.isoformat()
    data_json['date'] = date_iso
    return data_json
    #manager.insertar_documento(data_json)

@app.route('/save', methods=['GET'])
def save_last_hits():
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')
    if startTime is None or endTime is None:
        datos_param = {
            "error": "Parametros no valido"
        }
        response = jsonify(datos_param)
        response.status_code = 404
        return response
    
    else:
        try:
            manager = MongoDBManager()
            manager.insertar_documento(get_hit_virts(startTime, endTime))
        except BaseException as bs:
            return {"Error": str(bs)}



@app.route('/', methods=['GET'])
def obtener_datos():
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')
    if startTime is None or endTime is None:
        datos_param = {
            "error": "Parametros no valido"
        }
        response = jsonify(datos_param)
        response.status_code = 404
        return response
    
    else:
        return get_hit_virts(startTime, endTime)
    

        
if __name__ == "__main__":
    today = datetime.now()
    # Formatear la fecha y hora actual como una cadena
    today_format = today.strftime("%Y-%m-%d %H:%M:%S")
    # Imprimir la fecha y hora actual
    print("Fecha y hora actual:", today_format)
    print("Server puerto 5000")
    app.run(host='0.0.0.0', port=5000)