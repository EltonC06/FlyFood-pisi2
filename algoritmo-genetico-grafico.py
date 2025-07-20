import random
import time
import matplotlib.pyplot as plt
import numpy as np

# --- MÓDULO 1, 2, 3 e 4 (Sem alterações) ---
# (O código dos módulos anteriores permanece o mesmo)
# --- MÓDULO 1: Leitura de Dados e Funções de Custo para o TSP ---


def ler_distancias_brasil58(arquivo, dimensao=58):
    """Lê o arquivo de distâncias e retorna um dicionário."""
    distancias = {}
    try:
        with open(arquivo) as f:
            todos_os_pesos = [int(p) for linha in f for p in linha.strip().split()]
            k = 0
            for i in range(1, dimensao + 1):
                for j in range(i + 1, dimensao + 1):
                    peso = todos_os_pesos[k]
                    distancias[(i, j)] = peso
                    distancias[(j, i)] = peso
                    k += 1
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None
    print(f"Matriz de distâncias com {len(distancias)} arestas lida com sucesso.")
    return distancias


def calcular_custo_rota_tsp(rota, distancias):
    """Calcula o custo total (distância) de uma rota cíclica."""
    soma = 0
    for i in range(len(rota) - 1):
        soma += distancias.get((rota[i], rota[i + 1]), float("inf"))
    soma += distancias.get((rota[-1], rota[0]), float("inf"))
    return soma


def gerar_rota_aleatoria_tsp(num_cidades):
    """Gera uma rota (cromossomo) aleatória."""
    cidades = list(range(1, num_cidades + 1))
    random.shuffle(cidades)
    return cidades


# --- MÓDULO 2: Operadores do Algoritmo Genético ---


def selecao_por_torneio(populacao, aptidoes, k=3):
    """Seleciona um indivíduo da população usando o método de torneio."""
    indices_torneio = random.sample(range(len(populacao)), k)
    indice_vencedor = min(indices_torneio, key=lambda i: aptidoes[i])
    return populacao[indice_vencedor]


def crossover_ciclico(pai1, pai2):
    """Realiza o cruzamento usando Cycle Crossover (CX)."""
    filho = [None] * len(pai1)
    indices_visitados = [False] * len(pai1)
    indice_atual = 0
    while not indices_visitados[indice_atual]:
        filho[indice_atual] = pai1[indice_atual]
        indices_visitados[indice_atual] = True
        valor_pai2 = pai2[indice_atual]
        indice_atual = pai1.index(valor_pai2)
    for i in range(len(filho)):
        if filho[i] is None:
            filho[i] = pai2[i]
    return filho


def mutacao_por_inversao(rota, taxa_mutacao):
    """Aplica a mutação invertendo um segmento da rota."""
    if random.random() < taxa_mutacao:
        inicio, fim = sorted(random.sample(range(len(rota)), 2))
        segmento = rota[inicio : fim + 1]
        segmento.reverse()
        rota[inicio : fim + 1] = segmento
    return rota


# --- MÓDULO 3: O Algoritmo Genético Principal ---


def algoritmo_genetico_tsp(
    distancias,
    num_cidades,
    tam_pop=100,
    max_geracoes=500,
    taxa_mutacao=0.02,
    tam_torneio=3,
    elitismo=True,
):
    """Executa o Algoritmo Genético para o TSP."""
    populacao = [gerar_rota_aleatoria_tsp(num_cidades) for _ in range(tam_pop)]
    melhor_rota_global = None
    menor_custo_global = float("inf")
    historico_custos = []  # MODIFICADO: Adicionado para salvar histórico de convergência

    print("\nIniciando o processo evolutivo...")
    for geracao in range(max_geracoes):
        aptidoes = [calcular_custo_rota_tsp(rota, distancias) for rota in populacao]
        menor_custo_geracao = min(aptidoes)
        if menor_custo_geracao < menor_custo_global:
            menor_custo_global = menor_custo_geracao
            melhor_rota_global = populacao[aptidoes.index(menor_custo_geracao)]
            print(
                f"Geração {geracao + 1:03d}: Nova melhor rota! Custo: {menor_custo_global}"
            )

        historico_custos.append(
            menor_custo_global
        )  # MODIFICADO: Salva o melhor custo da geração

        nova_populacao = []
        if elitismo:
            nova_populacao.append(populacao[aptidoes.index(min(aptidoes))])
        while len(nova_populacao) < tam_pop:
            pai1 = selecao_por_torneio(populacao, aptidoes, k=tam_torneio)
            pai2 = selecao_por_torneio(populacao, aptidoes, k=tam_torneio)
            filho = crossover_ciclico(pai1, pai2)
            filho = mutacao_por_inversao(filho, taxa_mutacao)
            nova_populacao.append(filho)
        populacao = nova_populacao

    print("\nProcesso evolutivo concluído.")
    return melhor_rota_global, menor_custo_global, historico_custos


