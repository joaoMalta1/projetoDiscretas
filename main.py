from __future__ import annotations
import random, time, math, argparse
from collections import deque
from pathlib import Path
from xml.sax.saxutils import escape


Grafo = dict[int, set[int]]
N = 10
P = 0.30
SEED = 482


def gerar_grafo(qtd_vertices, prob, rng=random):
    if qtd_vertices < 1:
        raise ValueError("qtd_vertices deve ser positivo")
    if not 0 <= prob <= 1:
        raise ValueError("probabilidade deve estar entre 0 e 1")

    grafo = {}
    for v in range(1, qtd_vertices + 1):
        grafo[v] = set() # gera um conjunto pra cada um dos vertices do grafo

    for u in range(1, qtd_vertices + 1): # para cada vertice do grafo
        for v in range(u + 1, qtd_vertices + 1):# percorre os outros vertices sem ser o atual
            if rng.random() < prob: # calcula a chance de ter a aresta
                grafo[u].add(v) # adciona a aresta tanto no nó u quanto no nó v
                grafo[v].add(u)
    return grafo


def arestas(grafo): # retornar as aretas ordenadas
    arestas = []

    for u, vizinhos in grafo.items():     # percorre u e seus vizinhos
        for v in vizinhos:                # para cada vizinho v
            if u < v:                     # se u for menor que v adciona tupla na lista
                arestas.append((u, v))
    arestas_ordenadas = sorted(arestas)

    return arestas_ordenadas


def grafo_de_arestas(n_vertices, lista): #funcao que ajuda a testar grafos especificos
    if n_vertices < 1:
        raise ValueError("n deve ser positivo")
    grafo = {}
    for v in range(1, n_vertices + 1):
        grafo[v] = set()

    for u, v in lista:
        if u not in grafo or v not in grafo or u == v or v in grafo[u]: #valida as arestas, se nao tem laco, se nao tem paralelas e se conecta somenets os vertices do grfo
            raise ValueError(f"aresta invalida: ({u}, {v})")
        grafo[u].add(v)
        grafo[v].add(u)
    return grafo


def graus(grafo):
    resultado = {}
    for v, vizinhos in grafo.items():
        resultado[v] = len(vizinhos)       # calcula o grau
    return resultado                       # dict com os graus


def conexo(grafo):
    ativos = set() # ativos == possuem alguma aresta
    for v, vizinhos in grafo.items():
        if len(vizinhos) > 0:
            ativos.add(v)

    if len(ativos) == 0:
        return True # caso base

    visitados = set()
    inicio = min(ativos)
    visitados.add(inicio)

    fila = deque() #cria fila
    fila.append(inicio) #bota o inicio na fila

    while len(fila) > 0:
        u = fila.popleft() #tira o primeiro vertice da fila

        for v in grafo[u]:             #percorre todos os vizinhos
            if v not in visitados:     # se o vizinho ainda nao foi visitado
                visitados.add(v)       # marca como visitado
                fila.append(v) #bota na fila pra visitar os vizinhos de v

    if visitados == ativos:
        return True
    else:
        return False


def euleriano(grafo):
    tem_arestas = False
    for vizinhos in grafo.values():
        if len(vizinhos) > 0:
            tem_arestas = True
            break

    if tem_arestas == False:
        return False
    cond_conexo = conexo(grafo)
    cond_pares = True #assumimos que atende essa condicao
    dicionario_graus = graus(grafo)

    for grau in dicionario_graus.values():
        if grau > 0:
            if grau % 2 != 0:          #tem grau impar
                cond_pares = False     # A regra foi quebrada
                break

    if cond_conexo == True and cond_pares == True:
        return True
    else:
        return False


def circuito_euler(grafo):
    if euleriano(grafo) == False:
        return None

    restante = {}
    for v, vizinhos in grafo.items():
        restante[v] = vizinhos.copy()  #copia o grafo pra poder apagar arestas

    vertices_ativos = []
    for v, vizinhos in restante.items():
        if len(vizinhos) > 0:  # apenas vertices com ruas conectadas
            vertices_ativos.append(v)
    inicio = min(vertices_ativos)

    pilha = []  # usa pilha pra guardar o caminho que ta sendo explorado
    pilha.append(inicio)
    percurso_reverso = []

    while len(pilha) > 0:
        u = pilha[-1] # explora o ultimo vertice mas sem remover

        if len(restante[u]) > 0:
            # ainda tem aresta no ponto em que estamos
            v = min(restante[u])  #pega o menor

            # apaga a aresta
            restante[u].remove(v)
            restante[v].remove(u)

            # vai pro novo  vertice e coloca ele no topo da pilha
            pilha.append(v)

        else:
            # todas as arestas do vertice em que estamos ja foram apagadas
            vertice_preso = pilha.pop() # Tira o vértice do topo da pilha
            percurso_reverso.append(vertice_preso) # Coloca no caminho final

    percurso_reverso.reverse()
    return percurso_reverso


