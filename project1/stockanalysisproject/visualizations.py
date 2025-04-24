import plotly.express as px

def plot_stock_price(df, symbol):
    fig = px.line(df, x='date', y='close', title=f'{symbol} Closing Prices')
    fig.update_layout(xaxis_title='Date', yaxis_title='Price')
    fig.show()
