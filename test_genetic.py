# Rascunho do TDD

import random
from unittest.mock import patch
from AlgoritmoGenetico as ag

# Funçao de aptidão com base em Monte Carlo
# Esse teste visa verificar se os resultados estão dentro do limite
# do conceito de probabilidade do resultado(de 0% a 100%)

def AvaliarFuncaoAptidaoDentroDosLimites():
    populacao = gerar_populacao(10,20)

    populacao_avaliada = avaliar_populacao(populacao, 10)
    for i in range(len(populacao_avaliada)):
        individuo, resultado = populacao_avaliada[i]

        assert resultado >= 0 and resultado <= 1

def AvaliarFuncaoAptidaoUsandoMock():

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

def AvaliarSelecaoDePopulacaoNormal():
    populacao_avaliada = [
        (["left"], 0.3),
        (["right"], 0.9),
        (["down"], 0.1),
        (["up"], 0.8)
    ]

    pais = ag.selecionar_pais(populacao_avaliada, 2)

    assert pais == [["right"], ["up"]]  # melhores fitness: 0.9 e 0.8

def AvaliarSelecaoDePopulacaoVazia():
    populacao_vazia = ag.gerar_populacao(0,0)
    pais = ag.selecionar_pais(populacao, 3)

    assert pais == []

def AvaliarSelecaoDePopulacaoIgual() :
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
#   def AvaliarCruzamento() [...]


