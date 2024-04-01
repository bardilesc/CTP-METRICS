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


scheduler = BackgroundScheduler()
scheduler.add_job(save_last_hits, CronTrigger(hour=12))
scheduler.start()


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
        requester = HTTPRequest(BASE_URL_CTP)
        data_hits = requester.get(endpoint=get_hits_peer_dates(startTime,endTime))
        data_virts = get_virtualization(requester.get(endpoint="em/virtualizeservers/virtualassets"))

        print(data_hits)
        print(type(data_hits))
        data_json = json.loads(data_hits)
        return data_json


        
if __name__ == "__main__":
    today = datetime.now()
    # Formatear la fecha y hora actual como una cadena
    today_format = today.strftime("%Y-%m-%d %H:%M:%S")
    # Imprimir la fecha y hora actual
    print("Fecha y hora actual:", today_format)
    print("Server puerto 5000")
    app.run(host='0.0.0.0', port=5000)