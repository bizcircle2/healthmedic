import os

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
</body>
</html>
""")