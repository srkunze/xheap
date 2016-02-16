# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from timeit import repeat


class HeapTimeCase(object):

    def time_init(self):
        return [
            'init',
            (
                'heapq',
                'from heapq import heapify',
                'heapify(list(reversed(range({size}))))',
                1,
            ),
            (
                'Heap',
                'from xheap import Heap',
                'Heap(reversed(range({size})))',
                1,
            ),
            (
                'RemovalHeap',
                'from xheap import RemovalHeap',
                'RemovalHeap(reversed(range({size})))',
                1,
            ),
        ]

    def time_pop(self):
        return [
            'pop',
            (
                'heapq',
                'from heapq import heapify, heappop; heap = list(reversed(range({size}))); heapify(heap)',
                'heappop(heap)',
                None,
            ),
            (
                'Heap',
                'from xheap import Heap; heap = Heap(reversed(range({size})))',
                'heap.pop()',
                None,
            ),
            (
                'RemovalHeap',
                'from xheap import RemovalHeap; heap = RemovalHeap(reversed(range({size})))',
                'heap.pop()',
                None,
            ),
        ]

    def time_push(self):
        return [
            'push',
            (
                'heapq',
                'from heapq import heapify, heappush; heap = list(reversed(range(0, {size}*4, 4))); heapify(heap); i = 1',
                'heappush(heap, i); i += 4',
                None,
            ),
            (
                'Heap',
                'from xheap import Heap; heap = Heap(reversed(range(0, {size}*4, 4))); i = 1',
                'heap.push(i); i += 4',
                None,
            ),
            (
                'RemovalHeap',
                'from xheap import RemovalHeap; heap = RemovalHeap(reversed(range(0, {size}*4, 4))); i = 1',
                'heap.push(i); i += 4',
                None,
            ),
        ]


class OrderHeapTimeCase(object):

    def time_init(self):
        return [
            'init',
            (
                'heapq',
                'from heapq import heapify',
                'heapify(list(map(lambda x: (-x, x), range({size}))))',
                1,
            ),
            (
                'OrderHeap',
                'from xheap import OrderHeap',
                'OrderHeap(range({size}), key=lambda x: -x)',
                1,
            ),
            (
                'XHeap',
                'from xheap import XHeap',
                'XHeap(range({size}), key=lambda x: -x)',
                1,
            ),
        ]

    def time_pop(self):
        return [
            'pop',
            (
                'heapq',
                'from heapq import heapify, heappop; heap = list(map(lambda x: (-x, x), range({size}))); heapify(heap)',
                'heappop(heap)[1]',
                None,
            ),
            (
                'OrderHeap',
                'from xheap import OrderHeap; heap = OrderHeap(range({size}), key=lambda x: -x)',
                'heap.pop()',
                None,
            ),
            (
                'XHeap',
                'from xheap import XHeap; heap = XHeap(range({size}), key=lambda x: -x)',
                'heap.pop()',
                None,
            ),
        ]

    def time_push(self):
        return [
            'push',
            (
                'heapq',
                'from heapq import heapify, heappush; heap = list(map(lambda x: (-x, x), range(0, {size}*4, 4))); heapify(heap); i = 1',
                'heappush(heap, (-i, i)); i += 4',
                None,
            ),
            (
                'OrderHeap',
                'from xheap import OrderHeap; heap = OrderHeap(range(0, {size}*4, 4), key=lambda x: -x); i = 1',
                'heap.push(i); i += 4',
                None,
            ),
            (
                'XHeap',
                'from xheap import XHeap; heap = XHeap(range(0, {size}*4, 4), key=lambda x: -x); i = 1',
                'heap.push(i); i += 4',
                None,
            ),
        ]


class RemovalHeapTimeCase(object):

    def time_remove(self):
        return [
            'remove',
            (
                'RemovalHeap',
                'from xheap import RemovalHeap; heap = RemovalHeap(map(lambda x: (-x, x), reversed(range({size})))); i = {size}//2',
                'heap.remove((-i, i)); i += 1',
                None,
            ),
            (
                'XHeap',
                'from xheap import XHeap; heap = XHeap(reversed(range({size})), key=lambda x: -x); i = {size}//2',
                'heap.remove(i); i += 1',
                None,
            ),
        ]


initial_sizes = [10**3, 10**4, 10**5, 10**6]
repetitions = 10000
def perform_time_configs(configs):
    for _, setup, stmt, number in configs:
        yield [min(repeat(stmt.format(size=size), setup.format(size=size), number=(number or size//32), repeat=repetitions)) for size in initial_sizes]


for htc in (HeapTimeCase(), OrderHeapTimeCase(), RemovalHeapTimeCase()):
    config_methods = [getattr(htc, method) for method in dir(htc) if method.startswith('time_') and callable(getattr(htc, method))]
    configs_list = [config_method() for config_method in config_methods]
    align_label = max(len(cs[0]) for cs in configs_list)
    align_module = max(len(c[0]) for cs in configs_list for c in cs)

    for configs in configs_list:
        label, configs = configs[0], configs[1:]
        results = list(perform_time_configs(configs))

        baseline_config = configs[0]
        baseline_results = results[0]

        for i, (config, results) in enumerate(zip(configs, results)):
            printed_label = (label if i == 0 else '').ljust(align_label)

            print(printed_label, config[0].ljust(align_module), ' '.join('{:5.2f} ({:5.2f}x)'.format(result*1000, result/baseline_result) for result, baseline_result in zip(results, baseline_results)))

        print('--------------------------------------------------------------------')
    print('--------------------------------------------------------------------')
