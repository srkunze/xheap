# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import heapq
import unittest
from contextlib import contextmanager
from string import ascii_uppercase

from xheap import Heap, InvalidHeapError, OrderHeap


class HeapTestCase(unittest.TestCase):

    def test_init_(self):
        self.assertSetEqual(set(), set(Heap()))
        self.assertSetEqual(set(), set(Heap([])))
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


class HeapTimeTestCase(unittest.TestCase):

    def setUp(self):
        self.hqs = []
        for i in range(1000):
            hq = list(reversed(ascii_uppercase))*100
            heapq.heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(1000):
            h = Heap(list(reversed(ascii_uppercase))*100)
            self.hs.append(h)

    def tearDown(self):
        print('-'*40)

    def test_init_time(self):
        with print_time('heapq.init'):
            for _ in range(1000):
                heapq.heapify(list(reversed(ascii_uppercase)))
        with print_time('Heap.init'):
            for _ in range(1000):
                Heap(reversed(ascii_uppercase))

    def test_peek_time(self):
        with print_time('heapq[0]'):
            for _ in range(1000):
                self.hqs[0]
        with print_time('Heap[0]'):
            for _ in range(1000):
                self.hs[0]
        with print_time('Heap.peek'):
            for _ in range(1000):
                self.hs[0].peek()

    def test_pop_time(self):
        with print_time('heapq.heappop'):
            for i in range(1000):
                heapq.heappop(self.hqs[i])
        with print_time('Heap.pop'):
            for i in range(1000):
                self.hs[i].pop()

    def test_push_time(self):
        with print_time('heapq.heappush'):
            for i in range(1000):
                heapq.heappush(self.hqs[i], 'z')
        with print_time('Heap.push'):
            for i in range(1000):
                self.hs[i].push('z')

    def test_replace_time(self):
        with print_time('heapq.heapreplace'):
            for i in range(1000):
                heapq.heapreplace(self.hqs[i], 'z')
        with print_time('Heap.replace'):
            for i in range(1000):
                self.hs[i].replace('z')

    def test_pushpop_time(self):
        with print_time('heapq.heappushpop'):
            for i in range(1000):
                heapq.heappushpop(self.hqs[i], 'z')
        with print_time('Heap.pushpop'):
            for i in range(1000):
                self.hs[i].pushpop('z')

    def test_heapify_time(self):
        with print_time('heapq.heapify'):
            for i in range(1000):
                heapq.heapify(self.hqs[i])
        with print_time('Heap.heapify'):
            for i in range(1000):
                self.hs[i].heapify()


class OrderHeapTestCase(unittest.TestCase):

    @staticmethod
    def key(x):
        return -ord(x)

    def test_init(self):
        self.assertSetEqual(set(), set(OrderHeap([], key=self.key)))
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


@contextmanager
def print_time(label):
    import time
    start = time.time()
    yield
    end = time.time()
    print('{: <18} - {:8.4f}usec'.format(label, (end - start) * 1000.0))