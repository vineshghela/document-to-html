import re
import os

def clean_markdown(input_file, output_file):
    # Read the input markdown file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the patterns to remove
    end_pattern = r'\(#_Toc\d+\)'
    start_pattern = r'\[\]{#_Toc\d+ \.anchor}'
    newline_escape_pattern = r'\(\\l\)'
    

    # Remove the patterns
    cleaned_content = re.sub(end_pattern, '', content)
    cleaned_content = re.sub(start_pattern, '', cleaned_content)
    cleaned_content = re.sub(newline_escape_pattern, '', cleaned_content)

    # Save the cleaned content to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    # Delete the original file
    os.remove(input_file)

# Define the input and output file names
input_file = 'output.md'
output_file = 'output_cleaned.md'

# Call the function to clean the markdown file
clean_markdown(input_file, output_file)