def valida_circuito(grafo, circuito):
    tem_arestas = False
    for vizinhos in grafo.values():
        if len(vizinhos) > 0:
            tem_arestas = True
            break

    # sem ruas, sem circuito (convencao do trabalho) ou circuito vazio: invalido
    if tem_arestas == False or circuito is None or len(circuito) == 0:
        return False

    if circuito[0] != circuito[-1]:
        return False

    arestas_originais = set()
    for u, vizinhos in grafo.items():
        for v in vizinhos:
            aresta = frozenset([u, v]) # frozenset garante que a aresta (1, 2) eh igual a (2,1), dado que o grafo eh nao direcionado
            arestas_originais.add(aresta)

    # se a quantidade de passos for diferente do total de ruas deu ruim
    if (len(circuito) - 1) != len(arestas_originais):
        return False

    usadas = set()
    for i in range(len(circuito) - 1):
        u = circuito[i]       # origem
        v = circuito[i + 1]   # destino

        if u not in grafo or v not in grafo[u]: # pra nao evitar "saltos" no grafo
            return False

        aresta_atual = frozenset([u, v])
        if aresta_atual in usadas:
            return False
        usadas.add(aresta_atual)

    if usadas == arestas_originais:
        return True
    else:
        return False


def _desenhar_svg(grafo: Grafo, arquivo: str, titulo: str) -> str:
    """Alternativa sem dependências para ambientes que bloqueiam matplotlib."""
    destino = str(Path(arquivo).with_suffix(".svg"))
    vertices = sorted(grafo)
    posicoes = {
        v: (400 + 270 * math.cos(2 * math.pi * i / len(vertices)),
            410 + 270 * math.sin(2 * math.pi * i / len(vertices)))
        for i, v in enumerate(vertices)
    }
    elementos = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800">',
        '<rect width="800" height="800" fill="white"/>',
        f'<text x="400" y="58" text-anchor="middle" font-family="Arial" '
        f'font-size="25" fill="#183153">{escape(titulo)}</text>',
    ]
    for u, v in arestas(grafo):
        x1, y1 = posicoes[u]
        x2, y2 = posicoes[v]
        elementos.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            'stroke="#718096" stroke-width="2"/>'
        )
    for v in vertices:
        x, y = posicoes[v]
        elementos.extend([
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="42" fill="#dceeff" '
            'stroke="#183153" stroke-width="2"/>',
            f'<text x="{x:.2f}" y="{y - 4:.2f}" text-anchor="middle" '
            f'font-family="Arial" font-size="18" fill="#183153">{v}</text>',
            f'<text x="{x:.2f}" y="{y + 17:.2f}" text-anchor="middle" '
            f'font-family="Arial" font-size="13" fill="#183153">'
            f'grau {len(grafo[v])}</text>',
        ])
    elementos.append('</svg>')
    Path(destino).write_text("\n".join(elementos) + "\n", encoding="utf-8")
    return destino


