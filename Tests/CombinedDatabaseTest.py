import os
from CombinedDatabase import CombinedDatabase
from LoaderModule import LoaderModule

def main():
    # Set the directory to the Text Archive folder
    directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tests/combineddatatest')

    # Create an instance of the LoaderModule to load documents
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
        processor.save_data(preprocessed_filepath)
        print("Preprocessed data saved.")

    # Initialize the CombinedDatabase with the preprocessed documents
    combined_db = CombinedDatabase([doc['preprocessed'] for doc in documents])

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
        search_results = combined_db.search(query, top_n=5)

        if not search_results:
            print("No matching results found.")
            continue

        print(f"\nTop {len(search_results)} Results:")
        for result in search_results:
            print(f"Document: {result}")
            print("-" * 40)

if __name__ == "__main__":
    main()
