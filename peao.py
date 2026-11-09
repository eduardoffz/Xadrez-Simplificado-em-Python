"""
peao.py — Módulo do Peão e Controle de Turnos
Integrante 4 — Projeto de Xadrez em Python

Responsabilidades:
    - Lógica de movimentação do peão (branco e preto)
    - Controle e troca de turnos
"""

# ---------------------------------------------------------------------------
# CONTROLE DE TURNO
# ---------------------------------------------------------------------------

# Estado global do turno (usado por todo o sistema)
turno_atual = "brancas"


def controlar_turno():
    """
    Retorna qual jogador deve jogar agora.

    Retorna:
        str: "brancas" ou "pretas"

    Exemplo:
        >>> controlar_turno()
        'brancas'
    """
    return turno_atual


def trocar_turno():
    """
    Alterna o turno entre brancas e pretas.

    Modifica a variável global 'turno_atual'.
    Deve ser chamada após cada jogada válida.

    Retorna:
        str: O novo turno após a troca.

    Exemplo:
        >>> trocar_turno()
        'pretas'   # (se o turno anterior era 'brancas')
    """
    global turno_atual
    turno_atual = "pretas" if turno_atual == "brancas" else "brancas"
    return turno_atual


def resetar_turno():
    """
    Reinicia o turno para 'brancas' (usado no início da partida ou nos testes).

    Retorna:
        str: "brancas"
    """
    global turno_atual
    turno_atual = "brancas"
    return turno_atual


# ---------------------------------------------------------------------------
# MOVIMENTO DO PEÃO
# ---------------------------------------------------------------------------

def movimento_peao(tabuleiro, origem, destino, turno):
    """
    Verifica se o movimento de um peão é válido conforme as regras do xadrez.

    Regras implementadas:
        - Avança uma casa para frente.
        - Avança duas casas na primeira jogada (linha inicial).
        - Captura na diagonal (somente se houver peça adversária).
        - Não pode andar para trás.
        - Não pode atravessar peças ao avançar duas casas.

    Parâmetros:
        tabuleiro (list[list]): Matriz 8x8 representando o tabuleiro.
        origem  (tuple): Posição atual do peão  (linha, coluna).
        destino (tuple): Posição de destino       (linha, coluna).
        turno   (str):  "brancas" ou "pretas" — indica a cor do peão.

    Retorna:
        bool: True se o movimento for válido, False caso contrário.

    Exemplos:
        >>> movimento_peao(tab, (6, 0), (5, 0), "brancas")
        True   # avança uma casa
        >>> movimento_peao(tab, (6, 0), (4, 0), "brancas")
        True   # avança duas casas na primeira jogada
        >>> movimento_peao(tab, (6, 0), (7, 0), "brancas")
        False  # peão não anda para trás
    """
    lin_o, col_o = origem
    lin_d, col_d = destino

    # Brancas sobem no tabuleiro (linha decresce), pretas descem (linha cresce)
    direcao    = -1 if turno == "brancas" else 1
    linha_base = 6  if turno == "brancas" else 1   # linha inicial do peão

    peca_destino = tabuleiro[lin_d][col_d]

    # ── Avanço simples (uma casa à frente, mesma coluna) ────────────────────
    if col_d == col_o and lin_d == lin_o + direcao:
        # A casa de destino deve estar vazia
        if peca_destino is None or peca_destino == " ":
            return True
        return False  # caminho bloqueado

    # ── Avanço duplo (duas casas, apenas na posição inicial) ────────────────
    if col_d == col_o and lin_d == lin_o + 2 * direcao and lin_o == linha_base:
        casa_intermediaria = tabuleiro[lin_o + direcao][col_o]
        if (peca_destino is None or peca_destino == " ") and \
           (casa_intermediaria is None or casa_intermediaria == " "):
            return True
        return False  # caminho bloqueado

    # ── Captura na diagonal (uma casa à frente na diagonal) ─────────────────
    if abs(col_d - col_o) == 1 and lin_d == lin_o + direcao:
        if peca_destino is not None and peca_destino != " ":
            # Verifica se a peça no destino é do adversário
            if _e_adversario(peca_destino, turno):
                return True
        return False  # diagonal sem captura não é válida

    # Qualquer outro caso é inválido
    return False


# ---------------------------------------------------------------------------
# HELPERS INTERNOS
# ---------------------------------------------------------------------------

def _e_adversario(peca, turno):
    """
    Verifica se uma peça pertence ao adversário do turno atual.

    Convenção adotada (compatível com tabuleiro.py):
        - Peças brancas: representadas por strings MAIÚSCULAS (ex.: 'P', 'T', 'R')
        - Peças pretas:  representadas por strings minúsculas (ex.: 'p', 't', 'r')

    Parâmetros:
        peca  (str): Símbolo da peça no tabuleiro.
        turno (str): "brancas" ou "pretas".

    Retorna:
        bool: True se a peça for do adversário.
    """
    if peca is None or peca == " ":
        return False
    if turno == "brancas":
        return peca.islower()   # brancas capturam peças pretas (minúsculas)
    else:
        return peca.isupper()   # pretas capturam peças brancas (maiúsculas)


def peao_na_posicao_inicial(tabuleiro, origem, turno):
    """
    Verifica se o peão está em sua posição inicial (linha de largada).

    Parâmetros:
        tabuleiro (list[list]): Tabuleiro 8x8.
        origem    (tuple):      Posição (linha, coluna) do peão.
        turno     (str):        "brancas" ou "pretas".

    Retorna:
        bool: True se o peão estiver na linha inicial.
    """
    lin, _ = origem
    return lin == 6 if turno == "brancas" else lin == 1

