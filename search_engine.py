import os
import string
from stemmer import Stemmer
from trie import Trie
from tfidf import TFIDF
from spell_checker import SpellChecker
import phrase_function
from bm25 import BM25
from candidate_retrieval import CandidateRetrieval
from top_k import TopK
from boolean_search import BooleanSearch
from search_history import SearchHistory
from top_k_heap import TopK
from query_cache import QueryCache
from semantic_search import SemanticSearch
from hybrid_search import HybridSearch
from database import SearchDatabase


# =================================
# SQLITE DATABASE
# =================================

database = SearchDatabase()

documents = database.load_documents()


# =================================
# STEP 1: SQLITE DATABASE + SYNC
# =================================

database = SearchDatabase(
    "search_engine.db"
)


folder = r"C:\Users\sssid\Downloads\search_engine_basic\search_engine_basic\documents"


# =================================
# GET DATABASE DOCUMENTS
# =================================

database_documents = (
    database.get_documents_info()
)


# =================================
# GET FILES FROM FOLDER
# =================================

folder_documents = {}


for filename in os.listdir(folder):

    filepath = os.path.join(
        folder,
        filename
    )


    # Ignore folders
    if not os.path.isfile(filepath):

        continue


    # Read document
    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()


    # Get modification time
    modified_time = os.path.getmtime(
        filepath
    )


    folder_documents[filename] = {
        "content": text,
        "modified_time": modified_time
    }


# =================================
# SYNCHRONIZE DATABASE
# =================================

print(
    "\nChecking document changes..."
)


# =================================
# NEW / MODIFIED DOCUMENTS
# =================================

for filename, info in folder_documents.items():

    content = info["content"]

    modified_time = info["modified_time"]


    # --------------------------------
    # NEW DOCUMENT
    # --------------------------------

    if filename not in database_documents:

        print(
            "NEW document:",
            filename
        )


        database.save_document(
            filename,
            content,
            modified_time
        )


    # --------------------------------
    # EXISTING DOCUMENT
    # --------------------------------

    else:

        old_modified_time = (
            database_documents[
                filename
            ]["modified_time"]
        )


        # --------------------------------
        # MODIFIED DOCUMENT
        # --------------------------------

        if modified_time != old_modified_time:

            print(
                "MODIFIED document:",
                filename
            )


            database.save_document(
                filename,
                content,
                modified_time
            )


# =================================
# DELETED DOCUMENTS
# =================================

for filename in database_documents:

    if filename not in folder_documents:

        print(
            "DELETED document:",
            filename
        )


        database.delete_document(
            filename
        )


# =================================
# LOAD FINAL DOCUMENTS
# =================================

documents = database.load_documents()


print(
    "\nDocuments loaded:",
    len(documents)
)



# --------------------------------
# STOP WORDS
# --------------------------------

stop_words = {
    "the",
    "is",
    "a",
    "an",
    "for",
    "to",
    "of",
    "and",
    "in",
    "on"
}

# --------------------------------
# CREATE STEMMER OBJECT
# --------------------------------

stemmer = Stemmer()

# --------------------------------
# TEXT PREPROCESSING
# --------------------------------

def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Split into words
    words = text.split()

    # Remove stop words
    words = [
        word
        for word in words
        if word not in stop_words
    ]

    # Apply stemming
    words = stemmer.stem_words(words)

    return words

# --------------------------------
# CREATE ORIGINAL VOCABULARY
# --------------------------------

original_vocabulary = set()

for filename, text in documents.items():

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Split into words
    words = text.split()

    # Remove stop words
    words = [
        word
        for word in words
        if word not in stop_words
    ]

    # Add ORIGINAL words without stemming
    original_vocabulary.update(words)

# --------------------------------
# CREATE INVERTED INDEX
# --------------------------------

inverted_index = {}


for filename, text in documents.items():

    words = preprocess_text(text)


    for word in words:

        if word not in inverted_index:

            inverted_index[word] = set()


        inverted_index[word].add(
            filename
        )

# --------------------------------
# CREATE BOOLEAN SEARCH
# --------------------------------

boolean_search = BooleanSearch(
    inverted_index
)

# --------------------------------
# CREATE CANDIDATE RETRIEVAL
# --------------------------------

candidate_retrieval = CandidateRetrieval(
    inverted_index
)

# --------------------------------
# CREATE TOP-K OBJECT
# --------------------------------

top_k = TopK(5)


# --------------------------------
# CREATE SPELL CHECKER
# --------------------------------

spell_checker = SpellChecker(
    original_vocabulary
)

# --------------------------------
# CREATE TF-IDF OBJECT
# --------------------------------

tfidf = TFIDF(
    documents,
    inverted_index,
    preprocess_text
)

# --------------------------------
# CREATE BM25 OBJECT
# --------------------------------

bm25 = BM25(
    documents,
    inverted_index,
    preprocess_text
)

