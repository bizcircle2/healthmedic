import os

def get_display_names(filename):
    name, ext = os.path.splitext(filename)
    parts = name.split('-')
    if len(parts) == 2:
        chinese, english = parts
        return f"{chinese}{ext} / {english}{ext}"
    else:
        return filename

def walk_dir(root, parent_path=""):
    html = "<ul>"
    for entry in sorted(os.listdir(os.path.join(root, parent_path)), key=lambda x: x.lower()):
        if entry.startswith('.'):
            continue
        full_path = os.path.join(parent_path, entry)
        abs_path = os.path.join(root, full_path)
        if os.path.isdir(abs_path):
            html += f"<li><strong>{entry}/</strong>{walk_dir(root, full_path)}</li>"
        elif entry.endswith('.html'):
            display = get_display_names(entry)
            url = os.path.join(parent_path, entry).replace("\\", "/")
            html += f'<li><a href="{url}">{display}</a></li>'
    html += "</ul>"
    return html

html_tree = walk_dir(".")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HealthMedic Bilingual Sitemap</title>
    <style>
        ul {{ list-style-type: none; }}
        li {{ margin-left: 1em; }}
        strong {{ cursor: pointer; }}
    </style>
</head>
<body>
    <h1>HealthMedic Bilingual Sitemap / 双语网站地图</h1>
    {html_tree}
</body>
</html>
""")