from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

# ── Data ──────────────────────────────────────────────────────────────────────
df = pd.read_csv('data/formatted_data_task1.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

REGIONS = ['all', 'north', 'east', 'south', 'west']

REGION_COLORS = {
    'all':   '#F4A261',
    'north': '#48CAE4',
    'east':  '#F77F00',
    'south': '#A8DADC',
    'west':  '#E63946',
}

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(
    className='page',
    children=[

        # ── Left sidebar ──────────────────────────────────────────────────────
        html.Aside(className='sidebar', children=[

            html.Div(className='brand', children=[
                html.Span('SF', className='brand-monogram'),
                html.Div(className='brand-text', children=[
                    html.P('Soul Foods', className='brand-name'),
                    html.P('Analytics', className='brand-sub'),
                ]),
            ]),

            html.Hr(className='divider'),

            html.P('Filter by Region', className='filter-label'),

            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': html.Span([
                        html.Span(className=f'dot dot-{r}'),
                        r.capitalize()
                    ], className='radio-option-inner'), 'value': r}
                    for r in REGIONS
                ],
                value='all',
                className='radio-group',
                labelClassName='radio-label',
                inputClassName='radio-input',
            ),

            html.Hr(className='divider'),

            html.Div(className='legend-block', children=[
                html.P('Price Event', className='filter-label'),
                html.Div(className='legend-item', children=[
                    html.Span(className='legend-dash'),
                    html.Span('Jan 15 2021 — price increase', className='legend-text'),
                ]),
            ]),

            html.Div(className='sidebar-footer', children=[
                html.P('Pink Morsel Sales Visualiser', className='footer-title'),
                html.P('© 2024 Soul Foods', className='footer-copy'),
            ]),
        ]),

        # ── Main content ──────────────────────────────────────────────────────
        html.Main(className='main', children=[

            html.Header(className='header', children=[
                html.Div(className='header-text', children=[
                    html.H1('Pink Morsel', className='headline'),
                    html.H2('Sales Over Time', className='sub-headline'),
                ]),
                html.Div(id='summary-cards', className='summary-cards'),
            ]),

            html.Div(className='chart-container', children=[
                dcc.Graph(id='sales-line-chart', className='chart',
                          config={'displayModeBar': False}),
            ]),
        ]),
    ]
)

# ── Callback ──────────────────────────────────────────────────────────────────
@callback(
    Output('sales-line-chart', 'figure'),
    Output('summary-cards', 'children'),
    Input('region-filter', 'value'),
)
def update_chart(region):
    filtered = df if region == 'all' else df[df['region'] == region]
    color = REGION_COLORS.get(region, '#F4A261')

    # Convert hex color to rgba with low opacity for fill
    def hex_to_rgba(hex_color, alpha=0.08):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered['date'],
        y=filtered['sales'],
        mode='lines',
        name=region.capitalize(),
        line=dict(color=color, width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor=hex_to_rgba(color),
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>',
    ))

    vline_x = pd.Timestamp('2021-01-15').timestamp() * 1000

    fig.add_vline(
        x=vline_x,
        line_dash='dot',
        line_color='rgba(255,255,255,0.35)',
        line_width=1.5,
        annotation_text='Price Increase',
        annotation_font_color='rgba(255,255,255,0.5)',
        annotation_font_size=11,
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="'DM Mono', monospace",
        font_color='#E8E0D0',
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickformat='%b %Y',
            tickfont=dict(size=11, color='rgba(232,224,208,0.5)'),
            linecolor='rgba(255,255,255,0.05)',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False,
            tickprefix='$',
            tickformat=',.0f',
            tickfont=dict(size=11, color='rgba(232,224,208,0.5)'),
        ),
        hoverlabel=dict(
            bgcolor='#1A1412',
            bordercolor=color,
            font_family="'DM Mono', monospace",
            font_size=13,
        ),
        showlegend=False,
    )

    # Summary cards
    total   = filtered['sales'].sum()
    avg_day = filtered.groupby('date')['sales'].sum().mean()
    peak    = filtered.groupby('date')['sales'].sum().max()

    cards = [
        _card('Total Revenue', f'${total:,.0f}'),
        _card('Avg Daily',     f'${avg_day:,.0f}'),
        _card('Peak Day',      f'${peak:,.0f}'),
    ]

    return fig, cards


def _card(label, value):
    return html.Div(className='card', children=[
        html.P(label, className='card-label'),
        html.P(value, className='card-value'),
    ])


