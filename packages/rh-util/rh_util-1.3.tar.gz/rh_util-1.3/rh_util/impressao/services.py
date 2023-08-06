# coding=utf-8
import os
import os.path
import shutil
from subprocess import call
from tempfile import mkdtemp, mkstemp

from django.http import HttpResponse
from django.template.loader import render_to_string


def generate_pdf_from_template(template):
    """ Recebe um template e gera um PDF a partir dele"""
    original_path = os.getcwd()  # é necessário armazenar o caminho anterior para restaurar depois
    r = HttpResponse(content_type='application/pdf')
    try:
        tmp_folder = mkdtemp()
        os.chdir(tmp_folder)
        file, filename = mkstemp(dir=tmp_folder)
        os.write(file, template)
        os.close(file)
        call(['pdflatex', filename])
        with open(os.path.join(tmp_folder, filename + '.pdf'), 'rb') as f:
            pdf = f.read()
        # Remove intermediate files
        os.remove(filename)
        os.remove(filename + '.aux')
        os.remove(filename + '.log')
        r.write(pdf)
        shutil.rmtree(tmp_folder)
    finally:
        os.chdir(original_path)
    return r


def replace_caracter_especial(string):
    import re
    new_string = re.sub(r'([^.a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ@&\\\-/{}():;,?*%$ ])', "", string)
    return new_string.replace("&", "\&").encode("utf-8").decode("utf-8", "replace")
