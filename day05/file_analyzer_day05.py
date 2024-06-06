import pytest
from analyzer import count_characters, count_lines, count_words

test_4on4 = "4 4 4 4 \n 4 4 4 4 \n 4 4 4 4 \n 4 4 4 4"
test_fouronfour = "four four four four\n four four four four \n four four four four \n four four four four"
test_4onfour = "4 4 4 4 \n four four four four \n 4 4 4 4 \n four four four four \n 4 4 4 4"

def test_count_characters():
    assert count_characters(test_4onfour) == 71 

def test_count_lines():
    assert count_lines(test_4onfour) == 5

def count_words():
    assert count_words(test_4onfour) == 8 



# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python script.py filename")
#         sys.exit(1)
#     filename = sys.argv[1]
#     content = read_file(filename)
#     if content:
#         print(f"The file has {count_characters(content)} characters")
#         print(f"The file has {count_lines(content)} lines")
#         print(f"The file has {count_words(content)} words")

#main()
