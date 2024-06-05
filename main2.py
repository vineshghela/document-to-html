from docx import Document
from jinja2 import Template

def read_word_file(file_path):
    try:
        doc = Document(file_path)
        content = []
        for paragraph in doc.paragraphs:
            formatted_paragraph = format_paragraph(paragraph)
            content.append(formatted_paragraph)
        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def format_paragraph(paragraph):
    formatted_text = ''
    for run in paragraph.runs:
        text = run.text
        # Check for different styles and convert them accordingly
        if run.bold:
            text = f'<strong>{text}</strong>'
        if run.italic:
            text = f'<em>{text}</em>'
        if run.underline:
            text = f'<u>{text}</u>'
        formatted_text += text
    # Add appropriate tags for headings
    if paragraph.style.name.startswith('Heading'):
        level = int(paragraph.style.name.split()[1])
        formatted_text = f'<h{level}>{formatted_text}</h{level}>'
    else:
        formatted_text = f'<p>{formatted_text}</p>'
    return formatted_text

def create_jinja2_template(content, template_path):
    try:
        template_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Jinja2 Template</title>
        </head>
        <body>
            {% for paragraph in content %}
                {{ paragraph|safe }}
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

file_path = 'file-sample_1MB.docx'
content = read_word_file(file_path)

if content:
    template_path = 'output_template2.html'
    create_jinja2_template(content, template_path)
else:
    print("Failed to read the file.")
