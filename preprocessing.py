import nltk
from nltk.corpus import stopwords
import re, typing, unicodedata
import json



class Book:
    def __init__(self, name) -> None:
        self.name = name
        self.chapters = []

class Chapter:
    def __init__(self, number, title, text):
        self.number = number
        self.title = title
        self.text = text
        self.wordcount = 0
        self.avg_word_length = 0
        self.avg_wordcount_per_sentence = 0
        self.word_frequency = {}
        self.word_frequency_sorted = []
        self.word_frequency_no_stopwords = {}
        self.word_frequency_no_stopwords_sorted = []

        self.lute_count = 0
        self.nameCount = {}

        self.direct_speech = 0
        self.indirect_speech = 0

    def __str__(self):
        return f'chapter {self.number}: {self.title}'


def load_text(path: str = './Name of the Wind.txt') -> str:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def create_book(text: str, name: str) -> Book:
    book = Book(name)
    chapters = re.split('CHAPTER [a-zA-Z -]+\n\n|PROLOGUE\n\n|EPILOGUE\n\n', text)[1:]

    for (i, chapter) in enumerate(chapters):
        result = re.split('\n\n', chapter, maxsplit=1)
        c = Chapter(i, result[0], result[1])
        book.chapters.append(c)
    return book
    
def process_chapter(chapter: Chapter) -> None:
    nameList = [
    'Kvothe', 'Kote', 'Denna', 'Dinna', 'Bast', 'Auri', 'Elodin', 'Elodine', 
    'Simmon', 'Simon', 'Sim', 'Wilem', 'Will', 'Fela', 'Devi', 'Devee', 'Kilvin', 
    'Ambrose', 'Chronicler', 'Hemme', 'Jasom Hemme', 'Manet', 'Lorren', 
    'Threpe', 'Count Threpe', 'Laurian', 'Arliden', 'Ben', 'Abenthy', 
    'Vashet', 'Penthe', 'Tempi', 'Shehyn', 'Cenesa', 'Carceret', 
    'Hespe', 'Dedan', 'Stanchion', 'Deoch', 'Felurian', 'Cthaeh', 
    'Selitos', 'Selitos Lorren', 'Jax', 'Iax', 'Alec', 'Trebon Mayor', 
    'Taborlin', 'Taborlin the Great', 'Lanre', 'Lyra', 'Aethe', 
    'Haliax', 'Alaxel', 'Meluan', 'Lady Meluan Lackless', 'Alveron', 
    'Maer Lerand Alveron', 'Caudicus', 'Sovoy', 'Brandeur', 
    'Elxa Dal', 'Mola', 'Bredon', 'Marton', 'Sleat', 'Trapis', 
    'Tanee', 'Loni', 'Cinder', 'Aaron', 'Cob', 'Dagon', 'Stapes', 
    'Puppet', 'Trip', 'Magwyn', 'Celean', 'Illien', 'Gibea', 'Teccam', 
    'Old Listener'
    ]
    stop_words = set(stopwords.words('english'))

    chapter.wordcount = len(chapter.text.split())
    chapter.avg_word_length = sum(len(word) for word in chapter.text.split()) / chapter.wordcount
    chapter.word_frequency = {}
    chapter.word_frequency_no_stopwords = {}
    
    split_text = re.split('“|”', chapter.text)
    direct_speech_word_count = 0
    indirect_speech_word_count = 0
    for i in range(0, len(split_text)):
        if i % 2 == 1:
            direct_speech_word_count += len(split_text[i].split())
        else:
            indirect_speech_word_count += len(split_text[i].split())
    
    chapter.direct_speech = direct_speech_word_count
    chapter.indirect_speech = indirect_speech_word_count
    
    for word in chapter.text.split():
        word = unicodedata.normalize('NFKD', word)
        word = word.split('\'')[0]
        word = re.sub(r'[^\w\s]', '', word)
        if word == '':
            continue
        if word in chapter.word_frequency:
            chapter.word_frequency[word] += 1
        else:
            chapter.word_frequency[word] = 1
        
        if word not in stop_words:
            if word in chapter.word_frequency_no_stopwords:
                chapter.word_frequency_no_stopwords[word] += 1
            else:
                chapter.word_frequency_no_stopwords[word] = 1
        if word in nameList:
            if word in chapter.nameCount:
                chapter.nameCount[word] += 1
            else:
                chapter.nameCount[word] = 1
    
    chapter.word_frequency_sorted = sorted(chapter.word_frequency.items(), key=lambda x: x[1], reverse=True)
    chapter.word_frequency_no_stopwords = chapter.word_frequency_no_stopwords
    chapter.word_frequency_no_stopwords_sorted = sorted(chapter.word_frequency_no_stopwords.items(), key=lambda x: x[1], reverse=True)
    
    for sentence in re.split('\. |\? |! |\.\n|\?\n|!\n', chapter.text):
        chapter.avg_wordcount_per_sentence += len(sentence.split())
    chapter.avg_wordcount_per_sentence /= len(re.split('\. |\? |! |\.\n|\?\n|!\n', chapter.text))
    chapter.lute_count = chapter.text.lower().count('lute')


    
    return chapter

def print_chapter(chapter: Chapter) -> None:
    print(chapter)
    print(f'word count: {chapter.wordcount}')
    print(f'average word length: {chapter.avg_word_length}')
    print(f'average word count per sentence: {chapter.avg_wordcount_per_sentence}')
    print('word frequency:')
    i = 0
    for (word, count) in chapter.word_frequency_sorted:
        i += 1
        if i > 5:
            break
        print(f'{word}: {count}')
    print(f'lute count: {chapter.lute_count}')

    print('no stopwords', chapter.word_frequency_no_stopwords_sorted[:10])
    print('names', chapter.nameCount)
    print()

def process_book(book: Book) -> None:
    for chapter in book.chapters:
        process_chapter(chapter)

def save_book_by_chapters(book: Book) -> None:
    for chapter in book.chapters:
        with open(f'chapter_{chapter.number}.txt', 'w', encoding='utf-8') as f:
            f.write(chapter.text)

def save_book_as_json(book: Book) -> None:
    #book without the text
    b = book
    for chapter in b.chapters:
        del chapter.text
    
    with open(f'./{b.name}.json', 'w', encoding='utf-8') as f:
        json.dump(book, f, default=lambda x: x.__dict__, indent=4)


def main():
    nltk.download('stopwords')

    text1 = load_text()
    book1 = create_book(text1, 'Name of the Wind')
    process_book(book1)
    save_book_as_json(book1)

    text2 = load_text('./wise_mans_fear.txt')
    book2 = create_book(text2, 'Wise Man\'s Fear')
    process_book(book2)
    save_book_as_json(book2)


if __name__ == '__main__':
    main()
