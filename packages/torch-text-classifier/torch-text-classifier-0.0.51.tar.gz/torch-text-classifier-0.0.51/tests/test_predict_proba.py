# -*- coding: utf-8 -*-
"""Test Entry"""

import unittest

from torch_text_classifier import TextClassifier


class TestNumberFit(unittest.TestCase):
    def test_number_fit(self):
        """Test Number Fit"""
        x = ['我爱北京', '我不爱北京', '我爱你', '我不爱你', '我恨北京', '我恨你']
        y = [2, 1, 2, 1, 'hate', 'hate']
        clf = TextClassifier(batch_size=2, epochs=50)
        clf.fit(x, y)
        r = clf.predict_proba(['我爱'])[0]
        # print(r)
        # for example:
        # r == {
        #   1: 0.15828706324100494,
        #   2: 0.7740275263786316,
        #   'hate': 0.06768541038036346
        # }
        self.assertTrue(isinstance(r[1], float))
        self.assertTrue(isinstance(r[2], float))
        self.assertTrue(isinstance(r['hate'], float))


if __name__ == '__main__':
    unittest.main()
