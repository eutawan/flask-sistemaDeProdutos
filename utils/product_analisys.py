import plotly.express as px
import pandas as pd

def quantityAnalisys(data):
    if not data:
        return None
    
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="nome",
        y="qtde",
        title="Quantity of your products",
        labels={'nome': 'Product', "qtde": "quantityAnalisys"},
    )

    return fig.to_html(full_html=False)

def salesAnalisys(path):
    df = pd.read_csv(path)

    df['data'] = pd.to_datetime(df['data'])

    df['mes'] = df['data'].dt.to_period('M').astype(str)

    df_agrupado = df.groupby(['mes', 'nome_produto'])['quantidade_vendida'].sum().reset_index()

    fig = px.line(
        df_agrupado,
        x='mes',
        y='quantidade_vendida',
        color='nome_produto',
        title='Evolução das Vendas por Produto',
        labels={'data': 'Data', 'quantidade_vendida': 'Quantidade Vendida'},
    )
    return fig.to_html(full_html=False)