from mocks import simular_jogo_mock as simular_jogo # Após a implementação real, importar o módulo correto.

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
    #Resolvi usar a estratégia do Elitismo.
    populacao_com_fitness.sort(key=lambda item: item[0], reverse=True)
    n_melhores = populacao_com_fitness[:n]
    # Extrai apenas a parte do indivíduo (item[1] da tupla) para criar a lista de pais
    pais = [individuo for fitness, individuo in n_melhores]
    return pais