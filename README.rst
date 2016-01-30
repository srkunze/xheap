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

    heap = Heap(['H', 'D', 'B', 'A', 'E', 'C', 'L', 'J', 'I'])
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

Yes, that's what ``remove`` is supposed to do. You need to use the ``RemovalHeap`` for this.

.. code:: python

    heap = RemovalHeap(['A', 'D', 'B', 'H', 'E', 'C', 'L', 'J', 'I'])
    heap.remove('L')


Can I specify the order of item?
--------------------------------

Just imagine two heaps of the very same set of items but you need different sorting for each heap. That is
what ``OrderHeap`` is designed for:

.. code:: python

    items = [date(2016, 1, 1), date(2016, 1, 2),  date(2016, 1, 3),  date(2016, 1, 4)]

    day_heap = OrderHeap(items, key=lambda date: date.day)
    day_heap.peek()      # returns date(2016, 1, 1)

    weekday_heap = OrderHeap(items, key=lambda date: date.weekday())
    weekday_heap.peek()  # returns date(2016, 1, 4)


What about both remove+order?
-----------------------------

No problem. Use ``XHeap``.

If you wonder why there are four different heap implementations, it's a matter of speed.
More features basically mean, the heap is slower. So, you always could use XHeap for all features available but
beware of the slowdown.


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