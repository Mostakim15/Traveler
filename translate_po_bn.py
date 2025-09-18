import os
import polib
from googletrans import Translator

PO_PATH = 'locale/bn/LC_MESSAGES/django.po'
OUTPUT_PATH = 'locale/bn/LC_MESSAGES/django.po'

def ensure_dir_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    ensure_dir_exists(OUTPUT_PATH)
    po = polib.pofile(PO_PATH)
    translator = Translator()
    total = len([e for e in po if not e.msgstr and e.msgid.strip()])
    count = 0

    for entry in po:
        if not entry.msgstr and entry.msgid.strip():
            try:
                translation = translator.translate(entry.msgid, src='en', dest='bn').text
                entry.msgstr = translation
                count += 1
                print(f"[{count}/{total}] Translated: '{entry.msgid}' -> '{translation}'")
            except Exception as e:
                print(f"Error translating '{entry.msgid}': {e}")

    po.save(OUTPUT_PATH)
    print(f"Translation complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
