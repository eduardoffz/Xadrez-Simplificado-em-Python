"""
testes.py — Suite de Testes Automatizados
Integrante 4 — Projeto de Xadrez em Python

Cobre:
    ✔ Movimento do peão (simples, duplo, diagonal, inválidos)
    ✔ Turnos (alternância e controle)
    ✔ Peças lineares: Torre, Bispo e Dama  (via pecas_linha.py)
    ✔ Peças especiais: Rei e Cavalo        (via capturas.py)
    ✔ Obstrução no caminho das peças lineares
    ✔ Capturas (permitidas e bloqueadas)
    ✔ Movimentos inválidos de todas as peças

Execute com:
    python testes.py
ou:
    python -m pytest testes.py -v
"""

import sys
import unittest

# ── Importações dos módulos do projeto ──────────────────────────────────────
# Cada módulo é desenvolvido por um integrante diferente.
# Caso algum ainda não exista, o bloco try/except emite aviso e pula os testes.

try:
    from tabuleiro import criar_tabuleiro, posicao_valida, mover_peca
    TABULEIRO_OK = True
except ImportError:
    TABULEIRO_OK = False
    print("[AVISO] tabuleiro.py não encontrado — testes de tabuleiro pulados.")

try:
    from pecas_linha import movimento_torre, movimento_bispo, movimento_dama, caminho_livre
    PECAS_LINHA_OK = True
except ImportError:
    PECAS_LINHA_OK = False
    print("[AVISO] pecas_linha.py não encontrado — testes de peças lineares pulados.")

try:
    from capturas import (movimento_rei, movimento_cavalo,
                          mesma_cor, captura_permitida, capturar_peca)
    CAPTURAS_OK = True
except ImportError:
    CAPTURAS_OK = False
    print("[AVISO] capturas.py não encontrado — testes de capturas pulados.")

from peao import (movimento_peao, controlar_turno,
                  trocar_turno, resetar_turno)


# ===========================================================================
# HELPERS DE TABULEIRO MÍNIMO (para os testes do Integrante 4 rodarem sozinhos)
# ===========================================================================

def _tab_vazio():
    """Cria um tabuleiro 8x8 vazio (None em cada célula)."""
    return [[None] * 8 for _ in range(8)]


def _tab_padrao():
    """
    Cria um tabuleiro padrão simples usando convenção de letras:
        Brancas = MAIÚSCULAS  |  Pretas = minúsculas
        P/p = Peão, T/t = Torre, C/c = Cavalo, B/b = Bispo, D/d = Dama, R/r = Rei
    """
    tab = _tab_vazio()
    # Peças pretas (linha 0 e 1)
    tab[0] = ['t','c','b','d','r','b','c','t']
    tab[1] = ['p','p','p','p','p','p','p','p']
    # Peças brancas (linha 6 e 7)
    tab[6] = ['P','P','P','P','P','P','P','P']
    tab[7] = ['T','C','B','D','R','B','C','T']
    return tab


# ===========================================================================
# TESTES — CONTROLE DE TURNO
# ===========================================================================

class TesteTurnos(unittest.TestCase):
    """Testa a lógica de alternância de turnos."""

    def setUp(self):
        """Garante que cada teste começa com turno nas brancas."""
        resetar_turno()

    def test_turno_inicial_e_brancas(self):
        """O jogo deve começar com as brancas."""
        self.assertEqual(controlar_turno(), "brancas")

    def test_trocar_turno_de_brancas_para_pretas(self):
        """Após trocar, o turno deve ser das pretas."""
        trocar_turno()
        self.assertEqual(controlar_turno(), "pretas")

    def test_trocar_turno_de_pretas_para_brancas(self):
        """Após duas trocas, deve voltar para brancas."""
        trocar_turno()
        trocar_turno()
        self.assertEqual(controlar_turno(), "brancas")

    def test_sequencia_de_quatro_trocas(self):
        """Simula quatro trocas: B → P → B → P → B."""
        estados = []
        for _ in range(4):
            trocar_turno()
            estados.append(controlar_turno())
        self.assertEqual(estados, ["pretas", "brancas", "pretas", "brancas"])

    def test_resetar_turno(self):
        """resetar_turno() deve sempre retornar 'brancas'."""
        trocar_turno()  # vai para pretas
        resultado = resetar_turno()
        self.assertEqual(resultado, "brancas")
        self.assertEqual(controlar_turno(), "brancas")


