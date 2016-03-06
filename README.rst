`XHEAP <https://pypi.python.org/pypi/xheap>`_
=============================================

It's like `heapq <https://docs.python.org/3.5/library/heapq.html>`_ (blazingly fast) but object-oriented + more features.

`Read more here for the background story <http://srkunze.blogspot.com/2016/01/fast-object-oriented-heap-implementation.html>`_.


Why?
----

Less code.


What are heaps good for anyway?
-------------------------------

When you need the smallest item of a large list—fast and with no overhead.


How?
----

Let's suppose you have a heap, you can use ``pop`` to get its smallest item.

.. code:: python

    from xheap import Heap

    heap = Heap(['H', 'D', 'B', 'A', 'E', 'C', 'L', 'J', 'I'])
    heap.pop()   # returns A
    heap.pop()   # returns B
    heap.pop()   # returns C
    heap.pop()   # returns D

`Heapsort <https://en.wikipedia.org/wiki/Heapsort>`_ works this way.


Can I insert an item?
---------------------

Indeed and it's as fast as pop. Use ``push`` for insertion.

.. code:: python

    heap = Heap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.push('Z')


Can I remove an item from the middle of a heap?
-----------------------------------------------

Yes, that's what ``RemovalHeap.remove`` is supposed to do.

.. code:: python

    from xheap import RemovalHeap

    heap = RemovalHeap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.remove('L')


Can I specify the order of the heap?
------------------------------------

Just imagine two heaps of the very same set of items but you need different sorting for each heap. That is
what ``OrderHeap`` is designed for:

.. code:: python

    from xheap import OrderHeap

    items = [date(2016, 1, 1), date(2016, 1, 2),  date(2016, 1, 3),  date(2016, 1, 4)]

    day_heap = OrderHeap(items, key=lambda date: date.day)
    day_heap.peek()      # returns date(2016, 1, 1)

    weekday_heap = OrderHeap(items, key=lambda date: date.weekday())
    weekday_heap.peek()  # returns date(2016, 1, 4)


What about both remove+order?
-----------------------------

No problem. Use ``XHeap``.

If you wonder why there are 4 distinct heap implementations, it's a matter of speed.
Each additional feature slows a heap down. Thus, you could always use XHeap but beware
of the slowdown.


Checking Heap Invariant
-----------------------

A heap is just a list. So, if you tinker with it, you can check whether its invariant still holds:


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
- no slowdown if you don't need more than a simple heap
- removal possible
- custom orders possible
- works with Python2 and Python3

Bad
***

- no drawbacks discovered so far ;-)
- needs fix/work:

  - item wrapper which allows duplicate items
  - decrease-key+increase-key: another missing use-case of `heapq <https://docs.python.org/3.5/library/heapq.html>`_
  - merge heaps

- ideas are welcome :-)
