import random
import time

# --- MÓDULO 1: Funções Auxiliares e de Leitura (Base do Projeto) ---

def ler_matriz(arquivo):
    """
    Lê o arquivo de texto, encontra os pontos e retorna um dicionário
    com seus rótulos e coordenadas.
    """
    pontos = {}
    try:
        with open(arquivo) as f:
            matriz = f.readlines()
            # Tenta pular a primeira linha se ela contiver as dimensões
            try:
                int(matriz[0].strip().split()[0])
                matriz = matriz[1:]
            except (ValueError, IndexError):
                pass
            for i, linha in enumerate(matriz):
                for j, char in enumerate(linha.strip().split()):
                    if char.isalpha():
                        pontos[char] = {'linha': i, 'coluna': j}
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None
    return pontos

def calcular_custo_rota(rota, pontos, inicio='R'):
    """Calcula o custo total (Distância de Manhattan) de uma rota."""
    if not rota:
        return 0
    # Distância da origem ao primeiro ponto
    dist = abs(pontos[inicio]['linha'] - pontos[rota[0]]['linha']) + \
           abs(pontos[inicio]['coluna'] - pontos[rota[0]]['coluna'])
    
    # Distância entre os pontos da rota
    for i in range(len(rota) - 1):
        ponto_atual = pontos[rota[i]]
        proximo_ponto = pontos[rota[i+1]]
        dist += abs(ponto_atual['linha'] - proximo_ponto['linha']) + \
                abs(ponto_atual['coluna'] - proximo_ponto['coluna'])
                
    # Distância do último ponto de volta à origem
    dist += abs(pontos[rota[-1]]['linha'] - pontos[inicio]['linha']) + \
            abs(pontos[rota[-1]]['coluna'] - pontos[inicio]['coluna'])
    return dist

def gerar_rota_aleatoria(pontos, inicio='R'):
    """Gera uma única rota (cromossomo) aleatória."""
    waypoints = list(pontos.keys())
    waypoints.remove(inicio)
    random.shuffle(waypoints)
    return waypoints

# --- MÓDULO 2: Operadores do Algoritmo Genético ---

def selecao_por_torneio(populacao, pontos, k=3):
    """
    Seleciona um indivíduo (pai) da população usando o método de torneio.
    """
    # Seleciona k competidores aleatórios da população
    torneio = random.sample(populacao, k)
    # Retorna o melhor indivíduo (menor custo) do torneio
    vencedor = min(torneio, key=lambda rota: calcular_custo_rota(rota, pontos))
    return vencedor

def crossover_ciclico(pai1, pai2):
    """
    Realiza o cruzamento entre dois pais usando o método Cycle Crossover (CX).
    Gera um único filho.
    """
    filho = [None] * len(pai1)
    indices_visitados = [False] * len(pai1)
    
    # Começa o primeiro ciclo
    indice_atual = 0
    while not indices_visitados[indice_atual]:
        # Copia o elemento do pai1 para o filho
        filho[indice_atual] = pai1[indice_atual]
        indices_visitados[indice_atual] = True
        
        # Encontra o próximo elemento no ciclo
        valor_pai2 = pai2[indice_atual]
        indice_atual = pai1.index(valor_pai2)

    # Preenche os elementos restantes com os genes do pai2
    for i in range(len(filho)):
        if filho[i] is None:
            filho[i] = pai2[i]
            
    return filho

def mutacao_por_inversao(rota, taxa_mutacao):
    """
    Aplica a mutação em uma rota invertendo um segmento dela.
    """
    if random.random() < taxa_mutacao:
        # Escolhe dois pontos de corte aleatórios
        inicio, fim = sorted(random.sample(range(len(rota)), 2))
        
        # Inverte o segmento da rota entre os pontos de corte
        segmento = rota[inicio:fim+1]
        segmento.reverse()
        rota[inicio:fim+1] = segmento
        
    return rota

# --- MÓDULO 3: O Algoritmo Genético Principal ---

def algoritmo_genetico(pontos, tam_pop=100, max_geracoes=500, taxa_mutacao=0.02, tam_torneio=3, elitismo=True):
    """
    Executa o Algoritmo Genético para resolver o problema do Caixeiro Viajante.
    """
    inicio = 'R'
    
    # 1. Geração da População Inicial
    populacao = [gerar_rota_aleatoria(pontos, inicio) for _ in range(tam_pop)]
    
    melhor_rota_global = None
    menor_custo_global = float('inf')

    print("Iniciando o processo evolutivo...")
    
    # 2. Loop de Gerações
    for geracao in range(max_geracoes):
        # Avalia a população atual
        custos = [calcular_custo_rota(rota, pontos, inicio) for rota in populacao]
        
        # Encontra o melhor da geração atual
        menor_custo_geracao = min(custos)
        if menor_custo_geracao < menor_custo_global:
            menor_custo_global = menor_custo_geracao
            melhor_rota_global = populacao[custos.index(menor_custo_geracao)]
            print(f"Geração {geracao+1}: Nova melhor rota encontrada! Custo: {menor_custo_global}")
            
        # 3. Criação da Nova Geração
        nova_populacao = []
        
        # Elitismo: o melhor indivíduo passa diretamente para a próxima geração
        if elitismo:
            melhor_da_geracao = min(populacao, key=lambda r: calcular_custo_rota(r, pontos))
            nova_populacao.append(melhor_da_geracao)

        # Preenche o resto da nova população com filhos
        while len(nova_populacao) < tam_pop:
            # Seleção
            pai1 = selecao_por_torneio(populacao, pontos, k=tam_torneio)
            pai2 = selecao_por_torneio(populacao, pontos, k=tam_torneio)
            
            # Crossover
            filho = crossover_ciclico(pai1, pai2)
            
            # Mutação
            filho = mutacao_por_inversao(filho, taxa_mutacao)
            
            nova_populacao.append(filho)
            
        populacao = nova_populacao

    print("\nProcesso evolutivo concluído.")
    return melhor_rota_global, menor_custo_global

# --- Bloco Principal para Execução ---

if __name__ == "__main__":
    arquivo_cenario = 'cenario1.txt' # Mude aqui para 'cenario2.txt', etc.
    
    print(f"--- Algoritmo Genético para o FlyFood ---")
    print(f"Lendo o arquivo: {arquivo_cenario}\n")
    
    tempo_inicio = time.time()
    
    pontos = ler_matriz(arquivo_cenario)
    
    if pontos:
        # Ajuste os parâmetros do AG conforme a necessidade do problema
        # Para problemas maiores (ex: 10 pontos), pode ser necessário aumentar tam_pop e max_geracoes
        num_pontos_entrega = len(pontos) - 1
        
        if num_pontos_entrega <= 5:
            tam_populacao = 50
            geracoes = 100
        else:
            tam_populacao = 100
            geracoes = 500

        rota, dist = algoritmo_genetico(
            pontos,
            tam_pop=tam_populacao,
            max_geracoes=geracoes,
            taxa_mutacao=0.02
        )
        
        if rota:
            print(f"\n--- Resultado Final ---")
            print(f"Melhor Rota Encontrada: R -> {' -> '.join(rota)} -> R")
            print(f"Distância Total: {dist}")
        else:
            print("Não foi possível encontrar uma rota.")
    
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    print(f"\nTempo de execução total: {tempo_execucao:.4f} segundos")

