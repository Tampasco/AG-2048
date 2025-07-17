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

    if len(pai1) != len(pai2):
        raise ValueError("Os pais precisam ser do mesmo tamanho")
    
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


def gerar_nova_geracao(populacao_com_fitness: list[tuple[float, list[str]]], tamanho_pop: int, taxa_mutacao: float, num_pais: int) -> list[list[str]]:
    pais = selecionar_pais(populacao_com_fitness, num_pais)
    
    nova_geracao = []
    
    # Manter os melhores pais na nova geração (elitismo)
    nova_geracao.extend(pais)
    
    # Gerar filhos através de cruzamento até atingir o tamanho desejado da população
    while len(nova_geracao) < tamanho_pop:
        # Selecionar dois pais aleatoriamente
        pai1 = random.choice(pais)
        pai2 = random.choice(pais)
        
        # Realizar cruzamento
        filho1, filho2 = cruzar(pai1, pai2)
        
        # Aplicar mutação nos filhos
        filho1_mutado = mutar(filho1, taxa_mutacao)
        filho2_mutado = mutar(filho2, taxa_mutacao)
        
        # Adicionar filhos à nova geração
        if len(nova_geracao) < tamanho_pop:
            nova_geracao.append(filho1_mutado)
        if len(nova_geracao) < tamanho_pop:
            nova_geracao.append(filho2_mutado)
    
    return nova_geracao


