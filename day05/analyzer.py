import sys

def count_characters(content):
    return len(content)

def count_lines(content):
    return len(content.split('\n'))

def count_words(content):
    return len(content.split())

def read_file(filename):
    try:
        with open(filename, 'r') as fh:
            return fh.read()
    except FileNotFoundError:
        print("File not found:", filename)
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <filename>")
    else:
        filename = sys.argv[1]
        content = read_file(filename)
        if content:
            print("Character count:", count_characters(content))
            print("Line count:", count_lines(content))
            print("Word count:", count_words(content))
