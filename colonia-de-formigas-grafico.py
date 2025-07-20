import random
import time
import matplotlib.pyplot as plt
import numpy as np

# --- MÓDULO 1, 2, 3 e 4 (Sem alterações) ---
# (O código dos módulos anteriores permanece o mesmo)
# --- MÓDULO 1: Leitura de Dados e Funções Auxiliares ---


def ler_distancias_para_matriz(arquivo, dimensao=58):
    """
    Lê o arquivo de distâncias (mesmo formato do genético) e retorna
    uma matriz de distâncias numpy para o ACO.
    """
    matriz_distancias = np.zeros((dimensao, dimensao))
    try:
        with open(arquivo) as f:
            todos_os_pesos = [int(p) for linha in f for p in linha.strip().split()]
            k = 0
            # Índices da matriz numpy são base 0 (0 a 57)
            for i in range(dimensao):
                for j in range(i + 1, dimensao):
                    peso = todos_os_pesos[k]
                    matriz_distancias[i, j] = peso
                    matriz_distancias[j, i] = peso
                    k += 1
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None
    print(
        f"Matriz de distâncias de formato {matriz_distancias.shape} lida com sucesso."
    )
    return matriz_distancias


# --- MÓDULO 2: Funções do Algoritmo ACO ---


def inicializar_feromonio(num_cidades, valor_inicial=0.1):
    """Inicializa a matriz de feromônio com um valor uniforme."""
    return np.full((num_cidades, num_cidades), valor_inicial)


def calcular_probabilidades_transicao(
    cidade_atual, cidades_nao_visitadas, matriz_feromonio, matriz_distancias, alfa, beta
):
    """Calcula as probabilidades de transição para a próxima cidade."""
    feromonio = matriz_feromonio[cidade_atual, cidades_nao_visitadas] ** alfa
    # Adicionado um pequeno valor para evitar divisão por zero se a distância for 0
    distancias_inv = 1.0 / (
        matriz_distancias[cidade_atual, cidades_nao_visitadas] + 1e-10
    )
    visibilidade = distancias_inv**beta

    probabilidades = feromonio * visibilidade
    soma_prob = np.sum(probabilidades)

    if soma_prob == 0:  # Caso de estagnação ou problema numérico
        # Se a soma for zero, atribui probabilidade igual a todas as cidades restantes
        return np.full(len(cidades_nao_visitadas), 1.0 / len(cidades_nao_visitadas))

    return probabilidades / soma_prob


def construir_caminho_formiga(
    num_cidades, matriz_feromonio, matriz_distancias, alfa, beta
):
    """Uma formiga constrói um caminho completo."""
    cidade_inicial = random.randint(0, num_cidades - 1)
    caminho = [cidade_inicial]
    cidades_nao_visitadas = list(range(num_cidades))
    cidades_nao_visitadas.remove(cidade_inicial)

    while cidades_nao_visitadas:
        cidade_atual = caminho[-1]
        probabilidades = calcular_probabilidades_transicao(
            cidade_atual,
            cidades_nao_visitadas,
            matriz_feromonio,
            matriz_distancias,
            alfa,
            beta,
        )
        proxima_cidade = np.random.choice(cidades_nao_visitadas, p=probabilidades)
        caminho.append(proxima_cidade)
        cidades_nao_visitadas.remove(proxima_cidade)

    return caminho


def calcular_comprimento_caminho(caminho, matriz_distancias):
    """Calcula o comprimento total de um caminho."""
    # np.roll desloca os elementos do array. [1,2,3,0] se torna [0,1,2,3]
    # Isso alinha cada cidade com sua próxima cidade no caminho para cálculo vetorial
    dist = matriz_distancias[caminho, np.roll(caminho, -1)]
    return np.sum(dist)


def atualizar_feromonio(matriz_feromonio, caminhos, comprimentos, taxa_evaporacao, Q):
    """Atualiza a matriz de feromônio."""
    matriz_feromonio *= 1 - taxa_evaporacao
    for caminho, comprimento in zip(caminhos, comprimentos):
        feromonio_depositado = Q / comprimento
        for i in range(len(caminho)):
            # Atualiza a aresta entre a cidade atual e a próxima (com roll)
            cidade_inicio = caminho[i]
            cidade_fim = caminho[
                (i + 1) % len(caminho)
            ]  # Usa módulo para fechar o ciclo
            matriz_feromonio[cidade_inicio, cidade_fim] += feromonio_depositado
            matriz_feromonio[cidade_fim, cidade_inicio] += (
                feromonio_depositado  # Caminho simétrico
            )


# --- MÓDULO 3: O Algoritmo da Colônia de Formigas Principal ---


