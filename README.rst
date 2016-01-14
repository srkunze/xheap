XHEAP_
======

It's like heapq_ (blazingly fast) but object-oriented + more features.


Why?
----

Less code.


What are heaps good for anyway?
-------------------------------

They are fast when you need the smallest/biggest item of big collections - Runtime: O(log n).


How?
----

Suppose you have a heap, then use ``pop`` get the smallest one. Heapsort_ works this way.

.. code:: python

    heap = Heap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.pop()  # returns A
    heap.pop()  # returns B
    heap.pop()  # returns C
    ...

Can I insert an item?
---------------------

Indeed and it's as fast as pop. Use ``push`` for insertion.

.. code:: python

    heap = Heap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.push('Z')


Can I remove an item from the middle of a heap?
-----------------------------------------------

Yes, that's what ``remove`` is supposed to do.

.. code:: python

    heap = Heap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.remove('L')     # returns index: 6

A heap is basically a list. So, if you know the index of the item, you can use ``pop`` instead.

.. code:: python

    heap = Heap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.pop(6)          # returns item: L


Max-Heap or Min-Heap?
---------------------

**You define the order of items.** Just imagine two heaps of the very same set of items but you need
different sorting for each heap. So, you define what min and max means, via ``cmp``.

.. code:: python

    items = [date(2015, 1, 1), date(2015, 1, 2),  date(2015, 1, 3)]
    order1 = Heap(items, cmp=lambda x, y: x.day <= y.day)
    order2 = Heap(items, cmp=lambda x, y: x.weekday() >= y.weekday())


Checking Heap Invariant
-----------------------

If you tinker with a heap you can check whether the heap invariant still holds:


.. code:: python

    heap = Heap([4, 3, 7, 6, 1, 2, 9, 8, 5])
    heap[3] = 10           # I know what I am doing here
    heap.check_invariant() # but better check... ooops


Conclusion
----------

Good
****

- uses C implementation if available (i.e. fast)
- object-oriented
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
.. _heapsort: https://en.wikipedia.org/wiki/Heapsort