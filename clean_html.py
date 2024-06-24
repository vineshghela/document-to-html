import re
import os

def clean_html(input_file, output_file):
    # Read the input HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove id attributes from all elements
    cleaned_content = re.sub(r'\s+id\s*=\s*"[^"]*"', '', content)

    # Remove empty elements like <td></td>
    cleaned_content = re.sub(r'<([a-zA-Z0-9]+)\s*>\s*</\1>', '', cleaned_content)

    # Remove content within curly braces and any other content within {}
    cleaned_content = re.sub(r'{[^{}]*}', '', cleaned_content)
    html_comment_pattern = r'<!-- -->'
    cleaned_content = re.sub(html_comment_pattern, '', cleaned_content)

    # Save the cleaned content to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    
    os.remove(input_file)

# Define the input and output file names
input_file = 'output.html'
output_file = 'output_cleaned.html'

# Call the function to clean the HTML file
clean_html(input_file, output_file)
