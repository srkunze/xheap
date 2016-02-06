# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from heapq import heapify, heappushpop, heapreplace, heappop, heappush, _siftdown, _siftup

__version__ = '0.11'
__version_info__ = (0, 11)
__all__ = ['Heap', 'OrderHeap', 'RemovalHeap', 'XHeap', 'InvalidHeapError']


class Heap(list):
    """
    Heap shamelessly built upon heapq providing the following benefits:
      - object orientation
      - check_invariant
    It uses __lt__ for comparison (except for python 2 in case you don't define a __lt__ method, then its __le__).

    Heap Invariant: a[k] <= a[2*k+1] and a[k] <= a[2*k+2]
    """

    def __init__(self, iterable=[]):
        super(Heap, self).__init__(iterable)
        self.heapify()

    def peek(self):
        return self[0]

    def push(self, item):
        heappush(self, item)

    def pop(self):
        return heappop(self)

    def remove(self, item):
        raise NotImplementedError

    def heapify(self):
        heapify(self)

    def poppush(self, item):
        """Because I always forget what replace means."""
        return heapreplace(self, item)
    replace = poppush

    def pushpop(self, item):
        return heappushpop(self, item)

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

    def __init__(self, iterable=[], key=None):
        if not key:
            raise RuntimeError('specify key when using OrderHeap; otherwise, just use Heap')
        self.key = key
        super(OrderHeap, self).__init__((key(item), item) for item in iterable)

    def peek(self):
        return self[0][1]

    def push(self, item):
        super(OrderHeap, self).push((self.key(item), item))

    def pop(self):
        return super(OrderHeap, self).pop()[1]

    def poppush(self, item):
        return heapreplace(self, (self.key(item), item))[1]
    replace = poppush

    def pushpop(self, item):
        return heappushpop(self, (self.key(item), item))[1]

    def __iter__(self):
        return (item_tuple[1] for item_tuple in super(Heap, self).__iter__())

    def __repr__(self):
        return 'OrderHeap({content}, key={key})'.format(content=list(self), key=self.key)


class RemovalHeap(Heap):
    """
    RemovalHeap is a heap that allows you to remove an item without knowing its index in the heap; useful when
        - users want cancel tasks from a task queue
        - you have two queues of same items, pop an item from one and you want to remove it from the other, too
    """

    def push(self, item):
        if item in self._indexes:
            raise RuntimeError('same item not allowed to be inserted twice.')
        self.append(item)
        _siftdown(self, 0, len(self)-1)

    def pop(self):
        last_item = super(Heap, self).pop()
        if self:
            return_item = self[0]
            self[0] = last_item
            _siftup(self, 0)
        else:
            return_item = last_item
        del self._indexes[return_item]
        return return_item

    def remove(self, item):
        index = self._indexes[item]
        last_item = super(Heap, self).pop()
        if index != len(self):
            self[index] = last_item
            _siftdown(self, 0, index)
            _siftup(self, index)
        del self._indexes[item]

    def heapify(self):
        self._indexes = {}
        heapify(self)
        self._indexes = self._get_indexes()

    def poppush(self, item):
        return_item = self[0]
        self[0] = item
        _siftup(self, 0)
        del self._indexes[return_item]
        return return_item
    replace = poppush

    def pushpop(self, item):
        if self and self[0] < item:
            item, self[0] = self[0], item
            _siftup(self, 0)
            del self._indexes[item]
        return item

    def check(self):
        super(RemovalHeap, self).check()
        self.check_indexes()

    def check_indexes(self):
        if self._indexes != self._get_indexes():
            raise InvalidHeapError('_indexes is broken')

    def _get_indexes(self):
        indexes = {}
        for index, item in enumerate(self):
            if item in indexes:
                raise InvalidHeapError('items are not unique')
            indexes[item] = index
        return indexes

    def __setitem__(self, key, item):
        super(RemovalHeap, self).__setitem__(key, item)
        self._indexes[item] = key

    def __repr__(self):
        return 'RemovalHeap({content})'.format(content=list(self))


class XHeap(Heap):
    """Hybrid of OrderHeap and RemovalHeap."""

    # order
    def __init__(self, iterable=[], key=None):
        if not key:
            raise RuntimeError('specify key when using XHeap; otherwise, just use RemovalHeap')
        self.key = key
        super(XHeap, self).__init__((key(item), item) for item in iterable)

    # order
    def peek(self):
        return self[0][1]

    # remove + order
    def push(self, item):
        if item in self._indexes:
            raise RuntimeError('same item not allowed to be inserted twice.')
        self.append((self.key(item), item))
        _siftdown(self, 0, len(self)-1)

    def pop(self):
        last_item_tuple = super(Heap, self).pop()
        if self:
            return_item = self[0][1]
            self[0] = last_item_tuple
            _siftup(self, 0)
        else:
            return_item = last_item_tuple[1]
        del self._indexes[return_item]
        return return_item

    def remove(self, item):
        index = self._indexes[item]
        last_item_tuple = super(Heap, self).pop()
        if index != len(self):
            self[index] = last_item_tuple
            _siftdown(self, 0, index)
            _siftup(self, index)
        del self._indexes[item]

    #remove+order
    def poppush(self, item):
        return_item = self[0][1]
        self[0] = (self.key(item), item)
        _siftup(self, 0)
        del self._indexes[return_item]
        return return_item
    replace = poppush

    #remove+order
    def pushpop(self, item):
        item_tuple = (self.key(item), item)
        if self and self[0] < item_tuple:
            item, self[0] = self[0][1], item_tuple
            _siftup(self, 0)
            del self._indexes[item]
        return item

    #remove
    def heapify(self):
        self._indexes = {}
        heapify(self)
        self._indexes = self._get_indexes()

    #remove
    def check(self):
        super(XHeap, self).check()
        self.check_indexes()

    #remove
    def check_indexes(self):
        if self._indexes != self._get_indexes():
            raise InvalidHeapError('_indexes is broken')

    #remove
    def _get_indexes(self):
        indexes = {}
        for index, item in enumerate(self):
            if item in indexes:
                raise InvalidHeapError('items are not unique')
            indexes[item] = index
        return indexes

    #remove + order
    def __setitem__(self, key, item_tuple):
        super(XHeap, self).__setitem__(key, item_tuple)
        self._indexes[item_tuple[1]] = key

    # order
    def __iter__(self):
        return (item_tuple[1] for item_tuple in super(Heap, self).__iter__())

    def __repr__(self):
        return 'XHeap({content}, key={key})'.format(content=list(self), key=self.key)


class InvalidHeapError(RuntimeError):
    pass