# ===========================================================================
# TESTES — PEÃO BRANCO
# ===========================================================================

class TestePeaoBranco(unittest.TestCase):
    """Testa todos os movimentos possíveis do peão branco."""

    def setUp(self):
        self.tab = _tab_padrao()

    # ── Movimentos válidos ──────────────────────────────────────────────────

    def test_avanco_simples(self):
        """Peão branco avança uma casa normalmente."""
        self.assertTrue(movimento_peao(self.tab, (6, 0), (5, 0), "brancas"))

    def test_avanco_duplo_na_posicao_inicial(self):
        """Peão branco avança duas casas na primeira jogada."""
        self.assertTrue(movimento_peao(self.tab, (6, 0), (4, 0), "brancas"))

    def test_captura_diagonal_esquerda(self):
        """Peão branco captura peça preta na diagonal esquerda."""
        tab = _tab_vazio()
        tab[6][3] = 'P'   # peão branco
        tab[5][2] = 'p'   # peão preto (adversário)
        self.assertTrue(movimento_peao(tab, (6, 3), (5, 2), "brancas"))

    def test_captura_diagonal_direita(self):
        """Peão branco captura peça preta na diagonal direita."""
        tab = _tab_vazio()
        tab[6][3] = 'P'
        tab[5][4] = 'p'
        self.assertTrue(movimento_peao(tab, (6, 3), (5, 4), "brancas"))

    # ── Movimentos inválidos ────────────────────────────────────────────────

    def test_nao_anda_para_tras(self):
        """Peão branco não pode andar para trás."""
        self.assertFalse(movimento_peao(self.tab, (6, 0), (7, 0), "brancas"))

    def test_nao_avanca_duas_casas_fora_da_posicao_inicial(self):
        """Peão branco não avança duas casas fora da posição inicial."""
        tab = _tab_vazio()
        tab[5][0] = 'P'   # peão já movido (linha 5)
        self.assertFalse(movimento_peao(tab, (5, 0), (3, 0), "brancas"))

    def test_nao_captura_a_frente(self):
        """Peão branco não pode capturar indo reto para frente."""
        tab = _tab_vazio()
        tab[6][0] = 'P'
        tab[5][0] = 'p'   # bloqueando o caminho
        self.assertFalse(movimento_peao(tab, (6, 0), (5, 0), "brancas"))

    def test_nao_captura_propria_peca_na_diagonal(self):
        """Peão branco não pode capturar peça própria na diagonal."""
        tab = _tab_vazio()
        tab[6][3] = 'P'
        tab[5][4] = 'B'   # peça branca (mesma cor)
        self.assertFalse(movimento_peao(tab, (6, 3), (5, 4), "brancas"))

    def test_diagonal_vazia_invalida(self):
        """Peão não pode ir na diagonal se não houver captura."""
        tab = _tab_vazio()
        tab[6][3] = 'P'
        self.assertFalse(movimento_peao(tab, (6, 3), (5, 4), "brancas"))

    def test_avanco_duplo_bloqueado_por_peca_intermediaria(self):
        """Peão branco não avança duas casas se houver peça no meio."""
        tab = _tab_vazio()
        tab[6][0] = 'P'
        tab[5][0] = 'p'   # peça bloqueando a passagem
        self.assertFalse(movimento_peao(tab, (6, 0), (4, 0), "brancas"))

    def test_movimento_lateral_invalido(self):
        """Peão não pode se mover lateralmente."""
        self.assertFalse(movimento_peao(self.tab, (6, 0), (6, 1), "brancas"))

    def test_movimento_de_duas_casas_fora_da_coluna_invalido(self):
        """Peão não pode ir para frente e para o lado ao mesmo tempo."""
        self.assertFalse(movimento_peao(self.tab, (6, 0), (4, 1), "brancas"))


