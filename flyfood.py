import time

def ler_matriz(arquivo):
    """
    Lê o arquivo de texto, encontra os pontos e retorna um dicionário
    com seus rótulos e coordenadas.
    """
    pontos = {}
    try:
        with open(arquivo) as f:
            matriz = f.readlines()
            
            # Tenta pular a primeira linha se ela contiver as dimensões (ex: "4 5")
            try:
                int(matriz[0].strip()[0]) # Se o primeiro caractere for um número, assume que é a linha de dimensão
                matriz = matriz[1:]
            except (ValueError, IndexError):
                pass # Se não for número, provavelmente já é a matriz

            for i, linha in enumerate(matriz):
                # Usamos split() para lidar com espaços entre os caracteres, como em "R 0 B 0 0"
                for j, char in enumerate(linha.strip().split()):
                    if char.isalpha():
                        pontos[char] = {'linha': i, 'coluna': j}
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None
        
    return pontos

def distancia(ponto_a, ponto_b):
    """Calcula a Distância de Manhattan entre dois pontos."""
    return abs(ponto_a['linha'] - ponto_b['linha']) + abs(ponto_a['coluna'] - ponto_b['coluna'])

def gerar_permutacoes_recursivo(lista_elementos):
    """
    Gera todas as permutações para uma lista de elementos usando um
    algoritmo recursivo de backtracking.
    """
    # Caso base: se a lista tem 1 ou 0 elementos, a única permutação é a própria lista.
    if len(lista_elementos) <= 1:
        return [lista_elementos]

    # Lista para armazenar as permutações que serão geradas.
    permutacoes_geradas = []

    # Passo recursivo: itera sobre cada elemento da lista.
    for i in range(len(lista_elementos)):
        # Pega o elemento atual para ser o "pivô" da permutação.
        elemento_atual = lista_elementos[i]
        
        # Cria uma nova lista com todos os outros elementos.
        elementos_restantes = lista_elementos[:i] + lista_elementos[i+1:]
        
        # Chama a recursão para gerar todas as permutações dos elementos restantes.
        for permutacao_do_resto in gerar_permutacoes_recursivo(elementos_restantes):
            # Adiciona o pivô no início de cada permutação retornada.
            permutacoes_geradas.append([elemento_atual] + permutacao_do_resto)
            
    return permutacoes_geradas

def achar_menor_rota(pontos, inicio='R'):
    # Pega todos os pontos que não são o de início/retorno
    waypoints = [p for p in pontos if p != inicio]
    
    # Se não houver pontos de entrega, retorna imediatamente
    if not waypoints:
        return [], 0

    menor_distancia = float('inf')
    melhor_rota = None
    
    # 1. Gera a lista de todas as permutações usando nossa função recursiva
    print(f"Gerando {len(waypoints)}! permutações...")
    lista_de_permutacoes = gerar_permutacoes_recursivo(waypoints)
    print("Permutações geradas. Calculando distâncias...")
    
    # 2. Itera sobre a lista de permutações que acabamos de gerar
    for rota in lista_de_permutacoes:
        # O cálculo da distância para cada rota permanece o mesmo
        dist_atual = distancia(pontos[inicio], pontos[rota[0]])
        for i in range(len(rota) - 1):
            dist_atual += distancia(pontos[rota[i]], pontos[rota[i+1]])
        dist_atual += distancia(pontos[rota[-1]], pontos[inicio])

        if dist_atual < menor_distancia:
            menor_distancia = dist_atual
            melhor_rota = rota

    return melhor_rota, menor_distancia

if __name__ == "__main__":
    tempo_inicio = time.time()

    pontos = ler_matriz('cenario1.txt')
    if pontos:
        rota, dist = achar_menor_rota(pontos)
        if rota:
            print(f"\nMelhor Rota Encontrada: R -> {' -> '.join(rota)} -> R")
            print(f"Distância Total: {dist}")
        else:
            print("Não há pontos de entrega para traçar uma rota.")
    
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    print(f"\nTempo de execução: {tempo_execucao:.6f} segundos")