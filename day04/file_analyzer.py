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

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py filename")
        sys.exit(1)
    filename = sys.argv[1]
    content = read_file(filename)
    if content:
        print(f"The file has {count_characters(content)} characters")
        print(f"The file has {count_lines(content)} lines")
        print(f"The file has {count_words(content)} words")

main()
