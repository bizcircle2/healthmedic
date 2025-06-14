import os

# List of exact names to exclude (case-sensitive)
EXCLUDE_NAMES = {
    'env', 'Include', 'Lib', 'site-packages', 'Scripts',
    '__pycache__', 'licenses', 'cli', 'idna', 'pip', '_internal',
    'commands', 'distributions', 'index', 'locations', 'metadata', 'importlib',
    'models', 'network', 'operations', 'build', 'install', 'req', 'resolution',
    'legacy', 'resolvelib', 'utils', 'vcs', '_vendor', 'cachecontrol', 'caches',
    'chardet', 'colorama', 'distlib', 'distro', 'msgpack', 'packaging',
    'pep517', 'in_process', 'pkg_resources', 'platformdirs', 'pygments',
    'filters', 'formatters', 'lexers', 'styles', 'pyparsing', 'diagram',
    'extern', 'rich', 'tenacity', 'tomli', 'contrib', '_securetransport',
    'packages', 'backports', 'util', 'webencodings', 'importlib_resources',
    'jaraco', 'text', 'more_itertools', 'setuptools', '_distutils', 'command',
    'importlib_metadata', '_validate_pyproject', 'emscripten', 'http2'
}

# Exclude if the name matches any of these patterns
EXCLUDE_PATTERNS = (
    '__pycache__',
    '.dist-info',
    '.egg-info'
)

def should_exclude(name):
    if name in EXCLUDE_NAMES:
        return True
    for pat in EXCLUDE_PATTERNS:
        if pat in name:
            return True
    if name.startswith('_'):
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