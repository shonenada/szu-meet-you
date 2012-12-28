from unittest import TestLoader, TextTestRunner
def test():
    """Runs all unit test."""
    loader = TestLoader()
    suite = loader.discover("tests")
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)

test()