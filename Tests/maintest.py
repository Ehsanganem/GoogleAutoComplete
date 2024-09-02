import os

from InvertedIndex import InvertedIndex
from LoaderModule import LoaderModule


def main():
    # Set the directory to the Tests folder
    directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Text Archive')

    # Create an instance of the LoaderModule
    processor = LoaderModule()

    # Define the path to the preprocessed JSON file
    preprocessed_filepath = os.path.join(directory, 'preprocessed_data.json')

    # Load the preprocessed data if it exists, otherwise process the text files
    if os.path.exists(preprocessed_filepath):
        print(f"Loading preprocessed data from '{preprocessed_filepath}'...")
        documents = processor.load_data(preprocessed_filepath)
        print("Preprocessed data loaded.")
    else:
        print("Preprocessed data not found. Loading and preprocessing text files...")
        documents = processor.load_text_files(directory)
        print("Text files loaded and preprocessed.")

        # Save the preprocessed data to a file for future use
        print(f"Saving preprocessed data to '{preprocessed_filepath}'...")
        processor.save_data(preprocessed_filepath)
        print("Preprocessed data saved.")

    # # Debugging: Print the loaded/preprocessed documents
    # print("\nPreprocessed Documents:")
    # for doc in documents:
    #     print(f"{doc['preprocessed']} (File: {doc['source_file']}, Line: {doc['line_number']})")

    # Create an inverted index based on preprocessed text
    inverted_index = InvertedIndex([doc['preprocessed'] for doc in documents])

    # Debugging: Print the inverted index to verify it's correct
    # print("\nInverted Index:")
    # for ngram, docs in inverted_index.inverted_index.items():
    #     print(f"N-gram: {ngram} -> Documents: {docs}")

    # Perform a search
    while True:
        print("\nEnter a search query (or type 'exit' to quit):")
        query = input().strip()
        if query.lower() == 'exit':
            print("Exiting search.")
            break
        if not query:
            print("Empty query. Please enter a valid search term.")
            continue

        print(f"Searching for '{query}'...")
        search_results = processor.search(query, inverted_index, top_n=5)

        if not search_results:
            print("No matching results found.")
            continue

        print(f"\nTop {len(search_results)} Results:")
        for result, score in search_results:
            print(f"Score: {score:.2f}")
            print(f"Document: {result}")
            print("-" * 40)

if __name__ == "__main__":
    main()