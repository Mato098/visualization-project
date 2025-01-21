import dash
import dash_core_components as dcc
import dash_html_components as html
from wordcloud import WordCloud
import base64
from io import BytesIO
from preprocessing import Chapter

def cull_dict(dictionary: dict, n: int) -> dict:
    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)[:n])

def generate_wordcloud(chapter: Chapter, names: bool = False, green_colormap: bool = True) -> str:
    dict = chapter.word_frequency_no_stopwords if not names else chapter.nameCount 
    wordcloudd = WordCloud(width=800, height=800, margin=0,
                           background_color='#5D4E4A', colormap='summer' if green_colormap else 'Wistia').generate_from_frequencies(cull_dict(dict, 25))

    img = BytesIO()
    wordcloudd.to_image().save(img, format='PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64
