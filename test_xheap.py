# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from xheap import Heap


class TestCase(unittest.TestCase):

    def test___init__(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(range(100)), set(Heap(range(100))))

    def test_push(self):
        heap = Heap()
        for i in range(100):
            heap.push(i)
        self.assertSetEqual(set(range(100)), set(heap))

    def test_pop(self):
        heap = Heap(range(100))
        for i in range(100):
            self.assertEqual(i, heap.pop())
