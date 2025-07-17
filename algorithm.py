"""Algoritmo genético para jogar 2048 automaticamente."""

import random

# pylint: disable=import-error
import logic
import constants as c

valid_moves = ['up', 'down', 'left', 'right']

# Executa uma simulação do jogo com um indivíduo (lista de movimentos).
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

#Gera uma lista de movimentos aleatórios (indivíduo).
def generate_individual(size):

    return [random.choice(valid_moves) for _ in range(size)]


def generate_population(population_size, individual_size):
    """Gera uma população de indivíduos aleatórios."""
    return [generate_individual(individual_size) for _ in range(population_size)]


def fitness(individuo: list[str], num_simulacoes: int) -> float:
    """Calcula o fitness de um indivíduo com base em várias simulações."""
    if not individuo or num_simulacoes == 0:
        return 0.0

    soma_maior_tile = 0
    for _ in range(num_simulacoes):
        maior_tile, _ = executar_jogo(individuo)
        soma_maior_tile += maior_tile

    return soma_maior_tile / num_simulacoes

# Avalia uma população de indivíduos e retorna fitness + indivíduo.
def avaliar_populacao(
    populacao: list[list[str]], num_simulacoes: int
) -> list[tuple[float, list[str]]]:
    populacao_avaliada = []
    for individuo in populacao:
        fitness_do_individuo = fitness(individuo, num_simulacoes)
        populacao_avaliada.append((fitness_do_individuo, individuo))

    return populacao_avaliada

# Seleciona os N melhores indivíduos como pais (elitismo).
def selecionar_pais(
    populacao_com_fitness: list[tuple[float, list[str]]], n: int
) -> list[list[str]]:
    
    populacao_com_fitness.sort(key=lambda item: item[0], reverse=True)
    n_melhores = populacao_com_fitness[:n]
    return [individuo for _, individuo in n_melhores]