def desenhar_grafo(grafo: Grafo, arquivo: str, titulo: str) -> str:
    """Salva um PNG com matplotlib ou um SVG se a importação falhar."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle
    except ImportError:
        print("Aviso: matplotlib indisponivel; usando figura SVG.")
        return _desenhar_svg(grafo, arquivo, titulo)

    vertices = sorted(grafo)
    posicoes = {
        v: (math.cos(2 * math.pi * i / len(vertices)),
            math.sin(2 * math.pi * i / len(vertices)))
        for i, v in enumerate(vertices)
    }
    figura, eixo = plt.subplots(figsize=(8, 8))
    for u, v in arestas(grafo):
        x1, y1 = posicoes[u]
        x2, y2 = posicoes[v]
        eixo.plot((x1, x2), (y1, y2), color="#718096", linewidth=1.7, zorder=1)

    for v in vertices:
        x, y = posicoes[v]
        eixo.add_patch(Circle((x, y), 0.14, facecolor="#dceeff",
                              edgecolor="#183153", linewidth=1.8, zorder=2))
        eixo.text(x, y, f"{v}\ngrau {len(grafo[v])}", ha="center", va="center",
                  fontsize=9, color="#183153", zorder=3)

    eixo.set(xlim=(-1.23, 1.23), ylim=(-1.23, 1.23))
    eixo.set_aspect("equal")
    eixo.axis("off")
    eixo.set_title(titulo, fontsize=13, pad=16)
    figura.savefig(arquivo, dpi=180, bbox_inches="tight")
    plt.close(figura)
    return arquivo


def experimento_1(com_figura: bool = True) -> tuple[Grafo, list[int], int]:
    rng = random.Random(SEED)
    tentativas = 0
    while True:
        grafo = gerar_grafo(N, P, rng)
        tentativas += 1
        if euleriano(grafo):
            break

    circuito = circuito_euler(grafo)
    assert circuito is not None
    valido = valida_circuito(grafo, circuito)

    print(f"Numero de vertices: {N}")
    print(f"Probabilidade p: {P:.2f}")
    print(f"Seed: {SEED}")
    print("Grafo Euleriano encontrado!")
    print(f"Numero de grafos gerados: {tentativas}")
    print("Arestas:")
    print(" ".join(f"({u},{v})" for u, v in arestas(grafo)))
    print("Graus:")
    for v, grau in graus(grafo).items():
        print(f"v{v}: {grau}")
    print(f"Conexo: {'sim' if conexo(grafo) else 'nao'}")
    print(f"Todos os graus sao pares: {'sim' if all(d % 2 == 0 for d in graus(grafo).values()) else 'nao'}")
    print(f"Euleriano: {'sim' if euleriano(grafo) else 'nao'}")
    print("Circuito de Euler:")
    print(" -> ".join(map(str, circuito)))
    print(f"Validacao do circuito: {'OK' if valido else 'FALHOU'}")

    if com_figura:
        titulo = f"Grafo Euleriano - seed {SEED}, tentativa {tentativas}"
        arquivo = desenhar_grafo(grafo, "grafo_euleriano.png", titulo)
        print(f"Figura salva em {arquivo}")
    return grafo, circuito, tentativas


def experimento_2(k: int = 1000) -> dict[str, int | float]:
    """Classifica k grafos independentes e mede as fases e o laço completo."""
    if k <= 0:
        raise ValueError("k deve ser positivo")
    rng = random.Random(SEED)
    contagens = {
        "eulerianos": 0,
        "vazios": 0,
        "conexos": 0,
        "pares": 0,
        "pares_desconexos": 0,
        "conexos_impares": 0,
        "ambos_falham": 0,
        "soma_arestas": 0,
    }
    tempo_geracao = 0.0
    tempo_verificacao = 0.0
    inicio_total = time.perf_counter()
    for _ in range(k):
        inicio_geracao = time.perf_counter()
        grafo = gerar_grafo(N, P, rng)
        tempo_geracao += time.perf_counter() - inicio_geracao

        inicio_verificacao = time.perf_counter()
        quantidade_arestas = sum(map(len, grafo.values())) // 2
        contagens["soma_arestas"] += quantidade_arestas
        tem_arestas = quantidade_arestas > 0
        if not tem_arestas:
            contagens["vazios"] += 1
        else:
            cond_conexo = conexo(grafo)
            cond_pares = all(d % 2 == 0 for d in graus(grafo).values())
            contagens["conexos"] += cond_conexo
            contagens["pares"] += cond_pares
            contagens["pares_desconexos"] += cond_pares and not cond_conexo
            contagens["conexos_impares"] += cond_conexo and not cond_pares
            contagens["ambos_falham"] += not cond_conexo and not cond_pares
        contagens["eulerianos"] += euleriano(grafo)
        tempo_verificacao += time.perf_counter() - inicio_verificacao
    tempo_total = time.perf_counter() - inicio_total

    print("--------------------------------")
    print(f"Experimento com {k} grafos:")
    print(f"Tempo acumulado de geracao: {tempo_geracao:.6f} s")
    print(f"Tempo acumulado de verificacao: {tempo_verificacao:.6f} s")
    print(f"Tempo total do experimento: {tempo_total:.6f} s")
    print(f"Grafos Eulerianos: {contagens['eulerianos']}")
    print(f"Proporcao: {contagens['eulerianos'] / k:.6f}")
    print(f"Grafos vazios: {contagens['vazios']}")
    print(f"Conexos (nao vazios): {contagens['conexos']}")
    print(f"Todos os graus pares (nao vazios): {contagens['pares']}")
    print(f"Pares e desconexos: {contagens['pares_desconexos']}")
    print(f"Conexos e com grau impar: {contagens['conexos_impares']}")
    print(f"Desconexos e com grau impar: {contagens['ambos_falham']}")
    print(f"Media de arestas: {contagens['soma_arestas'] / k:.3f}")
    return {**contagens, "tempo_geracao": tempo_geracao,
            "tempo_verificacao": tempo_verificacao, "tempo_total": tempo_total}


def inteiro_positivo(valor: str) -> int:
    try:
        numero = int(valor)
    except ValueError as erro:
        raise argparse.ArgumentTypeError("deve ser um inteiro maior que zero") from erro
    if numero <= 0:
        raise argparse.ArgumentTypeError("deve ser um inteiro maior que zero")
    return numero


def main() -> None:
    parser = argparse.ArgumentParser(description="Projeto de grafos - grupo D")
    parser.add_argument("--repeticoes", type=inteiro_positivo, default=1000,
                        metavar="K", help="quantidade de grafos no experimento 2 (padrao: 1000)")
    parser.add_argument("--sem-figura", action="store_true", help="nao gera o PNG do grafo")
    args = parser.parse_args()
    experimento_1(com_figura=not args.sem_figura)
    experimento_2(args.repeticoes)


if __name__ == "__main__":
    main()
