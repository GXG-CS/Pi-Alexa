def create_files_from_sentences(input_file_path, output_dir, repeat_count=10):
    """
    Reads sentences from an input file and creates multiple files from each sentence.
    Each file will be numbered sequentially, and each sentence will be repeated in 'repeat_count' files.
    
    :param input_file_path: Path to the input text file containing the sentences.
    :param output_dir: Directory where the output files will be saved.
    :param repeat_count: The number of files to create for each sentence.
    """
    import os

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the content of the input file
    with open(input_file_path, 'r') as file:
        sentences = file.readlines()

    # Initialize a counter for the output file names
    file_counter = 1

    # Iterate over each line (sentence) in the input file
    for sentence in sentences:
        # Clean up the sentence
        sentence = sentence.strip()
        # Skip any empty lines
        if not sentence:
            continue
        # Write the sentence to 'repeat_count' number of files
        for _ in range(repeat_count):
            output_file_path = os.path.join(output_dir, f"{file_counter}.txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(sentence + '\n')
            file_counter += 1

# Example usage
input_file_path = 'text_total.txt'  
output_dir = 'text_A'  
create_files_from_sentences(input_file_path, output_dir)
