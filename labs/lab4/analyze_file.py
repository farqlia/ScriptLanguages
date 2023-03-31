import json
filepath = input("Enter file path: ")

n_of_lines = 0
chars_count = {}
words_count = {}
n_words = 0
n_chars = 0

with open(filepath) as f:
    for line in f:
        n_of_lines += 1
        words = line.split()
        n_words += len(words)
        for word in words:
            words_count[word] += words_count.get(word, 0) + 1
            chars_count += len(word)
            for chr in word:
                chars_count[chr] += chars_count.get(chr, 0) + 1

max_char = max(chars_count.keys(), key=lambda k: chars_count[k])
max_word = max(words_count.keys(), key=lambda k: words_count[k])

data_dir = r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\data"

stats = {
    'n_of_lines': n_of_lines,
    'max_char': max_char,
    'max_word': max_word,
    'n_words': n_words,
    'n_chars': n_chars
}

with open(data_dir + "\\stats.json") as f:
    json.dump(stats, f, indent=4)