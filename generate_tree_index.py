import os

# Set the root directory to index (current directory)
INDEX_ROOT = "."

# Names and patterns to exclude
EXCLUDE_NAMES = {"env", "env-env", "venv", "__pycache__", ".git", ".github", ".vscode", ".env", "Include", "Lib", "Scripts", "site-packages"}
EXCLUDE_PATTERNS = ["env", "venv", "__pycache__", ".dist-info", ".egg-info"]

def should_exclude(name):
    lname = name.lower()
    if lname in EXCLUDE_NAMES:
        return True
    for pat in EXCLUDE_PATTERNS:
        if pat in lname:
            return True
    if not all(ord(c) < 128 for c in name):  # Exclude non-ASCII
        return True
    if lname.startswith('.'):
        return True
    return False

def scan_dir(path, rel_path=""):
    items = []
    for name in sorted(os.listdir(path)):
        if should_exclude(name):
            continue
        full_path = os.path.join(path, name)
        rel_item_path = os.path.join(rel_path, name) if rel_path else name
        if os.path.isdir(full_path):
            children = scan_dir(full_path, rel_item_path)
            if children:
                items.append({
                    "type": "dir",
                    "name": name,
                    "rel_path": rel_item_path + '/',
                    "children": children
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
            html += f'  <li><details><summary>📁 <a href="{item["rel_path"].replace(os.sep, "/")}">{item["name"]}/</a></summary>\n'
            html += render_tree(item["children"])
            html += "  </details></li>\n"
        else:
            html += f'  <li>📄 <a href="{item["rel_path"].replace(os.sep, "/")}">{item["name"]}</a></li>\n'
    html += "</ul>\n"
    return html

tree = scan_dir(INDEX_ROOT)

with open("index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>HealthMedic Site Map</title>
  <style>
    body { font-family: Arial, sans-serif; }
    ul { list-style-type: none; }
    summary { cursor: pointer; }
    a { text-decoration: none; color: #0055aa; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>HealthMedic Site Map</h1>
""")
    f.write(render_tree(tree))
    f.write("""
</body>
</html>
""")