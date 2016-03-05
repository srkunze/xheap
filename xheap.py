# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from heapq import heapify, heappushpop, heapreplace, heappop, heappush, _siftdown, _siftup

__version__ = '0.12'
__version_info__ = (0, 12)
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
        for index in range(super(Heap, self).__len__()-1, 0, -1):
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

    def __init__(self, iterable=[]):
        _list = list(iterable)
        self._item_set = set(_list)
        if len(_list) != len(self._item_set):
            raise RuntimeError('duplicate items not allowed: {_list}'.format(_list=_list))
        super(RemovalHeap, self).__init__(_list)

    def push(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        heappush(self, item)
        self._item_set.add(item)

    def pop(self):
        return_item = heappop(self)
        while return_item not in self._item_set:
            return_item = heappop(self)
        self._item_set.remove(return_item)
        self.sweep()
        return return_item

    def remove(self, item):
        self._item_set.remove(item)
        self.sweep()

    def poppush(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        self._item_set.add(item)
        while self[0] not in self._item_set:
            self._item_set.remove(heappop(self))
        return_item = heapreplace(self, item)
        self._item_set.remove(return_item)
        return return_item
    replace = poppush

    def pushpop(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        self._item_set.add(item)
        return_item = heappushpop(self, item)
        while return_item not in self._item_set:
            return_item = heappop(self)
        self._item_set.remove(return_item)
        return return_item

    def sweep(self):
        if 2*len(self._item_set) < super(RemovalHeap, self).__len__():
            self[:] = list(self)
            self.heapify()

    def __iter__(self):
        return iter(self._item_set)

    def __contains__(self, item):
        return item in self._item_set

    def __len__(self):
        return len(self._item_set)

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
            item = self[0][1]
            self[0] = item_tuple
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
