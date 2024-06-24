import fitz  # PyMuPDF
import re
from jinja2 import Template
import os

def read_pdf_file(file_path):
    try:
        doc = fitz.open(file_path)
        content = []
        list_stack = []  # Stack to handle nested lists
        is_contents_section = False
        contents_table = []
        paragraph_buffer = []  # Buffer to collect related paragraphs

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")

            print(f"Processing page {page_num + 1}")  # Debugging statement

            for line in text.split('\n'):
                line = line.strip()
                if line:
                    if re.search(r'\bCONTENTS?\b', line.upper()):
                        is_contents_section = True
                        contents_table.append("<table>")
                        continue

                    if is_contents_section:
                        if not re.match(r'^\d+\.\s', line):
                            is_contents_section = False
                            contents_table.append("</table>")
                            content.extend(contents_table)
                            contents_table = []

                    if is_contents_section:
                        formatted_line = format_contents_line(line)
                        contents_table.append(formatted_line)
                    else:
                        if re.match(r'^[0-9]+\.\s', line):
                            # Line starts with a number followed by a period and a space
                            line = f"<b>{line}</b>"
                        paragraph_buffer.append(line)

                elif paragraph_buffer:
                    # End of a paragraph block
                    formatted_paragraph = format_paragraph(paragraph_buffer, list_stack)
                    if formatted_paragraph.strip():  # Ensure non-empty paragraph
                        print(f"Formatted paragraph: {formatted_paragraph}")  # Debugging statement
                        content.append(formatted_paragraph)
                    paragraph_buffer = []

        # Handle any remaining paragraphs
        if paragraph_buffer:
            formatted_paragraph = format_paragraph(paragraph_buffer, list_stack)
            if formatted_paragraph.strip():  # Ensure non-empty paragraph
                content.append(formatted_paragraph)

        # Close any remaining open lists
        while list_stack:
            list_type = list_stack.pop()
            content.append(f'</{list_type}>')

        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def format_contents_line(line):
    parts = re.split(r'(.{2,})', line)
    if len(parts) >= 3:
        title = parts[0].strip()
        page = parts[-1].strip()
        return f'<tr><td>{title}</td><td style="text-align: right;">{page}</td></tr>'
    return f'<tr><td colspan="2">{line}</td></tr>'

def format_paragraph(paragraphs, list_stack):
    formatted_text = "<p>" + " ".join(paragraphs) + "</p>"
    list_type = None

    # Handling bullets and numbering
    if re.match(r'^\(\d+\)', paragraphs[0]):
        list_type = 'ol'

    if list_type:
        if not list_stack or list_stack[-1] != list_type:
            if list_stack:
                closing_list_type = list_stack.pop()
                formatted_text = f'</{closing_list_type}>{formatted_text}'
            list_stack.append(list_type)
            formatted_text = f'<{list_type}><li>{formatted_text}</li>'
        else:
            formatted_text = f'<li>{formatted_text}</li>'
    else:
        if list_stack:
            closing_list_type = list_stack.pop()
            formatted_text = f'</{closing_list_type}>{formatted_text}'

    # Ensure the numbering format (e.g., "(1)", "(2)") is preserved
    numbered_list_match = re.match(r'^\(\d+\)', paragraphs[0])
    if numbered_list_match:
        formatted_text = f'{numbered_list_match.group(0)} {formatted_text[len(numbered_list_match.group(0)):].strip()}'

    return formatted_text.strip()

def create_jinja2_template(content, template_path, filename):
    try:
        template_content = """
<!DOCTYPE html>
<html>
<head>
    <title>{{filename}}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        p {
            margin: 0 0 10px;
        }
        b {
            display: block;
            margin: 10px 0;
            font-weight: bold;
        }
    </style>
</head>
<body>
    {% for element in content %}
    {% if element.strip() %}
    {{ element|safe }}
    {% endif %}
    {% endfor %}
</body>
</html>
"""
        template = Template(template_content)
        rendered_content = template.render(content=content, filename=filename)
        
        with open(template_path, 'w') as f:
            f.write(rendered_content)

        print(f"Jinja2 template created successfully at {template_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            print(f"Processing file: {filename}")
            file_path = os.path.join(input_folder, filename)
            content = read_pdf_file(file_path)
            
            if content:
                output_file_name = f"{os.path.splitext(filename)[0]}.html"
                template_path = os.path.join(output_folder, output_file_name)
                create_jinja2_template(content, template_path, filename)
            else:
                print(f"Failed to read the file: {filename}")

input_folder = 'files'
output_folder = 'output-pdf'
process_files(input_folder, output_folder)
