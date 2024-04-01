from datetime import datetime, timedelta
import urllib.parse

def get_last_hits():
    today = datetime.today()
    yesterday_2 = today - timedelta(days=2)
    init_yesterday_2 = yesterday_2.replace(hour=0, minute=0, second=0, microsecond=0)
    end_yesterday_2 = yesterday_2.replace(hour=23, minute=59, second=59, microsecond=999999)
    init_yestedaday2_str = init_yesterday_2.strftime('%Y-%m-%d %H:%M:%S.000')
    end_yestedaday2_str = end_yesterday_2.strftime('%Y-%m-%d %H:%M:%S.000')
    query_filter = {"startTimestamp": init_yestedaday2_str, "endTimestamp": end_yestedaday2_str}
    query_filter_encoded = urllib.parse.quote(str(query_filter))
    url_base = "em/usage?"
    url_params = f"queryFilter={query_filter_encoded}&_=1710444066974"
    url = url_base + url_params
    return url

def get_hits_peer_dates(startTime, endTime):
    # Convertir las cadenas de startTime y endTime a objetos datetime
    start_date = datetime.strptime(startTime, '%Y-%m-%d')
    end_date = datetime.strptime(endTime, '%Y-%m-%d')
    # Agregar un día más al objeto fecha_fin_dia_anterior
    end_date += timedelta(days=1)
    # Definir el formato de las fechas de inicio y fin
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S.000')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S.000')
    # Construir el filtro de consulta
    query_filter = {"startTimestamp": start_date_str, "endTimestamp": end_date_str}
    query_filter_encoded = urllib.parse.quote(str(query_filter))
    # Construir la URL
    url_base = "em/usage?"
    url_params = f"queryFilter={query_filter_encoded}&_=1710444066974"
    url = url_base + url_params
    return url



def get_virtualization(data):
    json_data = data[0]
    folder_ommit = ["traffic_templates", "recorded_traffic", ".settings"]
    for folder in json_data["virtualAssetsProject"]["folders"]:
        if folder["name"] not in folder_ommit:
            tribu = folder["name"]
            if folder["virtualAssets"]!= None:
                for virt in folder["virtualAssets"]:
                    virt_id = virt["id"]
                    virt_name = virt["name"]
                    print(tribu, "Na", "Na", virt_id, virt_name )
            if folder["folders"] != None:
                for clanes in folder["folders"]:
                    clan_name = clanes["name"]
                    #print(clanes, type(clanes))
                    if clanes["folders"]!= None:
                        #print(clan_name, "tiene celulas")
                        for celulas in clanes["folders"]:
                            celula_name = celulas["name"]
                            if celulas["virtualAssets"]!= None:
                               #print(celula_name, " Tiene virtualizaciones")
                                for virt in celulas["virtualAssets"]:
                                    print(tribu, clan_name, celula_name, virt["name"])