import heapq


class TopK:

    def __init__(self, k=10):
        self.k = k


    def get_top_k(self, results):

        # --------------------------------
        # REMOVE DUPLICATE DOCUMENTS
        # --------------------------------

        unique_results = {}

        for filename, score in results.items():

            if filename not in unique_results:

                unique_results[filename] = score

            else:

                # Keep highest score
                unique_results[filename] = max(
                    unique_results[filename],
                    score
                )


        # --------------------------------
        # GET TOP K
        # --------------------------------

        top_results = heapq.nlargest(
            self.k,
            unique_results.items(),
            key=lambda x: x[1]
        )


        # --------------------------------
        # RETURN FORMAT
        # --------------------------------
        # (score, filename)

        return [
            (score, filename)
            for filename, score in top_results
        ]