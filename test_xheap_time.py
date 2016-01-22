# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import heapq
import unittest
from contextlib import contextmanager
from string import ascii_uppercase

from xheap import Heap, RemovalHeap


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


class RemovalHeapTimeTestCase(unittest.TestCase):

    def setUp(self):
        self.hqs = []
        for i in range(1000):
            hq = list(reversed(range(2600)))
            heapq.heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(1000):
            h = RemovalHeap(list(reversed(range(2600))))
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
                heapq.heappush(self.hqs[i], 10000)
        with print_time('Heap.push'):
            for i in range(1000):
                self.hs[i].push(10000)

    def test_replace_time(self):
        with print_time('heapq.heapreplace'):
            for i in range(1000):
                heapq.heapreplace(self.hqs[i], 10000)
        with print_time('Heap.replace'):
            for i in range(1000):
                self.hs[i].replace(10000)

    def test_pushpop_time(self):
        with print_time('heapq.heappushpop'):
            for i in range(1000):
                heapq.heappushpop(self.hqs[i], 1000)
        with print_time('Heap.pushpop'):
            for i in range(1000):
                self.hs[i].pushpop(1000)

    def test_heapify_time(self):
        with print_time('heapq.heapify'):
            for i in range(1000):
                heapq.heapify(self.hqs[i])
        with print_time('Heap.heapify'):
            for i in range(1000):
                self.hs[i].heapify()


@contextmanager
def print_time(label):
    import time
    start = time.time()
    yield
    end = time.time()
    print('{: <18} - {:8.4f}usec'.format(label, (end - start) * 1000.0))