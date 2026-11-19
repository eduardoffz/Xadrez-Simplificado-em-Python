from pecas_linha import caminho_livre
from pecas_linha import caminho_livre, movimento_torre
from pecas_linha import caminho_livre, movimento_bispo
from pecas_linha import caminho_livre, movimento_dama

#Testes da função de caminho livre;
def tabuleiro_vazio():
    return([["." for _ in range(8)] for _ in range(8)])

t = tabuleiro_vazio()
assert caminho_livre(t, (0, 0), (0, 5)) == True, "Torre em linha vazia"

t[0][3] = "P"
assert caminho_livre(t, (0, 0), (0, 5)) == False, "Torre com peça no meio"

t[4][4] = "P"
assert caminho_livre(t, (1, 1), (4, 4)) == True, "Bispo com peça no final"

t = tabuleiro_vazio()
assert caminho_livre(t, (0, 0), (0, 1)) == True, "Torre linha vazia"

t[3][0] = "P"
assert caminho_livre(t, (0, 0), (5, 0)) == False, "Torre com peça no meio"

#Testes do movimento da torre;
def tabuleiro_vazio():
    return([["." for _ in range(8)] for _ in range(8)])

t = tabuleiro_vazio()
assert movimento_torre(t, (0, 0) , (0, 5)) == True, "Torre em movimento horizontal livre"

t[3][0] = "P"
assert movimento_torre(t, (0, 0), (5, 0)) == False, "Torre em movimento vertical bloqueada"

t = tabuleiro_vazio()
assert movimento_torre(t, (0, 0), (3, 5)) == False, "Torre em movimento inválido"

#Testes do bispo;
def tabuleiro_vazio():
    return([["." for _ in range(8)] for _ in range(8)])

t = tabuleiro_vazio()
assert movimento_bispo(t, (1, 1), (4, 4)) == True, "Bispo em diagonal principal livre"

t[3][2] = "P"
assert movimento_bispo(t, (4, 1), (1, 4)) == False, "Bispo em diagonal secundária bloqueado"

t = tabuleiro_vazio()
assert movimento_bispo(t, (4, 1), (0, 1)) == False, "Bispo em movimento inválido"

#Testes da dama;
def tabuleiro_vazio():
    return([["." for _ in range(8)] for _ in range(8)])

t = tabuleiro_vazio()
assert movimento_dama(t, (0, 0), (7, 7)) == True, "Dama em diagonal principal livre"

t[3][2] = "P"
assert movimento_dama(t, (4, 1), (1, 4)) == False, "Dama em diagonal secundaria bloqueada"

t = tabuleiro_vazio()
assert movimento_dama(t, (0, 0) , (0, 5)) == True, "Dama em movimento horizontal livre"

t[3][0] = "P"
assert movimento_dama(t, (0, 0), (5, 0)) == False, "Dama em movimento vertical bloqueada"