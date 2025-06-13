import os

def generate_sitemap(directory, output_file):
    with open(output_file, 'w') as sitemap:
        sitemap.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sitemap.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    sitemap.write(f'  <url>\n    <loc>https://github.com/bizcircle2/healthmedic/blob/main/{relative_path}</loc>\n  </url>\n')
        sitemap.write('</urlset>\n')

generate_sitemap('.', 'sitemap.xml')
