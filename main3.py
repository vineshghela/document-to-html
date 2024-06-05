import pytesseract
from PIL import Image
import re

# Path to the image file
image_path = 'test_pic.webp'

# Use pytesseract to extract text from the image
extracted_text = pytesseract.image_to_string(Image.open(image_path))

# Function to analyze text and apply HTML formatting
def format_to_html(text):
    # Regular expression pattern to identify headings and bold text
    heading_pattern = r'^[A-Z\s]+(?:\n[A-Z\s]+)*$'  # Matches lines with only uppercase letters and spaces
    bold_pattern = r'\b[A-Z\s]+\b'  # Matches words in all caps

    html_content = '<html><body>'
    in_heading = False

    for line in text.split('\n'):
        # Check if the line is a heading
        if re.match(heading_pattern, line):
            if in_heading:
                html_content += '</h1>'
            html_content += f'<h1><strong>{line}</strong>'
            in_heading = True
        # Check if the line contains bold text
        elif re.search(bold_pattern, line):
            html_content += f'<p><strong>{line}</strong></p>'
        else:
            html_content += f'<p>{line}</p>'

    if in_heading:
        html_content += '</h1>'

    html_content += '</body></html>'
    return html_content

# Convert the extracted text to HTML format with advanced formatting
html_content = format_to_html(extracted_text)

# Save the HTML content to a file
with open('output.html', 'w') as f:
    f.write(html_content)

print("HTML content saved to output.html")
