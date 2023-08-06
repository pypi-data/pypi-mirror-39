# -*- coding: utf-8 -*-
from flask import jsonify
from werkzeug.exceptions import HTTPException


def handle_generic_error(e):
    codigo = 500
    descricao = "Erro interno no servidor"
    if isinstance(e, HTTPException):
        codigo = e.code
        descricao = e.description
    
    erro = {
        'description': descricao,
        'error': type(e).__name__,
        'status_code': codigo
    }
    return jsonify(erro), codigo


def responder_com_erro(e=None, mensagem='', status=400):
    codigo = status
    if e and isinstance(e, HTTPException):
        codigo = e.code
        mensagem = e.description
    
    erro = {
        'mensagem': mensagem,
        'erro': type(e).__name__ if not type(e).__name__ else 'ocorreu um erro',
        'status_code': codigo
    }
    return jsonify(erro), codigo


class InvalidUsage(Exception):
    status_code = 400
    
    def __init__(self, description, error, status_code=None, payload=None):
        Exception.__init__(self)
        self.description = description
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['description'] = self.description
        rv['error'] = self.error
        rv['status_code'] = self.status_code
        return rv
