from analyzer import count_characters, count_lines, count_words

test_4on4 = "4 4 4 4 \n 4 4 4 4 \n 4 4 4 4 \n 4 4 4 4"
test_fouronfour = "four four four four\n four four four four \n four four four four \n four four four four"
test_4onfour = "4 4 4 4 \n four four four four \n 4 4 4 4 \n four four four four \n 4 4 4 4"

def test_count_characters():
    assert count_characters(test_4on4) == 32
    assert count_characters(test_fouronfour) == 79
    assert count_characters(test_4onfour) == 71

def test_count_lines():
    assert count_lines(test_4on4) == 4
    assert count_lines(test_fouronfour) == 4
    assert count_lines(test_4onfour) == 5

def test_count_words():
    assert count_words(test_4on4) == 16
    assert count_words(test_fouronfour) == 16
    assert count_words(test_4onfour) == 20
