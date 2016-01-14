# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from string import uppercase

from xheap import Heap, InvalidHeapError


class HeapTestCase(unittest.TestCase):

    def test___init__(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(uppercase), set(Heap(uppercase)))

    def test_check(self):
        Heap().check()
        Heap(uppercase).check()
        Heap(reversed(uppercase)).check()

    def test_check_invalid(self):
        heap = Heap(range(100))
        heap[3] = 10000
        self.assertRaises(InvalidHeapError, heap.check)

    def test_push(self):
        heap = Heap()
        for c in reversed(uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(uppercase), set(heap))

    def test_pop_first(self):
        heap = Heap(reversed(uppercase))
        sorted_items = []
        for c in uppercase:
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(uppercase, sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pop_middle(self):
        heap = Heap(reversed(uppercase))
        self.assertEqual('M', heap.pop(13))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_pop_last(self):
        heap = Heap(reversed(uppercase))
        self.assertEqual('U', heap.pop(25))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove(self):
        heap = Heap(reversed(uppercase))
        self.assertEqual(13, heap.remove('M'))
        self.assertEqual(25, len(heap))
        heap.check()
