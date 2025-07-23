# 🚀 FlyFood: Otimização de Rotas para Entregas com Drones 📦

## 👥 Membros da Equipe

* **Caio Bispo**
* **Guilherme Henrique**
* **Elton Costa**
* **Gabriel Lima**
* **Douglas Wesley**

## 🌟 Visão Geral do Projeto

Este projeto, desenvolvido como parte do **Bacharelado em Sistemas de Informação da Universidade Federal Rural de Pernambuco**, realiza uma análise comparativa de diferentes abordagens algorítmicas para o desafio logístico de entregas urbanas com drones. O "FlyFood" serve como um cenário para investigar a otimização de rotas, abordando o Problema do Caixeiro Viajante (PCV).

O estudo parte de um algoritmo de **Força Bruta** para estabelecer um *benchmark* de otimalidade em pequena escala e, em seguida, explora a eficácia e o desempenho de duas **meta-heurísticas** — **Algoritmo da Colônia de Formigas (ACO)** e **Algoritmo Genético (AG)** — como soluções viáveis para problemas de larga escala.

## 🎯 O Problema

O desafio central é determinar a sequência ótima de pontos de entrega para um drone, minimizando a distância total percorrida. O espaço é modelado como uma matriz, e o custo do percurso é medido pela **Distância de Manhattan**. Este problema é uma instância clássica do **Problema do Caixeiro Viajante (PCV)**, um desafio de otimização combinatória NP-Difícil.

## 🏆 Objetivos

* **Objetivo Geral:** Desenvolver e avaliar comparativamente diferentes abordagens algorítmicas para o roteamento de drones da FlyFood, analisando o trade-off entre a garantia de otimalidade e o desempenho computacional.
* **Objetivos Específicos:**
  * Implementar um algoritmo de **Força Bruta** para garantir a solução ótima e servir como padrão de comparação.
  * Implementar as meta-heurísticas **Algoritmo da Colônia de Formigas (ACO)** e **Algoritmo Genético (AG)** para resolver o problema em cenários de maior escala.
  * Avaliar e comparar a eficácia das abordagens, analisando a qualidade da rota encontrada e o tempo de execução.

## 💡 Metodologia e Abordagens

O projeto compara três algoritmos distintos:

1. **Força Bruta (Benchmark):**
   * **Propósito:** Garantir a solução 100% ótima para validar o modelo e servir como base de comparação.
   * **Técnica:** Implementação recursiva de *backtracking* que testa todas as `N!` permutações.
   * **Complexidade:** `O(N!)` em tempo, `O(N)` em espaço.

2. **Algoritmo da Colônia de Formigas (ACO):**
   * **Propósito:** Encontrar soluções de alta qualidade em tempo hábil para problemas complexos.
   * **Inspiração:** Inteligência de enxames e comportamento de forrageamento de formigas.
   * **Mecanismo:** "Formigas" virtuais depositam "feromônio" em caminhos mais curtos, guiando a busca coletiva.

3. **Algoritmo Genético (AG):**
   * **Propósito:** Evoluir uma população de soluções para convergir a um resultado de alta qualidade.
   * **Inspiração:** Teoria da evolução de Darwin.
   * **Mecanismo:** Opera sobre uma população de rotas, aplicando operadores de **Seleção (Torneio)**, **Crossover (Cycle)** e **Mutação (Inversão)** a cada geração.

## 📁 Estrutura do Diretório

```
.
├── algoritmos/
│   ├── forca_bruta.py
│   ├── colonia_formigas.py
│   └── genetico.py
├── cenarios/
│   ├── cenario1.txt      # N=3, para Força Bruta
│   ├── cenario2.txt      # N=4, para Força Bruta
│   ├── cenario3.txt      # N=10, para Força Bruta
│   └── brasil58.txt      # N=58, para ACO e AG
├── Relatorio_FlyFood.pdf
└── README.md
```

## 🛠️ Como Executar

### Pré-requisitos

* Python 3.x
* Bibliotecas: `matplotlib`, `numpy` (se aplicável para visualizações).

### Instruções

Cada algoritmo pode ser executado individualmente através da linha de comando, passando o arquivo do cenário como argumento.

**1. Para executar a Força Bruta:**
```bash
Abra o arquivo forca-bruta.py e clique em rodar
```

**2. Para executar o Algoritmo da Colônia de Formigas:**
```bash
Abra o arquivo colonia-de-formigas-grafico.py e clique em rodar
```

**3. Para executar o Algoritmo Genético:**
```bash
Abra o arquivo algoritmo-genetico-grafico.py e clique em rodar
```

## 📊 Experimentos e Resultados

* A **Força Bruta** foi validada com os cenários de 3, 4 e 10 pontos, confirmando sua corretude e demonstrando sua inviabilidade computacional para problemas maiores.
* O **ACO** e o **AG** foram testados com o cenário `brasil58` (58 cidades), um problema de larga escala. Os resultados são comparados em termos de:
  * **Qualidade da Solução:** A menor distância encontrada por cada meta-heurística.
  * **Tempo de Execução:** O tempo necessário para convergir para uma solução.
* A análise dos resultados evidencia o clássico trade-off entre a otimalidade garantida (Força Bruta) e a eficiência computacional (meta-heurísticas).
