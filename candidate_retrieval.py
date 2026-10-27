class CandidateRetrieval:

    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    # --------------------------------
    # Find candidate documents
    # --------------------------------

    def get_candidates(self, query_words):

        candidates = set()

        for word in query_words:

            if word in self.inverted_index:

                # Get documents containing this word
                documents = self.inverted_index[word]

                # Add them to candidate set
                candidates.update(documents)

        return candidates