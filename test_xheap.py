# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from xheap import Heap, InvalidHeapError


class MyTestCase(unittest.TestCase):

    def test___init__(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(range(100)), set(Heap(range(100))))

    def test_push(self):
        heap = Heap()
        for i in range(100):
            heap.push(i)
            heap.check_invariant()
        self.assertSetEqual(set(range(100)), set(heap))

    def test_pop(self):
        heap = Heap(range(100))
        for i in range(100):
            self.assertEqual(i, heap.pop())
            heap.check_invariant()
        self.assertSetEqual(set(), set(heap))

    def test_check_invariant(self):
        heap = Heap()
        heap.check_invariant()
        heap = Heap(range(99, -1, -1))
        heap.check_invariant()
        heap = Heap(range(100))
        heap[3] = 10000
        self.assertRaises(InvalidHeapError, heap.check_invariant)
