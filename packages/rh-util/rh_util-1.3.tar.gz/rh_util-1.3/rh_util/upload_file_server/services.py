import requests
from datetime import datetime

__URL_SERVER = "http://webserver.mateus:8080"


def download(hash):
    url = __URL_SERVER + "/download?hash={0}".format(hash)
    response = requests.get(url)
    return response


def upload(arquivo, categoria="", observacao="", nome_arquivo="", senha=""):
    url = __URL_SERVER + "/upload"
    prefixo = str(datetime.now().date())+'-'+nome_arquivo
    headers = {
        'ws-categoria': categoria,
        'ws-arquivo': prefixo,
        'ws-observacao': observacao,
        'ws-senha': senha,
        'content-disposition': 'form-data; name="data" filename="data"'
    }
    response = requests.post(url=url, files={'data': arquivo}, headers=headers)
    return response
