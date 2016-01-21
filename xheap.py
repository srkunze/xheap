# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import heapq

__version__ = '0.6'
__version_info__ = (0, 6)
__all__ = ['Heap', 'InvalidHeapError']


class Heap(list):
    """
    Heap shamelessly built upon heapq providing the following benefits:
      - object orientation
      - pop supports index (default=0)
      - cmp method is __lt__ (except for python 2 in case you don't define a __lt__ method)
      - peek
      - check_invariant

    Heap Invariant: a[k] <= a[2*k+1] and a[k] <= a[2*k+2]
    """

    def __init__(self, iterable=[]):
        super(Heap, self).__init__(iterable)
        self.heapify()

    def peek(self):
        return self[0]

    def push(self, item):
        heapq.heappush(self, item)

    def pop(self, index=None):
        if index:
            last_item = super(Heap, self).pop()
            if index == len(self):
                return_item = last_item
            else:
                return_item = self[index]
                self[index] = last_item
                if self[(index - 1) >> 1] < last_item:
                    heapq._siftup(self, index)
                else:
                    heapq._siftdown(self, 0, index)
            return return_item
        return heapq.heappop(self)

    def remove(self, item):
        raise NotImplementedError

    def replace(self, item):
        heapq.heapreplace(self, item)

    def pushpop(self, item):
        heapq.heappushpop(self, item)

    def heapify(self):
        heapq.heapify(self)

    def check(self):
        self.check_invariant()

    def check_invariant(self):
        for index in range(len(self)-1, 0, -1):
            parent_index = (index-1) >> 1
            if self[index] < self[parent_index]:
                raise InvalidHeapError('heap invariant (heap[{parent_index}] <= heap[{index}]) violated: {parent} !<= {item}'.format(parent=self[parent_index], parent_index=parent_index, item=self[index], index=index))

    def __setslice__(self, i, j, sequence):
        raise NotImplementedError

    def __repr__(self):
        return 'Heap({content})'.format(content=super(Heap, self).__repr__())


class OrderHeap(Heap):
    """
    OrderHeap is a heap that allows you to specify the sorting criteria which might come in handy for
        - several heaps for the same set of items but different orders
        - reversing the heap order
    """

    def __init__(self, iterable, key):
        self.key = key
        super(OrderHeap, self).__init__(list((key(value), value) for value in iterable))

    def peek(self):
        return self[0][1]

    def push(self, item):
        super(OrderHeap, self).push((self.key(item), item))

    def pop(self, index=None):
        return super(OrderHeap, self).pop(index)[1]

    def replace(self, item):
        heapq.heapreplace(self, (self.key(item), item))

    def pushpop(self, item):
        heapq.heappushpop(self, (self.key(item), item))

    def __iter__(self):
        return (item[1] for item in super(Heap, self).__iter__())


class RemovalHeap(Heap):
    """
    RemovalHeap is a heap that allows you to remove an item without knowing its index in the heap; useful when
        - users want cancel tasks out of the blue
        - you have two queues of same items, pop an item from one and you want to remove it from the other, too
    """

    def push(self, item):
        if item in self._indexes:
            raise RuntimeError('same item not allowed to be inserted twice.')
        super(RemovalHeap, self).push(item)

    def pop(self, index=None):
        return_item = super(RemovalHeap, self).pop(index)
        del self._indexes[return_item]
        return return_item

    def remove(self, value):
        index = self._indexes[value]
        self.pop(index)
        return index

    def heapify(self):
        heapq.heapify(self)
        self._indexes = self._get_indexes()

    def check(self):
        super(RemovalHeap, self).check()
        self.check_indexes()

    def check_indexes(self):
        if self._indexes != self._get_indexes():
            raise InvalidHeapError('_indexes is broken')

    def __setitem__(self, key, value):
        self._indexes[value] = key
        super(Heap, self).__setitem__(key, value)

    def _get_indexes(self):
        indexes = {}
        for index, value in enumerate(super(Heap, self).__iter__()):
            if value in indexes:
                raise InvalidHeapError('values are not unique')
            indexes[value] = index
        return indexes


class InvalidHeapError(RuntimeError):
    pass
