# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import unittest
from string import ascii_uppercase, ascii_lowercase

from xheap import Heap, InvalidHeapError, OrderHeap, RemovalHeap, XHeap


class HeapBaseTestCase(unittest.TestCase):

    def assertHeap(self, expected_set, unexpected_set, heap):
        heap.check()
        expected_set = set(expected_set)
        self.assertSetEqual(expected_set, set(heap))
        for item in expected_set:
            self.assertIn(item, heap)
        for item in unexpected_set:
            self.assertNotIn(item, heap)
        self.assertEqual(len(expected_set), len(heap))


class HeapTestCase(HeapBaseTestCase):

    def test_init(self):
        self.assertHeap([], [], Heap())
        self.assertHeap([], [], Heap([]))
        self.assertHeap(ascii_uppercase, [], Heap(ascii_uppercase))

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
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            wanted.add(c)
            not_wanted.remove(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_pop(self):
        heap = Heap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        sorted_items = []
        for c in ascii_uppercase:
            self.assertEqual(c, heap.pop())
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
            sorted_items.append(c)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = Heap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.poppush(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_replace(self):
        heap = Heap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.replace(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', Heap().pushpop('A'))

    def test_pushpop(self):
        heap = Heap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.pushpop(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_remove_not_implemented(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.remove, 'A')

    def test_setslice_not_implemented(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])

    def test_repr(self):
        heap = Heap(reversed(ascii_uppercase))
        self.assertHeap(heap, [], eval(repr(heap)))


class OrderHeapTestCase(HeapBaseTestCase):

    @staticmethod
    def key(x):
        return -ord(x)

    def test_init(self):
        self.assertHeap([], [], OrderHeap(key=self.key))
        self.assertHeap([], [], OrderHeap([], key=self.key))
        self.assertHeap(ascii_uppercase, [], OrderHeap(ascii_uppercase, key=self.key))

    def test_init_errors(self):
        self.assertRaises(RuntimeError, OrderHeap)
        self.assertRaises(RuntimeError, OrderHeap, ascii_uppercase)

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
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            wanted.add(c)
            not_wanted.remove(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_pop(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        wanted = set(ascii_uppercase)
        not_wanted = set()
        sorted_items = []
        for c in reversed(ascii_uppercase):
            self.assertEqual(c, heap.pop())
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
            sorted_items.append(c)
        self.assertSequenceEqual(list(reversed(ascii_uppercase)), sorted_items)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = OrderHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.poppush(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_replace(self):
        heap = OrderHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.replace(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', OrderHeap(key=self.key).pushpop('A'))

    def test_pushpop(self):
        heap = OrderHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.pushpop(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_remove_not_implemented(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.remove, 'A')

    def test_setslice_not_implemented(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])

    def test_repr(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertHeap(heap, [], eval(re.sub(r'key=<.*>', 'key=self.key', repr(heap))))


class RemovalHeapTestCase(HeapBaseTestCase):

    def test_init(self):
        self.assertHeap([], [], RemovalHeap())
        self.assertHeap([], [], RemovalHeap([]))
        self.assertHeap(ascii_uppercase, [], RemovalHeap(ascii_uppercase))

    def test_init_errors(self):
        self.assertRaises(RuntimeError, RemovalHeap, ascii_uppercase+ascii_uppercase)

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
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            wanted.add(c)
            not_wanted.remove(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_pop(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        sorted_items = []
        for c in ascii_uppercase:
            self.assertEqual(c, heap.pop())
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
            sorted_items.append(c)
        self.assertSequenceEqual(ascii_uppercase, sorted_items)
        self.assertHeap([], ascii_uppercase, heap)

    def test_remove(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for c in reversed(ascii_uppercase):
            heap.remove(c)
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.poppush(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_replace(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.replace(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', RemovalHeap().pushpop('A'))

    def test_pushpop(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for u, l in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(u, heap.pushpop(l))
            wanted.add(l)
            wanted.remove(u)
            not_wanted.add(u)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_setslice_not_implemented(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])

    def test_repr(self):
        heap = RemovalHeap(reversed(ascii_uppercase))
        self.assertHeap(heap, [], eval(repr(heap)))


class XHeapTestCase(HeapBaseTestCase):

    @staticmethod
    def key(x):
        return -ord(x)

    def test_init(self):
        self.assertHeap([], [], XHeap(key=self.key))
        self.assertHeap([], [], XHeap([], key=self.key))
        self.assertHeap(ascii_uppercase, [], XHeap(ascii_uppercase, key=self.key))

    def test_init_errors(self):
        self.assertRaises(RuntimeError, XHeap)
        self.assertRaises(RuntimeError, XHeap, ascii_uppercase+ascii_uppercase)
        self.assertRaises(RuntimeError, XHeap, ascii_uppercase+ascii_uppercase, key=self.key)

    def test_check(self):
        XHeap(key=self.key).check()
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
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for c in reversed(ascii_uppercase):
            heap.push(c)
            wanted.add(c)
            not_wanted.remove(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_pop(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        wanted = set(ascii_uppercase)
        not_wanted = set()
        sorted_items = []
        for c in reversed(ascii_uppercase):
            self.assertEqual(c, heap.pop())
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
            sorted_items.append(c)
        self.assertSequenceEqual(list(reversed(ascii_uppercase)), sorted_items)
        self.assertHeap([], ascii_uppercase, heap)

    def test_remove(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for c in reversed(ascii_uppercase):
            heap.remove(c)
            wanted.remove(c)
            not_wanted.add(c)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = XHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.poppush(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_replace(self):
        heap = XHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.replace(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', XHeap(key=self.key).pushpop('A'))

    def test_pushpop(self):
        heap = XHeap(reversed(ascii_lowercase), key=self.key)
        wanted = set(ascii_lowercase)
        not_wanted = set()
        for u, l in reversed(list(zip(ascii_uppercase, ascii_lowercase))):
            self.assertEqual(l, heap.pushpop(u))
            wanted.add(u)
            wanted.remove(l)
            not_wanted.add(l)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, ascii_lowercase, heap)

    def test_setslice_not_implemented(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        self.assertRaises(NotImplementedError, heap.__setslice__, 0, 0, [])

    def test_repr(self):
        heap = XHeap(reversed(ascii_uppercase), key=self.key)
        self.assertHeap(heap, [], eval(re.sub(r'key=<.*>', 'key=self.key', repr(heap))))