# --------------------------------
# CREATE SEMANTIC SEARCH
# --------------------------------

semantic_search = SemanticSearch(
    documents,
    database,
    folder
)

# --------------------------------
# CREATE HYBRID SEARCH
# --------------------------------

hybrid_search = HybridSearch(
    bm25,
    semantic_search,
    bm25_weight=0.6,
    semantic_weight=0.4
)

# --------------------------------
# CREATE QUERY CACHE (change max_size and ttl(cache lifetime) as needed)
# --------------------------------

query_cache = QueryCache(
    max_size=100,
    ttl=300
)

# --------------------------------
# CREATE SEARCH HISTORY
# --------------------------------

search_history = SearchHistory()

# --------------------------------
# BUILD TRIE
# --------------------------------

trie = Trie()


for word in inverted_index:

    trie.insert(word)


# --------------------------------
# CONTINUOUS SEARCH
# --------------------------------

while True:

    query = input("\nSearch: ").strip()

    if query.lower() == "exit":
        print("Exiting search engine...")
        break

    # rest of your search code here

    # --------------------------------
    # BEFORE AUTO CORRECTION, SAVE ORIGINAL QUERY
    # --------------------------------

    original_query = query
    corrected_query = None


    # --------------------------------
    # AUTOMATIC SPELL CORRECTION
    # --------------------------------

    is_phrase = (
        query.startswith('"')
        and query.endswith('"')
    )

    is_boolean = (
        " AND " in query.upper()
        or " OR " in query.upper()
        or " NOT " in query.upper()
    )


    # Don't correct exact phrases
    if is_phrase:

        pass


    # Correct words but protect AND / OR / NOT
    elif is_boolean:

        corrected_query = spell_checker.correct_boolean_query(
            query
        )

        if corrected_query != query:

            print(
                "\nCorrected query:",
                corrected_query
            )

            query = corrected_query


    # Normal query
    else:

        corrected_query = spell_checker.suggest_query(
            query
        )

        if corrected_query:

            print(
                "\nCorrected query:",
                corrected_query
            )

            query = corrected_query



    # --------------------------------
    # DETERMINE SEARCH TYPE
    # --------------------------------

    if query.startswith('"') and query.endswith('"'):

        search_type = "Phrase Search"

    elif " AND " in query.upper():

        search_type = "Boolean AND"

    elif " OR " in query.upper():

        search_type = "Boolean OR"

    elif " NOT " in query.upper():

        search_type = "Boolean NOT"

    else:

        query_words_temp = preprocess_text(query)

        if len(query_words_temp) == 1:
            search_type = "TF-IDF"
        else:
            search_type = "BM25"

    # --------------------------------
    # SAVE SEARCH HISTORY
    # --------------------------------

    search_history.save_search(
        original_query,
        corrected_query,
        search_type
    )


    # --------------------------------
    # CREATE WORDS FOR SEARCH
    # --------------------------------

    query_words = preprocess_text(query)


    # --------------------------------
    # INITIALIZE RESULTS
    # --------------------------------

    results = {}

    for filename in documents:

        results[filename] = 0


    # --------------------------------
    # AUTOCOMPLETE
    # --------------------------------

    suggestions = trie.autocomplete(
        query.lower()
    )


    if suggestions:

        print("\nSuggestions:")

        for i, word in enumerate(suggestions[:5], 1):

            print(f"{i}. {word}")


        # Ask user whether they want a suggestion
        choice = input(
            "\nEnter suggestion number "
            "(or press Enter to search your query): "
        ).strip()


        # If user selected a suggestion
        if choice.isdigit():

            choice = int(choice)

            if 1 <= choice <= min(5, len(suggestions)):

                query = suggestions[choice - 1]

                print(f"\nSearching for: {query}")


    # --------------------------------
    # CONVERT QUERY INTO WORDS
    # --------------------------------

    query_words = preprocess_text(
        query
    )


    # --------------------------------
    # INITIALIZE RESULTS
    # --------------------------------

    results = {}


    for filename in documents:

        results[filename] = 0


    # --------------------------------
    # PHRASE SEARCH
    # --------------------------------

    if (
        query.startswith('"')
        and query.endswith('"')
    ):

        # Remove double quotes
        phrase = query[1:-1].lower()


        # Create PhraseSearch object
        phrase_search = (
            phrase_function.PhraseSearch(
                documents
            )
        )


        # Search exact phrase
        phrase_results = (
            phrase_search.search(
                phrase
            )
        )


        # Give matching documents score 1
        for filename in phrase_results:

            results[filename] = 1


    # --------------------------------
    # CREATE EMPTY RESULTS
    # --------------------------------

    results = {}

    for filename in documents:

        results[filename] = 0


    # --------------------------------
    # CREATE CACHE KEY
    # --------------------------------

    cache_key = query.lower().strip()


    # --------------------------------
    # CHECK QUERY CACHE
    # --------------------------------

    cached_results = query_cache.get(
        cache_key
    )


    # =================================
    # CACHE HIT
    # =================================

    if cached_results is not None:

        print("\nCache HIT ⚡")

        top_results = cached_results


    # =================================
    # CACHE MISS
    # =================================

    else:

        print("\nCache MISS")


        # --------------------------------
        # CHOOSE SEARCH / RANKING METHOD
        # --------------------------------


        # =================================
        # 1. PHRASE SEARCH
        # =================================

        if (
            query.startswith('"')
            and query.endswith('"')
        ):

            print("\nUsing Phrase Search...")

            phrase = query[1:-1].lower()

            phrase_search = (
                phrase_function.PhraseSearch(
                    documents
                )
            )

            phrase_results = phrase_search.search(
                phrase
            )

            for filename in phrase_results:

                results[filename] = 1


        # =================================
        # 2. BOOLEAN AND
        # =================================

        elif " AND " in query.upper():

            print("\nUsing Boolean AND search...")

            parts = query.upper().split(
                " AND "
            )

            words = []

            for part in parts:

                words.extend(
                    preprocess_text(part)
                )


            candidates = boolean_search.and_search(
                words
            )

            print(
                "\nCandidate documents:",
                candidates
            )


            # BM25 ranking
            for filename in candidates:

                score = bm25.calculate_score(
                    words,
                    filename
                )

                results[filename] = score


        # =================================
        # 3. BOOLEAN OR
        # =================================

        elif " OR " in query.upper():

            print("\nUsing Boolean OR search...")

            parts = query.upper().split(
                " OR "
            )

            words = []

            for part in parts:

                words.extend(
                    preprocess_text(part)
                )


            candidates = boolean_search.or_search(
                words
            )

            print(
                "\nCandidate documents:",
                candidates
            )


            # BM25 ranking
            for filename in candidates:

                score = bm25.calculate_score(
                    words,
                    filename
                )

                results[filename] = score


        # =================================
        # 4. BOOLEAN NOT
        # =================================

        elif " NOT " in query.upper():

            print("\nUsing Boolean NOT search...")

            parts = query.upper().split(
                " NOT "
            )


            include_words = preprocess_text(
                parts[0]
            )

            exclude_words = preprocess_text(
                parts[1]
            )


            if include_words and exclude_words:

                candidates = (
                    boolean_search.not_search(
                        include_words[0],
                        exclude_words[0]
                    )
                )


                print(
                    "\nCandidate documents:",
                    candidates
                )


                # BM25 ranking
                for filename in candidates:

                    score = bm25.calculate_score(
                        include_words,
                        filename
                    )

                    results[filename] = score


        # =================================
        # 5. SINGLE WORD → TF-IDF
        # =================================

        elif len(query_words) == 1:

            print("\nUsing TF-IDF ranking...")

            word = query_words[0]


            if word in inverted_index:

                for filename in inverted_index[word]:

                    score = tfidf.calculate_tf_idf(
                        word,
                        filename
                    )

                    results[filename] += score


        else:

            # --------------------------------
            # MULTI-WORD → HYBRID SEARCH
            # --------------------------------

            print(
                "\nUsing Hybrid BM25 + Semantic ranking..."
            )


            # --------------------------------
            # CANDIDATE RETRIEVAL
            # --------------------------------

            candidates = (
                candidate_retrieval.get_candidates(
                    query_words
                )
            )

            print(
                "\nCandidate documents:",
                candidates
            )


            # --------------------------------
            # HYBRID RANKING
            # --------------------------------

            hybrid_scores = hybrid_search.search(
                query_words,
                query,
                documents,
                candidates
            )


            # --------------------------------
            # STORE RESULTS
            # --------------------------------

            for filename, score in hybrid_scores.items():

                results[filename] = score

        # --------------------------------
        # TOP-K
        # --------------------------------

        top_results = top_k.get_top_k(
            results
        )


        # --------------------------------
        # SAVE RESULTS TO CACHE
        # --------------------------------

        query_cache.set(
            cache_key,
            top_results
        )
            
    
    # --------------------------------
    # DISPLAY RESULTS
    # --------------------------------

    print("\nSearch Results:")

    rank = 1

    for score, filename in top_results:

        print(
            f"{rank}. {filename} - Score: {score:.4f}"
        )

        rank += 1

    # --------------------------------
    # CACHE STATISTICS
    # --------------------------------

    stats = query_cache.stats()

    print("\nCache Statistics:")

    print(
        "Cache size:",
        stats["size"]
    )

    print(
        "Cache hits:",
        stats["hits"]
    )

    print(
        "Cache misses:",
        stats["misses"]
    )

    print(
        "Cache hit rate:",
        f"{stats['hit_rate']:.2f}%"
    )
