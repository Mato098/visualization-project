import dash, json
from preprocessing import Book
import wordclouds
from dash import html, dcc
import utilities as utils

# Initialize the app
app = dash.Dash(__name__)

toggle1_state = True
toggle2_state = False

book1 = json.load(open('project/Name of the Wind.json'))
book2 = json.load(open('project/Wise Man\'s Fear.json'))

slider1_from = 1
slider1_to = 3
slider2_from = 1
slider2_to = 3

wordcloud1 = None
wordcloud2 = None
wordcloud3 = None
wordcloud4 = None
wordcloud1_invalid = True
wordcloud2_invalid = True
wordcloud3_invalid = True
wordcloud4_invalid = True

toggle1_style = {
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'borderRadius': '5px',
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        'transition': '0.3s'
    }
toggle2_style = {
        'backgroundColor': 'green' if toggle2_state else 'red',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'borderRadius': '5px',
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        'transition': '0.3s'
    }

toggle1 = html.Button(
    id="toggle-1",
    children="Name of the Wind",
    style = {**toggle1_style, 'backgroundColor': 'green' if toggle1_state else 'red'}
)
toggle2 = html.Button(
    id="toggle-2",
    children="Wise Man\'s Fear",
    style = {**toggle2_style, 'backgroundColor': 'green' if toggle2_state else 'red'}
)

app.layout = html.Div(
    style={'textAlign': 'center', 'fontFamily': 'Arial'},
    children=[
        html.H1("Analysis of The Kingkiller Chronicle", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div(
            id="chapter-display",
            style={
                'width': '60%',
                'height': 'auto',
                'margin': '0 auto',
                'padding': '20px',
                'border': '2px solid black',
                'borderRadius': '10px',
                'backgroundColor': '#f9f9f9',
                'textAlign': 'center',
                'fontSize': '20px',
                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'transition': '0.3s',
                
                'display': 'flex',
                'flexDirection': 'column',
            },
            children=["Displaying chapters: -", "asd"]
            

        ),
        html.Div(
            id="toggle-container",
            style={'width': '60%', 'margin': '0 auto', 'marginTop': '20px'},
            children=[
                html.Div(
                    toggle1,
                    style={**toggle1_style, 'backgroundColor': 'green' if toggle1_state else 'red'},
                ),
                html.Div(
                    toggle2,
                    style={**toggle2_style, 'backgroundColor': 'green' if toggle2_state else 'red'},
                )
            ]
        ),
        html.Div(
            style={'width': '70%', 'margin': '30px auto'},
            id="slider-container",
            children=[
                dcc.RangeSlider(
                    id='chapter-slider',
                    min=1,
                    max=len(book1['chapters']),  # Example range; can be updated dynamically
                    step=1,
                    marks={i: f"{i}" for i in range(1, len(book1['chapters']) + 1, 10)},  # Display every tenth number
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
    global slider1_from, slider1_to, slider2_from, slider2_to, toggle1_state
    if toggle1_state:
        slider1_from, slider1_to = (value[0] - 1, value[1] - 1) 
    else:
        slider2_from, slider2_to = (value[0] - 1, value[1] - 1)
    if value[0] == value[1]:  # Single chapter selected
        return f"""Displaying chapter: {value[0]}\n
          - {book1['chapters'][value[0] - 1]['title'] if toggle1_state else book2['chapters'][value[0] - 1]['title']}"""
    return [f"Displaying chapters: {value[0]} to {value[1]}",
      f"""\n- {book1['chapters'][value[0] - 1]['title'] if toggle1_state else book2['chapters'][value[0] - 1]['title']}
      - {book1['chapters'][value[1] - 1]['title'] if toggle1_state else book2['chapters'][value[1] - 1]['title']}"""]

#@app.callback(
    #dash.Input('chapter-slider', 'value'),
#)
def get_wordcloud(book: Book, slider_from, slider_to):
    return html.Img(src='data:image/png;base64,{}'.format(wordclouds.generate_wordcloud(utils.accumulate_chapters(book, slider_from, slider_to)))) 


@app.callback(
    dash.Output('tab-content', 'children'),
    dash.Input('tabs', 'value'),
    dash.Input('chapter-slider', 'value'),
    dash.Input('toggle-1', 'n_clicks'),
)
def render_tab_content(selected_tab, slider, toggle1_clicks):
    global wordcloud1, wordcloud2, toggle1_state, wordcloud1_invalid, wordcloud2_invalid
    print(dash.callback_context.triggered)
    
    if selected_tab == 'wordclouds':
        if 'chapter-slider' in dash.callback_context.triggered[0]['prop_id'] and len(dash.callback_context.triggered) == 1:
            print("SLIDERR")
            if toggle1_state or wordcloud1 is None:
                wordcloud1 = get_wordcloud(book1, slider[0] - 1, slider[1] - 1)
            elif not toggle1_state or wordcloud2 is None:
                wordcloud2 = get_wordcloud(book2, slider[0] - 1, slider[1] - 1)

        return wordcloud1 if toggle1_state else wordcloud2
    
    elif selected_tab == 'barcharts':
        return html.Div("Bar charts go here.")
    return html.Div("Select a view.")


@app.callback(
    dash.Output('slider-container', 'children'),
    dash.Output('toggle-container', 'children'),
    dash.Input('toggle-2', 'n_clicks'),
    dash.Input('toggle-1', 'n_clicks'),)
def buttons_toggle_children_update(_, __):
    global toggle1_state, toggle2_state, toggle1, toggle2, slider1_from, slider1_to, slider2_from, slider2_to
    toggle2_state = not toggle2_state
    toggle1_state = not toggle1_state
    
    toggle1.style = {
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'borderRadius': '5px',
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        'transition': '0.3s',
        'backgroundColor': 'green' if toggle1_state else 'red'
    }
    toggle2.style = {
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'borderRadius': '5px',
        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        'transition': '0.3s',
        'backgroundColor': 'green' if toggle2_state else 'red'
    }

    slider_max = len(book1['chapters']) if toggle1_state else len(book2['chapters'])
    slider_saved_from = slider1_from if toggle1_state else slider2_from
    slider_saved_to = slider1_to if toggle1_state else slider2_to
    new_slider = dcc.RangeSlider(
        id='chapter-slider',
        min=1,
        max=slider_max,
        step=1,
        marks={1: "1", slider_max: f"{slider_max}"} | {i: f"{i}" for i in range(0, slider_max, 10)},
        value=[slider_saved_from + 1, slider_saved_to + 1]
    )
    return new_slider, [
        html.Div(
            toggle1,
            style={'display': 'inline-block', 'marginRight': '20px', 'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none', 'color': 'white'}
        ),
        html.Div(
            toggle2,
            style={'display': 'inline-block', 'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none', 'color': 'white'}
        )
    ],



# Run the app locally
if __name__ == "__main__":
    app.run_server(debug=True)#, dev_tools_silence_routes_logging = False)