# --- MÓDULO 4: Funções de Plotagem (ADICIONADO) ---


def plotar_caminho_tsp(caminho, custo, coordenadas_cidades):
    """Plota o melhor caminho encontrado, com o estilo de plot.py."""
    if not caminho:
        print("Caminho inválido para plotagem.")
        return

    fig, ax = plt.subplots(figsize=(12, 10))
    # Ajusta o título para incluir o custo
    ax.set_title(f"Melhor Caminho Encontrado (GA)\nCusto Total: {custo}", fontsize=16)

    # Configurações do plano cartesiano (estilo de plot.py)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Conecta o último ponto ao primeiro para fechar o ciclo
    caminho_fechado = caminho + [caminho[0]]
    # O -1 é necessário pois as cidades são 1-58 e os índices das coordenadas 0-57
    caminho_x = [
        coordenadas_cidades[cidade_idx - 1][0] for cidade_idx in caminho_fechado
    ]
    caminho_y = [
        coordenadas_cidades[cidade_idx - 1][1] for cidade_idx in caminho_fechado
    ]
    ax.plot(
        caminho_x,
        caminho_y,
        c="red",
        linestyle="-",
        linewidth=1.5,
        marker=".",
        markersize=5,
    )

    # Plota as cidades
    coords_array = np.array([coordenadas_cidades[c - 1] for c in caminho])
    ax.scatter(
        coords_array[:, 0], coords_array[:, 1], c="blue", marker="o", s=50, zorder=5
    )

    # Adiciona rótulos às cidades
    for cidade_idx in caminho:
        x, y = coordenadas_cidades[cidade_idx - 1]
        ax.text(x + 1, y + 1, str(cidade_idx), fontsize=9, ha="center")

    plt.xlabel("Coordenada X (Placeholder)")
    plt.ylabel("Coordenada Y (Placeholder)")
    plt.savefig("resultado_genetico_caminho.png", dpi=300)
    plt.show()


def plotar_convergencia(historico_custos):
    """Plota o gráfico de convergência do algoritmo."""
    plt.figure(figsize=(10, 6))
    plt.plot(historico_custos, c="green", linestyle="-", linewidth=2)
    plt.title("Convergência do Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Custo Encontrado")
    plt.grid(True)
    plt.savefig("resultado_genetico_convergencia.png", dpi=300)
    plt.show()


# --- Bloco Principal para Execução ---
if __name__ == "__main__":
    ARQUIVO_DISTANCIAS = "edgesbrasil58.txt"
    NUM_CIDADES = 58
    print("--- Algoritmo Genético para o TSP: Problema Brazil58 ---")

    tempo_inicio_total = time.time()  # Mede o tempo total
    distancias = ler_distancias_brasil58(ARQUIVO_DISTANCIAS, NUM_CIDADES)

    if distancias:
        # Parâmetros do Algoritmo Genético
        TAM_POPULACAO = 100
        MAX_GERACOES = 5000
        TAXA_MUTACAO = 0.02
        TAM_TORNEIO = 5

        # MODIFICADO: Inicia o cronômetro aqui
        tempo_inicio_algoritmo = time.time()

        rota, custo, historico = algoritmo_genetico_tsp(
            distancias,
            NUM_CIDADES,
            TAM_POPULACAO,
            MAX_GERACOES,
            TAXA_MUTACAO,
            TAM_TORNEIO,
        )

        # MODIFICADO: Para o cronômetro aqui
        tempo_fim_algoritmo = time.time()
        tempo_execucao_algoritmo = tempo_fim_algoritmo - tempo_inicio_algoritmo

        if rota:
            print(f"\n--- Resultado Final ---")
            print(f"Menor Custo Encontrado: {custo}")
            # ADICIONADO: Imprime o tempo de execução apenas do algoritmo
            print(
                f"Tempo de execução DO ALGORITMO: {tempo_execucao_algoritmo:.4f} segundos"
            )

            coordenadas_placeholder = np.random.rand(NUM_CIDADES, 2) * 100
            plotar_caminho_tsp(rota, custo, coordenadas_placeholder)
            plotar_convergencia(historico)
        else:
            print("Não foi possível encontrar uma rota.")

    # ADICIONADO: Imprime o tempo de execução total, incluindo plotagem
    tempo_fim_total = time.time()
    print(
        f"\nTempo de execução TOTAL (com plotagem): {tempo_fim_total - tempo_inicio_total:.4f} segundos"
    )
