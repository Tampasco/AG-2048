import random
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


def cruzar(pai1: List[str], pai2: List[str]) -> Tuple[List[str], List[str]]:
    tamanho = len(pai1)
    ponto_corte = random.randint(1, tamanho - 1)

    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

    return filho1, filho2
