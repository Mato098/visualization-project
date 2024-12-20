import dash, json
from dash import html, dcc

# Initialize the app
app = dash.Dash(__name__)

toggle1_state = True
toggle2_state = False

book1 = json.load(open('project/Name of the Wind.json'))
book2 = json.load(open('project/Wise Man\'s Fear.json'))

slider_from = 1
slider_to = len(book1['chapters'])


toggle1 = html.Button(
    id="toggle-1",
    children="Toggle 1: ON",
    style={'backgroundColor': 'green', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'},
)
toggle2 = html.Button(
    id="toggle-2",
    children="Toggle 2: ON",
    style={'backgroundColor': 'red', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px'},
)

app.layout = html.Div(
    style={'textAlign': 'center', 'fontFamily': 'Arial'},
    children=[
        html.H1("Analysis of Book XY", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div(
            id="chapter-display",
            style={
                'width': '60%',
                'margin': '0 auto',
                'padding': '20px',
                'border': '2px solid black',
                'borderRadius': '10px',
                'backgroundColor': '#f9f9f9',
                'textAlign': 'center',
                'fontSize': '20px'
            },
            children="Displaying chapters: -"
        ),
        html.Div(
            id="toggle-container",
            style={'width': '60%', 'margin': '0 auto', 'marginTop': '20px'},
            children=[
                html.Div(
                    toggle1,
                    style={'display': 'inline-block', 'marginRight': '20px'}
                ),
                html.Div(
                    toggle2,
                    style={'display': 'inline-block', 'color': 'red'},
                )
            ]
        ),
        html.Div(
            style={'width': '70%', 'margin': '30px auto'},
            children=[
                dcc.RangeSlider(
                    id='chapter-slider',
                    min=slider_from,
                    max=slider_to,  # Example range; can be updated dynamically
                    step=1,
                    marks={i: f"{i}" for i in range(1, slider_to + 1)},  # Adjust as needed
                    value=[1, 3]  # Initial range
                )
            ]
        ),
        
        # Tabs for views
        dcc.Tabs(id="tabs", value='wordclouds', children=[
            dcc.Tab(label='Wordclouds', value='wordclouds'),
            dcc.Tab(label='Bar Charts', value='barcharts'),
        ]),
        
        # Placeholder for graphs based on selected tab
        html.Div(id="tab-content", style={'marginTop': '20px'})
    ]
)

# Callbacks for interactivity
@app.callback(
    dash.Output('chapter-display', 'children'),
    dash.Input('chapter-slider', 'value')
)
def update_chapter_display(value):
    if value[0] == value[1]:  # Single chapter selected
        return f"Displaying chapter: {value[0]}"
    return f"Displaying chapters: {value[0]} to {value[1]}"

@app.callback(
    dash.Output('tab-content', 'children'),
    dash.Input('tabs', 'value')
)
def render_tab_content(selected_tab):
    if selected_tab == 'wordclouds':
        return html.Div("Wordclouds go here.")
    elif selected_tab == 'barcharts':
        return html.Div("Bar charts go here.")
    return html.Div("Select a view.")


@app.callback(
    dash.Output('toggle-container', 'children'),
    dash.Input('toggle-2', 'n_clicks'),
    dash.Input('toggle-1', 'n_clicks'),)
def buttons_toggle_children_update(_, __):
    global toggle1_state, toggle2_state, toggle1, toggle2
    if dash.callback_context.triggered[0]['prop_id'] == 'toggle-2.n_clicks':
        if toggle2_state and not toggle1_state:
            toggle2_state = not toggle2_state
            toggle1_state = not toggle1_state
        else:
            toggle2_state = not toggle2_state
    else:
        if toggle1_state and not toggle2_state:
            toggle1_state = not toggle1_state
            toggle2_state = not toggle2_state
        else:
            toggle1_state = not toggle1_state
    toggle1.children = "Toggle 1: " + ("ON" if toggle1_state else "OFF")
    toggle2.children = "Toggle 2: " + ("ON" if toggle2_state else "OFF")
    toggle1.style = {'backgroundColor': 'green' if toggle1_state else 'red'}
    toggle2.style = {'backgroundColor': 'green' if toggle2_state else 'red'}
    return [
                html.Div(
                    toggle1,
                    style={'display': 'inline-block', 'marginRight': '20px'}
                ),
                html.Div(
                    toggle2,
                    style={'display': 'inline-block'},
                )
            ]

@app.callback(
    dash.Output('toggle-1', 'style'),
    dash.Input('toggle-1', 'n_clicks'),)
def toggle1_style_update(current_text):
    global toggle1_state
    return {'display': 'inline-block', 'background': 'lightgreen' if toggle1_state else 'red'}

@app.callback(
    dash.Output('toggle-2', 'style'),
    dash.Input('toggle-2', 'n_clicks'),)
def toggle2_style_update(current_text):
    global toggle2_state
    return {'display': 'inline-block', 'background': 'lightgreen' if toggle2_state else 'red'}



# Run the app locally
if __name__ == "__main__":
    app.run_server(debug=True)
