# filename: reformat_strings.py
# Usage: python reformat_strings.py

import re
from pathlib import Path
from textwrap import wrap

SRC_DIR = Path("src/planet_overlap")
MAX_LINE = 79

STRING_PATTERN = re.compile(r'(?P<quote>["\']{3}|["\'])(?P<content>.*?)(?P=quote)', re.DOTALL)

def split_long_string(s, max_length=MAX_LINE):
    """Split a string into multiple concatenated strings <= max_length."""
    lines = wrap(s, width=max_length, break_long_words=False, replace_whitespace=False)
    # Wrap each line in quotes
    return "(\n    " + "\n    ".join(f'"{line}"' for line in lines) + "\n)"

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    def replacer(match):
        quote = match.group("quote")
        text = match.group("content")
        # Only process if longer than max
        if "\n" in text or len(text) > MAX_LINE:
            # Remove internal newlines to avoid double line breaks
            text_clean = " ".join(line.strip() for line in text.splitlines())
            return split_long_string(text_clean)
        return match.group(0)

    new_content = STRING_PATTERN.sub(replacer, content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Processed {file_path}")

def main():
    for py_file in SRC_DIR.rglob("*.py"):
        process_file(py_file)

if __name__ == "__main__":
    main()