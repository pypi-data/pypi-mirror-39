# -*- coding: utf-8 -*-
"""Test Entry"""

import unittest

from torch_text_classifier import TextClassifier


class TestFit(unittest.TestCase):
    def test_fit(self):
        """Test Fit"""
        x = ['我爱北京', '我不爱北京', '我爱你', '我不爱你']
        y = ['ai', 'no', 'ai', 'no']
        clf = TextClassifier(batch_size=2, epochs=50)
        clf.fit(x, y)
        self.assertEqual(clf.predict(['我爱'])[0], 'ai')
        self.assertEqual(clf.predict(['不爱'])[0], 'no')


if __name__ == '__main__':
    unittest.main()
