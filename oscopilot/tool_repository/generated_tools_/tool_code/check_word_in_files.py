def check_word_in_files(file_paths, target_word):
    """
    Check if a specific word is present in each text file.

    Args:
        file_paths (list): List of file paths to check.
        target_word (str): The word to search for in the text files.

    Returns:
        list: A list of tuples where each tuple contains the file path and a boolean indicating if the word was found.
    """
    word_found_list = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                word_found = target_word in content
                word_found_list.append((file_path, word_found))
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            word_found_list.append((file_path, False))
    
    return word_found_list