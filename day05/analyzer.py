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