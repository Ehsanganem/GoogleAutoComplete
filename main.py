from LoaderModule import LoaderModule
import timeit
from ScoreFunction import sentences_score

def main():
    loader = LoaderModule()

    # Load the reverse index from a preprocessed file
    print("Loading reverse index from MessagePack...")
    loader.load_reverse_index_from_msgpack('reverse_index.msgpack')

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

        # Search for matching original strings, file names, and line numbers
        matching_results = search()

        # If there are no matches, inform the user
        if not matching_results:
            print("No matching results found.")
            continue

        # Rank the results using the sentences_score function
        scored_results = [(file_name, string, line_num, sentences_score(user_input, string))
                          for file_name, string, line_num in matching_results]

        # Sort results by score in descending order
        scored_results.sort(key=lambda x: x[3], reverse=True)

        # Display the search duration
        print(f"Search completed in {search_duration:.4f} seconds.")

        # Display the top 5 results
        print("\nTop 5 matches:")
        for i, (file_name, string, line_num, score) in enumerate(scored_results[:5]):
            print(f"{i+1}. Score: {score} - File: {file_name} - Line: {line_num} - String: {string}")

        print("\n")

if __name__ == "__main__":
    main()
