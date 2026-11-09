# Xadrez em Python 🏁

Projeto acadêmico de simulação de xadrez desenvolvido em Python, com foco em modularização, validação de regras e testes automatizados.

---

## Estrutura do Projeto

```
xadrez/
├── main.py          # Simulação da partida (integração final)
├── tabuleiro.py     # Integrante 1 — Tabuleiro e estrutura
├── pecas_linha.py   # Integrante 2 — Torre, Bispo e Dama
├── capturas.py      # Integrante 3 — Rei, Cavalo e sistema de capturas
├── peao.py          # Integrante 4 — Peão e controle de turnos
├── testes.py        # Integrante 4 — Testes automatizados
└── README.md        # Esta documentação
```

---

## Módulos

### `tabuleiro.py` — Integrante 1
Responsável pela infraestrutura do jogo.

| Função | Descrição |
|---|---|
| `criar_tabuleiro()` | Cria e popula o tabuleiro 8×8 com as peças nas posições iniciais |
| `mostrar_tabuleiro(tab)` | Exibe o tabuleiro no terminal de forma organizada |
| `posicao_valida(pos)` | Verifica se uma posição está dentro dos limites do tabuleiro |
| `mover_peca(tab, origem, destino)` | Atualiza o tabuleiro após um movimento |

---

### `pecas_linha.py` — Integrante 2
Implementa peças de movimento linear e verifica obstruções.

| Função | Descrição |
|---|---|
| `movimento_torre(tab, origem, destino)` | Valida movimento horizontal/vertical da torre |
| `movimento_bispo(tab, origem, destino)` | Valida movimento diagonal do bispo |
| `movimento_dama(tab, origem, destino)` | Valida movimento da dama (torre + bispo) |
| `caminho_livre(tab, origem, destino)` | Verifica se não há peças obstruindo o caminho |

---

### `capturas.py` — Integrante 3
Implementa peças especiais e o sistema de capturas.

| Função | Descrição |
|---|---|
| `movimento_rei(tab, origem, destino)` | Valida movimento do rei (1 casa em qualquer direção) |
| `movimento_cavalo(tab, origem, destino)` | Valida movimento do cavalo (em L, pula peças) |
| `mesma_cor(peca1, peca2)` | Verifica se duas peças são da mesma cor |
| `captura_permitida(tab, origem, destino, turno)` | Verifica se uma captura é legal |
| `capturar_peca(tab, origem, destino)` | Executa a captura e atualiza o tabuleiro |

---

### `peao.py` — Integrante 4
Implementa a lógica do peão e o controle de turnos.

| Função | Descrição |
|---|---|
| `movimento_peao(tab, origem, destino, turno)` | Valida todas as regras de movimento do peão |
| `controlar_turno()` | Retorna o jogador do turno atual (`"brancas"` ou `"pretas"`) |
| `trocar_turno()` | Alterna o turno entre brancas e pretas |
| `resetar_turno()` | Reinicia o turno para `"brancas"` |

---

### `testes.py` — Integrante 4
Suite de testes automatizados com `unittest`.

**Cobertura:**
- ✅ Turnos (alternância, reset, sequência)
- ✅ Peão branco (avanço simples, duplo, diagonal, inválidos)
- ✅ Peão preto (mesmas regras, direção oposta)
- ✅ Torre (horizontal, vertical, obstrução, captura)
- ✅ Bispo (diagonal, obstrução, movimento reto inválido)
- ✅ Dama (todos os eixos, obstrução, movimento em L inválido)
- ✅ Rei (uma casa, mais de uma casa inválido, captura)
- ✅ Cavalo (movimento em L, pular peças, movimento inválido)
- ✅ Capturas (permitidas, bloqueadas, remoção do tabuleiro)
- ✅ Tabuleiro (limites, dimensões, mover peça)

---

## Convenção de Peças

| Símbolo | Peça | Cor |
|---|---|---|
| `P` | Peão | Branca |
| `T` | Torre | Branca |
| `C` | Cavalo | Branca |
| `B` | Bispo | Branca |
| `D` | Dama | Branca |
| `R` | Rei | Branca |
| `p` | Peão | Preta |
| `t` | Torre | Preta |
| `c` | Cavalo | Preta |
| `b` | Bispo | Preta |
| `d` | Dama | Preta |
| `r` | Rei | Preto |

> **Regra:** Letras **MAIÚSCULAS** = peças brancas · Letras **minúsculas** = peças pretas

---

## Regras do Peão Implementadas

```
✔ Avança uma casa para frente
✔ Avança duas casas na posição inicial (linha 6 para brancas, linha 1 para pretas)
✔ Captura na diagonal (somente se houver peça adversária)
✗ Não anda para trás
✗ Não atravessa peças ao avançar duas casas
✗ Não captura reto para frente
✗ Não vai na diagonal sem captura
✗ Não captura peça da mesma cor
```

---

## Como Executar os Testes

```bash
# Execução direta
python testes.py

# Com pytest (mais visual)
pip install pytest
python -m pytest testes.py -v
```

**Saída esperada:**

```
============================================================
  SUITE DE TESTES — XADREZ EM PYTHON
  Integrante 4
============================================================
test_turno_inicial_e_brancas ... ok
test_trocar_turno_de_brancas_para_pretas ... ok
...
============================================================
  RESULTADO FINAL: 30/30 testes passaram
  ✅ Todos os testes passaram!
============================================================
```

> **Nota:** Testes que dependem de módulos ainda não criados (dos outros integrantes) são pulados automaticamente com aviso, sem quebrar a execução.

---

## Como Executar a Simulação

```bash
python main.py
```

---

## Requisitos

- Python 3.8 ou superior
- Sem dependências externas (apenas `unittest` da biblioteca padrão)

---

## Autores

| Integrante | Módulo |
|---|---|
| Integrante 1 | `tabuleiro.py` |
| Integrante 2 | `pecas_linha.py` |
| Integrante 3 | `capturas.py` |
| Integrante 4 | `peao.py`, `testes.py`, `README.md` |

