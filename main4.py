import pandas as pd

def convert_csv_to_html(file_path):
    df = pd.read_csv(file_path)
    html_content = df.to_html(index=False)

    return html_content

csv_file_path = 'price_list.csv'

html_content = convert_csv_to_html(csv_file_path)

output_file_path = 'price_list.html'
with open(output_file_path, 'w') as f:
    f.write(html_content)

print(f"HTML content saved to {output_file_path}")
