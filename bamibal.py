import re  # Import regular expression module for pattern matching and substitution
import os  # Import operating system module for file and directory operations
from pathlib import Path  # Import Path class from pathlib module for path manipulation
import time  # Import time module for performance measurement
import psutil  # Import psutil module for system and process utilities

def process_files(input_folder_path, output_folder_path):
    # Record start time for performance measurement
    start_time = time.perf_counter()
    
    # Get initial memory usage of the process
    start_memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    
    # Initialize file count
    file_count = 0

    # Create Path objects for input and output folders
    input_folder = Path(input_folder_path)
    output_folder = Path(output_folder_path)

    # Check if input folder exists
    if not input_folder.exists():
        print(f"Input folder {input_folder} does not exist.")
        return
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Define regular expression pattern for matching
    pattern = re.compile(r'(\d+),(\d+)(?![\s,])')   

    # Iterate through files in the input folder
    for input_file in input_folder.glob('*'):
        # Check if the item is a file
        if input_file.is_file():
            # Define the path for the output file
            output_file_path = output_folder / (input_file.stem + '_output' + input_file.suffix)

            try:
                # Open input file for reading and output file for writing
                with input_file.open('r', encoding='utf-8') as infile, \
                        output_file_path.open('w', encoding='utf-8') as outfile:
                    # Iterate through lines in the input file
                    for line in infile:
                        # Substitute matched pattern with desired format
                        line = pattern.sub(r'\1.\2', line)
                        # Replace commas with semicolons
                        line = line.replace(',', ';')
                        # Write modified line to output file
                        outfile.write(line)
                
                # Increment file count upon successful processing
                file_count += 1
            except Exception as e:
                # Print error message if an exception occurs during processing
                print(f"An error occurred with {input_file.name}: {e}")

    # Calculate elapsed time for processing
    elapsed_time = time.perf_counter() - start_time
    
    # Get final memory usage of the process
    end_memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    
    # Calculate memory used during processing
    memory_used = end_memory - start_memory

    # Print summary of processing
    print(f"Processed {file_count} files in {elapsed_time:.6f} seconds.")
    print(f"Memory used: {memory_used:.2f} MB.")

# Example usage:
input_folder_path = 'input_folder'
output_folder_path = 'output_folder'
process_files(input_folder_path, output_folder_path)
