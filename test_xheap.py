# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from string import ascii_uppercase, ascii_lowercase

from xheap import Heap, InvalidHeapError, OrderHeap, RemovalHeap, XHeap


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

    def test_peek(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertEqual('A', heap.peek())
        self.assertEqual('A', heap[0])

    def test_push(self):
        heap = Heap()
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for c in ascii_uppercase:
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_pushpop(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            popped_item = heap.pushpop(l)
            heap.check()
            self.assertEqual(u, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(ascii_lowercase), set(heap))

    def test_poppush(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            popped_item = heap.poppush(l)
            heap.check()
            self.assertEqual(u, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(ascii_lowercase), set(heap))

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
        self.assertSetEqual(set(), set(OrderHeap(key=self.key)))
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

    def test_peek(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertEqual('Z', heap.peek())

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

    def test_peek(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertEqual('A', heap.peek())
        self.assertEqual('A', heap[0])

    def test_push(self):
        heap = RemovalHeap()
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        sorted_items = []
        for c in ascii_uppercase:
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_remove(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        for c in reversed(ascii_uppercase):
            wanted = set(heap)
            wanted.remove(c)
            heap.remove(c)
            heap.check()
            self.assertSetEqual(wanted, set(heap))
        self.assertSetEqual(set(), set(heap))

    def test_pushpop(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            popped_item = heap.pushpop(l)
            heap.check()
            self.assertEqual(u, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(ascii_lowercase), set(heap))

    def test_poppush(self):
        heap = Heap(reversed(ascii_uppercase))
        sorted_items = []
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            popped_item = heap.poppush(l)
            heap.check()
            self.assertEqual(u, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertSetEqual(set(ascii_lowercase), set(heap))

    def test_setslice_not_implemented(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])


class XHeapTestCase(unittest.TestCase):

    @staticmethod
    def key(x):
        return -ord(x)

    def test_init(self):
        self.assertSetEqual(set(), set(XHeap(key=self.key)))
        self.assertSetEqual(set(), set(XHeap(set(), key=self.key)))
        self.assertSetEqual(set(ascii_uppercase), set(XHeap(ascii_uppercase, key=self.key)))

    def test_check(self):
        XHeap([], key=self.key).check()
        XHeap(ascii_uppercase, key=self.key).check()
        XHeap(reversed(ascii_uppercase), key=self.key).check()

    def test_check_variant_invalid(self):
        heap = XHeap(ascii_uppercase, key=self.key)
        heap[3] = (self.key('t'), 't')
        self.assertRaises(InvalidHeapError, heap.check)

    def test_peek(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        self.assertEqual('Z', heap.peek())

    def test_push(self):
        heap = XHeap([], key=self.key)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            heap.check()
        self.assertSetEqual(set(ascii_uppercase), set(heap))

    def test_pop(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        sorted_items = []
        for c in reversed(ascii_uppercase):
            popped_item = heap.pop()
            heap.check()
            self.assertEqual(c, popped_item)
            sorted_items.append(popped_item)
        self.assertSequenceEqual(list(reversed(ascii_uppercase)), sorted_items)
        self.assertSetEqual(set(), set(heap))

    def test_remove(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        for c in reversed(ascii_uppercase):
            wanted = set(heap)
            wanted.remove(c)
            heap.remove(c)
            heap.check()
            self.assertSetEqual(wanted, set(heap))
        self.assertSetEqual(set(), set(heap))

    def test_setslice_not_implemented(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])
