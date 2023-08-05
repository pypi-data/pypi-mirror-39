# -*- coding: utf-8 -*-
"""Test Entry"""

import unittest

from torch_text_classifier import TextClassifier


class TestNumberFit(unittest.TestCase):
    def test_number_fit(self):
        """Test Number Fit"""
        x = ['我爱北京', '我不爱北京', '我爱你', '我不爱你']
        y = [2, 1, 2, 1]
        clf = TextClassifier(batch_size=2, epochs=50)
        clf.fit(x, y)
        self.assertEqual(clf.predict(['我爱'])[0], 2)
        self.assertEqual(clf.predict(['不爱'])[0], 1)


if __name__ == '__main__':
    unittest.main()
