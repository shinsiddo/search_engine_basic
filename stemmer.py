from nltk.stem import PorterStemmer


class Stemmer:

    def __init__(self):

        # Create Porter Stemmer object
        self.stemmer = PorterStemmer()


    def stem_word(self, word):

        # Convert word to lowercase
        word = word.lower()

        # Return stemmed word
        return self.stemmer.stem(word)


    def stem_words(self, words):

        # Create empty list
        stemmed_words = []

        # Stem every word
        for word in words:

            stemmed_word = self.stem_word(word)

            stemmed_words.append(stemmed_word)

        return stemmed_words
stemmer = Stemmer()
