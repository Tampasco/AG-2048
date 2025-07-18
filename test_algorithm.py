# Testes TDD para o algoritmo genético

import random
import algorithm as ag
from unittest.mock import patch

# Criação de Individuo de tamanho variavel

def test_avaliarGeracaoDeIndividuo():
    individuo = ag.generate_individual(10)

    assert len(individuo) == 10
    for e in individuo:
        assert e in ["up", "left", "right", "down"]

# Simulação do jogo feito pelo individuo gerado

def test_avaliarSimulacaoDoJogo():
    individuo = ag.generate_individual(10)
    maior_tile, movimentos = ag.simular_jogo(individuo)

    assert maior_tile <= 2048 and maior_tile >= 2
    assert movimentos <= 10 

# Criação de população de individuos de tamanho variavel

def test_avaliarGeracaoDePopulacao():
    populacao = ag.generate_population(10,10)
    populacao_sem_movimentos = ag.generate_population(10,0)

    assert len(populacao) == 10
    for i in range(len(populacao)):
        assert len(populacao[i]) == 10
        for e in populacao[i]:
            assert e in ["up", "left", "right", "down"]

    for p in populacao_sem_movimentos:
        assert len(p) == 0

# Funçao de aptidão com base em Monte Carlo
# Esse teste visa verificar se os resultados estão dentro do limite

def test_avaliarFuncaoAptidaoDentroDosLimites():
    individuo = ag.generate_individual(10)

    resultado = ag.fitness(individuo, 10)
    # Máximo e minimo possíveis que o fitness pode chegar com 10 movimentos
    assert resultado <= 2048 and resultado >= 0
    

def test_avaliarFuncaoDeAvaliacaoDePopulacaoUsandoMock():

    # População desejada (ação de um agente, por exemplo)
    populacao_fake = [
        ["left", "up", "up"],
        ["down", "up", "down"],
        ["right", "left", "right"]
    ]

    # Avaliações desejadas (fitness)
    avaliacoes_desejadas = [0.2, 0.5, 0.7]

    # Esperado: combinação indivíduo + valor
    esperado = list(zip(avaliacoes_desejadas,populacao_fake))

    with patch.object(ag, "generate_population", return_value=populacao_fake), \
         patch.object(ag, "avaliar_populacao", return_value=esperado) as avaliar_mock:

        populacao = ag.generate_population(3, 3)  # geraria 3 indivíduos de 3 ações cada
        resultado = ag.avaliar_populacao(populacao, 10)

    assert resultado == esperado
    assert avaliar_mock.call_count == 1
    avaliar_mock.assert_called_once_with(populacao_fake, 10)


# Esse teste serve para avaliar como será a escolha dos melhores indiviuos(pais)

def test_avaliarSelecaoDePopulacaoNormal():
    populacao_avaliada = [
        (0.3, ["left"]),
        (0.9, ["right"]),
        (0.1, ["down"]),
        (0.8, ["up"])
    ]

    pais = ag.selecionar_pais(populacao_avaliada, 2)

    assert pais == [["right"], ["up"]]  # melhores fitness: 0.9 e 0.8

def test_avaliarSelecaoDePopulacaoVazia():
    populacao_vazia = ag.generate_population(0,0)
    pais = ag.selecionar_pais(populacao_vazia, 3)

    assert pais == []

def test_avaliarSelecaoDePopulacaoIgual():
    populacao_avaliada = [
        (0.5,["left"]),
        (0.5,["right"]),
        (0.5,["up"])
    ]

    pais = ag.selecionar_pais(populacao_avaliada, 2)

    # Pode aceitar qualquer ordem nesse caso, contanto que os pais estejam certos
    assert len(pais) == 2
    for p in pais:
        assert p in [["up"], ["right"], ["left"]]

