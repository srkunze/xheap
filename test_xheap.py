# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from xheap import Heap, InvalidHeapError


class MyTestCase(unittest.TestCase):

    def test___init__(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(range(100)), set(Heap(Heap(range(99, -1, -1)))))

    def test_push(self):
        heap = Heap()
        for i in range(100):
            heap.push(i)
            heap.check_invariant()
        self.assertSetEqual(set(range(100)), set(heap))

    def test_pop_first(self):
        heap = Heap(range(99, -1, -1))
        sorted_items = []
        for i in range(100):
            popped_item = heap.pop()
            heap.check_invariant()
            self.assertEqual(i, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(range(100), sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pop_middle(self):
        heap = Heap(range(99, -1, -1))
        self.assertEqual(88, heap.pop(50))
        self.assertEqual(99, len(heap))
        heap.check_invariant()

    def test_pop_last(self):
        heap = Heap(range(99, -1, -1))
        self.assertEqual(75, heap.pop(99))
        self.assertEqual(99, len(heap))
        heap.check_invariant()

    def test_remove(self):
        heap = Heap(range(99, -1, -1))
        self.assertEqual(39, heap.remove(60))
        self.assertEqual(99, len(heap))
        heap.check_invariant()

    def test_check_invariant(self):
        heap = Heap()
        heap.check_invariant()
        heap = Heap(range(99, -1, -1))
        heap.check_invariant()
        heap = Heap(range(100))
        heap[3] = 10000
        self.assertRaises(InvalidHeapError, heap.check_invariant)
