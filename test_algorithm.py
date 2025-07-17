# Testes TDD para o algoritmo genético

import random
from unittest.mock import patch
from algorithm as ag


# Criação de Individuo de tamanho variavel

def avaliarGeracaoDeIndividuo():
    individuo = ag.generate_individual(10)

    assert len(individuo) == 10
    for e in individuo:
        assert e in ["up", "left", "right", "down"]

# Simulação do jogo feito pelo individuo gerado

def avaliarSimulacaoDoJogo():
    individuo = ag.generate_individual(10)
    maior_tile, movimentos = ag.simular_jogo(individuo)

    assert maior_tile <= 2048 and maior_tile >= 2
    assert movimentos <= 10

    

# Criação de população de individuos de tamanho variavel

def avaliarGeracaoDePopulacao():
    populacao = ag.generate_population(10,10)
    populacao_sem_movimentos = ag.generate_population(10,0)

    assert len(populacao) == 10
    for e in populacao:
        assert len(e) == 10
        assert e in ["up", "left", "right", "down"]

    for p in populacao_sem_movimentos:
        assert len(p) == 0

# Funçao de aptidão com base em Monte Carlo
# Esse teste visa verificar se os resultados estão dentro do limite

def avaliarFuncaoAptidaoDentroDosLimites():
    individuo = ag.generate_individual(10)

    resultado = ag.fitness(individuo, 10)
    # Máximo e minimo possíveis que o fitness pode chegar com 10 movimentos
    assert resultado <= 2048 and resultado >= 0
    

def avaliarFuncaoDeAvaliacaoDePopulacaoUsandoMock():

    # População desejada (ação de um agente, por exemplo)
    populacao_fake = [
        ["left", "up", "up"],
        ["down", "up", "down"],
        ["right", "left", "right"]
    ]

    # Avaliações desejadas (fitness)
    avaliacoes_desejadas = [0.2, 0.5, 0.7]

    # Esperado: combinação indivíduo + valor
    esperado = list(zip(populacao_fake, avaliacoes_desejadas))

    with patch.object(ag, "gerar_populacao", return_value=populacao_fake), \
         patch.object(ag, "avaliar_populacao", return_value=esperado) as avaliar_mock:

        populacao = ag.gerar_populacao(3, 3)  # geraria 3 indivíduos de 3 ações cada
        resultado = ag.avaliar_populacao(populacao, 10)

    assert resultado == esperado
    assert avaliar_mock.call_count == 1
    avaliar_mock.assert_called_once_with(populacao_fake, 10)



# Esse teste serve para avaliar como será a escolha dos melhores indiviuos(pais)

def avaliarSelecaoDePopulacaoNormal():
    populacao_avaliada = [
        (["left"], 0.3),
        (["right"], 0.9),
        (["down"], 0.1),
        (["up"], 0.8)
    ]

    pais = ag.selecionar_pais(populacao_avaliada, 2)

    assert pais == [["right"], ["up"]]  # melhores fitness: 0.9 e 0.8

def avaliarSelecaoDePopulacaoVazia():
    populacao_vazia = ag.gerar_populacao(0,0)
    pais = ag.selecionar_pais(populacao, 3)

    assert pais == []

def avaliarSelecaoDePopulacaoIgual():
    populacao_avaliada = [
        (["left"], 0.5),
        (["right"], 0.5),
        (["up"], 0.5)
    ]

    pais = ag.selecionar_pais(populacao_avaliada, 2)

    # Pode aceitar qualquer ordem nesse caso, contanto que os pais estejam certos
    assert len(pais) == 2
    for p in pais:
        assert p in [["up"], ["right"], ["left"]]

#Cruzamento
def avaliarCruzamento():
    pai1 = ["up", "up", "down", "left"]
    pai2 = ["left", "right", "up", "down"]

    
    filho1, filho2 = ag.cruzar(pai1, pai2)

    assert filho1 == ["up", "up", "up", "down"]
    assert filho2 == ["left", "right", "down", "left"]

def avaliarMutacaoComProbabilidadeCerteira():
    individuo = ["up", "up", "up"]

    # Sempre sorteia "down" para cada mutação
    with patch("algorithm.random.random", return_value=0.0), \
        #A ssumindo que a escolha do movimento novo seja com random.choice
         patch("algorithm.random.choice", return_value="down"):
            mutado = ag.mutar(individuo, 1.0)

    assert mutado == ["down", "down", "down"]

def avaliarMutacaoComProbabilidade50porcento():
    individuo = ["up", "down", "left"]

    # Simula mutação só no primeiro e no terceiro gene
    with patch("algorithm.random.random", side_effect=[0.3, 0.7, 0.4]), \
         patch("algorithm.random.choice", side_effect=["right", "up"]):
        mutado = ag.mutar(individuo, 0.5)

    assert mutado == ["right", "down", "up"]

def avaliarGeracaoDeNovaPopulacao():
    pai1 = ["up", "up", "left", "down"]
    pai2 = ["down", "down", "right", "up"]
    pais = [pai1, pai2]

    with patch.object(ag, "cruzar", return_value=(["up", "up","right", "up"], ["down", "down","left", "down"])) as mock_cruzar, \
         patch.object(ag, "mutar", side_effect=lambda ind, _: ind) as mock_mutar:
        
        nova_pop = ag.gerar_nova_geracao(pais, 2, 0.1)

    assert nova_pop == [["up", "up","right", "up"], ["down", "down","left", "down"]]
    # Cruamento deve ser chamado 1 vez
    assert mock_cruzar.call_count == 1
    # Mutar deve ser chamado 2 vezes
    assert mock_mutar.call_count == 2




