# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import unittest
from string import ascii_uppercase, ascii_lowercase, digits, punctuation

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

    def test_init_error(self):
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

    def test_repr(self):
        heap = OrderHeap(reversed(ascii_uppercase), key=self.key)
        self.assertHeap(heap, [], eval(re.sub(r'key=<.*>', 'key=self.key', repr(heap))))


class RemovalHeapTestCase(HeapBaseTestCase):

    @property
    def empty_heap(self):
        return RemovalHeap()

    @property
    def filled_heap(self):
        heap = RemovalHeap(digits + ascii_uppercase)
        for c in digits:
            heap.remove(c)
        return heap

    def test_init(self):
        self.assertHeap([], [], RemovalHeap())
        self.assertHeap([], [], RemovalHeap([]))
        self.assertHeap(ascii_uppercase, [], RemovalHeap(ascii_uppercase))

    def test_init_error(self):
        self.assertRaises(RuntimeError, RemovalHeap, ascii_uppercase+ascii_uppercase)

    def test_check(self):
        RemovalHeap().check()
        RemovalHeap(ascii_uppercase).check()
        RemovalHeap(reversed(ascii_uppercase)).check()

    def test_check_variant_invalid(self):
        heap = self.filled_heap
        heap[3] = 't'
        self.assertRaises(InvalidHeapError, heap.check)

    def test_peek(self):
        heap = self.filled_heap
        self.assertEqual('A', heap.peek())

    def test_push(self):
        heap = self.empty_heap
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for new in ascii_uppercase:
            heap.push(new)
            wanted.add(new)
            not_wanted.remove(new)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_push_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.push, 'A')

    def test_pop(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old in ascii_uppercase:
            self.assertEqual(old, heap.pop())
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_remove(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old in reversed(ascii_uppercase):
            heap.remove(old)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.poppush(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_poppush_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.poppush, 'A')

    def test_replace(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.replace(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_replace_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.replace, 'A')

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', self.empty_heap.pushpop('A'))

    def test_pushpop(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.pushpop(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_pushpop_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.pushpop, 'A')

    def test_repr(self):
        heap = self.filled_heap
        self.assertHeap(heap, [], eval(repr(heap)))


class XHeapTestCase(HeapBaseTestCase):

    @property
    def empty_heap(self):
        return XHeap(key=self.key)

    @property
    def filled_heap(self):
        heap = XHeap(digits + ascii_uppercase, key=self.key)
        for c in digits:
            heap.remove(c)
        return heap

    @staticmethod
    def key(x):
        return ord(x)**2

    def test_init(self):
        self.assertHeap([], [], XHeap(key=self.key))
        self.assertHeap([], [], XHeap([], key=self.key))
        self.assertHeap(ascii_uppercase, [], XHeap(ascii_uppercase, key=self.key))

    def test_init_error(self):
        self.assertRaises(RuntimeError, XHeap)
        self.assertRaises(RuntimeError, XHeap, ascii_uppercase+ascii_uppercase)
        self.assertRaises(RuntimeError, XHeap, ascii_uppercase+ascii_uppercase, key=self.key)

    def test_check(self):
        XHeap(key=self.key).check()
        XHeap(ascii_uppercase, key=self.key).check()
        XHeap(reversed(ascii_uppercase), key=self.key).check()

    def test_check_variant_invalid(self):
        heap = self.filled_heap
        heap[3] = (self.key('t'), 't')
        self.assertRaises(InvalidHeapError, heap.check)

    def test_peek(self):
        heap = self.filled_heap
        self.assertEqual('A', heap.peek())

    def test_push(self):
        heap = self.empty_heap
        wanted = set()
        not_wanted = set(ascii_uppercase)
        for new in ascii_uppercase:
            heap.push(new)
            wanted.add(new)
            not_wanted.remove(new)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_uppercase, [], heap)

    def test_push_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.push, 'A')

    def test_pop(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old in ascii_uppercase:
            self.assertEqual(old, heap.pop())
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_remove(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old in reversed(ascii_uppercase):
            heap.remove(old)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap([], ascii_uppercase, heap)

    def test_poppush(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.poppush(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_poppush_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.poppush, 'A')

    def test_replace(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.replace(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_replace_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.replace, 'A')

    def test_pushpop_on_empty_heap(self):
        self.assertEqual('A', self.empty_heap.pushpop('A'))

    def test_pushpop(self):
        heap = self.filled_heap
        wanted = set(ascii_uppercase)
        not_wanted = set()
        for old, new in zip(ascii_uppercase, ascii_lowercase):
            self.assertEqual(old, heap.pushpop(new))
            wanted.add(new)
            wanted.remove(old)
            not_wanted.add(old)
            self.assertHeap(wanted, not_wanted, heap)
        self.assertHeap(ascii_lowercase, ascii_uppercase, heap)

    def test_pushpop_error(self):
        self.assertRaises(RuntimeError, self.filled_heap.pushpop, 'A')

    def test_repr(self):
        heap = self.filled_heap
        self.assertHeap(heap, [], eval(re.sub(r'key=<.*>', 'key=self.key', repr(heap))))
