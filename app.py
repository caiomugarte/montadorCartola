from urllib.request import urlopen

import json
import pprint


url = "https://api.cartolafc.globo.com/atletas/mercado"
urlStatusMercado = 'https://api.cartolafc.globo.com/mercado/status'
urlEsquemas = 'https://api.cartolafc.globo.com/esquemas'
urlPartidas = 'https://api.cartolafc.globo.com/partidas'
response = urlopen(url)
mercado = json.loads(response.read())
responseEsquemas = urlopen(urlEsquemas)
jsonEsquemas = json.loads(responseEsquemas.read())
jsonPartidas = json.loads(urlopen(urlPartidas).read())

def calcularDiferenca(i):
    diferenca = float(i['media_num']) - float(i['pontos_num'])
    return round(diferenca, 2)


def calcularPrecoPonto(i):
    precoPonto = float(i['preco_num']/float(i['media_num']))
    return round(precoPonto, 2)


def calcularFatorCompra(i, timeID):
    fatorCompra = (calcularDiferenca(i)/calcularPrecoPonto(i)) + calcularPontosTime(timeID)
    #Peso em relação à Posição
    #Historico Soma +1 Vitoria -1 Derrota Empate +0
    return round(fatorCompra, 2)

def calcularPesoAproveitamento(aproveitamento):
    pontoAproveitamento = 0
    for i in aproveitamento:
        if(i == 'v'):
            pontoAproveitamento += 1
        elif(i == 'd'):
            pontoAproveitamento -= 1
    return pontoAproveitamento/5

def calcularPontosTime(timeID):
    for partida in jsonPartidas['partidas']:
        if(timeID == partida['clube_casa_id']):
            return getPesoTime(partida['clube_casa_posicao']) + calcularPesoAproveitamento(partida['aproveitamento_mandante'])
        elif(timeID == partida['clube_visitante_id']):
            return getPesoTime(partida['clube_visitante_posicao']) + calcularPesoAproveitamento(partida['aproveitamento_visitante'])
def getPesoTime(pos):
    return (21 - pos)/20

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
def getTimeAtleta(timeID):
    for time in jsonPartidas['clubes'].items():
        if(str(timeID) == time[0]):
            return time[1]['nome']

def acharAtletas():
    # Acha todo os atletas
    atletas = []
    for i in mercado['atletas']:
        # Acha os Atacantes Prováveis
        if(i['status_id'] == 7) and calcularDiferenca(i) > 0 and i['media_num'] > 0:
            atleta = {"Nome": str, "Diferença": float,
                      "Fator Compra": float, "Posicao": str, "Preco": float, "Media": float, 'Time': str, 'TimeID': str}
            atleta['Nome'] = (i['apelido'])
            atleta['Diferença'] = (calcularDiferenca(i))
            atleta['Time'] = getTimeAtleta(i['clube_id'])
            atleta['TimeID'] = i['clube_id']
            atleta['Fator Compra'] = calcularFatorCompra(i, atleta['TimeID'])
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

atletas = acharAtletas()
def getMelhoresAtletas(posicaoJogador):
    melhoresAtletas = []
    for i in atletas:
        if(i['Posicao'] == posicaoJogador):
            melhorAtleta = {'Atleta': str, 'Preco': float, 'PrevisaoPontos': int, 'Time': str , 'TimeID': str}
            melhorAtleta['Atleta'] = i['Nome']
            melhorAtleta['Preco'] = i['Preco']
            melhorAtleta['PrevisaoPontos'] = i['Media']
            melhorAtleta['Time'] = getTimeAtleta(i['TimeID'])
            melhorAtleta['TimeID'] = i['TimeID']
            melhoresAtletas.append(melhorAtleta)
    return melhoresAtletas

def getTimeAtleta(timeID):
    for time in jsonPartidas['clubes'].items():
        if(str(timeID) == time[0]):
            return time[1]['nome']

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
    melhoresAtacantes = getMelhoresAtletas('Atacante')
    melhoresZagueiros = getMelhoresAtletas('Zagueiros')
    melhoresMeias = getMelhoresAtletas('Meias')
    melhoresLaterais = getMelhoresAtletas('Laterais')
    melhoresGoleiros = getMelhoresAtletas('Goleiro')
    melhoresTecnicos = getMelhoresAtletas('Técnico')
    times = {"Times": []}
    for esquema in getEsquemasPossiveis():
        time = {"Esquema": str, "Preco": float, "PrevisaoPontos": float, "Atacantes": [], "Meias": [
        ], "Zagueiros": [], "Laterais": [], "Goleiro": [], "Tecnico": [], "PrevisaoPontos": [], 'Capitao': str}
        time['Esquema'] = esquema['Esquema']
        time['Atacantes'].append(melhoresAtacantes[:esquema['nrAtacantes']])
        time['Meias'].append(melhoresMeias[:esquema['nrMeias']])
        time['Zagueiros'].append(melhoresZagueiros[:esquema['nrZagueiros']])
        time['Laterais'].append(melhoresLaterais[:esquema['nrLaterais']])
        time['Goleiro'].append(melhoresGoleiros[:esquema['nrGoleiro']])
        time['Tecnico'].append(melhoresTecnicos[:esquema['nrTecnico']])
        time['Preco'] = (getPrecoTime(time['Atacantes'], time['Meias'],
                         time['Zagueiros'], time['Laterais'], time['Goleiro'], time['Tecnico']))
        time['PrevisaoPontos'] = (getMediaTime(time['Atacantes'], time['Meias'],
                         time['Zagueiros'], time['Laterais'], time['Goleiro'], time['Tecnico']))
        time['Capitao'] = getCapitao(time['Atacantes'], time['Meias'], time['Zagueiros'],time['Laterais'] , time['Goleiro'])
        times["Times"].append(time)
    return times

def getCapitao(atacantes, meias, zagueiros, laterais, goleiros):
    capitao = ''
    pontosTemp = 0
    for i in atacantes[0]:
        if(i['PrevisaoPontos'] > pontosTemp):
            pontosTemp = i['PrevisaoPontos'] * calcularPontosTime(i['TimeID'])
            capitao = i['Atleta']
    for i in meias[0]:
        if(i['PrevisaoPontos'] > pontosTemp):
            pontosTemp = i['PrevisaoPontos']
            capitao = i['Atleta']
    for i in zagueiros[0]:
        if(i['PrevisaoPontos'] > pontosTemp):
            pontosTemp = i['PrevisaoPontos']
            capitao = i['Atleta']
    for i in laterais[0]:
        if(i['PrevisaoPontos'] > pontosTemp):
            pontosTemp = i['PrevisaoPontos']
            capitao = i['Atleta']
    for i in goleiros[0]:
        if(i['PrevisaoPontos'] > pontosTemp):
            pontosTemp = i['PrevisaoPontos']
            capitao = i['Atleta']
    return capitao

    
    
    return 0
data = acharMelhorTime()
times = data.get('Times')
pprint.pprint(acharMelhorTime(), width=10, indent=1, sort_dicts=False)
