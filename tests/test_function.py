from twitter_analysis_tools import Example


def test_example():
    e = Example()
    assert e.get_value() == 10
