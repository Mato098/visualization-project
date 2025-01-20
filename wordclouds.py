import dash
import dash_core_components as dcc
import dash_html_components as html
from wordcloud import WordCloud
import base64
from io import BytesIO
from preprocessing import Chapter

def cull_dict(dictionary: dict, n: int):
    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)[:n])

def generate_wordcloud(chapter: Chapter, names: bool = False):
    dict = chapter.word_frequency_no_stopwords if not names else chapter.nameCount 
    wordcloud = WordCloud(width=800, height=800, margin=0,
                           background_color='white', colormap='viridis').generate_from_frequencies(cull_dict(dict, 25))

    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    return img_base64
