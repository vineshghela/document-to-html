import os
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from jinja2 import Template

def read_word_file(file_path):
    try:
        doc = Document(file_path)
        content = []

        # Iterate through all elements (paragraphs and tables) in the document
        for element in doc.element.body:
            if element.tag.endswith('tbl'):
                table = Table(element, doc)
                formatted_table = format_table(table)
                if formatted_table.strip():  # Ensure non-empty table
                    content.append(formatted_table)
                    content.append('<br>')  # Add a break after each table
            elif element.tag.endswith('p'):
                paragraph = Paragraph(element, doc)
                if paragraph.text.strip():
                    formatted_paragraph = format_paragraph(paragraph)
                    if formatted_paragraph.strip():  # Ensure non-empty paragraph
                        content.append(formatted_paragraph)

        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def format_table(table):
    table_html = '<table style="border-collapse: collapse; border: 1px solid black; background-color: lightgray; width:100%;">'
    merged_cells = set()

    for row in table.rows:
        table_html += '<tr>'
        for cell in row.cells:
            cell_text = cell.text.strip()
            span = 1

            if cell._element.grid_span is not None:
                span = int(cell._element.grid_span)
                cell_html = f'<td colspan="{span}" style="border: 1px solid black; padding: 5px;">{cell_text}</td>'
            else:
                cell_html = f'<td style="border: 1px solid black; padding: 5px;">{cell_text}</td>'

            # Ensure we do not duplicate merged cells
            if cell_text not in merged_cells or span == 1:
                table_html += cell_html
                if span > 1:
                    merged_cells.add(cell_text)

        table_html += '</tr>'

    table_html += '</table>'
    return table_html

def format_paragraph(paragraph):
    formatted_text = ''
    all_bold = all(run.bold for run in paragraph.runs if run.text.strip())  # Check if all runs are bold

    for run in paragraph.runs:
        text = run.text
        if run.bold:
            text = f'<strong>{text}</strong>'
        if run.italic:
            text = f'<em>{text}</em>'
        if run.underline:
            text = f'<u>{text}</u>'
        formatted_text += text

    # Debugging: Print the style name of each paragraph
    # print(f"Paragraph text: '{paragraph.text}' | Style: '{paragraph.style.name}'")

    if (paragraph.style.name.startswith('Heading') or all_bold) and formatted_text.strip():
        # Center align all headings and use <h1> tag
        formatted_text = f'<h1 style="text-align: center;">{formatted_text}</h1>'
    elif formatted_text.strip():
        formatted_text = f'<p>{formatted_text}</p>'
    return formatted_text

def create_jinja2_template(content, template_path, filename):
    try:
        template_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{filename}}</title>
        </head>
        <body>
            {% for element in content %}
                {{ element|safe }}
            {% endfor %}
        </body>
        </html>
        """
        template = Template(template_content)
        rendered_content = template.render(content=content)

        with open(template_path, 'w') as f:
            f.write(rendered_content)

        print(f"Jinja2 template created successfully at {template_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.docx'):
            print(filename)
            file_path = os.path.join(input_folder, filename)
            content = read_word_file(file_path)
            
            if content:
                output_file_name = f"{os.path.splitext(filename)[0]}.html"
                template_path = os.path.join(output_folder, output_file_name)
                create_jinja2_template(content, template_path, filename)
            else:
                print(f"Failed to read the file: {filename}")

input_folder = 'files'
output_folder = 'output'

process_files(input_folder, output_folder)
