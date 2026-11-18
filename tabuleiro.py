icones = {
    "T": "♖", "C": "♘", "B": "♗", "D": "♕", "R": "♔", "P": "♙",
    "t": "♜", "c": "♞", "b": "♝", "d": "♛", "r": "♚", "p": "♟",
}

vazio = "."


def criar_tabuleiro():
    
    tabuleiro = []
    
    for i in range(8):
        linha = []
        
        for j in range(8):
            linha.append(vazio)
            
        tabuleiro.append(linha)
        

    ordem = ["t", "c", "b", "d", "r", "b", "c", "t"]

    for coluna in range(8):
        
        tabuleiro[0][coluna] = ordem[coluna]
        tabuleiro[1][coluna] = "p"
        tabuleiro[6][coluna] = "P"
        tabuleiro[7][coluna] = ordem[coluna].upper()
        
    return tabuleiro
        
        
def mostrar_tabuleiro(tabuleiro):
    
    print()
    print("    a b c d e f g h")
    print("   -----------------")
    for linha in range(8):
        casas = []
        for coluna in range(8):
            peca = tabuleiro[linha][coluna]
            if peca == vazio:
                casas.append(vazio)
            
            else:
                casas.append(icones[peca])
                
        print(8 - linha, "|", " ".join(casas), "|", 8 - linha)
    print("   -----------------")
    print("    a b c d e f g h")
    print()



def posicao_valida(posicao):
    
    if not isinstance(posicao, tuple) or len(posicao) != 2:
        return False
    
    linha, coluna = posicao
    
    if not isinstance(linha, int) or not isinstance(coluna, int):
        return False
    
    if 0 <= linha < 8 and 0 <= coluna < 8:
        return True
    
    else:
        return False
    
    
def mover_peca(tabuleiro, origem:tuple, destino:tuple):
    
    linha_origem , coluna_origem = origem
    linha_destino , coluna_destino = destino
    
    peca = tabuleiro[linha_origem] [coluna_origem]
    removida = tabuleiro[linha_destino] [coluna_destino]
    
    tabuleiro[linha_destino] [coluna_destino] = peca
    tabuleiro[linha_origem]  [coluna_origem] = vazio
    
    return removida

# ---------- testes ----------
t = criar_tabuleiro()
mostrar_tabuleiro(t)

print("posicao_valida")
print((0, 0), posicao_valida((0, 0)))      
print((7, 7), posicao_valida((7, 7)))      
print((8, 0), posicao_valida((8, 0)))      
print((0, -1), posicao_valida((0, -1)))   

print("mover_peca")
print("destino vazio:", mover_peca(t, (6, 4), (4, 4)))   
mostrar_tabuleiro(t)

t[5][5] = "p"
print("captura:", mover_peca(t, (7, 6), (5, 5)))        
mostrar_tabuleiro(t)