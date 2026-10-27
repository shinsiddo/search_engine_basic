from collections import OrderedDict
from threading import Lock
from time import time


class QueryCache:

    def __init__(self, max_size=100, ttl=300):

        # Maximum number of cached queries
        self.max_size = max_size

        # Cache lifetime in seconds
        self.ttl = ttl

        # OrderedDict allows LRU management
        self.cache = OrderedDict()

        # Thread safety
        self.lock = Lock()

        # Statistics
        self.hits = 0
        self.misses = 0


    # --------------------------------
    # GET FROM CACHE
    # --------------------------------

    def get(self, query):

        with self.lock:

            if query not in self.cache:

                self.misses += 1

                return None


            results, timestamp = self.cache[query]


            # --------------------------------
            # TTL CHECK
            # --------------------------------

            if time() - timestamp > self.ttl:

                del self.cache[query]

                self.misses += 1

                return None


            # --------------------------------
            # MARK AS RECENTLY USED
            # --------------------------------

            self.cache.move_to_end(query)

            self.hits += 1

            return results


    # --------------------------------
    # STORE IN CACHE
    # --------------------------------

    def set(self, query, results):

        with self.lock:

            # If query already exists,
            # remove old version first

            if query in self.cache:

                del self.cache[query]


            # Add newest result
            self.cache[query] = (
                results,
                time()
            )


            # --------------------------------
            # LRU LIMIT
            # --------------------------------

            while len(self.cache) > self.max_size:

                self.cache.popitem(
                    last=False
                )


    # --------------------------------
    # REMOVE ONE QUERY
    # --------------------------------

    def delete(self, query):

        with self.lock:

            if query in self.cache:

                del self.cache[query]


    # --------------------------------
    # CLEAR CACHE
    # --------------------------------

    def clear(self):

        with self.lock:

            self.cache.clear()


    # --------------------------------
    # CACHE STATISTICS
    # --------------------------------

    def stats(self):

        with self.lock:

            total = self.hits + self.misses

            if total == 0:

                hit_rate = 0

            else:

                hit_rate = (
                    self.hits / total
                ) * 100


            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate
            }