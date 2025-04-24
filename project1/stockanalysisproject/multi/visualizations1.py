import plotly.express as px

def plot_multiple_stocks(df, symbols):
    fig = px.line(df, x='date', y='close', color='symbol',
                  title='Closing Prices of Selected Stocks')
    fig.update_layout(xaxis_title='Date', yaxis_title='Close Price')
    fig.show()
