# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from string import ascii_uppercase

from xheap import Heap, InvalidHeapError


class HeapTestCase(unittest.TestCase):

    def test___init__(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(ascii_uppercase), set(Heap(ascii_uppercase)))

    def test_check(self):
        Heap().check()
        Heap(ascii_uppercase).check()
        Heap(reversed(ascii_uppercase)).check()

    def test_check_variant_invalid(self):
        heap = Heap(range(100))
        heap[3] = (10000, 10000)
        self.assertRaises(InvalidHeapError, heap.check)

    def test_check_indexes_invalid(self):
        heap = Heap(range(100))
        heap._indexes[(10000, 10000)] = 3
        self.assertRaises(InvalidHeapError, heap.check)

    def test_push(self):
        heap = Heap()
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop_first(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for c in ascii_uppercase:
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pop_middle(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual('M', heap.pop(13))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_pop_last(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual('U', heap.pop(25))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_first(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual(0, heap.remove('A'))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_middle(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual(13, heap.remove('M'))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_last(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual(24, heap.remove('Z'))
        self.assertEqual(25, len(heap))
        heap.check()
