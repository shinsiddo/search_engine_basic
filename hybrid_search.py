import numpy as np


class HybridSearch:

    def __init__(
        self,
        bm25,
        semantic_search,
        bm25_weight=0.6,
        semantic_weight=0.4
    ):

        self.bm25 = bm25
        self.semantic_search = semantic_search

        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight


    # --------------------------------
    # NORMALIZE SCORES
    # --------------------------------

    def normalize_scores(self, scores):

        if not scores:
            return {}

        values = list(scores.values())

        minimum = min(values)
        maximum = max(values)

        # All scores are same
        if maximum == minimum:

            return {
                filename: 1.0
                for filename in scores
            }

        normalized = {}

        for filename, score in scores.items():

            normalized[filename] = (
                (score - minimum)
                /
                (maximum - minimum)
            )

        return normalized


    # --------------------------------
    # HYBRID SEARCH
    # --------------------------------

    def search(
        self,
        query_words,
        query,
        documents,
        candidates
    ):

        # =================================
        # 1. BM25
        # =================================

        bm25_scores = {}

        for filename in candidates:

            score = self.bm25.calculate_score(
                query_words,
                filename
            )

            bm25_scores[filename] = score


        # =================================
        # 2. NORMALIZE BM25
        # =================================

        normalized_bm25 = (
            self.normalize_scores(
                bm25_scores
            )
        )


        # =================================
        # 3. SEMANTIC SEARCH
        # =================================

        semantic_results = (
            self.semantic_search.search(
                query,
                top_k=len(documents)
            )
        )


        semantic_scores = {}

        for score, filename in semantic_results:

            semantic_scores[filename] = score


        # =================================
        # 4. NORMALIZE SEMANTIC
        # =================================

        normalized_semantic = (
            self.normalize_scores(
                semantic_scores
            )
        )


        # =================================
        # 5. COMBINE BM25 + SEMANTIC
        # =================================

        hybrid_scores = {}

        for filename in candidates:

            bm25_score = normalized_bm25.get(
                filename,
                0
            )

            semantic_score = normalized_semantic.get(
                filename,
                0
            )

            final_score = (

                self.bm25_weight
                *
                bm25_score

                +

                self.semantic_weight
                *
                semantic_score

            )

            hybrid_scores[filename] = final_score


        return hybrid_scores