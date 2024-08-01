from models.user_model import Sessoes_Atualizacao, Tipo_Atualizacao
from datetime import datetime


class SessaoGlobal:

    @classmethod
    def criar_sessao_global(cls, tipo_atualizacao):
        """Efetua uma criação no banco de dados de sessão de atualização.

        Args:
            tipo_atualizacao (str): Tipo de atualização a ser criada (e.g., 'steam', 'api')

        SessaoGlobal.criar_sessao_global('steam')
        > cria no banco de dados a sessão com tipo steam
        """        
        try:
            tipo, created = Tipo_Atualizacao.get_or_create(Tipo=tipo_atualizacao)
            sessao = Sessoes_Atualizacao.create(Data_sessao=datetime.now(), tipo=tipo)
            print(f'Sessão global de atualização criada com ID: {sessao.id}')
        except Exception as e:
            print(f'Erro ao criar sessão global de atualização: {str(e)}')

