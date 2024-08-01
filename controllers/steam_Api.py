import requests
import pandas as pd
import openpyxl
from keys import keyapi

def lista_de_amigos(id:int):
    '''
    informe um id steam
    id steam'76561198266319437' #cássio

    colunas = ['Steam_id', 'Nome', 'Avatar']
    retorna um pd.DataFrame(columns=colunas) 
    ex de retorno:

        Steam_id    Nome    Avatar
    0 123456789   cassio    https://imagem.jpg
    1 987654321   joao      https://imagem2.jpg
    '''
    
    '''
    amigos = openpyxl.Workbook()
    ws = amigos.active
    ws.append( ['steamid', 'nome'])
    amigos.save('amigosid.xlsx') #criando o DF
    df = pd.read_excel('amigosid.xlsx')
     '''
    
    
    id = str(id) #cássio


    ###### lista de amigos salvas em Excel ######

    friendlist = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={keyapi}&steamid={id}&relationship=friend') #amigos do Ranking
    friendlist = friendlist.json()
    friends =  friendlist['friendslist']['friends']
    friends_ids =[]

    for friend in friends:
        x = friend.get('steamid')
        friends_ids.append(x)

     # lista com as ids dos amigos, até aqui o codigo está funcionando
    

    colunas = ['Steam_id', 'Nome', 'Avatar']
    df_friends = pd.DataFrame(columns=colunas)

    for friendd in friends_ids:
        
        requisicaofriend = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={keyapi}&steamids={friendd}')
        requisicaofriend = requisicaofriend.json() # retorna os dados de cada jogador em dicionarios dentro de dicionarios
        requisicaofriend = requisicaofriend['response']['players']
        
        for t in requisicaofriend:
            tempo = {'Steam_id': t['steamid'], 'Nome': t['personaname'], 'Avatar': t['avatarmedium'], 'Publico':t['communityvisibilitystate']}
            df_tempo = pd.DataFrame([tempo])
            df_friends = pd.concat([df_friends, df_tempo], ignore_index=True)

    return df_friends