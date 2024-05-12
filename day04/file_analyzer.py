import sys
def characters(text):
    try:
        with open(text, 'r') as fh:
            content = fh.read()
            return len(content)
    except FileNotFoundError:
        print("File not found:", text)
        return -1
def lines(text):
    try:
        with open(text, 'r') as fh:
            lines = fh.readlines()
            return len(lines)
    except FileNotFoundError:
        print("File not found:", text)
        return -1

def words(text):
    try:
        with open(text, 'r') as fh:
            content = fh.read()
            words = content.split()
            return len(words)
    except FileNotFoundError:
        print("File not found:", text)
        return -1

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    file = sys.argv[1]

    if characters(file) != -1:
        print(f"the file has {characters(file)} characters") 
    if lines(file) != -1:
        print(f"the file has {lines(file)} lines")
    if words(file) != -1:
        print(f"the file has {words(file)} words")

main()
