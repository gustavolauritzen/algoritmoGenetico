import pandas as pd
import streamlit as st

st.set_page_config(page_title="Simulador B3 - 10 Potes", layout="wide")
st.title("📈 Simulador de Alocação Otimizada - B3 (10 Potes)")

# Upload do arquivo
file = st.file_uploader("📤 Envie o arquivo de cotações (.csv)", type=["csv"])

if file:
    df = pd.read_csv(file, sep=';', engine='python')
    df.columns = ['Data', 'Codigo', 'Fechamento']
    df['Fechamento'] = df['Fechamento'].str.replace(',', '.').astype(float)
    df = df[df['Codigo'].str.match(r'^[A-Z0-9]{5}$')]
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.sort_values(by='Data')

    price_table = df.pivot(index='Data', columns='Codigo', values='Fechamento')
    price_table = price_table.sort_index()

    initial_capital = 1000.0
    num_potes = 10
    capital = initial_capital
    dates = price_table.index
    num_days = len(dates)
    operations = []

    st.success("📊 Dados carregados com sucesso!")

    for i in range(0, num_days - 1, 2):
        day_buy = dates[i]
        day_sell = dates[i + 1]

        buy_prices = price_table.loc[day_buy]
        sell_prices = price_table.loc[day_sell]

        valid_actions = buy_prices.dropna().index.intersection(sell_prices.dropna().index)
        returns = (sell_prices[valid_actions] / buy_prices[valid_actions]) - 1

        top_10 = returns.sort_values(ascending=False).head(num_potes)
        pot_value = capital / num_potes
        new_capital = 0
        pot_results = []

        for action in top_10.index:
            qty = pot_value / buy_prices[action]
            final_value = qty * sell_prices[action]
            new_capital += final_value
            pot_results.append({
                'Ação': action,
                'Preço Compra': round(buy_prices[action], 2),
                'Preço Venda': round(sell_prices[action], 2),
                'Quantidade': round(qty, 2),
                'Valor Final': round(final_value, 2),
                'Lucro (%)': round((sell_prices[action] / buy_prices[action] - 1) * 100, 2)
            })

        capital = new_capital
        operations.append({
            'buy_date': day_buy.strftime('%Y-%m-%d'),
            'sell_date': day_sell.strftime('%Y-%m-%d'),
            'capital': round(capital, 2),
            'pot_details': pot_results
        })

    # Exibir simulação
    for i, op in enumerate(operations):
        with st.expander(f"🔁 Ciclo {i+1} | Compra: {op['buy_date']} → Venda: {op['sell_date']} | Capital: R$ {op['capital']:.2f}"):
            st.dataframe(pd.DataFrame(op['pot_details']))

    st.header(f"💰 Capital final: R$ {capital:.2f}")
    st.caption("Simulação baseada nas 10 ações mais lucrativas a cada ciclo de 2 dias úteis.")