# ===========================================================================
# TESTES — PEÃO PRETO
# ===========================================================================

class TestePeaoPreto(unittest.TestCase):
    """Testa todos os movimentos possíveis do peão preto."""

    def setUp(self):
        self.tab = _tab_padrao()

    def test_avanco_simples(self):
        """Peão preto avança uma casa (sentido oposto ao branco)."""
        self.assertTrue(movimento_peao(self.tab, (1, 0), (2, 0), "pretas"))

    def test_avanco_duplo_na_posicao_inicial(self):
        """Peão preto avança duas casas na primeira jogada."""
        self.assertTrue(movimento_peao(self.tab, (1, 0), (3, 0), "pretas"))

    def test_captura_diagonal(self):
        """Peão preto captura peça branca na diagonal."""
        tab = _tab_vazio()
        tab[1][3] = 'p'
        tab[2][4] = 'P'   # peça branca (adversário)
        self.assertTrue(movimento_peao(tab, (1, 3), (2, 4), "pretas"))

    def test_nao_anda_para_tras(self):
        """Peão preto não pode andar para trás (direção das brancas)."""
        self.assertFalse(movimento_peao(self.tab, (1, 0), (0, 0), "pretas"))

    def test_nao_captura_propria_peca(self):
        """Peão preto não captura peça preta."""
        tab = _tab_vazio()
        tab[1][3] = 'p'
        tab[2][4] = 'p'   # mesma cor
        self.assertFalse(movimento_peao(tab, (1, 3), (2, 4), "pretas"))


# ===========================================================================
# TESTES — TORRE  (requerem pecas_linha.py)
# ===========================================================================

@unittest.skipUnless(PECAS_LINHA_OK, "pecas_linha.py não disponível")
class TesteTorre(unittest.TestCase):
    """Testa os movimentos da torre."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_movimento_horizontal_valido(self):
        """Torre se move horizontalmente sem obstáculos."""
        self.tab[0][0] = 'T'
        self.assertTrue(movimento_torre(self.tab, (0, 0), (0, 5)))

    def test_movimento_vertical_valido(self):
        """Torre se move verticalmente sem obstáculos."""
        self.tab[0][0] = 'T'
        self.assertTrue(movimento_torre(self.tab, (0, 0), (5, 0)))

    def test_movimento_diagonal_invalido(self):
        """Torre não pode se mover na diagonal."""
        self.tab[0][0] = 'T'
        self.assertFalse(movimento_torre(self.tab, (0, 0), (3, 3)))

    def test_obstrucao_no_caminho(self):
        """Torre não pode atravessar peças."""
        self.tab[0][0] = 'T'
        self.tab[0][3] = 'P'   # peça bloqueando
        self.assertFalse(movimento_torre(self.tab, (0, 0), (0, 5)))

    def test_captura_adversario(self):
        """Torre pode capturar peça adversária."""
        self.tab[0][0] = 'T'
        self.tab[0][5] = 'p'   # peça preta (adversário)
        self.assertTrue(movimento_torre(self.tab, (0, 0), (0, 5)))

    def test_nao_captura_mesma_cor(self):
        """Torre não pode capturar peça da mesma cor."""
        self.tab[0][0] = 'T'
        self.tab[0][5] = 'P'   # peça branca (mesma cor)
        self.assertFalse(movimento_torre(self.tab, (0, 0), (0, 5)))


# ===========================================================================
# TESTES — BISPO  (requerem pecas_linha.py)
# ===========================================================================

@unittest.skipUnless(PECAS_LINHA_OK, "pecas_linha.py não disponível")
class TesteBispo(unittest.TestCase):
    """Testa os movimentos do bispo."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_movimento_diagonal_valido(self):
        """Bispo se move na diagonal sem obstáculos."""
        self.tab[1][1] = 'B'
        self.assertTrue(movimento_bispo(self.tab, (1, 1), (4, 4)))

    def test_movimento_reto_invalido(self):
        """Bispo não pode se mover em linha reta."""
        self.tab[1][1] = 'B'
        self.assertFalse(movimento_bispo(self.tab, (1, 1), (1, 5)))

    def test_obstrucao_diagonal(self):
        """Bispo não atravessa peças na diagonal."""
        self.tab[1][1] = 'B'
        self.tab[2][2] = 'P'   # bloqueando o caminho
        self.assertFalse(movimento_bispo(self.tab, (1, 1), (4, 4)))


