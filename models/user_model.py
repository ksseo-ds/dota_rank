from peewee import *
from .db import db

class BaseModel(Model):
    class Meta:
        database = db

class Jogadores(BaseModel):
    Id_Steam = TextField(unique=True)
    Id_Dota = TextField(unique=True)
    Nome_jogador = TextField()
    Avatar = TextField()
    Perfil_Publico = IntegerField()

class Tiers(BaseModel):
    Tier = IntegerField(unique=True)
    Bracket = IntegerField(default=0)
    Estrela = IntegerField(default=0)
    Descricao = TextField(default='')

class Tipo_Atualizacao(BaseModel):
    Id_tipo = AutoField()
    Tipo = TextField()

class Sessoes_Atualizacao(BaseModel):
    Id_Sessao = AutoField()
    Data_sessao = DateTimeField()
    tipo = ForeignKeyField(Tipo_Atualizacao, backref='sessoes')

class Atualizacoes(BaseModel):
    Id_Atualizacoes_Jogadores = AutoField()
    Id_Steam = ForeignKeyField(Jogadores, backref='atualizacoes')
    Id_Sessao = ForeignKeyField(Sessoes_Atualizacao, backref='atualizacoes')
    Atualizacao_Steam = BooleanField()
    Atualizacao_Tier = BooleanField()

class Historico_Tiers(BaseModel):
    Id_Historico = AutoField()
    Id_Steam = ForeignKeyField(Jogadores, backref='historico_tiers')
    Tier = ForeignKeyField(Tiers, backref='historico_tiers')
    Id_Sessao = ForeignKeyField(Sessoes_Atualizacao, backref='historico_tiers')
