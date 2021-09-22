from urllib.request import urlopen

import json
import pprint


url = "https://api.cartolafc.globo.com/atletas/mercado"

response = urlopen(url)

mercado = json.loads(response.read())


def calcularDiferenca(i):
    diferenca = float(i['media_num']) - float(i['pontos_num'])
    return round(diferenca, 2)

def calcularPrecoPonto(i):
    precoPonto =  float(i['preco_num']/float(i['media_num']))
    return round(precoPonto, 2)
    
def calcularFatorCompra(i):
    fatorCompra =  calcularDiferenca(i)/calcularPrecoPonto(i)
    return round(fatorCompra, 2)

def orderBy(e):
    return e['Fator Compra']

def acharAtletas(posicao_ID):
    #Acha todo os atletas
    atletas = []
    for i in mercado['atletas']:
        #Acha os Atacantes Prováveis
        if(i['posicao_id'] == posicao_ID and i['status_id'] == 7) and calcularDiferenca(i) >= 0 and i['media_num'] > 0:
            atleta = {"Nome": [], "Diferença": [], "Fator Compra": []}
            atleta['Nome'].append(i['apelido'])
            atleta['Diferença'].append(calcularDiferenca(i))
            atleta['Fator Compra'].append(calcularFatorCompra(i))
            atletas.append(atleta)
            #print(str(nomes) + " // " + str(diferenca))
            #print ("Nome " + str(i['apelido']) + ";" " Diferença " + str(calcularDiferenca(i)))
    atletas.sort(key=orderBy)
    return atletas

pprint.pprint("ATACANTES")
pprint.pprint(acharAtletas(5))
pprint.pprint("MEIAS")
pprint.pprint(acharAtletas(4))
pprint.pprint("ZAGUEIROS")
pprint.pprint(acharAtletas(3))
pprint.pprint("LATERAIS")
pprint.pprint(acharAtletas(2))
pprint.pprint("TECNICO")
pprint.pprint(acharAtletas(6))
pprint.pprint("GOLEIRO")
pprint.pprint(acharAtletas(1))



