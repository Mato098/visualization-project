from preprocessing import Book, Chapter
import plotly.express as px
import pandas as pd
import plotly.colors


summer = ['rgb(1,97,73)', 'rgb(221,211,78)']
dark_complement = 'rgb(68,56,53)'
wistia = ['rgb(194,211,92)', 'rgb(214,99,28)']

def accumulate_chapters(book: Book, ch_from: int, ch_to: int) -> Chapter:
    result: Chapter = Chapter(0, '', '')
    for i in range(ch_from, ch_to + 1):
        result.wordcount += book['chapters'][i]['wordcount']
        result.avg_word_length += book['chapters'][i]['avg_word_length']
        result.avg_wordcount_per_sentence += book['chapters'][i]['avg_wordcount_per_sentence']
        result.lute_count += book['chapters'][i]['lute_count']

        for name, count in book['chapters'][i]['nameCount'].items():
            if name in result.nameCount:
                result.nameCount[name] += count
            else:
                result.nameCount[name] = count

        for word in book['chapters'][i]['word_frequency']:
            if word in result.word_frequency:
                result.word_frequency[word] += book['chapters'][i]['word_frequency'][word]
            else:
                result.word_frequency[word] = book['chapters'][i]['word_frequency'][word]

        for word in book['chapters'][i]['word_frequency_no_stopwords']:
            if word in result.word_frequency_no_stopwords:
                result.word_frequency_no_stopwords[word] += book['chapters'][i]['word_frequency_no_stopwords'][word]
            else:
                result.word_frequency_no_stopwords[word] = book['chapters'][i]['word_frequency_no_stopwords'][word]
                
    result.avg_word_length /= max(ch_to - ch_from, 1)
    result.avg_wordcount_per_sentence /= max(ch_to - ch_from, 1)
    result.word_frequency_sorted = sorted(result.word_frequency.items(), key=lambda x: x[1], reverse=True)
    result.word_frequency_no_stopwords_sorted = sorted(result.word_frequency_no_stopwords.items(), key=lambda x: x[1], reverse=True)

    if len(result.nameCount) == 0:
        result.nameCount["No names found"] = 0

    return result

def rgb_float_string_to_rgb_int(rgb_float_string): # 'rgb(0.0, 0.0, 0.0)' -> 'rgb(0, 0, 0)'
    return 'rgb(' + ', '.join([str(int(float(x))) for x in rgb_float_string[4:-1].split(', ')]) + ')'


def map_values_to_colors(values, color_scale):
    max_val = max(max(values), 1)
    normalized_values = values
    colors = [rgb_float_string_to_rgb_int(plotly.colors.find_intermediate_color(color_scale[0], color_scale[-1], val/max_val, colortype='rgb')) for val in normalized_values]
    return colors


def get_word_freq_no_stopwords_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:

    chapter = accumulate_chapters(book, from_idx, to_idx)

    color_scale = summer if theme == 'summer' else wistia

    values = [freq for word, freq in chapter.word_frequency_no_stopwords_sorted[:25]]
    
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Words': [word for word, freq in chapter.word_frequency_no_stopwords_sorted[:25]],
        'Frequency': values,
        'category': [str(i) for i in range(25)]
    })

    fig = px.bar(
        data_frame=df,
        x='Words',
        y='Frequency',
        labels={'x': 'Words', 'y': 'Frequency'},
        title=f'Word Frequency (No Stopwords)',
        color_discrete_sequence=colors,
        color='category',
    )
    fig = style_fig(fig, theme)
    return fig

def style_fig(fig: px.bar, theme: str = '', clamp: int = 100, customdata_column: str = None) -> px.bar:
    fig.update_yaxes(linecolor='rgb(228,236,246)', gridcolor='rgb(228,236,246)', zerolinecolor='rgb(228,236,246)')
    fig.update_layout(plot_bgcolor='rgb(64,60,57)', paper_bgcolor=dark_complement, font_color='white')
    fig.update_layout(showlegend=False)
    fig.update_layout(hovermode='x')
    fig.update_layout(xaxis=dict(range=[-0.5, min(clamp - 0.5, len(fig.data))]))
    
    return fig

def get_lute_count_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:

    color_scale = summer if theme == 'summer' else wistia

    values = []
    chapter_names = []
    for i in range(from_idx, to_idx + 1):
        values.append(book['chapters'][i]['lute_count'])
        chapter_names.append(f'{book["chapters"][i]["number"]} - {book["chapters"][i]["title"]}')
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Chapter': [f'Chapter {i}' for i in range(from_idx, to_idx + 1)],
        'Lute Count': values,
        'category': [str(i) for i in range(to_idx - from_idx + 1)],
        'Chapter Names': chapter_names
        
    })

    fig = px.bar(
        data_frame=df,
        x='Chapter',
        y='Lute Count',
        labels={'x': 'Chapter', 'y': 'Lute Count'},
        title=f'Times the word "lute" was mentioned',
        color_discrete_sequence=colors,
        color='category',
        hover_name='Chapter Names'
    )
    fig = style_fig(fig, theme, customdata_column='Chapter Names')
    return fig

