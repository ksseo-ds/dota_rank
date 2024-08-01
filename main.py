from controllers.steam_Api import lista_de_amigos
from models.user_model import Jogadores, Atualizacoes, Sessoes_Atualizacao, Tipo_Atualizacao, Tiers, Historico_Tiers
from models.db import db
from controllers.user_controller import JogadorController
from time import sleep
import os

print('Iniciando ...')

# Apagar e criar tabelas
db.drop_tables([Jogadores, Atualizacoes, Sessoes_Atualizacao, Tipo_Atualizacao, Tiers, Historico_Tiers])
db.create_tables([Jogadores, Atualizacoes, Sessoes_Atualizacao, Tipo_Atualizacao, Tiers, Historico_Tiers]) 
print('Tabelas Criadas')

# Inserir os tipos de atualização e tiers
tipos_atualizacao = ['Tipo 1', 'Tipo 2']
for tipo in tipos_atualizacao:
    Tipo_Atualizacao.get_or_create(Tipo=tipo)

tiers = [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 51, 52, 53, 54, 55, 61, 62, 63, 64, 65]
for tier in tiers:
    Tiers.get_or_create(Tier=tier)

id_steam_ranking = 76561198266319437

# Pega a lista de ids steam de amigos
friendlist = lista_de_amigos(id_steam_ranking)
print('Adicionando e Atualizando jogadores no Banco de Dados')
print(f'Um total de {len(friendlist)} Jogadores encontrados')
sleep(2)

jogador_adicionado = 0
for index, row in friendlist.iterrows():
    JogadorController.adicionar_jogador(id_steam=row['Steam_id'], nome_jogador=row['Nome'], avatar=row['Avatar'])#,perfil_publico=row['Publico'])
    jogador_adicionado += 1
    #os.system('cls') # desablitar para ver os logs
    print(f'Progresso : {int((jogador_adicionado / len(friendlist)) * 100)} %')

print('Processo concluído')
