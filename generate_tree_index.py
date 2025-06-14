import os

<<<<<<< HEAD
def walk_dir(root):
    tree = []
    for entry in sorted(os.listdir(root)):
        path = os.path.join(root, entry)
        # Exclude .git, .vscode, etc.
        if entry.startswith("."):
            continue
        if os.path.isdir(path):
            tree.append({
                'type': 'dir',
                'name': entry,
                'children': walk_dir(path)
            })
        elif entry.endswith('.html'):
            tree.append({
                'type': 'file',
                'name': entry,
                'path': os.path.relpath(path)
            })
    return tree

def render_tree(tree, parent_path=""):
    html = "<ul>"
    for node in tree:
        if node['type'] == 'dir':
            html += f"<li><strong>{node['name']}/</strong>{render_tree(node['children'], os.path.join(parent_path, node['name']))}</li>"
        else:
            url = os.path.join(parent_path, node['name']).replace("\\", "/")
            html += f'<li><a href="{url}">{node["name"]}</a></li>'
    html += "</ul>"
    return html

tree = walk_dir(".")
html_tree = render_tree(tree)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HealthMedic Site Map</title>
    <style>
        ul {{ list-style-type: none; }}
        li {{ margin-left: 1em; }}
        strong {{ cursor: pointer; }}
    </style>
</head>
<body>
    <h1>HealthMedic Site Map</h1>
    {html_tree}
=======
# Set the root directory you want to index (change this if needed)
INDEX_ROOT = os.path.join(os.path.dirname(__file__), "your_content_folder")  # e.g., "src" or "docs" or "public"
# If you want the current folder, use "."
INDEX_ROOT = "."

# Names and patterns to exclude
EXCLUDE_NAMES = {"env", "env-env", "venv", "__pycache__", ".git", ".github", ".vscode"}
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
>>>>>>> master
</body>
</html>
""")