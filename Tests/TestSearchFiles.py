from SearchFiles import search_files

SET1 = {1, 2, 3}
SET2 = {2, 4}
SET3 = {1, 3}
WORD_DICT = {"hello": SET1, "world": SET2}
HELLO_WORLD = "hello world"
HELLO = "hello"
HELO = "helo"
ORLD = "orld"

MISTAKE_HELLO = "helok"


def test_search_files():
    res = search_files(HELLO_WORLD, WORD_DICT)
    assert res == [2]


def test_search_files2():
    res = search_files(HELLO, WORD_DICT)
    assert res == [1, 2, 3]


def test_mistake_in_word():
    res = search_files(HELO, WORD_DICT)
    assert res == [1, 2, 3]


def test_mistake_in_word2():
    res = search_files(ORLD, WORD_DICT)
    assert res == [2, 4]


def test_mistake_in_word3():
    res = search_files(HELO+" "+ORLD, WORD_DICT)
    assert res == [2]
    assert not res == [2, 4]


def test_mistake_in_word4():
    res = search_files(MISTAKE_HELLO, WORD_DICT)
    assert res == [1, 2, 3]


def test_empty_intersection():
    tmp = WORD_DICT.copy()
    tmp[HELLO] = SET3
    res = search_files(HELLO_WORLD, tmp)
    assert res == []
