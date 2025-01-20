from preprocessing import Book, Chapter

def accumulate_chapters(book: Book, ch_from: int, ch_to: int) -> Chapter:
    result: Chapter = Chapter(0, '', '')
    for i in range(ch_from, ch_to + 1):
        result.wordcount += book['chapters'][i]['wordcount']
        result.avg_word_length += book['chapters'][i]['avg_word_length']
        result.avg_wordcount_per_sentence += book['chapters'][i]['avg_wordcount_per_sentence']
        result.lute_count += book['chapters'][i]['lute_count']
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
    return result
