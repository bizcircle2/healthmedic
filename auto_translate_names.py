import os
from googletrans import Translator

translator = Translator()

def contains_chinese(text):
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)

def translate_to_chinese(text):
    try:
        result = translator.translate(text, src='en', dest='zh-cn')
        return result.text
    except Exception as e:
        print(f"Translation failed for '{text}': {e}")
        return text

def process_directory(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # Process directories (folders)
        for dirname in dirnames[:]:
            if '-' not in dirname and not contains_chinese(dirname):
                chinese = translate_to_chinese(dirname)
                new_dirname = f"{chinese}-{dirname}"
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                print(f"Renaming folder: {old_path} -> {new_path}")
                os.rename(old_path, new_path)
                # Update dirnames in-place so os.walk continues correctly
                dirnames[dirnames.index(dirname)] = new_dirname
        # Process files
        for filename in filenames:
            if filename.endswith('.html') and '-' not in filename and not contains_chinese(filename):
                name, ext = os.path.splitext(filename)
                chinese = translate_to_chinese(name)
                new_filename = f"{chinese}-{name}{ext}"
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                print(f"Renaming file: {old_path} -> {new_path}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    print("Starting auto-translation and renaming...")
    process_directory(".")
    print("Done! Review changes, then re-run your index script.")