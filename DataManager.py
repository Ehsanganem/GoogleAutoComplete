from LoaderModule import LoaderModule

"""
This script is used to create the initial database.
As the file is over 4.4 GB, we won't upload it to the GitHub repository.
"""

if __name__ == "__main__":
    loader = LoaderModule()

    # Load and preprocess text files from the specified directory
    print("Starting to load and process text files...")
    reverse_index = loader.load_text_files('Text Archive')

    # Check if any files were processed
    if not loader.processed_files:
        print("No files were processed. Please check the directory path and file extensions.")

    # Save the reverse index to a MessagePack file
    print("Saving the reverse index as MessagePack...")
    loader.save_index_msgpack('reverse_index.msgpack')

    print("Processing completed successfully.")
