
# 📊 Algoritmo Genético para Simulação de Investimentos na B3

Este projeto utiliza um **algoritmo genético** para simular estratégias de investimento em ações da **B3 (Bolsa de Valores do Brasil)**. A cada execução, o algoritmo busca **maximizar o retorno financeiro** ao longo de múltiplos ciclos de compra e venda de ações, baseado em dados históricos.

---

## 👨‍💻 Desenvolvido por

- Gustavo Baron Lauritzen  
- Matheus Baron Lauritzen  
- Gabriel Bósio  

---

## 🧬 Visão Geral

O sistema simula a alocação de capital em múltiplos "potes de investimento", onde cada pote representa uma ação diferente. Através de **evolução genética**, a simulação seleciona os melhores conjuntos de ações para investir em cada ciclo de compra e venda, com base em dados históricos.

---

## 📁 Estrutura do Projeto

- `main.py`: Código principal do algoritmo genético.
- `dataset/cotacoes_b3_2025_05.csv`: Arquivo CSV com cotações históricas de ações (formato: Data, Código, Fechamento).
- `README.md`: Este arquivo com a documentação do projeto.

---

## ⚙️ Parâmetros de Configuração

| Parâmetro         | Descrição                                     | Valor Padrão |
|-------------------|-----------------------------------------------|---------------|
| `CSV_PATH`        | Caminho para o arquivo CSV de cotações        | `dataset/cotacoes_b3_2025_05.csv` |
| `INITIAL_CAPITAL` | Capital inicial do investidor                | `1000.0` R$    |
| `POP_SIZE`        | Tamanho da população de DNAs (cromossomos)    | `50`          |
| `NUM_GENERATIONS` | Número de gerações para evoluir               | `100`         |
| `MUTATION_RATE`   | Taxa de mutação genética                      | `0.1` (10%)    |
| `NUM_POTS`        | Número de potes de investimento (ações por ciclo) | `10`       |

---

## 🔄 Funcionamento

1. **Leitura dos dados** do arquivo CSV de cotações da B3.
2. Criação da **tabela de preços** com datas como índice e os códigos das ações como colunas.
3. Divisão dos dados em **ciclos de 2 dias** (1 dia de compra, 1 de venda).
4. Geração de uma **população inicial aleatória** de estratégias (DNAs).
5. Avaliação dos DNAs por retorno de capital final.
6. Aplicação de **seleção, crossover e mutação** para evoluir as estratégias.
7. Impressão do **melhor DNA**, com detalhamento por ciclo de investimento.

---

## 📈 Exemplo de Saída

```text
📈 Detalhamento dos ciclos:

🔹 Ciclo 1 | Compra: 2025-05-02 → Venda: 2025-05-03
  🧪 Pote 1: PETR4 | Compra: 30.12 | Venda: 30.85 | Lucro: 2.42%
  🧪 Pote 2: VALE3 | Compra: 70.00 | Venda: 71.40 | Lucro: 2.00%
  ...
  💼 Capital antes: R$ 1000.00 → depois: R$ 1025.00 | Lucro total ciclo: 2.5%

...

💰 Melhor capital final: R$ 1689.45
```

---

## 📦 Requisitos

- Python 3.8+
- Bibliotecas:
  - `pandas`
  - `numpy`

Instale com:

```bash
pip install pandas numpy
```

---

## 📂 Como usar

1. Coloque seu arquivo de cotações no caminho definido em `CSV_PATH`.
2. Execute o script:

```bash
python main.py
```

3. Observe o resultado final no terminal.

---

## 📜 Licença

Este projeto é de livre uso para fins educacionais.

---

## 💡 Observações

- Os dados usados são **fictícios** ou históricos e não representam uma recomendação de investimento.
- O algoritmo não leva em conta taxas, liquidez, nem outros fatores do mercado real.
- Pode ser utilizado como base para estudos em **aprendizado de máquina**, **otimização**, e **mercado financeiro**.

---

## 🚀 Futuras melhorias

- Inclusão de custos operacionais (taxas de corretagem).
- Aplicação em períodos maiores (dados históricos reais).
- Visualização gráfica do crescimento do capital.
- Exportação dos resultados para arquivo CSV ou gráfico interativo.

---
