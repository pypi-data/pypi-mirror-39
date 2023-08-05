# -*- coding: utf-8 -*-
from random import randint


def formatar_cpf(cpf):
    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])


def generate(formatar=False):
    """
     * Essa função gera um número de CPF válido.
     * @param {Boolean} formatar define se o número do CPF deve ser gerado com os pontos e hífen.
     * @return {String} CPF
     *
     * Regra de Formação
     *
     * O número de um CPF tem exatamente 9 algarismos em sua raiz e mais dois dígitos verificadores que são indicados por último.
     * Portanto, um CPF tem 11 algarismos. O número do CPF é escrito na forma abcdefghi-jk ou diretamente como abcdefghijk onde
     * os algarismos não podem ser todos iguais entre si.
     *
     *                  abc.def.ghi-jk
     *
     * O j é chamado 1° dígito verificador do número do CPF.
     *
     * O k é chamado 2° dígito verificador do número do CPF.
     *
     * Primeiro Dígito
     *
     * Para obter j multiplicamos a, b, c, d, e, f, g, h e i pelas constantes correspondentes, e somamos os resultados de cada multiplicação:
     *
     * S = 10a + 9b + 8c + 7d + 6e + 5f + 4g + 3h + 2i
     *
     * O resultado da soma é dividido por 11, e resto da divisão é tratada da seguinte forma:
     *
     * se o resto for igual a 0 ou 1, j será 0 (zero)
     * se o resto for 2, 3, 4, 5, 6, 7, 8, 9 ou 10, j será 11 - resto
     *
     * Para obter k, multiplicamos a, b, c, d, e, f, g, h, i e j pelas constantes correspondentes, e somamos os resultados de cada multiplicação:
     *
     * S = 11a + 10b + 9c + 8d + 7e + 6f + 5g + 4h + 3i + 2j
     *
     * O resultado da soma é dividido por 11, e resto da divisão é tratada da seguinte forma:
     *
     * se o resto for igual a 0 ou 1, k será 0 (zero)
     * se o resto for 2, 3, 4, 5, 6, 7, 8, 9 ou 10, k será 11 - resto
     *
    """
    # 9 números aleatórios
    arNumeros = []
    for i in range(9):
        arNumeros.append(randint(0, 9))
    
    # Calculado o primeiro DV
    somaJ = (arNumeros[0] * 10) + (arNumeros[1] * 9) + (arNumeros[2] * 8) + (arNumeros[3] * 7) + (arNumeros[4] * 6) + (
            arNumeros[5] * 5) + (arNumeros[6] * 4) + (arNumeros[7] * 3) + (arNumeros[8] * 2)
    
    restoJ = somaJ % 11
    
    if restoJ == 0 or restoJ == 1:
        j = 0
    else:
        j = 11 - restoJ
    
    arNumeros.append(j)
    
    # Calculado o segundo DV
    somaK = (arNumeros[0] * 11) + (arNumeros[1] * 10) + (arNumeros[2] * 9) + (arNumeros[3] * 8) + (arNumeros[4] * 7) + (
            arNumeros[5] * 6) + (arNumeros[6] * 5) + (arNumeros[7] * 4) + (arNumeros[8] * 3) + (j * 2)
    
    restoK = somaK % 11
    
    if restoK == 0 or restoK == 1:
        k = 0
    else:
        k = 11 - restoK
    
    arNumeros.append(k)
    
    cpf = ''.join(str(x) for x in arNumeros)
    
    if formatar:
        return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]
    else:
        return cpf