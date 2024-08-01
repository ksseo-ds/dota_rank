from peewee import *
from models.user_model import Jogadores, Atualizacoes, Sessoes_Atualizacao, Tipo_Atualizacao
import requests
import time
from datetime import datetime

class JogadorController:

    @classmethod
    def status_model_jogador(cls, id_steam):
        try:
            Jogadores.get(Jogadores.Id_Steam == id_steam)
            return True
        except Jogadores.DoesNotExist:
            return False

    @staticmethod
    def steamid64_to_accountid(steamid64):
        base_number = 76561197960265728
        account_id = int(steamid64) - base_number
        if account_id < 0:
            raise ValueError("ID Dota não pode ser negativo")
        return account_id

    @classmethod
    def adicionar_jogador(cls, id_steam, nome_jogador, avatar=None, perfil_publico=None):
        try:
            dota_id = str(cls.steamid64_to_accountid(id_steam))
            cadastrado = cls.status_model_jogador(id_steam)

            perfil_publico = int(perfil_publico) if perfil_publico is not None else None

            print(f'Preparando para cadastrar jogador: Id_Steam={id_steam}, Id_Dota={dota_id}, Nome_jogador={nome_jogador}, Avatar={avatar}, Perfil_Publico={perfil_publico}')
            if not cadastrado:
                Jogadores.create(
                    Id_Steam=str(id_steam),
                    Id_Dota=str(dota_id),
                    Nome_jogador=nome_jogador,
                    Avatar=avatar,
                    Perfil_Publico=perfil_publico
                )
                print(f'Jogador {id_steam} criado com sucesso.')
            else:
                Jogadores.update(
                    Id_Dota=str(dota_id),
                    Nome_jogador=nome_jogador,
                    Avatar=avatar,
                    Perfil_Publico=perfil_publico
                ).where(Jogadores.Id_Steam == str(id_steam)).execute()
                print(f'Jogador {id_steam} atualizado com sucesso.')

            print(f'Criando entrada em Atualizacoes: Id_Steam={id_steam}, Atualizacao_Steam=True, Atualizacao_Tier=False')
            Atualizacoes.create(
                Id_Steam=str(id_steam),
                Id_Sessao=Sessoes_Atualizacao.get().id,  # Utilizando a sessão global
                Atualizacao_Steam=True,
                Atualizacao_Tier=False
            )
            print(f'Entrada em Atualizacoes criada com sucesso para {id_steam}.')

            return True, f'Jogador {id_steam}, {nome_jogador}, cadastrado com sucesso'
        except Exception as e:
            print(f'Erro ao atualizar jogador: {id_steam}, {str(e)}')
            return False, f'Erro ao atualizar jogador: {id_steam}, {str(e)}'

    # Requisição da API
    @classmethod
    def atualizar_tier(cls):
        lista_atualizar = Jogadores.select().where(Jogadores.Perfil_Publico == 3)

        for player in lista_atualizar:
            id_dota = player.Id_Dota
            try:
                response = requests.get(f"https://api.opendota.com/api/players/{id_dota}")
                if response.status_code == 200:
                    data = response.json()
                    rank_tier = data.get('rank_tier')
                    if rank_tier is not None:
                        player.rank = rank_tier
                        player.save()
            except Exception as e:
                print(f'Erro ao obter o rank_tier do jogador {id_dota}:{e}')
            time.sleep(2)
