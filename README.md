# 🚀 FlyFood: Otimização de Rotas para Entregas com Drones 📦

## 👥 Membros da Equipe

* **Caio Bispo**
* **Guilherme Henrique**
* **Elton Costa**
* **Gabriel Lima**
* **Douglas Wesley**
  
## 🌟 Visão Geral do Projeto

Este projeto, desenvolvido como parte do **Bacharelado em Sistemas de Informação da Universidade Federal Rural de Pernambuco**, propõe uma solução otimizada para o desafio logístico de entregas urbanas, utilizando drones como meio principal. O "FlyFood" é uma empresa fictícia que explora a otimização de rotas para minimizar distâncias e custos, abordando as crescentes demandas de delivery, especialmente após a pandemia de Covid-19.

## 🎯 O Problema

O problema central consiste em determinar a sequência ótima de pontos de entrega para um drone, minimizando a distância total percorrida. O espaço urbano é modelado como uma matriz bidimensional, onde `R` representa o ponto de origem e retorno, e `P` é um conjunto de pontos de entrega a serem visitados exatamente uma vez. A movimentação do drone é restrita aos eixos horizontal e vertical, e o custo do percurso é medido em "dronômetros" utilizando a Distância de Manhattan.

Este desafio é classificado como uma variante do **Problema do Caixeiro Viajante (PCV)**, um problema de otimização combinatória NP-Difícil.

## 🏆 Objetivos

* **Objetivo Geral:** Desenvolver um algoritmo de roteamento que determine a sequência ótima de pontos de entrega para um drone da FlyFood, minimizando a distância total em dronômetros, partindo e retornando ao ponto de origem, considerando as restrições de movimento em uma matriz representativa da cidade.
* **Objetivos Específicos:**
    * Modelar o problema de roteamento como um problema de otimização combinatória, utilizando uma matriz bidimensional.
    * Implementar um algoritmo capaz de ler a matriz de entrada, calcular distâncias e determinar a sequência de pontos de menor custo.
    * Avaliar a eficácia do algoritmo por meio de testes com diferentes configurações de matrizes, analisando a corretude da solução e o desempenho computacional.

## 💡 Metodologia e Abordagem

 Para garantir a otimalidade da rota, optou-se pela implementação de um **algoritmo de força bruta** com base em **recursão**. Essa abordagem avalia sistematicamente todas as permutações possíveis dos pontos de entrega, garantindo a identificação da rota de menor custo total.

* **Modelagem:** Tradução do cenário para uma estrutura de dados formal, armazenando rótulos e coordenadas dos pontos em um dicionário.
* **Distância de Manhattan:** Métrica fundamental para calcular o custo de deslocamento do drone, apropriada para movimentos ortogonais em grade.
* **Complexidade:** A complexidade de tempo do algoritmo é de **O(N!)**, decorrente da natureza NP-Difícil do PCV. A complexidade de espaço é de **O(N)**.

## 🛠️ Estrutura do Algoritmo

O algoritmo é modular, com uma função recursiva para gerar todas as permutações (rotas candidatas) e uma função principal que orquestra o processo, calcula o custo de cada rota e identifica a solução ótima.

## 📊 Experimentos e Resultados

Foram realizados experimentos em três cenários de teste (3, 4 e 6 pontos de entrega) para validar a corretude e analisar o desempenho. Os resultados confirmaram a corretude do algoritmo para pequena escala e evidenciaram o crescimento drástico e não linear do tempo de execução com o aumento dos pontos, reforçando a natureza computacionalmente intensiva da força bruta.

## ⏭️ Próximos Passos

Dada a limitação de escalabilidade da força bruta para problemas maiores, futuras pesquisas incluirão:

1.  **Implementação de Heurísticas:** Desenvolvimento de algoritmos aproximados (e.g., Vizinho Mais Próximo, Algoritmos Genéticos) para soluções de alta qualidade em tempo viável.
2.  **Enriquecimento do Modelo:** Inclusão de restrições realistas como limite de bateria, capacidade de carga e priorização de entregas.
3.  **Roteamento Dinâmico:** Capacidade de recalcular rotas em tempo real para novos pedidos.
