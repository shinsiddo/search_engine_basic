import math
from collections import Counter


class TFIDF:

    def __init__(self, documents, inverted_index, preprocess_text):

        self.documents = documents
        self.inverted_index = inverted_index
        self.preprocess_text = preprocess_text


    def calculate_tf_idf(self, word, filename):

        # Get the words from the document
        words = self.preprocess_text(
            self.documents[filename]
        )

        # Count words
        word_count = Counter(words)


        # -----------------------------
        # Term Frequency (TF)
        # -----------------------------

        tf = word_count[word] / len(words)


        # -----------------------------
        # Total documents
        # -----------------------------

        total_documents = len(self.documents)


        # -----------------------------
        # Document Frequency (DF)
        # -----------------------------

        document_frequency = len(
            self.inverted_index[word]
        )


        # -----------------------------
        # IDF
        # -----------------------------

        idf = math.log(
            total_documents / document_frequency
        )

        print(word,filename,"TF =", tf,"DF =", document_frequency,"IDF =", idf,"TF-IDF =", tf * idf)
        # -----------------------------
        # TF-IDF
        # -----------------------------

        return tf * idf