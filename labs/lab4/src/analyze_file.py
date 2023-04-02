import json
import os
import sys
from pathlib import Path

DATA_DIR = Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\data")

if __name__ == "__main__":

    filepath = Path(sys.stdin.readline().strip())

    if filepath.is_file():
        n_of_lines = 0
        chars_count = {}
        words_count = {}
        n_words = 0
        n_chars = 0

        with open(filepath, encoding='utf-8') as f:
            for line in f:
                n_of_lines += 1
                words = line.split()
                n_words += len(words)
                for word in words:
                    words_count[word] = words_count.get(word, 0) + 1
                    n_chars += len(word)
                    for char in word:
                        chars_count[char] = chars_count.get(char, 0) + 1

        max_char = max(chars_count.keys(), key=lambda k: chars_count[k])
        max_word = max(words_count.keys(), key=lambda k: words_count[k])

        stats = {
            'filepath': str(filepath.absolute()),
            'n_of_lines': n_of_lines,
            'max_char': max_char,
            'max_word': max_word,
            'n_words': n_words,
            'n_chars': n_chars
        }

        with open(os.path.join(DATA_DIR, f"{filepath.stem}_stats.json"), mode='w') as f:
            json.dump(stats, f, indent=4)
            print(f.name)

    else:
        raise IOError("Not a file: ", filepath)
