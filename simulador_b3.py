# DESENVOLVIDO POR: Gustavo Baron Lauritzen, Matheus Baron Lauritzen e Gabriel Bósio

import pandas as pd
import random
import numpy as np

# === CONFIGURAÇÃO ===
CSV_PATH = "dataset/cotacoes_b3_2025_05.csv"  # Caminho do dataset de cotações
INITIAL_CAPITAL = 1000.0                      # Capital inicial
POP_SIZE = 100                                 # Tamanho da população (quantos DNAs por geração)
NUM_GENERATIONS = 5000                         # Número de gerações a evoluir
MUTATION_RATE = 0.1                           # Taxa de mutação (10%)
NUM_POTS = 10                                 # Número de potes de investimento (ações simultâneas)

# === CARREGAR DADOS ===
data = pd.read_csv(CSV_PATH, sep=';', engine='python')  # Lê o CSV
data.columns = ['Data', 'Codigo', 'Fechamento']         # Renomeia as colunas
data['Fechamento'] = data['Fechamento'].str.replace(',', '.').astype(float)  # Converte o valor
data = data[data['Codigo'].str.match(r'^[A-Z0-9]{5}$')]      # Filtra ações com códigos de 5 caracteres
data['Data'] = pd.to_datetime(data['Data'])               # Converte a coluna de data
data = data.sort_values(by='Data')                        # Ordena cronologicamente

# === TABELA DE PREÇOS ===
#Uma tabela onde o índice é a data e cada coluna é uma ação
price_table = data.pivot(index='Data', columns='Codigo', values='Fechamento').sort_index()
dates = price_table.index
day_pairs = [(dates[i], dates[i+1]) for i in range(0, len(dates) - 1, 2)]  # Cria pares de dias: compra/venda
NUM_CYCLES = len(day_pairs)                             # Quantos ciclos temos (10 para 20 dias úteis)
TOTAL_GENES = NUM_CYCLES * NUM_POTS                    # Quantos genes tem um DNA
VALID_CODES = list(price_table.columns.dropna())       # Lista de ações válidas


# === FUNÇÕES GENÉTICAS ===

def random_dna():
    return [random.choice(VALID_CODES) for _ in range(TOTAL_GENES)]  # Cria uma lista com TOTAL_GENES ações aleatórias (códigos válidos)

def evaluate_dna(dna):  # Avalia quão bom é esse DNA (quanto dinheiro ele gera)
    capital = INITIAL_CAPITAL  # Começa com o capital inicial
    
    for cycle_index, (buy_day, sell_day) in enumerate(day_pairs):  # Para cada par de dias (compra e venda)
        buy_prices = price_table.loc[buy_day]    # Preços no dia de compra
        sell_prices = price_table.loc[sell_day]  # Preços no dia de venda
        
        cycle_genes = dna[cycle_index * NUM_POTS: (cycle_index + 1) * NUM_POTS]  # Genes (ações) usados nesse ciclo
        
        pot_value = capital / NUM_POTS  # Cada pote recebe uma fração igual do capital
        new_capital = 0  # Acumula o capital após esse ciclo
        
        for gene in cycle_genes:  # Para cada pote (ação escolhida)
            if gene not in buy_prices or gene not in sell_prices:  # Se não tiver preço, ignora
                continue

            buy_price = buy_prices[gene]
            sell_price = sell_prices[gene]
            
            if np.isnan(buy_price) or np.isnan(sell_price):  # Se algum preço for inválido (NaN), ignora
                continue
            
            qty = pot_value / buy_price  # Quantidade comprada com o valor do pote
            new_capital += qty * sell_price  # Valor recebido na venda é somado ao novo capital
        
        capital = new_capital  # Atualiza o capital total para o próximo ciclo

    return capital  # Retorna o capital final após todos os ciclos

def crossover(dna1, dna2):
    point = random.randint(1, TOTAL_GENES - 1)  # Escolhe um ponto de corte aleatório (evita extremos)
    return dna1[:point] + dna2[point:]          # Combina os genes do pai 1 até o ponto, e do pai 2 a partir do ponto

def mutate(dna):
    return [
        gene if random.random() > MUTATION_RATE else random.choice(VALID_CODES)  # Com chance igual à MUTATION_RATE, substitui o gene
        for gene in dna
    ]

# === ALGORITMO GENÉTICO ===
population = [random_dna() for _ in range(POP_SIZE)]  # Cria a população inicial com DNAs aleatórios

for generation in range(NUM_GENERATIONS):  # Repete o processo de evolução por várias gerações
    scored_population = [(evaluate_dna(dna), dna) for dna in population]  # Avalia cada DNA: (capital final, DNA)
    scored_population.sort(reverse=True, key=lambda x: x[0])  # Ordena do melhor para o pior com base no capital final
    population = [dna for _, dna in scored_population[:POP_SIZE//2]]  # Mantém apenas os melhores 50% (seleção natural)

    while len(population) < POP_SIZE:  # Preenche a população de volta até o tamanho original
        parents = random.sample(population[:POP_SIZE//4], 2)  # Escolhe 2 pais entre os top 25% (elitismo)
        child = mutate(crossover(parents[0], parents[1]))  # Aplica crossover e mutação para criar um novo DNA
        population.append(child)  # Adiciona o novo DNA à população

# === GUARDA RESULTADO FINAL ===
best_score, best_dna = max([(evaluate_dna(dna), dna) for dna in population], key=lambda x: x[0])  # Escolhe o DNA com maior capital final

# === DETALHAMENTO DOS CICLOS DO MELHOR DNA ===
capital = INITIAL_CAPITAL
print("\n📈 Detalhamento dos ciclos:")
for cycle_index, (buy_day, sell_day) in enumerate(day_pairs):
    buy_prices = price_table.loc[buy_day]
    sell_prices = price_table.loc[sell_day]
    cycle_genes = best_dna[cycle_index * NUM_POTS: (cycle_index + 1) * NUM_POTS]
    pot_value = capital / NUM_POTS
    new_capital = 0

    print(f"\n🔹 Ciclo {cycle_index + 1} | Compra: {buy_day.date()} → Venda: {sell_day.date()}")
    for i, gene in enumerate(cycle_genes):
        if gene not in buy_prices or gene not in sell_prices:
            continue
        buy_price = buy_prices[gene]
        sell_price = sell_prices[gene]
        if pd.isna(buy_price) or pd.isna(sell_price):
            continue
        qty = pot_value / buy_price
        final_value = qty * sell_price
        lucro_pct = (sell_price / buy_price - 1) * 100
        new_capital += final_value
        print(f"  🧪 Pote {i+1}: {gene} | Compra: {buy_price:.2f} | Venda: {sell_price:.2f} | Lucro: {lucro_pct:.2f}%")

    lucro_total = (new_capital / capital - 1) * 100
    print(f"  💼 Capital antes: R$ {capital:.2f} → depois: R$ {new_capital:.2f} | Lucro total ciclo: {lucro_total:.2f}%")
    capital = new_capital

# === MOSTRA O RESULTADO FINAL ===
print(f"💰 Melhor capital final: R$ {best_score:.2f}")