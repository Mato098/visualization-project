import dash
import dash_core_components as dcc
import dash_html_components as html
from wordcloud import WordCloud
import base64
from io import BytesIO
from preprocessing import Chapter

def generate_wordcloud(chapter: Chapter):
    print("WORDCLOUD GENERATION")
    wordcloud = WordCloud(width=800, height=800, margin=0,
                           background_color='white', colormap='viridis').generate_from_frequencies(chapter.word_frequency_no_stopwords)

    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    return img_base64