# ── Inline CSS (injected via index_string) ────────────────────────────────────
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
  {%metas%}
  <title>Soul Foods — Pink Morsel</title>
  {%favicon%}
  {%css%}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Bebas+Neue&family=DM+Sans:wght@300;400&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:          #120E0C;
      --sidebar-bg:  #1A1412;
      --border:      rgba(255,255,255,0.07);
      --accent:      #F4A261;
      --text:        #E8E0D0;
      --muted:       rgba(232,224,208,0.45);
      --card-bg:     rgba(255,255,255,0.04);
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      height: 100vh;
      overflow: hidden;
    }

    /* ── Page shell ── */
    .page {
      display: grid;
      grid-template-columns: 220px 1fr;
      height: 100vh;
    }

    /* ── Sidebar ── */
    .sidebar {
      background: var(--sidebar-bg);
      border-right: 1px solid var(--border);
      padding: 28px 20px;
      display: flex;
      flex-direction: column;
      gap: 0;
    }

    .brand { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
    .brand-monogram {
      width: 40px; height: 40px;
      background: var(--accent);
      color: var(--bg);
      font-family: 'Bebas Neue', sans-serif;
      font-size: 20px;
      letter-spacing: 1px;
      display: flex; align-items: center; justify-content: center;
      border-radius: 8px;
      flex-shrink: 0;
    }
    .brand-name { font-family: 'Bebas Neue', cursive; font-size: 18px; letter-spacing: 2px; color: var(--text); line-height: 1; }
    .brand-sub  { font-size: 10px; color: var(--muted); letter-spacing: 3px; text-transform: uppercase; margin-top: 2px; }

    .divider { border: none; border-top: 1px solid var(--border); margin: 18px 0; }

    .filter-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); margin-bottom: 14px; }

    /* Radio buttons */
    .radio-group { display: flex; flex-direction: column; gap: 6px; }
    .radio-label {
      display: flex; align-items: center;
      padding: 8px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.15s;
      font-size: 13px;
      color: var(--muted);
    }
    .radio-label:hover { background: rgba(255,255,255,0.05); color: var(--text); }
    .radio-input { display: none; }
    .radio-option-inner { display: flex; align-items: center; gap: 10px; }

    .dot {
      width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;
      opacity: 0.5; transition: opacity 0.15s;
    }
    .dot-all   { background: #F4A261; }
    .dot-north { background: #48CAE4; }
    .dot-east  { background: #F77F00; }
    .dot-south { background: #A8DADC; }
    .dot-west  { background: #E63946; }

    /* Highlight selected radio row */
    .radio-label:has(input:checked) {
      background: rgba(244,162,97,0.1);
      color: var(--text);
    }
    .radio-label:has(input:checked) .dot { opacity: 1; }

    /* Legend */
    .legend-block { margin-bottom: 0; }
    .legend-item  { display: flex; align-items: center; gap: 10px; margin-top: 4px; }
    .legend-dash  {
      width: 22px; height: 2px;
      background: repeating-linear-gradient(90deg, rgba(255,255,255,0.35) 0 4px, transparent 4px 8px);
      flex-shrink: 0;
    }
    .legend-text  { font-size: 11px; color: var(--muted); }

    .sidebar-footer { margin-top: auto; padding-top: 24px; }
    .footer-title   { font-size: 11px; color: var(--muted); }
    .footer-copy    { font-size: 10px; color: rgba(232,224,208,0.2); margin-top: 3px; }

    /* ── Main ── */
    .main {
      display: grid;
      grid-template-rows: auto 1fr;
      padding: 36px 40px 28px;
      gap: 28px;
      overflow: hidden;
    }

    /* ── Header ── */
    .header { display: flex; align-items: flex-start; justify-content: space-between; }
    .headline     { font-family: 'Bebas Neue', cursive; font-size: 52px; letter-spacing: 4px; line-height: 0.9; color: var(--text); }
    .sub-headline { font-family: 'Bebas Neue', cursive; font-size: 52px; letter-spacing: 4px; line-height: 0.9; color: var(--accent); }

    /* Summary cards */
    .summary-cards { display: flex; gap: 12px; align-items: center; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 18px;
      min-width: 120px;
    }
    .card-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 5px; }
    .card-value { font-family: 'DM Mono', monospace; font-size: 16px; color: var(--text); }

    /* ── Chart ── */
    .chart-container {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px 8px 8px;
      overflow: hidden;
    }
    .chart { width: 100% !important; height: 100% !important; }
    .js-plotly-plot, .plot-container { height: 100% !important; }
  </style>
</head>
<body>
  {%app_entry%}
  <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)