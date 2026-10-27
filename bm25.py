import math
from collections import Counter


class BM25:

    def __init__(
        self,
        documents,
        inverted_index,
        preprocess_text
    ):

        self.documents = documents
        self.inverted_index = inverted_index
        self.preprocess_text = preprocess_text

        # BM25 parameters
        self.k1 = 1.5
        self.b = 0.75

        # --------------------------------
        # Preprocess documents
        # --------------------------------

        self.processed_documents = {}

        for filename, text in documents.items():

            words = preprocess_text(text)

            self.processed_documents[filename] = words

        # --------------------------------
        # Calculate average document length
        # --------------------------------

        total_length = 0

        for words in self.processed_documents.values():

            total_length += len(words)

        self.average_document_length = (
            total_length / len(documents)
        )


    # --------------------------------
    # Calculate BM25 score
    # --------------------------------

    def calculate_score(
        self,
        query_words,
        filename
    ):

        words = self.processed_documents[filename]

        word_count = Counter(words)

        document_length = len(words)

        total_documents = len(
            self.processed_documents
        )

        score = 0


        # --------------------------------
        # Process every query word
        # --------------------------------

        for word in query_words:

            # Check whether word exists
            if word not in self.inverted_index:
                continue


            # --------------------------------
            # Term Frequency
            # --------------------------------

            tf = word_count[word]

            if tf == 0:
                continue


            # --------------------------------
            # Document Frequency
            # --------------------------------

            # Instead of scanning every document,
            # use the inverted index

            document_frequency = len(
                self.inverted_index[word]
            )


            # --------------------------------
            # IDF
            # --------------------------------

            idf = math.log(
                1 +
                (
                    total_documents
                    -
                    document_frequency
                    +
                    0.5
                )
                /
                (
                    document_frequency
                    +
                    0.5
                )
            )


            # --------------------------------
            # BM25 Formula
            # --------------------------------

            numerator = (
                tf * (self.k1 + 1)
            )


            denominator = (
                tf
                +
                self.k1 *
                (
                    1
                    -
                    self.b
                    +
                    self.b *
                    (
                        document_length
                        /
                        self.average_document_length
                    )
                )
            )


            score += idf * (
                numerator / denominator
            )


        return score