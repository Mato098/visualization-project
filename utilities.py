from preprocessing import Book, Chapter
import plotly.express as px
import pandas as pd
import plotly.colors


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
            elif count > 0:
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
        result.nameCount["No names found"] = 1
        
    return result

def rgb_float_string_to_rgb_int(rgb_float_string): # 'rgb(0.0, 0.0, 0.0)' -> 'rgb(0, 0, 0)'
    return 'rgb(' + ', '.join([str(int(float(x))) for x in rgb_float_string[4:-1].split(', ')]) + ')'


def map_values_to_colors(values, color_scale):
    max_val = max(values)
    normalized_values = values
    colors = [rgb_float_string_to_rgb_int(plotly.colors.find_intermediate_color(color_scale[0], color_scale[-1], val/max_val, colortype='rgb')) for val in normalized_values]
    return colors




def get_word_freq_no_stopwords_bar_graph(book: Book, from_idx: int, to_idx: int, theme: str) -> px.bar:

    chapter = accumulate_chapters(book, from_idx, to_idx)

    color_scale = px.colors.colorbrewer.Greens if theme == 'summer' else px.colors.colorbrewer.Oranges

    values = [freq for word, freq in chapter.word_frequency_no_stopwords_sorted[:10]]
    colors = map_values_to_colors(values, color_scale)

    df = pd.DataFrame({
        'Words': [word for word, freq in chapter.word_frequency_no_stopwords_sorted[:10]],
        'Frequency': values,
        'category': [str(i) for i in range(10)]
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
    return fig

