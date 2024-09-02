from LoaderModule import LoaderModule
from SearchFiles import search_files
from ScoreFunction import sentences_score
import timeit

import timeit

def main():
    loader = LoaderModule()

    # Load the reverse index from a preprocessed JSON file
    print("Loading reverse index from JSON...")
    loader.load_reverse_index_from_json('reverse_index_full.json')

    while True:
        # Get user input
        user_input = input("Enter a search query (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break

        # Define a small wrapper function for timing
        def search():
            return loader.search(user_input)

        # Time the search using timeit
        search_duration = timeit.timeit(search, number=1)

        # Search for matching original strings and file names
        matching_results = search()

        # If there are no matches, inform the user
        if not matching_results:
            print("No matching results found.")
            continue

        # Rank the results using the sentences_score function
        scored_results = [(file_name, string, sentences_score(user_input, string)) for file_name, string in matching_results]

        # Sort results by score in descending order
        scored_results.sort(key=lambda x: x[2], reverse=True)

        # Display the search duration
        print(f"Search completed in {search_duration:.4f} seconds.")

        # Display the top 5 results
        print("\nTop 5 matches:")
        for i, (file_name, string, score) in enumerate(scored_results[:5]):
            print(f"{i+1}. Score: {score} - File: {file_name} - String: {string}")

        print("\n")

# Run the program
if __name__ == "__main__":
    main()


