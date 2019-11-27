import unittest
import pandas as pd
import numpy as np

import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))

        first, last = main.split_last(df, 30)

        self.assertEqual(len(df), len(first) + len(last))



if __name__ == '__main__':
    unittest.main()
