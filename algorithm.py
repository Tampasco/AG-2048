import random
import csv
import time
import statistics
from mocks import simular_jogo_mock as simular_jogo # Após a implementação real, importar o módulo correto.

valid_moves = ['up', 'down', 'left', 'right']


def generate_individual(size):
    return [random.choice(valid_moves) for _ in range(size)]


def generate_population(population_size, individual_size):
    return [generate_individual(individual_size) for _ in range(population_size)]



def fitness(individuo: list[str], num_simulacoes: int) -> float:
    if not individuo or num_simulacoes == 0:
        return 0.0
    
    soma_maior_tile = 0
    
    for _ in range(num_simulacoes):
        maior_tile, movimentos_validos = simular_jogo(individuo)
        soma_maior_tile += maior_tile
    # O fitness final do indivíduo é a média da maior peça alcançada
    return soma_maior_tile / num_simulacoes


def avaliar_populacao(populacao: list[list[str]], num_simulacoes: int) -> list[tuple[float, list[str]]]:
    populacao_avaliada = []
    for individuo in populacao:
        fitness_do_individuo = fitness(individuo, num_simulacoes)
        populacao_avaliada.append((fitness_do_individuo, individuo))

    return populacao_avaliada

def selecionar_pais(populacao_com_fitness: list[tuple[float, list[str]]], n: int) -> list[list[str]]:
    # Resolvi usar a estratégia do Elitismo.
    populacao_com_fitness.sort(key=lambda item: item[0], reverse=True)
    n_melhores = populacao_com_fitness[:n]
    # Extrai apenas a parte do indivíduo (item[1] da tupla) para criar a lista de pais
    pais = [individuo for fitness, individuo in n_melhores]
    return pais


def cruzar(pai1: list[str], pai2: list[str]) -> tuple[list[str], list[str]]:
    # Estratégia de Single Point Crossover
    tamanho = len(pai1)
    ponto_corte = random.randint(1, tamanho - 1)

    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

    return filho1, filho2


def mutar(individuo: list[str], taxa_mutacao: float) -> list[str]:
    mutante = individuo.copy()

    for i in range(len(mutante)):
        if random.random() < taxa_mutacao:
            mutante[i] = random.choice(valid_moves)
    
    return mutante


def gerar_nova_populacao(populacao_com_fitness: list[tuple[float, list[str]]], tamanho_pop: int, taxa_mutacao: float, num_pais: int) -> list[list[str]]:
    pais = selecionar_pais(populacao_com_fitness, num_pais)
    
    nova_populacao = []
    
    # Manter os melhores pais na nova geração (elitismo)
    nova_populacao.extend(pais)
    
    # Gerar filhos através de cruzamento até atingir o tamanho desejado da população
    while len(nova_populacao) < tamanho_pop:
        # Selecionar dois pais aleatoriamente
        pai1 = random.choice(pais)
        pai2 = random.choice(pais)
        
        # Realizar cruzamento
        filho1, filho2 = cruzar(pai1, pai2)
        
        # Aplicar mutação nos filhos
        filho1_mutado = mutar(filho1, taxa_mutacao)
        filho2_mutado = mutar(filho2, taxa_mutacao)
        
        # Adicionar filhos à nova geração
        if len(nova_populacao) < tamanho_pop:
            nova_populacao.append(filho1_mutado)
        if len(nova_populacao) < tamanho_pop:
            nova_populacao.append(filho2_mutado)
    
    return nova_populacao


def calcular_metricas(fitness_geral: list[float]):
    melhor_fitness = max(fitness_geral)
    pior_fitness = min(fitness_geral)
    medio_fitness = statistics.mean(fitness_geral)
    desvio_padrao = statistics.stdev(fitness_geral) if len(fitness_geral) > 1 else 0
    mediana = statistics.median(fitness_geral)
    
    metricas = {
        "melhor_fitness": melhor_fitness,
        "pior_fitness": pior_fitness,
        "medio_fitness": medio_fitness,
        "desvio_padrao": desvio_padrao,
        "mediana": mediana
    }
    
    return metricas


def rodar_ag(populacoes: int, tamanho_pop: int, tamanho_individuo: int, taxa_mutacao: float, num_simulacoes: int) -> tuple[float, list[str]]:
    # Configurar parametros
    num_pais = max(2, tamanho_pop // 2)
    tempo_inicio = time.time()
    melhor_fitness_historico = []
    melhor_individuo_global = None
    melhor_fitness_global = float('-inf')

    # Criar populacao original
    populacao = generate_population(tamanho_pop, tamanho_individuo)
    ciclos = 0

    # Ciclo evolutivo
    while ciclos < populacoes:

        # Avaliar populacao atual
        populacao_avaliada = avaliar_populacao(populacao, num_simulacoes)

        # Calcular metricas
        fitness_geral = [fitness_val for fitness_val, _ in populacao_avaliada]
        metricas = calcular_metricas(fitness_geral)

        # Atualizar melhor global
        melhor_fitness = metricas["melhor_fitness"]
        if melhor_fitness > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness
            melhor_individuo_global = max(populacao_avaliada, key=lambda x: x[0])[1].copy()
        
        # Evoluir populacao
        if ciclos < populacoes - 1:
            populacao = gerar_nova_populacao(populacao_avaliada, tamanho_pop, taxa_mutacao, num_pais)
        ciclos += 1

    return melhor_fitness_global, melhor_individuo_global