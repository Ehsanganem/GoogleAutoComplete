from ScoreFunction import sentences_score

HELLO = "Hello"
WORLD = "World"
HELLO_WORLD = "Hello World"
HELO = "Helo"
WORLLD = "Worlld"

class TestScoreFunction():
    def test_score_function1(self):
        assert sentences_score(HELLO, HELLO) == 10
        assert sentences_score(HELLO, HELLO_WORLD) == 10

    def test_score_function2(self):
        assert sentences_score(HELO, HELLO_WORLD) == 6

    def test_score_function3(self):
        assert sentences_score(HELLO_WORLD, HELLO_WORLD) == 22

    def test_score_function4(self):
        assert sentences_score(HELO, HELLO) == 6

    def test_score_function5(self):
        assert sentences_score(WORLLD, WORLD) == 8


