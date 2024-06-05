import pypandoc

# Download Pandoc and install it in the venv
pypandoc.download_pandoc()

# Convert DOCX to HTML
output = pypandoc.convert_file('example.docx', 'html', outputfile='example.html')

print(output)
