# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from string import ascii_uppercase

from xheap import Heap, InvalidHeapError, OrderHeap, RemovalHeap


class HeapTestCase(unittest.TestCase):

    def test_init(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(), set(Heap(set())))
        self.assertSetEqual(set(ascii_uppercase), set(Heap(ascii_uppercase)))

    def test_check(self):
        Heap().check()
        Heap(ascii_uppercase).check()
        Heap(reversed(ascii_uppercase)).check()

    def test_check_variant_invalid(self):
        heap = Heap(range(100))
        heap[3] = 10000
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

    def test_remove_not_implemented(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.remove, 'A')

    def test_setslice_not_implemented(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])


class OrderHeapTestCase(unittest.TestCase):

    @staticmethod
    def key(x):
        return -ord(x)

    def test_init(self):
        self.assertSetEqual(set(), set(OrderHeap(set(), key=self.key)))
        self.assertSetEqual(set(ascii_uppercase), set(OrderHeap(ascii_uppercase, key=self.key)))

    def test_check(self):
        OrderHeap([], key=self.key).check()
        OrderHeap(ascii_uppercase, key=self.key).check()
        OrderHeap(reversed(ascii_uppercase), key=self.key).check()

    def test_check_variant_invalid(self):
        heap = OrderHeap(ascii_uppercase, key=self.key)
        heap[3] = (self.key('t'), 't')
        self.assertRaises(InvalidHeapError, heap.check)

    def test_push(self):
        heap = OrderHeap([], key=self.key)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop_first(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        sorted_items = []
        for c in reversed(ascii_uppercase):
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(list(reversed(ascii_uppercase)), sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pop_middle(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertEqual('M', heap.pop(13))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_pop_last(self):
        heap = OrderHeap(ascii_uppercase, key=self.key)
        self.assertEqual('F', heap.pop(25))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_not_implemented(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.remove, 'A')

    def test_setslice_not_implemented(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])


class RemovalHeapTestCase(unittest.TestCase):

    def test_init(self):
        self.assertSetEqual(set(), set(RemovalHeap()))
        self.assertSetEqual(set(), set(RemovalHeap(set())))
        self.assertSetEqual(set(ascii_uppercase), set(RemovalHeap(ascii_uppercase)))

    def test_check(self):
        RemovalHeap().check()
        RemovalHeap(ascii_uppercase).check()
        RemovalHeap(reversed(ascii_uppercase)).check()

    def test_check_variant_invalid(self):
        heap = RemovalHeap(range(100))
        heap[3] = 10000
        self.assertRaises(InvalidHeapError, heap.check)

    def test_push(self):
        heap = RemovalHeap()
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop_first(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        sorted_items = []
        for c in ascii_uppercase:
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pop_middle(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual('M', heap.pop(13))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_pop_last(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual('U', heap.pop(25))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_first(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual(0, heap.remove('A'))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_middle(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual(13, heap.remove('M'))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_remove_last(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual(25, heap.remove('U'))
        self.assertEqual(25, len(heap))
        heap.check()

    def test_setslice_not_implemented(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])
