def caminho_livre(tabuleiro, origem, destino) -> bool:
    """
    Função para verificar se o caminho está livre;
    tabuleiro: matriz que estará representando o tabuleiro;
    origem: tupla com a posição inicial da peça;
    destino: tupla com a posição de destino da peça;
    retorna: True se o caminho estiver livre, ou False se o caminho não estiver livre.
    """
    #Desempacotando os valores das tuplas de origem e destino e atribuindo em variaveis separadas;
    linha_atual, col_atual = origem
    linha_des, col_des = destino

    #Verificando a direção dos movimentos;
    if (linha_des> linha_atual):
        passo_linha = 1
    elif (linha_des < linha_atual):
        passo_linha = -1
    else:
        passo_linha = 0
    if (col_des > col_atual):
        passo_col = 1
    elif (col_des < col_atual):
        passo_col = -1
    else:
        passo_col = 0

    #Correção de bug;
    linha_atual += passo_linha
    col_atual += passo_col

    #Verificação de fato: Enquanto a posição atual for diferente do destino, verificamos se a casa atual está vazia ou não.
    while (linha_atual, col_atual) != (linha_des, col_des):
        if tabuleiro[linha_atual][col_atual] != ".":
            return False

        linha_atual += passo_linha
        col_atual += passo_col
    
    return True

#Movimento da torre;
def movimento_torre(tabuleiro, origem, destino) -> bool:
    """
    Função para o movimento das torres;
    tabuleiro: matriz que vai representar o tabuleiro;
    origem: tupla com a posição de origem da peça;
    destino: tupla com a posição de destino da peça;
    retorna: True se o movimento for válido, ou False se o movimento for inválido.
    """
    #Desempacotando os valores das tuplas de origem e destino e atribuindo em variaveis separadas;
    linha_atual, col_atual = origem
    linha_dest, col_dest = destino

    #Validação de movimentos;
    if ((linha_dest == linha_atual) and (col_dest != col_atual)) or ((linha_dest != linha_atual) and (col_dest == col_atual)):
        freeway = caminho_livre(tabuleiro, origem, destino)
        if (freeway == True):       
            return True
        else:
            return False
    else:
        return False

def movimento_bispo(tabuleiro, origem, destino) -> bool:
    """
    Função para o movimento ddos bispos;
    tabuleiro: matriz que vai representar o tabuleiro;
    origem: tupla com a posição de origem da peça;
    destino: tupla com a posição de destino da peça;
    retorna: True se o movimento for válido, ou False se o movimento for inválido.
    """
    #Desempacotando os valores das tuplas de origem e destino e atribuindo em variaveis separadas;
    linha_atual, col_atual = origem
    linha_dest, col_dest = destino
    dif_linha = linha_dest - linha_atual
    dif_col = col_dest - col_atual

    #Impedindo que o jogador tente mover a peça para a casa que a peça está;
    if ((linha_dest == linha_atual) and (col_dest == col_atual)):
        return False

    #Validando o movimento;
    if (dif_linha == dif_col) or (dif_linha == -dif_col):
        freeway = caminho_livre(tabuleiro, origem, destino)
        if (freeway == True):
            return True
        else:
            return False
    else:
        return False

def movimento_dama(tabuleiro, origem, destino) -> bool:
    """
    Função para o movimento da dama;
    tabuleiro: matriz que vai representar o tabuleiro;
    origem: tupla com a posição de origem da peça;
    destino: tupla com a posição de destino da peça;
    retorna: True se o movimento for válido, ou False se o movimento for inválido.
    """
    #Reaproveitando o código da torre e do bispo para executar o movimento da dama.
    return movimento_bispo(tabuleiro, origem, destino) or movimento_torre(tabuleiro, origem, destino)

