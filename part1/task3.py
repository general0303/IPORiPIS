import os
import time
from datetime import datetime
import string
import codecs


if __name__ == "__main__":
    with open("result.csv", "w") as f:
        f.write(f"N;Second;Millisecond\n")
        for i in range(200):
            f.write(f"{i+1};{int(time.time() % 60)};{int(datetime.now().microsecond / 1000)}\n")
            time.sleep(0.02)
    print("________________________________")
    for root, dirs, files in os.walk("../venv"):
        print(root, dirs, files, sep="\n")
    print("________________________________")
    remove_punct_dict = dict((ord(p), None) for p in string.punctuation)
    with codecs.open("text.txt", "r", "utf_8_sig") as f:
        word_tokens = f.read().translate(remove_punct_dict).replace("\n", " ").split(" ")
        a = list(set([w.strip().lower() for w in word_tokens]))
        a.sort(key=lambda x: len(x), reverse=True)
        print(a)
    print("________________________________")
    row = lambda l: list(map(lambda x: x.strip(), l.split(";")))
    with open("result.csv", "r") as f:
        headers, rows = row(f.readline()), [row(line) for line in f.readlines()]
    print(headers, rows, sep="\n")
