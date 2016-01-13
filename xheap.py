# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import heapq


__all__ = ['Heap', 'InvalidHeapError']


class Heap(list):
    """
    Heap Invariant: a[k] <= a[2*k+1] and a[k] <= a[2*k+2]
    """

    def __init__(self, iterable=[], cmp=lambda x, y: x <= y):
        super(Heap, self).__init__(list(iterable))
        self.cmp = cmp
        self.heapify()

    def push(self, item):
        """Push item onto heap, maintaining the heap invariant."""
        if item in self._indexes:
            raise RuntimeError('same item not allowed to be inserted twice.')
        self.append(item)
        self._siftdown(0, len(self) - 1)

    def pop(self, index=0):
        """Pop item with given index off the heap (default smallest), maintaining the heap invariant."""
        lastelt = super(Heap, self).pop()    # raises appropriate IndexError if heap is empty
        if index == len(self):
            returnitem = lastelt
        else:
            returnitem = self[index]
            self[index] = lastelt
            if not index or self.cmp(self[(index - 1) >> 2], lastelt):
                self._siftup(index)
            else:
                self._siftdown(0, index)
        return returnitem

    def remove(self, item):
        return self.pop(self._indexes.pop(item))

    def check_invariant(self):
        for index in range(len(self)-1, 0, -1):
            parent_index = (index-1) >> 1
            if self.cmp(self[parent_index], self[index]):
                continue
            break
        else:
            return
        raise InvalidHeapError('heap invariant (heap[{parent_index}] <= heap[{index}]) violated: {parent} !<= {item}'.format(parent=self[parent_index], parent_index=parent_index, item=self[index], index=index))

    def __setitem__(self, key, value):
        self._indexes[value] = key
        super(Heap, self).__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        super(Heap, self).__setslice__(i, j, sequence)
        self._indexes = {value: index for index, value in enumerate(self)}

    def __repr__(self):
        return 'Heap({content})'.format(content=super(Heap, self).__repr__())

    # Functions below embedded shamelessly from heapq.

    def replace(self, item):
        heapq.heapreplace(self, item)

    def pushpop(self, item):
        heapq.heappushpop(self, item)

    def _siftdown(*args):
        heapq._siftdown(*args)

    def _siftup(*args):
        heapq._siftup(*args)

    def heapify(self):
        self._indexes = {value: index for index, value in enumerate(self)}
        heapq.heapify(self)


class InvalidHeapError(RuntimeError):
    pass