#Cruzamento
def test_avaliarCruzamento():
    pai1 = ["up", "up", "down", "left"]
    pai2 = ["left", "right", "up", "down"]

    with patch("algorithm.random.randint", return_value=2):
        filho1, filho2 = ag.cruzar(pai1, pai2)

    assert filho1 == ["up", "up", "up", "down"]
    assert filho2 == ["left", "right", "down", "left"]

def test_avaliarMutacaoComProbabilidadeCerteira():
    individuo = ["up", "up", "up"]

    # Sempre sorteia "down" para cada mutação
    # Assumindo que a escolha do movimento novo seja com random.choice
    with patch("algorithm.random.random", return_value=0.0), \
         patch("algorithm.random.choice", return_value="down"):
            mutado = ag.mutar(individuo, 1.0)

    assert mutado == ["down", "down", "down"]

def test_avaliarMutacaoComProbabilidade50porcento():
    individuo = ["up", "down", "left"]

    # Simula mutação só no primeiro e no terceiro gene
    with patch("algorithm.random.random", side_effect=[0.3, 0.7, 0.4]), \
         patch("algorithm.random.choice", side_effect=["right", "up"]):
        mutado = ag.mutar(individuo, 0.5)

    assert mutado == ["right", "down", "up"]

def test_avaliarGeracaoDeNovaPopulacao():
    pai1 = ["up", "up", "left", "down"]
    pai2 = ["down", "down", "right", "up"]
    populacao = [pai1, pai2]
    populacao_avaliada = ag.avaliar_populacao(populacao, 10)

    with patch.object(ag, "cruzar", return_value=(["up", "up","right", "up"], ["down", "down","left", "down"])) as mock_cruzar, \
         patch.object(ag, "mutar", side_effect=lambda ind, _: ind) as mock_mutar:
        
        nova_pop = ag.gerar_nova_populacao(populacao_avaliada, 2, 0.1,2)

    assert nova_pop == [["up", "up","right", "up"], ["down", "down","left", "down"]]
    # Cruamento deve ser chamado 1 vez
    assert mock_cruzar.call_count == 1
    # Mutar deve ser chamado 2 vezes
    assert mock_mutar.call_count == 2

def test_avaliarCalculoMetricas():
    fitness_geral = [0.3, 0.5, 0, 0.9, 0.99]
    fitness_vazio = []

    metricas = ag.calcular_metricas(fitness_geral)

    assert metricas["melhor_fitness"] == 0.99
    assert metricas["pior_fitness"] == 0

    metricas = ag.calcular_metricas(fitness_vazio)

    assert metricas["medio_fitness"] == 0 
    assert metricas["desvio_padrao"] == 0
    assert metricas["mediana"] == 0

def test_avaliarRodarAlgoritmoGenetico():
    # Simular as chamadas das funções
    with patch.object(ag, "generate_population") as mock_generate, \
         patch.object(ag, "avaliar_populacao") as mock_avaliar, \
         patch.object(ag, "calcular_metricas") as mock_metricas, \
         patch.object(ag, "gerar_nova_populacao") as mock_gerar_nova:

        # Usando mock para gerar população inicial
        mock_generate.return_value = [["up", "down", "left"], ["down", "left", "right"]]
        mock_avaliar.return_value = [(0.8, ["up", "down", "left"]), (0.5, ["down", "left", "right"])]

        # Métricas para cada avaliação 
        mock_metricas.return_value = {
            "melhor_fitness": 0.8,
            "pior_fitness": 0.5,
            "medio_fitness": 0.8,
            "desvio_padrao": 0.6,
            "mediana": 0.7
        }

        mock_gerar_nova.return_value = [["up", "up", "left"],  ["down", "down", "right"]]

        # Executa o AG por 3 gerações
        resultado = ag.rodar_ag(3, 1, 3, 0.4, 1)

        melhor_fitness, melhor_individuo = resultado # Resultado baseado nas simulações

        assert melhor_fitness == 0.8
        assert melhor_individuo == ["up", "down", "left"]
        assert mock_avaliar.call_count == 3
        assert mock_gerar_nova.call_count == 2





