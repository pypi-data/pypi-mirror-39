# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import pytest
    import sys
    import os

    testdir, _ = os.path.split(__file__)

    if len(sys.argv) > 1:
        testdir = os.path.join(testdir, sys.argv[1])
    pytest.main([testdir, '-v'])  # Run tests
