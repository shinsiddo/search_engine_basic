class BooleanSearch:

    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    # --------------------------------
    # AND search
    # --------------------------------

    def and_search(self, words):

        if not words:
            return set()

        # Start with documents of first word
        results = self.inverted_index.get(
            words[0],
            set()
        ).copy()

        # Keep only documents containing
        # every other word
        for word in words[1:]:

            results = results.intersection(
                self.inverted_index.get(word, set())
            )

        return results


    # --------------------------------
    # OR search
    # --------------------------------

    def or_search(self, words):

        results = set()

        for word in words:

            results.update(
                self.inverted_index.get(word, set())
            )

        return results


    # --------------------------------
    # NOT search
    # --------------------------------

    def not_search(self, include_word, exclude_word):

        include_documents = self.inverted_index.get(
            include_word,
            set()
        )

        exclude_documents = self.inverted_index.get(
            exclude_word,
            set()
        )

        return include_documents.difference(
            exclude_documents
        )