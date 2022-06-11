from md2html.pipe import pipe


def test_pipe_single_func():
    def add_1(x: int) -> int:
        return x + 1

    assert pipe(1, add_1) == 2


def test_pipe_multiple_funcs():
    def add_1(x: int) -> int:
        return x + 1

    def add_2(x: int) -> int:
        return x + 2

    assert pipe(1, add_1, add_2) == 4
