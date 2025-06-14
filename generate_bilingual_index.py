import os
from googletrans import Translator
from opencc import OpenCC
import time

cc = OpenCC('s2t')  # Simplified Chinese to Traditional
translator = Translator()

def is_displayable(name):
    return not name.startswith('.') and not name.startswith('__')

def display_name(name):
    # If bilingual: hyphenated
    if '-' in name:
        zh, en = name.split('-', 1)
        zh_trad = cc.convert(zh)
        return f"{zh} ({zh_trad}) ({en})"
    # Otherwise: auto-translate English to Chinese
    # (Google Translate sometimes rate-limits, so add a short delay)
    try:
        translated = translator.translate(name, src='en', dest='zh-cn').text
        time.sleep(0.2)  # Avoid rate limit
    except Exception as e:
        translated = name  # fallback
    zh_trad = cc.convert(translated)
    return f"{translated} ({zh_trad}) ({name})"

items = [f for f in os.listdir('.') if is_displayable(f)]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head><meta charset="UTF-8"><title>健康醫藥 - HealthMedic</title></head><body>\n')
    f.write('<h1>健康醫藥站點導航 / HealthMedic Site Map</h1>\n<ul>\n')
    for item in items:
        if os.path.isdir(item):
            f.write(f'  <li><a href="{item}/">{display_name(item)}/</a></li>\n')
        else:
            f.write(f'  <li><a href="{item}">{display_name(item)}</a></li>\n')
    f.write('</ul>\n</body></html>\n')