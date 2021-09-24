from re import I
from urllib.request import urlopen

import json
import pprint


url = "https://api.cartolafc.globo.com/atletas/mercado"
urlStatusMercado = 'https://api.cartolafc.globo.com/mercado/status'
urlEsquemas = 'https://api.cartolafc.globo.com/esquemas'


def calcularDiferenca(i):
    diferenca = float(i['media_num']) - float(i['pontos_num'])
    return round(diferenca, 2)


def calcularPrecoPonto(i):
    precoPonto = float(i['preco_num']/float(i['media_num']))
    return round(precoPonto, 2)


def calcularFatorCompra(i):
    fatorCompra = calcularDiferenca(i)/calcularPrecoPonto(i)
    return round(fatorCompra, 2)


def orderBy(e):
    return e['Fator Compra']


def acharPosicao(posicaoId, mercado):
    posicoes = getPosicoesJson(mercado)
    posicao = ''
    for i in posicoes['id']:
        if(i == posicaoId):
            posicao = posicoes['Nome'][i-1]
    return posicao


def getPosicoesJson(mercado):
    posicoesJson = mercado['posicoes'].items()
    posicoes = {"id": [], "Nome": []}
    for key, value in posicoesJson:
        posicoes['id'].append(value['id'])
        posicoes['Nome'].append(value['nome'])
    return posicoes


def acharAtletas():
    response = urlopen(url)
    mercado = json.loads(response.read())
    # Acha todo os atletas
    atletas = []
    for i in mercado['atletas']:
        # Acha os Atacantes Prováveis
        if(i['status_id'] == 7) and calcularDiferenca(i) >= 0 and i['media_num'] > 0:
            atleta = {"Nome": str, "Diferença": float,
                      "Fator Compra": float, "Posicao": str, "Preco": float, "Media": float}
            atleta['Nome'] = (i['apelido'])
            atleta['Diferença'] = (calcularDiferenca(i))
            atleta['Fator Compra'] = (calcularFatorCompra(i))
            atleta['Posicao'] = (acharPosicao(i['posicao_id'], mercado))
            atleta['Preco'] = i['preco_num']
            atleta['Media'] = i['media_num']
            atletas.append(atleta)
    atletas.sort(key=orderBy, reverse=True)
    return atletas

def acharNrJogadores(jsonEsquemas):
    posicoes = []
    for key, nrPosicao in jsonEsquemas['posicoes'].items():
        posicoes.append(nrPosicao),
    return posicoes


def getEsquemasPossiveis():
    responseEsquemas = urlopen(urlEsquemas)
    jsonEsquemas = json.loads(responseEsquemas.read())
    esquemas = []
    for i in jsonEsquemas:
        esquema = {"Esquema": str, "nrAtacantes": int, "nrMeias": int,
                   "nrZagueiros": int, "nrLaterais": int, "nrGoleiro": 1, "nrTecnico": 1}
        esquema['Esquema'] = i['nome']
        esquema['nrAtacantes'] = int(acharNrJogadores(i)[0])
        esquema['nrMeias'] = int(acharNrJogadores(i)[3])
        esquema['nrLaterais'] = int(acharNrJogadores(i)[2])
        esquema['nrZagueiros'] = int(acharNrJogadores(i)[5])
        esquemas.append(esquema)
    return esquemas


def getMelhoresAtletas(posicaoJogador, nrPos):
    atletas = acharAtletas()
    melhoresAtletas = []
    for i in atletas:
        if(i['Posicao'] == posicaoJogador):
            melhorAtleta = {'Atleta': [], 'Preco': float, 'PrevisaoPontos': int}
            melhorAtleta['Atleta'].append(i['Nome'])
            melhorAtleta['Preco'] = i['Preco']
            melhorAtleta['PrevisaoPontos'] = i['Media']
            melhoresAtletas.append(melhorAtleta)
    return melhoresAtletas[:nrPos]


def getPrecoTime(atacantes, meias, zagueiros, laterais, goleiro, tecnico):
    preco = 0
    for i in atacantes[0]:
        preco += i['Preco']
    for i in meias[0]:
        preco += i['Preco']
    for i in zagueiros[0]:
        preco += i['Preco']
    for i in laterais[0]:
        preco += i['Preco']
    for i in goleiro[0]:
        preco += i['Preco']
    for i in tecnico[0]:
        preco += i['Preco']
    return round(preco, 2)

def getMediaTime(atacantes, meias, zagueiros, laterais, goleiro, tecnico):
    media = 0
    for i in atacantes[0]:
        media += i['PrevisaoPontos']
    for i in meias[0]:
        media += i['PrevisaoPontos']
    for i in zagueiros[0]:
        media += i['PrevisaoPontos']
    for i in laterais[0]:
        media += i['PrevisaoPontos']
    for i in goleiro[0]:
        media += i['PrevisaoPontos']
    for i in tecnico[0]:
        media += i['PrevisaoPontos']
    return round(media, 2)


def acharMelhorTime():
    times = []
    for esquema in getEsquemasPossiveis():
        time = {"Esquema": str, "Preco": float, "PrevisaoPontos": float, "Atacantes": [], "Meias": [
        ], "Zagueiros": [], "Laterais": [], "Goleiro": [], "Tecnico": [], "PrevisaoPontos": []}
        time['Esquema'] = esquema['Esquema']
        time['Atacantes'].append(getMelhoresAtletas(
            'Atacante', esquema['nrAtacantes']))
        time['Meias'].append(getMelhoresAtletas('Meia', esquema['nrMeias']))
        time['Zagueiros'].append(getMelhoresAtletas(
            'Zagueiro', esquema['nrZagueiros']))
        time['Laterais'].append(getMelhoresAtletas(
            'Lateral', esquema['nrLaterais']))
        time['Goleiro'].append(getMelhoresAtletas(
            'Goleiro', esquema['nrGoleiro']))
        time['Tecnico'].append(getMelhoresAtletas(
            'Técnico', esquema['nrTecnico']))
        time['Preco'] = (getPrecoTime(time['Atacantes'], time['Meias'],
                         time['Zagueiros'], time['Laterais'], time['Goleiro'], time['Tecnico']))
        time['PrevisaoPontos'] = (getMediaTime(time['Atacantes'], time['Meias'],
                         time['Zagueiros'], time['Laterais'], time['Goleiro'], time['Tecnico']))
        times.append(time)
    return times


pprint.pprint(acharMelhorTime())
