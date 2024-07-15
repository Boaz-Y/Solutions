# import sys
# def characters(text):
#     try:
#         with open(text, 'r') as fh:
#             content = fh.read()
#             return len(content)
#     except FileNotFoundError:
#         print("File not found:", text)
#         return -1
# def lines(text):
#     try:
#         with open(text, 'r') as fh:
#             lines = fh.readlines()
#             return len(lines)
#     except FileNotFoundError:
#         print("File not found:", text)
#         return -1

# def words(text):
#     try:
#         with open(text, 'r') as fh:
#             content = fh.read()
#             words = content.split()
#             return len(words)
#     except FileNotFoundError:
#         print("File not found:", text)
#         return -1

# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python script.py filename")
#         sys.exit(1)

#     file = sys.argv[1]

#     if characters(file) != -1:
#         print(f"the file has {characters(file)} characters") 
#     if lines(file) != -1:
#         print(f"the file has {lines(file)} lines")
#     if words(file) != -1:
#         print(f"the file has {words(file)} words")

# main()

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
