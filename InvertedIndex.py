import concurrent.futures
from collections import defaultdict
from fuzzywuzzy import fuzz


class InvertedIndex:
    def __init__(self, documents, n=2):
        self.inverted_index = self.create_inverted_index(documents, n)

    def create_inverted_index(self, documents, n=2):
        inverted_index = defaultdict(set)  # Use a set instead of a list for faster lookups

        for document in documents:
            words = document.split()
            ngrams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]

            for ngram in ngrams:
                inverted_index[ngram].add(document)

        return inverted_index

    import concurrent.futures

    def retrieve_documents(self, query_ngram, threshold=80):
        matched_documents = set()  # Use a set to avoid duplicates and for faster operations
        query_ngram_str = ' '.join(query_ngram)

        def match_ngrams(ngram_docs_pair):
            ngram, docs = ngram_docs_pair
            ngram_str = ' '.join(ngram)
            if fuzz.partial_ratio(query_ngram_str, ngram_str) >= threshold:
                return docs
            return set()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(match_ngrams, self.inverted_index.items())

        for docs in results:
            matched_documents.update(docs)

        return list(matched_documents)
