class TopK:

    def __init__(self, k=5):

        self.k = k


    # --------------------------------
    # Get top K results
    # --------------------------------

    def get_top_results(self, results):

        # Sort results by score
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Return only top K
        return sorted_results[:self.k]