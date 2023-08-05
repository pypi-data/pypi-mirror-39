# -*- coding: utf-8 -*-
"""Test utils class"""

import unittest

import numpy as np

import torch
from torch_tagger.utils import pad_seq, sequence_mask


class TestUtil(unittest.TestCase):
    def test_pad_seq(self):
        r = pad_seq([1, 2, 3], 5)
        self.assertEqual(r, [1, 2, 3, 0, 0])

    def test_sequence_mask(self):
        lengths = torch.from_numpy(np.array([1, 2, 3, 4]))
        masks = sequence_mask(lengths, None)
        self.assertEqual(masks.size(1), 4)


if __name__ == '__main__':
    unittest.main()
