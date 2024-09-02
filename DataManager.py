from LoaderModule import LoaderModule
"""
this script is used to create the initial data base
as the file is over 4.4 gigs we wont upload it to the github
"""
if __name__ == "__main__":
    loader = LoaderModule()

    # Load and preprocess text files from the specified directory
    print("Starting to load and process text files...")
    reverse_index = loader.load_text_files('Text Archive')

    # Check if any files were processed
    if not loader.processed_files:
        print("No files were processed. Please check the directory path and file extensions.")

    # Save the reverse index to a JSON file
    print("Saving the reverse index as JSON...")
    loader.save_index_json('reverse_index.json')

    # Print the reverse index to verify its contents
    # print("Loaded Reverse Index Contents:")
    # for word, file_metadata_list in reverse_index.index.items():
    #     print(f"Word: '{word}'")
    #     for metadata in file_metadata_list:
    #         print(f"  File: {metadata.file_name}, Strings: {metadata.strings}")

    print("Processing completed successfully.")


