from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# 1. Load and prepare the data
df = pd.read_csv('data/formatted_data_task1.csv')
# Ensure date is in datetime format and sorted
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# 2. Create the line chart
fig = px.line(
    df,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'sales': 'Total Sales ($)', 'date': 'Transaction Date'}
)

# Optional: Add a vertical line for the price increase date
fig.add_vline(x='2021-01-15', line_dash="dash", line_color="red")

# 3. Define the app layout
app.layout = html.Div(children=[
    html.H1(
        children='Soul Foods Pink Morsel Sales Visualizer',
        style={'textAlign': 'center', 'color': '#2C3E50'}
    ),

    html.Div(children='''
        An interactive tool to analyze sales performance before and after the 
        Pink Morsel price increase on January 15th, 2021.
    ''', style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)