def get_name_count_per_name_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:
    
    chapter = accumulate_chapters(book, from_idx, to_idx)

    color_scale = summer if theme == 'summer' else wistia

    values = [count for name, count in chapter.nameCount.items()]
    values, names = zip(*sorted(zip(values, chapter.nameCount.keys()), reverse=True))

    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Name': names,
        'Count': values,
        'category': [str(i) for i in range(len(chapter.nameCount))]
    })

    fig = px.bar(
        data_frame=df,
        x='Name',
        y='Count',
        labels={'x': 'Name', 'y': 'Count'},
        title=f'Times each character name was mentioned',
        color_discrete_sequence=colors,
        color='category',
    )
    fig = style_fig(fig, theme, 25)
    return fig

def get_chapter_length_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:

    color_scale = summer if theme == 'summer' else wistia

    values = [book['chapters'][i]['wordcount'] for i in range(from_idx, to_idx + 1)]
    
    chapter_names = []
    for i in range(from_idx, to_idx + 1):
        chapter_names.append(f'{book["chapters"][i]["number"]} - {book["chapters"][i]["title"]}')
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Chapter': [f'Chapter {i}' for i in range(from_idx, to_idx + 1)],
        'Word Count': values,
        'category': [str(i) for i in range(to_idx - from_idx + 1)],
        'Chapter Names': chapter_names
    })

    fig = px.bar(
        data_frame=df,
        x='Chapter',
        y='Word Count',
        labels={'x': 'Chapter', 'y': 'Word Count'},
        title=f'Chapter Length',
        color_discrete_sequence=colors,
        color='category',
        hover_name='Chapter Names'
    )
    fig = style_fig(fig, theme, customdata_column='Chapter Names')
    return fig

def get_avg_word_length_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:

    color_scale = summer if theme == 'summer' else wistia
    
    chapter_names = []
    for i in range(from_idx, to_idx + 1):
        chapter_names.append(f'{book["chapters"][i]["number"]} - {book["chapters"][i]["title"]}')
    values = [book['chapters'][i]['avg_word_length'] for i in range(from_idx, to_idx + 1)]
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Chapter': [f'Chapter {i}' for i in range(from_idx, to_idx + 1)],
        'Average Word Length': values,
        'category': [str(i) for i in range(to_idx - from_idx + 1)],
        'Chapter Names': chapter_names
    })

    fig = px.bar(
        data_frame=df,
        x='Chapter',
        y='Average Word Length',
        labels={'x': 'Chapter', 'y': 'Average Word Length'},
        title=f'Average Word Length',
        color_discrete_sequence=colors,
        color='category',
        hover_name='Chapter Names',
    )
    fig = style_fig(fig, theme, customdata_column='Chapter Names')
    return fig

def get_avg_wordcount_per_sentence_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:
    
    color_scale = summer if theme == 'summer' else wistia

    values = [book['chapters'][i]['avg_wordcount_per_sentence'] for i in range(from_idx, to_idx + 1)]
    chapter_names = []
    for i in range(from_idx, to_idx + 1):
        chapter_names.append(f'{book["chapters"][i]["number"]} - {book["chapters"][i]["title"]}')
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Chapter': [f'Chapter {i}' for i in range(from_idx, to_idx + 1)],
        'Average Word Count per Sentence': values,
        'category': [str(i) for i in range(to_idx - from_idx + 1)],
        'Chapter Names': chapter_names
    })

    fig = px.bar(
        data_frame=df,
        x='Chapter',
        y='Average Word Count per Sentence',
        labels={'x': 'Chapter', 'y': 'Average Word Count per Sentence'},
        title=f'Average Word Count per Sentence',
        color_discrete_sequence=colors,
        color='category',
        hover_name='Chapter Names'
    )
    fig = style_fig(fig, theme, customdata_column='Chapter Names')
    return fig

def get_direct_vs_indirect_speech_graph(book: Book, from_idx: int, to_idx: int, theme: str):
    values_direct = [book['chapters'][i]['direct_speech'] for i in range(from_idx, to_idx + 1)]
    values_indirect = [book['chapters'][i]['indirect_speech'] for i in range(from_idx, to_idx + 1)]
    color_scale_direct = summer if theme == 'summer' else wistia
    color_scale_indirect = wistia if theme == 'summer' else summer
    colors_direct = map_values_to_colors(values_direct, color_scale_direct)
    colors_indirect = map_values_to_colors(values_indirect, color_scale_indirect)

    chapter_names = []
    for i in range(from_idx, to_idx + 1):
        chapter_names.append(f'{book["chapters"][i]["number"]} - {book["chapters"][i]["title"]}')

    df = pd.DataFrame({
        'Chapter': [f'Chapter {i}' for i in range(from_idx, to_idx + 1)],
        'Direct': values_direct,
        'Indirect': values_indirect,
        'Chapter Names': chapter_names
    })


    fig = px.bar(
        data_frame=df,
        x='Chapter',
        y=['Direct', 'Indirect'],
        labels={'x': 'Chapter', 'y': 'Frequency'},
        title=f'Direct and Indirect Speech',
        color_discrete_sequence=[colors_direct, colors_indirect],
        hover_name='Chapter Names'
    )
    fig = style_fig(fig, theme, customdata_column='Chapter Names')
    fig.update_layout(showlegend=True)
    return fig
