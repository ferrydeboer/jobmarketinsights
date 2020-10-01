# content of test_sample.py
from jomai.sample import inc

# def inc(x):
#    return x + 1


def test_answer():
    assert inc(3) == 4
