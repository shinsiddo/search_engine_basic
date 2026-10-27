from sentence_transformers import SentenceTransformer
import numpy as np


class SemanticSearch:

    def __init__(
        self,
        documents,
        database=None,
        folder=None
    ):

        self.documents = documents

        self.database = database

        self.folder = folder


        # =================================
        # LOAD MODEL
        # =================================

        print("\nLoading semantic model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Semantic model loaded.")


        # =================================
        # DOCUMENT INFORMATION
        # =================================

        self.filenames = list(
            documents.keys()
        )


        self.texts = [
            documents[filename]
            for filename in self.filenames
        ]


        # =================================
        # CREATE / LOAD EMBEDDINGS
        # =================================

        self.document_embeddings = []


        print(
            "\nLoading semantic embeddings..."
        )


        for filename, text in documents.items():

            embedding = None


            # =================================
            # CHECK SQLITE
            # =================================

            if (
                self.database is not None
                and self.folder is not None
            ):

                filepath = (
                    self.folder
                    + "\\"
                    + filename
                )


                modified_time = (
                    __import__("os")
                    .path.getmtime(filepath)
                )


                stored_info = (
                    self.database
                    .get_embedding_info()
                )


                if (
                    filename in stored_info
                    and
                    stored_info[filename]
                    == modified_time
                ):

                    embedding = (
                        self.database
                        .load_embedding(
                            filename
                        )
                    )


                    print(
                        "Loaded embedding:",
                        filename
                    )


            # =================================
            # CREATE NEW EMBEDDING
            # =================================

            if embedding is None:

                print(
                    "Creating embedding:",
                    filename
                )


                embedding = self.model.encode(
                    text,
                    normalize_embeddings=True
                )


                # =================================
                # SAVE TO SQLITE
                # =================================

                if (
                    self.database is not None
                    and self.folder is not None
                ):

                    filepath = (
                        self.folder
                        + "\\"
                        + filename
                    )


                    modified_time = (
                        __import__("os")
                        .path.getmtime(filepath)
                    )


                    self.database.save_embedding(
                        filename,
                        embedding,
                        modified_time
                    )


            self.document_embeddings.append(
                embedding
            )


        # =================================
        # CONVERT TO NUMPY ARRAY
        # =================================

        self.document_embeddings = np.array(
            self.document_embeddings
        )


        print(
            "\nSemantic embeddings ready."
        )


    # =================================
    # SEARCH
    # =================================

    def search(
        self,
        query,
        top_k=10
    ):

        # --------------------------------
        # QUERY EMBEDDING
        # --------------------------------

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )


        # --------------------------------
        # COSINE SIMILARITY
        # --------------------------------

        scores = np.dot(
            self.document_embeddings,
            query_embedding
        )


        # --------------------------------
        # SORT
        # --------------------------------

        ranked_indices = np.argsort(
            scores
        )[::-1]


        results = []


        for index in ranked_indices[:top_k]:

            filename = self.filenames[
                index
            ]


            score = float(
                scores[index]
            )


            results.append(
                (
                    score,
                    filename
                )
            )


        return results