def rodar_ag(geracoes: int, tamanho_pop: int, tamanho_individuo: int, taxa_mutacao: float, num_simulacoes: int) -> tuple[float, list[str]]:
    # Validação de parâmetros
    if geracoes <= 0 or tamanho_pop <= 0 or tamanho_individuo <= 0:
        raise ValueError("Parâmetros devem ser positivos")
    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("Taxa de mutação deve estar entre 0 e 1")
    if num_simulacoes <= 0:
        raise ValueError("Número de simulações deve ser positivo")
    
    # Configuração inicial
    num_pais = max(2, tamanho_pop // 2)  # Número de pais para seleção
    tempo_inicio = time.time()
    melhor_fitness_historico = []
    melhor_individuo_global = None
    melhor_fitness_global = float('-inf')
    
    # 1. INICIALIZAÇÃO - Gerar população inicial
    populacao = generate_population(tamanho_pop, tamanho_individuo)
    
    # Arquivo CSV para registrar métricas
    with open('ga_metricas.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        
        # Cabeçalho do CSV
        escritor.writerow([
            'Geracao', 'Melhor_Fitness', 'Fitness_Medio', 'Pior_Fitness', 
            'Desvio_Padrao', 'Mediana', 'Quartil_Q1', 'Quartil_Q3',
            'Diversidade_Genetica', 'Taxa_Convergencia', 'Tempo_Geracao_s',
            'Tempo_Acumulado_s', 'Operacoes_Fitness', 'Complexidade_O_n'
        ])
        
        # CICLO PRINCIPAL DO ALGORITMO GENÉTICO
        for geracao in range(geracoes):
            tempo_geracao_inicio = time.time()
            
            # 2. AVALIAÇÃO - Calcular fitness de toda a população
            populacao_avaliada = avaliar_populacao(populacao, num_simulacoes)
            
            # 3. EXTRAÇÃO DE MÉTRICAS ESTATÍSTICAS
            fitness_values = [fitness_val for fitness_val, _ in populacao_avaliada]
            
            melhor_fitness = max(fitness_values)
            fitness_medio = statistics.mean(fitness_values)
            pior_fitness = min(fitness_values)
            desvio_padrao = statistics.stdev(fitness_values) if len(fitness_values) > 1 else 0
            mediana = statistics.median(fitness_values)
            
            # Quartis
            fitness_sorted = sorted(fitness_values)
            n = len(fitness_sorted)
            q1 = fitness_sorted[n//4] if n > 3 else fitness_sorted[0]
            q3 = fitness_sorted[3*n//4] if n > 3 else fitness_sorted[-1]
            
            # 4. ATUALIZAÇÃO DO MELHOR GLOBAL
            if melhor_fitness > melhor_fitness_global:
                melhor_fitness_global = melhor_fitness
                melhor_individuo_global = max(populacao_avaliada, key=lambda x: x[0])[1].copy()
            
            # 5. CÁLCULO DE MÉTRICAS AVANÇADAS
            # Diversidade genética (coeficiente de variação)
            diversidade_genetica = desvio_padrao / fitness_medio if fitness_medio > 0 else 0
            
            # Taxa de convergência (melhoria relativa)
            melhor_fitness_historico.append(melhor_fitness)
            if geracao > 0:
                fitness_anterior = melhor_fitness_historico[geracao-1]
                taxa_convergencia = (melhor_fitness - fitness_anterior) / fitness_anterior if fitness_anterior > 0 else 0
            else:
                taxa_convergencia = 0
            
            # 6. MÉTRICAS DE TEMPO E COMPLEXIDADE
            tempo_geracao_fim = time.time()
            tempo_geracao = tempo_geracao_fim - tempo_geracao_inicio
            tempo_acumulado = tempo_geracao_fim - tempo_inicio
            operacoes_fitness = tamanho_pop * num_simulacoes
            
            # 7. REGISTRO DE MÉTRICAS NO CSV
            escritor.writerow([
                geracao + 1, round(melhor_fitness, 4), round(fitness_medio, 4), 
                round(pior_fitness, 4), round(desvio_padrao, 4), round(mediana, 4),
                round(q1, 4), round(q3, 4), round(diversidade_genetica, 4),
                round(taxa_convergencia, 6), round(tempo_geracao, 4),
                round(tempo_acumulado, 4), operacoes_fitness, tamanho_pop
            ])
            
            # 8. SELEÇÃO, CRUZAMENTO E MUTAÇÃO - Gerar próxima geração
            if geracao < geracoes - 1:  # Não gerar nova população na última geração
                try:
                    populacao = gerar_nova_geracao(
                        populacao_avaliada, 
                        tamanho_pop, 
                        taxa_mutacao, 
                        num_pais
                    )
                except Exception as e:
                    # Em caso de erro, manter população atual e continuar
                    print(f"Aviso: Erro na geração {geracao + 1}: {e}")
                    break
    
    # 10. GERAÇÃO DO RELATÓRIO FINAL
    tempo_total = time.time() - tempo_inicio
    
    with open('ga_relatorio.txt', 'w', encoding='utf-8') as relatorio:
        relatorio.write("RELATÓRIO DE DESEMPENHO - ALGORITMO GENÉTICO\n")
        relatorio.write("=" * 50 + "\n\n")
        
        relatorio.write("PARÂMETROS DE EXECUÇÃO:\n")
        relatorio.write(f"- Gerações executadas: {len(melhor_fitness_historico)}/{geracoes}\n")
        relatorio.write(f"- Tamanho da população: {tamanho_pop}\n")
        relatorio.write(f"- Tamanho do indivíduo: {tamanho_individuo}\n")
        relatorio.write(f"- Taxa de mutação: {taxa_mutacao}\n")
        relatorio.write(f"- Número de simulações por fitness: {num_simulacoes}\n")
        relatorio.write(f"- Número de pais selecionados: {num_pais}\n\n")
        
        relatorio.write("ANÁLISE DE COMPLEXIDADE:\n")
        relatorio.write(f"- Complexidade temporal: O(G × P × S × I)\n")
        relatorio.write(f"  onde G={len(melhor_fitness_historico)}, P={tamanho_pop}, S={num_simulacoes}, I={tamanho_individuo}\n")
        relatorio.write(f"- Complexidade espacial: O(P × I) = O({tamanho_pop} × {tamanho_individuo})\n")
        relatorio.write(f"- Operações totais de fitness: {len(melhor_fitness_historico) * tamanho_pop * num_simulacoes:,}\n\n")
        
        relatorio.write("MÉTRICAS DE TEMPO:\n")
        relatorio.write(f"- Tempo total de execução: {tempo_total:.4f} segundos\n")
        
        relatorio.write("ANÁLISE DE CONVERGÊNCIA:\n")
        if len(melhor_fitness_historico) > 1:
            fitness_inicial = melhor_fitness_historico[0]
            fitness_final = melhor_fitness_historico[-1]
            melhoria_total = ((fitness_final - fitness_inicial) / fitness_inicial * 100) if fitness_inicial > 0 else 0
            
            relatorio.write(f"- Fitness inicial: {fitness_inicial:.4f}\n")
            relatorio.write(f"- Fitness final: {fitness_final:.4f}\n")
            relatorio.write(f"- Melhor fitness global: {melhor_fitness_global:.4f}\n")
            relatorio.write(f"- Melhoria total: {melhoria_total:.2f}%\n\n")
            
            # Intervalos de confiança (95%)
            if len(melhor_fitness_historico) > 1:
                media_fitness = statistics.mean(melhor_fitness_historico)
                desvio_fitness = statistics.stdev(melhor_fitness_historico)
                margem_erro = 1.96 * (desvio_fitness / (len(melhor_fitness_historico) ** 0.5))
                relatorio.write("INTERVALOS DE CONFIANÇA (95%):\n")
                relatorio.write(f"- Fitness médio: {media_fitness:.4f} ± {margem_erro:.4f}\n")
                relatorio.write(f"- Intervalo: [{media_fitness - margem_erro:.4f}, {media_fitness + margem_erro:.4f}]\n\n")
        
        relatorio.write("RESULTADO FINAL:\n")
        relatorio.write(f"- Melhor fitness alcançado: {melhor_fitness_global:.4f}\n")
        relatorio.write(f"- Sequência de movimentos (primeiros 20): {melhor_individuo_global[:20] if melhor_individuo_global else 'N/A'}\n")
        relatorio.write(f"- Arquivo de métricas: ga_metricas.csv\n")
    
    # 11. RETORNO DO RESULTADO FINAL
    return melhor_fitness_global, melhor_individuo_global if melhor_individuo_global else []