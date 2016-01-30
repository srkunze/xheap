# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from contextlib import contextmanager
from heapq import heapify, heappush, heappop, heapreplace, heappushpop
from string import ascii_uppercase

from xheap import Heap, RemovalHeap, OrderHeap, XHeap

repeat = 100


class BaseTimeTestCaseMixin(object):


    def tearDown(self):
        print('-'*40)

    def test_init_time(self):
        with print_time('heapq.init'):
            for _ in range(repeat):
                heapify(list(reversed(ascii_uppercase)))
        with print_time('Heap.init'):
            for _ in range(repeat):
                Heap(reversed(ascii_uppercase))

    def test_peek_time(self):
        with print_time('heapq[0]'):
            for _ in range(repeat):
                self.hqs[0]
        with print_time('Heap.peek'):
            for _ in range(repeat):
                self.hs[0].peek()

    def test_pop_time(self):
        with print_time('heapq.heappop'):
            for i in range(repeat):
                heappop(self.hqs[i])
        with print_time('Heap.pop'):
            for i in range(repeat):
                self.hs[i].pop()

    def test_push_time(self):
        with print_time('heapq.heappush'):
            for i in range(repeat):
                heappush(self.hqs[i], 10000000)
        with print_time('Heap.push'):
            for i in range(repeat):
                self.hs[i].push(10000000)

    def test_replace_time(self):
        with print_time('heapq.heapreplace'):
            for i in range(repeat):
                heapreplace(self.hqs[i], 10000000)
        with print_time('Heap.replace'):
            for i in range(repeat):
                self.hs[i].replace(10000000)

    def test_pushpop_time(self):
        with print_time('heapq.heappushpop'):
            for i in range(repeat):
                heappushpop(self.hqs[i], 10000000)
        with print_time('Heap.pushpop'):
            for i in range(repeat):
                self.hs[i].pushpop(10000000)

    def test_heapify_time(self):
        with print_time('heapq.heapify'):
            for i in range(repeat):
                heapify(self.hqs[i])
        with print_time('Heap.heapify'):
            for i in range(repeat):
                self.hs[i].heapify()


class HeapTimeTestCase(BaseTimeTestCaseMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('### Heap ###')

    def setUp(self):
        self.hqs = []
        for i in range(repeat):
            hq = list(reversed(range(2600)))
            heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(repeat):
            h = Heap(reversed(range(2600)))
            self.hs.append(h)


class OrderHeapTimeTestCase(BaseTimeTestCaseMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('### OrderHeap ###')

    @staticmethod
    def key(x):
        return -x

    def setUp(self):
        self.hqs = []
        for i in range(repeat):
            hq = list(reversed(range(2600)))
            heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(repeat):
            h = OrderHeap(reversed(range(2600)), key=self.key)
            self.hs.append(h)


class RemovalHeapTimeTestCase(BaseTimeTestCaseMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('### RemovalHeap ###')

    def setUp(self):
        self.hqs = []
        for i in range(repeat):
            hq = list(reversed(range(2600)))
            heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(repeat):
            h = RemovalHeap(reversed(range(2600)))
            self.hs.append(h)


class XHeapTimeTestCase(BaseTimeTestCaseMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('### OrderHeap ###')

    @staticmethod
    def key(x):
        return -x

    def setUp(self):
        self.hqs = []
        for i in range(repeat):
            hq = list(reversed(range(2600)))
            heapify(hq)
            self.hqs.append(hq)
        self.hs = []
        for i in range(repeat):
            h = XHeap(reversed(range(2600)), key=self.key)
            self.hs.append(h)


@contextmanager
def print_time(label):
    import time
    start = time.time()
    yield
    end = time.time()
    print('{: <18} - {:8.4f}usec'.format(label, (end - start) * repeat))