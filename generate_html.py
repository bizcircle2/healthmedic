import os

root_folder = os.path.dirname(os.path.abspath(__file__))

def find_html_files(base):
    html_files = []
    for dirpath, dirs, files in os.walk(base):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(dirpath, file)
                # Replace backslashes with forward slashes for web compatibility
                rel_path = os.path.relpath(full_path, base).replace("\\", "/")
                html_files.append(rel_path)
    return sorted(html_files)

def make_html_ul(files):
    items = []
    for path in files:
        items.append(f'<li><a href="{path}">{path}</a></li>')
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

def create_index(files):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<html><head><title>HealthMedic Index</title></head><body>\n')
        f.write('<h1>HealthMedic Index</h1>\n')
        f.write(make_html_ul(files))
        f.write('\n</body></html>')

def create_sitemap(files):
    with open('sitemap.html', 'w', encoding='utf-8') as f:
        f.write('<html><head><title>Sitemap</title></head><body>\n')
        f.write('<h1>Sitemap</h1>\n')
        f.write(make_html_ul(files))
        f.write('\n</body></html>')

if __name__ == "__main__":
    html_files = find_html_files(root_folder)
    create_index(html_files)
    create_sitemap(html_files)