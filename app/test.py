import requests

# URL a la que se realizará la solicitud GET
url = 'http://localhost:8080/em/virtualizeservers/virtualassets'

# Realiza la solicitud GET
response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:

    dataFinal = {}

    data = response.json()
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

#####################################
# Refactoring chatgpt

# import requests

# def print_virtual_assets(folders, tribe_name="", clan_name=""):
#     for folder in folders:
#         if folder["name"] not in ["traffic_templates", "recorded_traffic", ".settings"]:
#             if folder["virtualAssets"]:
#                 for virt in folder["virtualAssets"]:
#                     print(tribe_name, clan_name, folder["name"], virt["id"], virt["name"])
            
#             if folder["folders"]:
#                 print_virtual_assets(folder["folders"], tribe_name, folder["name"])

# URL a la que se realizará la solicitud GET
# url = 'http://localhost:8080/em/virtualizeservers/virtualassets'

# Realiza la solicitud GET
# response = requests.get(url)

# Verifica si la solicitud fue exitosa (código de estado 200)
# if response.status_code == 200:
#     data = response.json()
#     json_data = data[0]

#     for tribe in json_data["virtualAssetsProject"]["folders"]:
#         tribe_name = tribe["name"]
#         print_virtual_assets(tribe["folders"], tribe_name)