# ===========================================================================
# TESTES — DAMA  (requerem pecas_linha.py)
# ===========================================================================

@unittest.skipUnless(PECAS_LINHA_OK, "pecas_linha.py não disponível")
class TesteDama(unittest.TestCase):
    """Testa os movimentos da dama."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_movimento_horizontal(self):
        """Dama se move horizontalmente."""
        self.tab[0][0] = 'D'
        self.assertTrue(movimento_dama(self.tab, (0, 0), (0, 7)))

    def test_movimento_vertical(self):
        """Dama se move verticalmente."""
        self.tab[0][0] = 'D'
        self.assertTrue(movimento_dama(self.tab, (0, 0), (7, 0)))

    def test_movimento_diagonal(self):
        """Dama se move na diagonal."""
        self.tab[0][0] = 'D'
        self.assertTrue(movimento_dama(self.tab, (0, 0), (7, 7)))

    def test_movimento_invalido_em_L(self):
        """Dama não se move em L (isso é do cavalo)."""
        self.tab[0][0] = 'D'
        self.assertFalse(movimento_dama(self.tab, (0, 0), (2, 1)))

    def test_obstrucao(self):
        """Dama não atravessa peças."""
        self.tab[0][0] = 'D'
        self.tab[3][3] = 'p'
        self.assertFalse(movimento_dama(self.tab, (0, 0), (7, 7)))


# ===========================================================================
# TESTES — REI  (requerem capturas.py)
# ===========================================================================

@unittest.skipUnless(CAPTURAS_OK, "capturas.py não disponível")
class TesteRei(unittest.TestCase):
    """Testa os movimentos do rei."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_movimento_uma_casa_valido(self):
        """Rei se move uma casa em qualquer direção."""
        self.tab[4][4] = 'R'
        self.assertTrue(movimento_rei(self.tab, (4, 4), (5, 5)))

    def test_movimento_duas_casas_invalido(self):
        """Rei não pode se mover mais de uma casa."""
        self.tab[4][4] = 'R'
        self.assertFalse(movimento_rei(self.tab, (4, 4), (6, 6)))

    def test_captura_adversario(self):
        """Rei captura peça adversária adjacente."""
        self.tab[4][4] = 'R'
        self.tab[5][5] = 'r'   # rei preto (adversário)
        self.assertTrue(movimento_rei(self.tab, (4, 4), (5, 5)))

    def test_nao_captura_mesma_cor(self):
        """Rei não captura peça da mesma cor."""
        self.tab[4][4] = 'R'
        self.tab[5][5] = 'P'
        self.assertFalse(movimento_rei(self.tab, (4, 4), (5, 5)))


# ===========================================================================
# TESTES — CAVALO  (requerem capturas.py)
# ===========================================================================

