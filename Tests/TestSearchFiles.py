from SearchFiles import search_files

SET1 = {1,2,3}
SET2 = {2,4}
SET3 = {1,3}
WORD_DICT = { "hello": SET1, "world": SET2 }
HELLO_WORLD = "hello world"
HELLO = "hello"


def test_search_files():
    res = search_files(HELLO_WORLD, WORD_DICT)
    assert res == [2]

def test_search_files2():
    res = search_files(HELLO, WORD_DICT)
    assert res == [1,2,3]

def test_empty_intersection():
    WORD_DICT[HELLO] = SET3
    res = search_files(HELLO_WORLD, WORD_DICT)
    assert res == []