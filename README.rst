XHEAP_
======

It's like heapq_ (which is blazingly fast) but it's object-oriented and has more features.


Why?
----

Less code.

Easy Removal.

No need to re-invent the wheel.


How?
----

Before:

.. code:: python

    import heapq

    heap = [1234, 12]
    heapq.heapify(heap)
    heapq.heappush(heap, 55)
    print(heapq.heappop(heap))

After:

.. code:: python

    from xheap import Heap

    heap = Heap([1234, 12])
    heap.push(55)
    print(heap.pop())


About that removal of items ...
-------------------------------

Imagine a priority queue of tasks. Say, you need to remove an arbitrary item from it. Just call ``remove``.

.. code:: python

    heap = Heap([4, 3, 7, 6, 1, 2, 9, 8, 0, 5])
    heap.remove(6)

If you know the item's index, you can use ``pop``.

.. code:: python

    heap = Heap([4, 3, 7, 6, 1, 2, 9, 8, 0, 5])
    heap.pop(3)


Max-Heap or Min-Heap?
---------------------

**You define the order of items.** Just imagine two heaps of the very same set of items but you need
different sorting for each heap. So, you define what min and max means, via ``cmp``.

.. code:: python

    items = [date(2015, 1, 1), date(2015, 1, 2),  date(2015, 1, 3)]
    order1 = Heap(items, cmp=lambda x, y: x.day <= y.day)
    order2 = Heap(items, cmp=lambda x, y: x.weekday() >= y.weekday())


Conclusion
----------

Good
****

- OO
- can remove items from within the heap
- can remove items with unknown index
- sorting defined per heap (falls back to Pythonic ``<=``)
- works with Python2 and Python3

Bad
***

- no drawbacks discovered so far ;)
- needs fix:

  - decrease-key and increase-key seem to be another important missing use-case of heapq_; so, I will dig into that as well
  - merge heaps

- ideas are welcome :-)


.. _XHEAP: https://pypi.python.org/pypi/xheap
.. _heapq: https://docs.python.org/3.5/library/heapq.html