def movimento_rei(origem, destino):
    """
    Verifica se o movimento do rei é válido.

    O rei pode movimentar-se apenas uma casa por vez,
    em qualquer direção: horizontal, vertical ou diagonal.

    Parâmetros:
    origem: posição atual do rei (linha, coluna).
    destino: posição desejada (linha, coluna).

    Retorno:
    True se o movimento for válido.
    False se o movimento for inválido.
    """

    diferenca_linha = abs(destino[0] - origem[0])
    diferenca_coluna = abs(destino[1] - origem[1])

    if diferenca_linha <= 1 and diferenca_coluna <= 1:
        if diferenca_linha != 0 or diferenca_coluna != 0:
            return True

    return False


def movimento_cavalo(origem, destino):
    """
    Verifica se o movimento do cavalo é válido.

    O cavalo movimenta-se em formato de L:
    duas casas em uma direção e uma casa na outra.

    Parâmetros:
    origem: posição atual do cavalo (linha, coluna).
    destino: posição desejada (linha, coluna).

    Retorno:
    True se o movimento for válido.
    False se o movimento for inválido.
    """

    diferenca_linha = abs(destino[0] - origem[0])
    diferenca_coluna = abs(destino[1] - origem[1])

    if (diferenca_linha == 2 and diferenca_coluna == 1) or \
       (diferenca_linha == 1 and diferenca_coluna == 2):
        return True

    return False


def mesma_cor(peca1, peca2):
    """
    Verifica se duas peças pertencem ao mesmo jogador.

    Peças brancas são representadas por letras maiúsculas.
    Peças pretas são representadas por letras minúsculas.

    Parâmetros:
    peca1: primeira peça.
    peca2: segunda peça.

    Retorno:
    True se as peças forem da mesma cor.
    False se forem de cores diferentes ou vazias.
    """

    if peca1 == " " or peca2 == " ":
        return False

    if peca1.isupper() == peca2.isupper():
        return True

    return False


def captura_permitida(tabuleiro, origem, destino):
    """
    Verifica se uma peça pode capturar outra.

    A captura é permitida somente quando:
    - A posição de origem possui uma peça.
    - A posição de destino possui uma peça adversária.
    - A peça de destino não é o rei.

    Parâmetros:
    tabuleiro: matriz 8x8 representando o tabuleiro.
    origem: posição da peça atacante (linha, coluna).
    destino: posição da peça adversária (linha, coluna).

    Retorno:
    True se a captura for permitida.
    False se a captura não for permitida.
    """

    if not (0 <= origem[0] < 8 and 0 <= origem[1] < 8):
        return False

    if not (0 <= destino[0] < 8 and 0 <= destino[1] < 8):
        return False

    peca_origem = tabuleiro[origem[0]][origem[1]]
    peca_destino = tabuleiro[destino[0]][destino[1]]

    if peca_origem == " " or peca_destino == " ":
        return False

    if peca_destino.lower() == "k":
        return False

    if mesma_cor(peca_origem, peca_destino):
        return False

    return True


def capturar_peca(tabuleiro, origem, destino):
    """
    Realiza a captura de uma peça adversária no tabuleiro.

    Quando a captura é permitida:
    - A peça atacante ocupa a posição da peça adversária.
    - A posição de origem fica vazia.

    Caso a captura não seja permitida, o tabuleiro
    permanece sem alterações.

    Parâmetros:
    tabuleiro: matriz 8x8 representando o tabuleiro.
    origem: posição da peça atacante (linha, coluna).
    destino: posição da peça adversária (linha, coluna).

    Retorno:
    True se a captura for realizada.
    False se a captura não for realizada.
    """

    if captura_permitida(tabuleiro, origem, destino):

        peca = tabuleiro[origem[0]][origem[1]]

        tabuleiro[destino[0]][destino[1]] = peca

        tabuleiro[origem[0]][origem[1]] = " "

        return True

    return False