@unittest.skipUnless(CAPTURAS_OK, "capturas.py não disponível")
class TesteCavalo(unittest.TestCase):
    """Testa os movimentos do cavalo."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_movimento_em_L_valido(self):
        """Cavalo se move em L (2+1 casas)."""
        self.tab[4][4] = 'C'
        self.assertTrue(movimento_cavalo(self.tab, (4, 4), (6, 5)))

    def test_movimento_invalido(self):
        """Cavalo não pode se mover em linha reta."""
        self.tab[4][4] = 'C'
        self.assertFalse(movimento_cavalo(self.tab, (4, 4), (4, 6)))

    def test_cavalo_pula_pecas(self):
        """Cavalo pode pular sobre outras peças."""
        self.tab[4][4] = 'C'
        self.tab[5][4] = 'P'   # peça no caminho — deve ser ignorada
        self.tab[4][5] = 'P'
        self.assertTrue(movimento_cavalo(self.tab, (4, 4), (6, 5)))


# ===========================================================================
# TESTES — CAPTURAS  (requerem capturas.py)
# ===========================================================================

@unittest.skipUnless(CAPTURAS_OK, "capturas.py não disponível")
class TesteCapturas(unittest.TestCase):
    """Testa o sistema de capturas."""

    def setUp(self):
        self.tab = _tab_vazio()

    def test_captura_permitida_cores_diferentes(self):
        """Captura é permitida entre peças de cores diferentes."""
        self.tab[3][3] = 'T'
        self.tab[3][7] = 't'
        self.assertTrue(captura_permitida(self.tab, (3, 3), (3, 7), "brancas"))

    def test_captura_bloqueada_mesma_cor(self):
        """Captura é bloqueada quando as peças são da mesma cor."""
        self.tab[3][3] = 'T'
        self.tab[3][7] = 'P'   # mesma cor
        self.assertFalse(captura_permitida(self.tab, (3, 3), (3, 7), "brancas"))

    def test_capturar_peca_remove_do_tabuleiro(self):
        """Após captura, o destino contém a peça capturante e a origem fica vazia."""
        self.tab[3][3] = 'T'
        self.tab[3][7] = 't'
        capturar_peca(self.tab, (3, 3), (3, 7))
        self.assertEqual(self.tab[3][7], 'T')
        self.assertIsNone(self.tab[3][3])


# ===========================================================================
# TESTES — TABULEIRO  (requerem tabuleiro.py)
# ===========================================================================

@unittest.skipUnless(TABULEIRO_OK, "tabuleiro.py não disponível")
class TesteTabuleiro(unittest.TestCase):
    """Testa funções do tabuleiro."""

    def test_posicao_valida_dentro_dos_limites(self):
        """Posição (0,0) deve ser válida."""
        self.assertTrue(posicao_valida((0, 0)))

    def test_posicao_valida_extremo(self):
        """Posição (7,7) deve ser válida."""
        self.assertTrue(posicao_valida((7, 7)))

    def test_posicao_invalida_negativa(self):
        """Posição negativa deve ser inválida."""
        self.assertFalse(posicao_valida((-1, 0)))

    def test_posicao_invalida_fora_do_limite(self):
        """Posição (8,0) deve ser inválida."""
        self.assertFalse(posicao_valida((8, 0)))

    def test_criar_tabuleiro_8x8(self):
        """O tabuleiro criado deve ter 8 linhas e 8 colunas."""
        tab = criar_tabuleiro()
        self.assertEqual(len(tab), 8)
        for linha in tab:
            self.assertEqual(len(linha), 8)

    def test_mover_peca(self):
        """mover_peca() deve atualizar o tabuleiro corretamente."""
        tab = criar_tabuleiro()
        peca = tab[6][0]  # peão branco
        mover_peca(tab, (6, 0), (5, 0))
        self.assertEqual(tab[5][0], peca)
        self.assertIsNone(tab[6][0])


# ===========================================================================
# ENTRADA PRINCIPAL
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SUITE DE TESTES — XADREZ EM PYTHON")
    print("  Integrante 4")
    print("=" * 60)

    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()

    # Adiciona os grupos de teste na ordem de apresentação
    grupos = [
        TesteTurnos,
        TestePeaoBranco,
        TestePeaoPreto,
        TesteTorre,
        TesteBispo,
        TesteDama,
        TesteRei,
        TesteCavalo,
        TesteCapturas,
        TesteTabuleiro,
    ]

    for grupo in grupos:
        suite.addTests(loader.loadTestsFromTestCase(grupo))

    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    print("\n" + "=" * 60)
    total    = resultado.testsRun
    falhas   = len(resultado.failures) + len(resultado.errors)
    passou   = total - falhas
    print(f"  RESULTADO FINAL: {passou}/{total} testes passaram")
    if falhas == 0:
        print("  ✅ Todos os testes passaram!")
    else:
        print(f"  ❌ {falhas} teste(s) falharam.")
    print("=" * 60)

    sys.exit(0 if falhas == 0 else 1)

