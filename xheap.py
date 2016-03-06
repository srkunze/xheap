# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from heapq import heapify, heappushpop, heapreplace, heappop, heappush

__version__ = '0.15'
__version_info__ = (0, 15)
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

    def __contains__(self, item):
        return item in iter(self)

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

    def peek(self):
        return_item = self[0]
        while return_item not in self._item_set:
            heappop(self)
            return_item = self[0]
        return return_item

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
            heappop(self)
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

    # order + removal
    def __init__(self, iterable=[], key=None):
        if not key:
            raise RuntimeError('specify key when using XHeap; otherwise, just use RemovalHeap')
        self.key = key
        _list = list(iterable)
        self._item_set = set(_list)
        if len(_list) != len(self._item_set):
            raise RuntimeError('duplicate items not allowed: {_list}'.format(_list=_list))
        super(XHeap, self).__init__((key(item), item) for item in _list)

    # order
    def peek(self):
        return_item = self[0][1]
        while return_item not in self._item_set:
            heappop(self)
            return_item = self[0][1]
        return return_item

    # order + removal
    def push(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        heappush(self, (self.key(item), item))
        self._item_set.add(item)

    def pop(self):
        return_item = heappop(self)[1]
        while return_item not in self._item_set:
            return_item = heappop(self)[1]
        self._item_set.remove(return_item)
        self.sweep()
        return return_item

    def remove(self, item):
        self._item_set.remove(item)
        self.sweep()

    def sweep(self):
        if 2*len(self._item_set) < super(XHeap, self).__len__():
            self[:] = (item_tuple for item_tuple in super(XHeap, self).__iter__() if item_tuple[1] in self._item_set)
            self.heapify()

    # order + removal
    def poppush(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        self._item_set.add(item)
        while self[0][1] not in self._item_set:
            heappop(self)
        return_item = heapreplace(self, (self.key(item), item))[1]
        self._item_set.remove(return_item)
        return return_item
    replace = poppush

    # order + removal
    def pushpop(self, item):
        if item in self._item_set:
            raise RuntimeError('duplicate item not allowed: {item}'.format(item=item))
        self._item_set.add(item)
        return_item = heappushpop(self, (self.key(item), item))[1]
        while return_item not in self._item_set:
            return_item = heappop(self)[1]
        self._item_set.remove(return_item)
        return return_item

    # removal
    def __iter__(self):
        return iter(self._item_set)

    # removal
    def __contains__(self, item):
        return item in self._item_set

    # removal
    def __len__(self):
        return len(self._item_set)

    def __repr__(self):
        return 'XHeap({content}, key={key})'.format(content=list(self), key=self.key)


class InvalidHeapError(RuntimeError):
    pass


#TODO: why reversed(zip(...)) not working TypeError: argument to reversed() must be a sequence