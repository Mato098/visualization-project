import dash, json, time
from preprocessing import Book
import wordclouds
from dash import html, dcc
import utilities as utils

external_stylesheets = [
    '/assets/style.css?v={}'.format(int(time.time()))  # Disable caching by appending a timestamp
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                background-color: #685752;
            }
            #main-container {
                height: 100%;
            }
            /* Loading spinner styles */
            .spinner {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 16px solid #f3f3f3;
                border-top: 16px solid #3498db;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                animation: spin 3s linear infinite;
                z-index: 9999;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .hidden {
                display: none;
            }
        </style>
    </head>
    <body>
        <div id="spinner" class="spinner"></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var spinner = document.getElementById('spinner');
                spinner.classList.add('hidden');
            });
        </script>
    </body>
</html>
'''

toggle1_state = False
toggle2_state = True

book1 = json.load(open('./Name of the Wind.json'))
book2 = json.load(open('./Wise Man\'s Fear.json'))

slider1_from = 0
slider1_to = 14
slider2_from = 0
slider2_to = 14

wordcloud1 = None
wordcloud2 = None
wordcloud3 = None
wordcloud4 = None
wordcloud1_invalid = True
wordcloud2_invalid = True
wordcloud3_invalid = True
wordcloud4_invalid = True

fig1 = None
fig2 = None
fig3 = None
fig4 = None
fig5 = None
fig6 = None

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
    className='toggle-button toggle-button-green' if toggle1_state else 'toggle-button toggle-button-red'
)
toggle2 = html.Button(
    id="toggle-2",
    children="Wise Man\'s Fear",
    className='toggle-button toggle-button-green' if toggle2_state else 'toggle-button toggle-button-red'
)

app.layout = html.Div(
    id="main-container",
    style={'textAlign': 'center', 'fontFamily': 'Arial',
            'backgroundColor': '#685752', 'padding': '0', 'margin': '0'},
    children=[
        html.H1("Analysis of The Kingkiller Chronicle"),
        
        html.Div(
            id="chapter-display",
            className='chapter-display',
            children=["Displaying chapters: -"]
        ),
        html.Div(
            id="toggle-container",
            style={'width': '60%', 'margin': '0 auto', 'marginTop': '20px'},
            children=[
                toggle1,
                toggle2
            ]
        ),
        html.Div(
            style={'width': '70%', 'margin': '30px auto'},
            id="slider-container",
            children=[
                dcc.RangeSlider(
                    id='chapter-slider',
                    min=0,
                    max=len(book1['chapters']),
                    step=1,
                    marks={i: f"{i}" for i in range(1, len(book1['chapters']) + 1, 10)},
                    value=[0, 14],
                    tooltip={'always_visible': True, 'placement': 'bottom'},
                    className='book1-slider' if toggle1_state else 'book2-slider'
                )
            ]
        ),

        dcc.Tabs(id="tabs", value='wordclouds', className='custom-tabs', children=[
            dcc.Tab(id="tab1", label='Wordclouds', value='wordclouds', className='tab-green', selected_className='tab--selected'),
            dcc.Tab(id="tab2", label='Bar Charts', value='barcharts', className='tab-green', selected_className='tab--selected'),
        ]),
        
        html.Div(id="tab-content", className='content-container', children=[
            dcc.Graph(id='graph1', className='bar-chart'),
            dcc.Graph(id='graph2', className='bar-chart'),
            dcc.Graph(id='graph3', className='bar-chart'),
            dcc.Graph(id='graph4', className='bar-chart'),
            dcc.Graph(id='graph5', className='bar-chart'),
            dcc.Graph(id='graph6', className='bar-chart')
        ]),
        dcc.Store(id='hovered-chapter', data=None)
    ]
)


@app.callback(
    dash.Output('chapter-display', 'children'),
    dash.Input('chapter-slider', 'value')
)
def update_chapter_display(value):
    global slider1_from, slider1_to, slider2_from, slider2_to, toggle1_state
    if toggle1_state:
        slider1_from, slider1_to = (value[0], value[1] - 1)
    else:
        slider2_from, slider2_to =  (value[0], value[1] - 1)
    if value[0] == value[1]:  # Single chapter selected
        return f"""Displaying chapter: {value[0] + 1}\n
          - {book1['chapters'][value[0]]['title'] if toggle1_state else book2['chapters'][value[0]]['title']}"""
    return [f"Displaying chapters: {value[0] + 1} to {value[1] + 1}",
      f"""\n- {book1['chapters'][value[0]]['title'] if toggle1_state else book2['chapters'][value[0]]['title']}
      - {book1['chapters'][value[1]]['title'] if toggle1_state else book2['chapters'][value[1]]['title']}"""]

#@app.callback(
    #dash.Input('chapter-slider', 'value'),
#)
def get_wordcloud(book: Book, slider_from, slider_to, names: bool = False, green_colormap: bool = True):
    return html.Img(src='data:image/png;base64,{}'.format(wordclouds.generate_wordcloud(utils.accumulate_chapters(book, slider_from, slider_to), names, green_colormap))) 


@app.callback(
    dash.Output('tab-content', 'children'),
    dash.Input('tabs', 'value'),
    dash.Input('chapter-slider', 'value'),
    dash.Input('toggle-1', 'n_clicks'),
    dash.State('hovered-chapter', 'data')
)
def render_tab_content(selected_tab, slider, toggle1_clicks, hovered_chapter):
    global wordcloud1, wordcloud2, wordcloud3, wordcloud4,\
          toggle1_state, wordcloud1_invalid, wordcloud2_invalid, wordcloud3_invalid, wordcloud4_invalid
    
    if 'chapter-slider' in dash.callback_context.triggered[0]['prop_id'] and len(dash.callback_context.triggered) == 1:
        if toggle1_state:
            wordcloud1_invalid = True
            wordcloud3_invalid = True
        else:
            wordcloud2_invalid = True
            wordcloud4_invalid = True
    
    if selected_tab == 'wordclouds':
        for idx, i in enumerate([(wordcloud1, wordcloud1_invalid), (wordcloud2, wordcloud2_invalid), (wordcloud3, wordcloud3_invalid), (wordcloud4, wordcloud4_invalid)]):
            if idx == 0:
                if i[0] is None or i[1]:
                    wordcloud1 = get_wordcloud(book1, slider[0], slider[1])
                    wordcloud1_invalid = False
            elif idx == 1:
                if i[0] is None or i[1]:
                    wordcloud2 = get_wordcloud(book2, slider[0], slider[1], green_colormap=False)
                    wordcloud2_invalid = False
            elif idx == 2:
                if i[0] is None or i[1]:
                    wordcloud3 = get_wordcloud(book1, slider[0], slider[1], True)
                    wordcloud3_invalid = False
            elif idx == 3:
                if i[0] is None or i[1]:
                    wordcloud4 = get_wordcloud(book2, slider[0], slider[1], True, False)
                    wordcloud4_invalid = False

        if toggle1_state:
            return [
                html.Div([
                    html.Label('Meaningful words', className='label'), wordcloud1], className='wordcloud-container'),
                html.Div([
                    html.Label('Names', className='label'), wordcloud3], className='wordcloud-container')
            ]
        else:
            return[
                html.Div([
                    html.Label('Meaningful words', className='label'), wordcloud2], className='wordcloud-container'),
                html.Div([
                    html.Label('Names', className='label'), wordcloud4], className='wordcloud-container')
            ]
    
    else:
        global fig1, fig2, fig3, fig4, fig5, fig6
        fig1 = utils.get_word_freq_no_stopwords_bar_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        fig2 = utils.get_lute_count_bar_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        fig3 = utils.get_name_count_per_name_bar_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        fig4 = utils.get_chapter_length_bar_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        fig5 = utils.get_direct_vs_indirect_speech_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        fig6 = utils.get_avg_wordcount_per_sentence_bar_graph(book1 if toggle1_state else book2, slider[0], slider[1], 'summer' if toggle1_state else 'autumn')
        return html.Div(
            [
                dcc.Graph(id='graph1', className='bar-chart', figure=fig1),
                dcc.Graph(id='graph2', className='bar-chart', figure=fig2),
                dcc.Graph(id='graph3', className='bar-chart', figure=fig3),
                dcc.Graph(id='graph4', className='bar-chart', figure=fig4),
                dcc.Graph(id='graph5', className='bar-chart', figure=fig5),
                dcc.Graph(id='graph6', className='bar-chart', figure=fig6)
            ],
            className='bar-chart-container'
        )
    
@app.callback(
    dash.Output('hovered-chapter', 'data'),
    [dash.Input('graph1', 'hoverData'), dash.Input('graph2', 'hoverData'), dash.Input('graph3', 'hoverData'), dash.Input('graph4', 'hoverData'), dash.Input('graph5', 'hoverData'), dash.Input('graph6', 'hoverData')]
)
def store_hovered_chapter(hoverData1, hoverData2, hoverData3, hoverData4, hoverData5, hoverData6):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    hover_data = ctx.triggered[0]['value']
    if hover_data:
        return hover_data['points'][0]['x']
    return None

@app.callback(
    [dash.Output('graph1', 'figure'), dash.Output('graph2', 'figure'), dash.Output('graph3', 'figure'), dash.Output('graph4', 'figure'), dash.Output('graph5', 'figure'), dash.Output('graph6', 'figure')],
    [dash.Input('hovered-chapter', 'data')]
)
def highlight_hovered_chapter(hovered_chapter):
    global fig1, fig2, fig3, fig4, fig5, fig6
    if hovered_chapter is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    for fig in [fig1, fig2, fig3, fig4, fig5, fig6]:
        max_val = max(max([a for trace in fig['data'] for a in trace['y']]), 1)        

        for trace in fig['data']:
            if hovered_chapter in trace['x']:
                if fig == fig5:
                    max_val = max(max(fig['data'][0]['y']), 1)
                    trace['marker']['color'] = [
                            ("red" if trace['name'] == 'Indirect' else '#FF006E') if chapter == hovered_chapter else 
                            ('#DDD34E' if toggle1_state else'#C4C252') if trace['name'] == 'Indirect' else '#0C6749' if toggle1_state else '#D6631E'
                        for chapter in trace['x']
                    ]
                else:
                    trace['marker']['color'] = "red"
            else:
                if fig == fig5:
                    pass
                else:
                    trace['marker']['color'] = utils.map_values_to_colors([trace['y'][0] / max_val], utils.summer if toggle1_state else utils.wistia)

    return fig1, fig2, fig3, fig4, fig5, fig6

@app.callback(
        dash.Output('tab1', 'className'),
        dash.Output('tab2', 'className'),
        dash.Input('toggle-1', 'n_clicks'),
        dash.Input('toggle-2', 'n_clicks'),
)
def update_tab_colors(_, __):
    global toggle1_state
    return ('tab-green', 'tab-green') if toggle1_state else ('tab-red', 'tab-red')


@app.callback(
    dash.Output('slider-container', 'children'),
    dash.Output('toggle-container', 'children'),
    dash.Input('toggle-2', 'n_clicks'),
    dash.Input('toggle-1', 'n_clicks'),)
def buttons_toggle_children_update(_, __):
    global toggle1_state, toggle2_state, toggle1, toggle2, slider1_from, slider1_to, slider2_from, slider2_to
    toggle2_state = not toggle2_state
    toggle1_state = not toggle1_state
    
    toggle1 = html.Button(
        id="toggle-1",
        children="Name of the Wind",
        className='toggle-button toggle-button-green' if toggle1_state else 'toggle-button toggle-button-grey'
    )
    toggle2 = html.Button(
        id="toggle-2",
        children="Wise Man\'s Fear",
        className='toggle-button toggle-button-red' if toggle2_state else 'toggle-button toggle-button-grey'
    )

    slider_max = len(book1['chapters']) if toggle1_state else len(book2['chapters'])
    slider_saved_from = slider1_from if toggle1_state else slider2_from
    slider_saved_to = slider1_to if toggle1_state else slider2_to
    new_slider = dcc.RangeSlider(
        id='chapter-slider',
        min=0,
        max=slider_max - 1,
        step=1,
        marks={0: "1", slider_max: f"{slider_max}"} | {i: f"{i}" for i in range(10, slider_max, 10)},
        value=[slider_saved_from, slider_saved_to + 1],
        tooltip={'always_visible': True, 'placement': 'bottom', 'transform': 'addOne'},
        className='book1-slider' if toggle1_state else 'book2-slider'
    )
    
    return new_slider, [
        html.Div(
            toggle1,
            style={'display': 'inline-block', 'marginRight': '20px'}
        ),
        html.Div(
            toggle2,
            style={'display': 'inline-block'}
        )
    ],


if __name__ == "__main__":
    app.run_server(debug=True)#, dev_tools_silence_routes_logging = False)
