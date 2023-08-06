# -*- coding: utf-8 -*-
"""Test Entry"""

import unittest

import pandas as pd
from torch_text_classifier import TextClassifier


class TestSeriesFit(unittest.TestCase):
    def test_series_fit(self):
        """Test Series Fit"""
        x = ['我爱北京', '我不爱北京', '我爱你', '我不爱你']
        x = pd.Series(x, name='x')
        y = pd.Series([2, 1, 2, 1], name='y')
        clf = TextClassifier(batch_size=2, epochs=50)
        clf.fit(x, y)
        self.assertEqual(clf.predict(['我爱'])[0], 2)
        self.assertEqual(clf.predict(['不爱'])[0], 1)


if __name__ == '__main__':
    unittest.main()
