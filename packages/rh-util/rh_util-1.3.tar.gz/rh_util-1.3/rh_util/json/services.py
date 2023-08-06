import decimal
import re
import json
import flask


def extract_json(content):
    string_json = str(content)
    # Procura se o json esta dentro de um objeto data
    # Caso esteja extrai esse json
    if re.search('data', string_json[0:7]):
        string_json = str(string_json.replace("{\"data\": \"", "", 1))
        string_json = str(string_json.replace("\"}}\"}", "\"}}", 1))
        string_json = str(string_json.replace('\\', ''))
    return json.loads(string_json)


def remove_caracteres_invalidos(str_json):
    return re.sub(u'[^{}"''_,.a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', str_json)


class MyJSONEncoder(flask.json.JSONEncoder):
    """"Criado para suportar decimal no json"""
    
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return float(obj)
        return super(MyJSONEncoder, self).default(obj)
