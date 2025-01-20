import nltk
from nltk.corpus import stopwords
import re, typing, unicodedata
import json

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))

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
    chapter.wordcount = len(chapter.text.split())
    chapter.avg_word_length = sum(len(word) for word in chapter.text.split()) / chapter.wordcount
    chapter.word_frequency = {}
    chapter.word_frequency_no_stopwords = {}
    
    for word in chapter.text.split():
        word = word.lower()
        word = unicodedata.normalize('NFKD', word)
        word = re.sub(r'[^\w\s]', '', word)
        if word in chapter.word_frequency:
            chapter.word_frequency[word] += 1
        else:
            chapter.word_frequency[word] = 1
        
        if word not in stop_words:
            if word in chapter.word_frequency_no_stopwords:
                chapter.word_frequency_no_stopwords[word] += 1
            else:
                chapter.word_frequency_no_stopwords[word] = 1
    
    chapter.word_frequency = {k: v for k, v in chapter.word_frequency.items() if v >= 5} # delete words with count less than 5
    chapter.word_frequency_sorted = sorted(chapter.word_frequency.items(), key=lambda x: x[1], reverse=True)
    
    # Filter out words with occurrences less than 5
    filtered_words = {k: v for k, v in chapter.word_frequency_no_stopwords.items() if v >= 5}

    # Check if the remaining words are 15 or more
    if len(filtered_words) >= 15:
        chapter.word_frequency_no_stopwords = filtered_words
    else:
        # If fewer than 15 words, keep all words
        chapter.word_frequency_no_stopwords = chapter.word_frequency_no_stopwords

    # Sort the word frequencies
    chapter.word_frequency_no_stopwords_sorted = sorted(chapter.word_frequency_no_stopwords.items(), key=lambda x: x[1], reverse=True)
    
    for sentence in re.split('\. |\? |! |\.\n|\?\n|!\n', chapter.text):
        chapter.avg_wordcount_per_sentence += len(sentence.split())
    chapter.avg_wordcount_per_sentence /= len(re.split('\. |\? |! |\.\n|\?\n|!\n', chapter.text))
    chapter.lute_count = chapter.text.lower().count('lute')

    nameList = [
    'Kvothe', 'Denna', 'Bast', 'Auri', 'Elodin', 'Simmon', 'Wilem', 
    'Fela', 'Devi', 'Kilvin', 'Ambrose', 'Chronicler', 'Hemme', 
    'Manet', 'Lorren', 'Threpe', 'Laurian', 'Arliden', 'Ben', 
    'Vashet', 'Penthe', 'Tempi', 'Shehyn', 'Cenesa', 'Carceret', 
    'Hespe', 'Dedan', 'Stanchion', 'Deoch', 'Felurian', 'Cthaeh', 
    'Selitos', 'Jax', 'Alec', 'Trebon Mayor', 'Taborlin', 'Lanre', 
    'Lyra', 'Aethe', 'Haliax', 'Meluan', 'Alveron', 'Caudicus', 
    'Sovoy', 'Brandeur', 'Elxa Dal', 'Mola', 'Bredon', 'Marton', 
    'Sleat'
]
    
    for name in nameList:
        #name = name.lower()
        chapter.nameCount[name] = chapter.text.count(name)

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
