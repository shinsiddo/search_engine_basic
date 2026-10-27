class PhraseSearch:

    def __init__(self, documents):

        self.documents = documents


    def search(self, query):

        results = []

        # Convert query to lowercase
        query = query.lower()


        # Check every document
        for filename, text in self.documents.items():

            text = text.lower()

            # Check if exact phrase exists
            if query in text:

                results.append(filename)


        return results