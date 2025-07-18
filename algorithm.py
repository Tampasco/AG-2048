

import random
import statistics
import logic
import constants as c

valid_moves = ['up', 'down', 'left', 'right']


def executar_jogo(individuo: list[str]) -> tuple[int, int]:
    movimentos_map = {
        'up': logic.up,
        'down': logic.down,
        'left': logic.left,
        'right': logic.right
    }

    matriz = logic.new_game(c.GRID_LEN)
    movimentos_validos = 0
    maior_numero = 0

    for movimento in individuo:
        if movimento not in movimentos_map:
            continue

        estado_jogo = logic.game_state(matriz)
        if estado_jogo in ('lose', 'win'):
            break

        matriz, movimento_realizado = movimentos_map[movimento](matriz)

        if movimento_realizado:
            matriz = logic.add_two(matriz)
            movimentos_validos += 1
            for linha in matriz:
                for numero in linha:
                    maior_numero = max(maior_numero, numero)

    if maior_numero == 0:
        for linha in matriz:
            for numero in linha:
                maior_numero = max(maior_numero, numero)

    return maior_numero, movimentos_validos


def generate_individual(size: int) -> list[str]:
    return [random.choice(valid_moves) for _ in range(size)]


def generate_population(population_size: int, individual_size: int) -> list[list[str]]:
    return [generate_individual(individual_size) for _ in range(population_size)]


def fitness(individuo: list[str], num_simulacoes: int) -> float:
    if not individuo or num_simulacoes == 0:
        return 0.0

    soma_maior_tile = 0
    for _ in range(num_simulacoes):
        maior_tile, _ = executar_jogo(individuo)
        soma_maior_tile += maior_tile

    return soma_maior_tile / num_simulacoes


def avaliar_populacao(
    populacao: list[list[str]], num_simulacoes: int
) -> list[tuple[float, list[str]]]:
    return [(fitness(individuo, num_simulacoes), individuo) for individuo in populacao]


def selecionar_pais(
    populacao_com_fitness: list[tuple[float, list[str]]], n: int
) -> list[list[str]]:
    populacao_com_fitness.sort(key=lambda item: item[0], reverse=True)
    return [individuo for _, individuo in populacao_com_fitness[:n]]


def cruzar(pai1: list[str], pai2: list[str]) -> tuple[list[str], list[str]]:
    tamanho = len(pai1)
    ponto_corte = random.randint(1, tamanho - 1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2


def mutar(individuo: list[str], taxa_mutacao: float) -> list[str]:
    mutante = individuo.copy()
    for i, _ in enumerate(mutante):
        if random.random() < taxa_mutacao:
            mutante[i] = random.choice(valid_moves)
    return mutante


def gerar_nova_populacao(
    populacao_com_fitness: list[tuple[float, list[str]]],
    tamanho_pop: int,
    taxa_mutacao: float,
    num_pais: int
) -> list[list[str]]:
    pais = selecionar_pais(populacao_com_fitness, num_pais)
    nova_populacao = pais.copy()

    while len(nova_populacao) < tamanho_pop:
        pai1 = random.choice(pais)
        pai2 = random.choice(pais)
        filho1, filho2 = cruzar(pai1, pai2)
        nova_populacao.append(mutar(filho1, taxa_mutacao))
        if len(nova_populacao) < tamanho_pop:
            nova_populacao.append(mutar(filho2, taxa_mutacao))

    return nova_populacao


def calcular_metricas(fitness_geral: list[float]) -> dict[str, float]:
    return {
        "melhor_fitness": max(fitness_geral),
        "pior_fitness": min(fitness_geral),
        "medio_fitness": statistics.mean(fitness_geral),
        "desvio_padrao": statistics.stdev(fitness_geral) if len(fitness_geral) > 1 else 0,
        "mediana": statistics.median(fitness_geral)
    }


def rodar_ag(
    populacoes: int,
    tamanho_pop: int,
    tamanho_individuo: int,
    taxa_mutacao: float,
    num_simulacoes: int
) -> tuple[float, list[str]]:
    num_pais = max(2, tamanho_pop // 2)
    melhor_individuo_global = None
    melhor_fitness_global = float('-inf')
    populacao = generate_population(tamanho_pop, tamanho_individuo)

    for _ in range(populacoes):
        populacao_avaliada = avaliar_populacao(populacao, num_simulacoes)
        fitness_geral = [fitness_val for fitness_val, _ in populacao_avaliada]
        metricas = calcular_metricas(fitness_geral)
        melhor_fitness = metricas["melhor_fitness"]

        if melhor_fitness > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness
            melhor_individuo_global = max(
                populacao_avaliada, key=lambda x: x[0]
            )[1].copy()

        populacao = gerar_nova_populacao(
            populacao_avaliada, tamanho_pop, taxa_mutacao, num_pais
        )

    return melhor_fitness_global, melhor_individuo_global
