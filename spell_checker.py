class SpellChecker:

    def __init__(self, vocabulary):

        self.vocabulary = vocabulary


    # --------------------------------
    # Calculate Edit Distance
    # --------------------------------

    def edit_distance(self, word1, word2):

        m = len(word1)
        n = len(word2)

        dp = [
            [0] * (n + 1)
            for _ in range(m + 1)
        ]

        # Empty word cases
        for i in range(m + 1):
            dp[i][0] = i

        for j in range(n + 1):
            dp[0][j] = j

        # Fill DP table
        for i in range(1, m + 1):

            for j in range(1, n + 1):

                if word1[i - 1] == word2[j - 1]:

                    dp[i][j] = dp[i - 1][j - 1]

                else:

                    dp[i][j] = 1 + min(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i - 1][j - 1]
                    )

        return dp[m][n]


    # --------------------------------
    # Find closest word
    # --------------------------------

    def suggest_word(self, word, max_distance=2):

        suggestions = []

        for vocabulary_word in self.vocabulary:

            distance = self.edit_distance(
                word,
                vocabulary_word
            )

            if distance <= max_distance:

                suggestions.append(
                    (vocabulary_word, distance)
                )

        suggestions.sort(
            key=lambda x: x[1]
        )

        return suggestions


    # --------------------------------
# Correct complete query
# --------------------------------

    def suggest_query(
        self,
        query,
        max_distance=2
    ):

        words = query.split()

        corrected_words = []

        changed = False


        # Common words that should NEVER
        # be spell corrected
        protected_words = {

            "a",
            "an",
            "the",

            "and",
            "or",
            "not",

            "is",
            "are",
            "am",
            "was",
            "were",

            "be",
            "been",
            "being",

            "can",
            "could",
            "will",
            "would",
            "should",
            "may",
            "might",

            "how",
            "what",
            "when",
            "where",
            "why",
            "who",
            "whom",
            "which",

            "use",
            "uses",
            "using",

            "computer",
            "computers",

            "storage",

            "ram",

            "insufficient"
        }


        for original_word in words:

            # --------------------------------
            # Remove punctuation for checking
            # --------------------------------

            word = original_word.lower().strip(
                ".,!?;:()[]{}\"'"
            )


            # --------------------------------
            # Empty word
            # --------------------------------

            if not word:

                corrected_words.append(
                    original_word
                )

                continue


            # --------------------------------
            # Numbers
            # --------------------------------

            if word.isdigit():

                corrected_words.append(
                    original_word
                )

                continue


            # --------------------------------
            # Protected words
            # --------------------------------

            if word in protected_words:

                corrected_words.append(
                    original_word
                )

                continue


            # --------------------------------
            # Already correct
            # --------------------------------

            if word in self.vocabulary:

                corrected_words.append(
                    original_word
                )

                continue


            # --------------------------------
            # Find suggestions
            # --------------------------------

            suggestions = self.suggest_word(
                word,
                max_distance
            )


            # --------------------------------
            # Correct only strong matches
            # --------------------------------

            if suggestions:

                best_word, best_distance = (
                    suggestions[0]
                )


                if best_distance == 1:

                    # Preserve punctuation
                    punctuation = ""

                    if original_word[-1:] in ".,!?;:":

                        punctuation = (
                            original_word[-1]
                        )


                    corrected_words.append(
                        best_word + punctuation
                    )

                    changed = True

                else:

                    corrected_words.append(
                        original_word
                    )

            else:

                corrected_words.append(
                    original_word
                )


        # --------------------------------
        # Build corrected query
        # --------------------------------

        corrected_query = " ".join(
            corrected_words
        )


        # --------------------------------
        # Return only if changed
        # --------------------------------

        if changed:

            return corrected_query

        return None
    
    # --------------------------------
    # Correct Boolean query
    # --------------------------------

    def correct_boolean_query(
        self,
        query,
        max_distance=2
    ):

        operators = {"AND", "OR", "NOT"}

        parts = query.lower().split()

        corrected_parts = []

        for part in parts:

            # Keep Boolean operators unchanged
            if part.upper() in operators:

                corrected_parts.append(
                    part.upper()
                )

            else:

                # Check if word is already correct
                if part in self.vocabulary:

                    corrected_parts.append(part)

                else:

                    # Find closest word
                    suggestions = self.suggest_word(
                        part,
                        max_distance
                    )

                    if suggestions:

                        best_word = suggestions[0][0]

                        corrected_parts.append(
                            best_word
                        )

                    else:

                        corrected_parts.append(part)

        return " ".join(corrected_parts)