def algoritmo_colonia_formigas(
    matriz_distancias,
    num_cidades,
    num_formigas,
    num_iteracoes,
    alfa,
    beta,
    taxa_evaporacao,
    Q,
):
    """Executa o algoritmo da colônia de formigas para o TSP."""
    matriz_feromonio = inicializar_feromonio(num_cidades)
    melhor_caminho_global = None
    melhor_comprimento_global = float("inf")
    historico_comprimentos = []

    print("\nIniciando otimização por colônia de formigas...")
    for iteracao in range(num_iteracoes):
        caminhos_formigas = [
            construir_caminho_formiga(
                num_cidades, matriz_feromonio, matriz_distancias, alfa, beta
            )
            for _ in range(num_formigas)
        ]
        comprimentos_caminhos = [
            calcular_comprimento_caminho(c, matriz_distancias)
            for c in caminhos_formigas
        ]

        melhor_comprimento_iteracao = min(comprimentos_caminhos)
        if melhor_comprimento_iteracao < melhor_comprimento_global:
            melhor_comprimento_global = melhor_comprimento_iteracao
            melhor_caminho_global = caminhos_formigas[
                comprimentos_caminhos.index(melhor_comprimento_iteracao)
            ]
            print(
                f"Iteração {iteracao + 1:03d}: Novo melhor caminho! Comprimento: {melhor_comprimento_global:.2f}"
            )

        historico_comprimentos.append(melhor_comprimento_global)
        atualizar_feromonio(
            matriz_feromonio,
            caminhos_formigas,
            comprimentos_caminhos,
            taxa_evaporacao,
            Q,
        )

    print("\nOtimização concluída.")
    return melhor_caminho_global, melhor_comprimento_global, historico_comprimentos


# --- MÓDULO 4: Funções de Plotagem ---


def plotar_caminho_aco(caminho, custo, coordenadas_cidades):
    """Plota o melhor caminho encontrado pelo ACO, com o estilo de plot.py."""
    caminho_plot = caminho + [caminho[0]]  # Fecha o ciclo para plotagem

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_title(
        f"Melhor Caminho Encontrado (ACO)\nCusto Total: {custo:.2f}", fontsize=16
    )

    # Configurações do plano cartesiano (estilo de plot.py)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Plotar o caminho
    caminho_x = [coordenadas_cidades[i][0] for i in caminho_plot]
    caminho_y = [coordenadas_cidades[i][1] for i in caminho_plot]
    ax.plot(
        caminho_x,
        caminho_y,
        c="orange",
        linestyle="-",
        linewidth=1.5,
        marker=".",
        markersize=5,
    )

    # Plotar as cidades
    ax.scatter(
        coordenadas_cidades[:, 0],
        coordenadas_cidades[:, 1],
        c="darkgreen",
        marker="o",
        s=50,
        zorder=5,
    )
    for i, (x, y) in enumerate(coordenadas_cidades):
        ax.text(x + 1, y + 1, str(i + 1), fontsize=9, ha="center")

    plt.xlabel("Coordenada X (Placeholder)")
    plt.ylabel("Coordenada Y (Placeholder)")
    plt.savefig("resultado_aco_caminho.png", dpi=300)
    plt.show()


def plotar_convergencia_aco(historico):
    """Plota o gráfico de convergência do algoritmo ACO."""
    plt.figure(figsize=(10, 6))
    plt.plot(historico, c="purple", linestyle="-", linewidth=2)
    plt.title("Convergência do Algoritmo ACO")
    plt.xlabel("Iteração")
    plt.ylabel("Melhor Comprimento Encontrado")
    plt.grid(True)
    plt.savefig("resultado_aco_convergencia.png", dpi=300)
    plt.show()


# --- Bloco Principal para Execução ---
if __name__ == "__main__":
    ARQUIVO_DISTANCIAS = "edgesbrasil58.txt"
    NUM_CIDADES = 58

    # Parâmetros do ACO
    NUM_FORMIGAS = 20
    NUM_ITERACOES = 500
    ALFA = 1.0  # Importância do feromônio
    BETA = 5.0  # Importância da visibilidade
    TAXA_EVAPORACAO = 0.1
    Q = 100.0  # Quantidade de feromônio

    print("--- ACO para o TSP: Problema Brazil58 (Estrutura Padronizada) ---")

    tempo_inicio_total = time.time()  # Mede o tempo total
    matriz_distancias = ler_distancias_para_matriz(ARQUIVO_DISTANCIAS, NUM_CIDADES)

    if matriz_distancias is not None:
        # MODIFICADO: Inicia o cronômetro aqui
        tempo_inicio_algoritmo = time.time()

        melhor_caminho, melhor_custo, historico = algoritmo_colonia_formigas(
            matriz_distancias,
            NUM_CIDADES,
            NUM_FORMIGAS,
            NUM_ITERACOES,
            ALFA,
            BETA,
            TAXA_EVAPORACAO,
            Q,
        )

        # MODIFICADO: Para o cronômetro aqui
        tempo_fim_algoritmo = time.time()
        tempo_execucao_algoritmo = tempo_fim_algoritmo - tempo_inicio_algoritmo

        if melhor_caminho:
            print(f"\n--- Resultado Final ---")
            print(f"Melhor comprimento do caminho: {melhor_custo:.2f}")
            # ADICIONADO: Imprime o tempo de execução apenas do algoritmo
            print(
                f"Tempo de execução DO ALGORITMO: {tempo_execucao_algoritmo:.4f} segundos"
            )

            coordenadas_placeholder = np.random.rand(NUM_CIDADES, 2) * 100
            plotar_caminho_aco(melhor_caminho, melhor_custo, coordenadas_placeholder)
            plotar_convergencia_aco(historico)

    # ADICIONADO: Imprime o tempo de execução total, incluindo plotagem
    tempo_fim_total = time.time()
    print(
        f"\nTempo de execução TOTAL (com plotagem): {tempo_fim_total - tempo_inicio_total:.4f} segundos"
    )
