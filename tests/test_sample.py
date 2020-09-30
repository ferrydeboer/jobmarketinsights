# content of test_sample.py
#from jomai.temp import inc
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5