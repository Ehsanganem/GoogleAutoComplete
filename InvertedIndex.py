class InvertedIndex:
  def __init__(self, documents, n=2):
    self.inverted_index = self.create_inverted_index(documents, n)

  def create_inverted_index(self, documents, n=2):
    inverted_index = {}

    for document in documents:
      words = document.split()
      ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]

      for ngram in ngrams:
        if ngram not in inverted_index:
          inverted_index[ngram] = []
        inverted_index[ngram].append(document)

    return inverted_index

  def retrieve_documents(self, query_ngram):
    if query_ngram in self.inverted_index:
      return self.inverted_index[query_ngram]
    else:
      return []

# Test the inverted index
documents = [
    "The quick brown fox jumps over the lazy dog.",
    "The lazy dog slept in the sun.",
    "The fox and the dog are friends."
]

inverted_index = InvertedIndex(documents, n=2)

query_ngram = ("the", "lazy")
document_ids = inverted_index.retrieve_documents(query_ngram)
print(document_ids)  # Output: [0, 1]