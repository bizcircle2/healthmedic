import os

def scan_dir(path, rel_path=""):
    items = []
    for name in sorted(os.listdir(path)):
        if name.startswith('.'):
            continue  # skip hidden files/folders
        full_path = os.path.join(path, name)
        rel_item_path = os.path.join(rel_path, name) if rel_path else name
        if os.path.isdir(full_path):
            items.append({
                "type": "dir",
                "name": name,
                "rel_path": rel_item_path + '/',
                "children": scan_dir(full_path, rel_item_path)
            })
        else:
            items.append({
                "type": "file",
                "name": name,
                "rel_path": rel_item_path
            })
    return items

def render_tree(items):
    html = "<ul>\n"
    for item in items:
        if item["type"] == "dir":
            html += f'  <li><details><summary>📁 <a href="{item["rel_path"]}">{item["name"]}/</a></summary>\n'
            html += render_tree(item["children"])
            html += "  </details></li>\n"
        else:
            html += f'  <li>📄 <a href="{item["rel_path"]}">{item["name"]}</a></li>\n'
    html += "</ul>\n"
    return html

tree = scan_dir(".")

with open("index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Project Index</title>
  <style>
    body { font-family: Arial, sans-serif; }
    ul { list-style-type: none; }
    summary { cursor: pointer; }
    a { text-decoration: none; color: #0055aa; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Project Directory Index</h1>
""")
    f.write(render_tree(tree))
    f.write("""
</body>
</html>
""")