from Trie import Trie
from InvertedIndex import InvertedIndex

class CombinedDatabase:
    def __init__(self, documents):
        self.trie = Trie()  # Initialize Trie
        self.inverted_index = InvertedIndex(documents)  # Initialize Inverted Index

        # Populate the Trie with words from the documents
        for doc in documents:
            for word in doc.split():
                self.trie.insert(word, doc)

    def search(self, query, top_n=5, threshold=80):
        """Searches for relevant documents using both Trie and Inverted Index."""
        query_words = query.lower().split()

        # Retrieve documents from Trie based on the first word
        possible_documents = set()
        if query_words:
            possible_documents = self.trie.search_prefix(query_words[0])

        # Handle single word queries or n-grams
        if len(query_words) < 2:
            query_ngrams = [tuple(query_words)]
        else:
            query_ngrams = [tuple(query_words[i:i + 2]) for i in range(len(query_words) - 1)]

        # Retrieve documents using inverted index
        retrieved_documents = []
        for ngram in query_ngrams:
            retrieved_documents.extend(self.inverted_index.retrieve_documents(ngram, threshold=threshold))

        # Filter documents found in Trie
        if possible_documents:
            retrieved_documents = [doc for doc in retrieved_documents if doc in possible_documents]

        # Remove duplicates
        retrieved_documents = list(set(retrieved_documents))

        return retrieved_documents[:top_n]
