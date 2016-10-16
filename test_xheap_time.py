# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from timeit import repeat


class HeapTimeCase(object):

    def time_init(self):
        return [
            'init',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from heapq import heapify;'
                ),
                'heapify(values)',
                1,
            ),
            (
                'Heap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import Heap;'
                ),
                'Heap(values)',
                1,
            ),
            (
                'RemovalHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import RemovalHeap;'
                ),
                'RemovalHeap(values)',
                1,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                ),
                'SortedList(values, load=100)',
                1,
            ),
        ]

    def time_pop(self):
        return [
            'pop',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from heapq import heapify, heappop;'
                    'heapify(values);'
                ),
                'heappop(values)',
                None,
            ),
            (
                'Heap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import Heap;'
                    'heap = Heap(values);'
                ),
                'heap.pop()',
                None,
            ),
            (
                'RemovalHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import RemovalHeap;'
                    'heap = RemovalHeap(values);'
                ),
                'heap.pop()',
                None,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                    'heap = SortedList(values, load=100);'
                ),
                'heap.pop(0)',
                None,
            ),
        ]

    def time_push(self):
        return [
            'push',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from heapq import heapify, heappush;'
                    'heap = list(values);'
                    'heapify(heap);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heappush(heap, values[i] + 1); i += 1',
                None,
            ),
            (
                'Heap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from xheap import Heap;'
                    'heap = Heap(values);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.push(values[i] + 1); i += 1',
                None,
            ),
            (
                'RemovalHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from xheap import RemovalHeap;'
                    'heap = RemovalHeap(values);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.push(values[i] + 1); i += 1',
                None,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                    'heap = SortedList(values, load=100);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.add(values[i] + 1); i += 1',
                None,
            ),
        ]


class OrderHeapTimeCase(object):

    def time_init(self):
        return [
            'init',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = [(-x, x) for x in range({size})];'
                    'random.shuffle(values);'
                    'from heapq import heapify;'
                ),
                'heapify(values)',
                1,
            ),
            (
                'OrderHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import OrderHeap;'
                ),
                'OrderHeap(values, key=lambda x: -x)',
                1,
            ),
            (
                'XHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import XHeap;'
                ),
                'XHeap(values, key=lambda x: -x)',
                1,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                ),
                'SortedList(values, key=lambda x: -x, load=100)',
                1,
            ),
        ]

    def time_pop(self):
        return [
            'pop',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = [(-x, x) for x in range({size})];'
                    'from heapq import heapify, heappop;'
                    'heapify(values);'
                ),
                'heappop(values)[1]',
                None,
            ),
            (
                'OrderHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'from xheap import OrderHeap;'
                    'heap = OrderHeap(values, key=lambda x: -x);'
                ),
                'heap.pop()',
                None,
            ),
            (
                'XHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'from xheap import XHeap;'
                    'heap = XHeap(values, key=lambda x: -x);'
                ),
                'heap.pop()',
                None,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'from sortedcontainers import SortedList;'
                    'heap = SortedList(values, key=lambda x: -x, load=100);'
                ),
                'heap.pop(0)',
                None,
            ),
        ]

    def time_push(self):
        return [
            'push',
            (
                'heapq',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = [(-x, x) for x in range(0, {size} * 2, 2)];'
                    'random.shuffle(values);'
                    'from heapq import heapify, heappush;'
                    'heap = list(values);'
                    'heapify(heap);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heappush(heap, (values[i][0] - 1, values[i][1] + 1)); i += 1',
                None,
            ),
            (
                'OrderHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from xheap import OrderHeap;'
                    'heap = OrderHeap(values, key=lambda x: -x);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.push(values[i] + 1); i += 1',
                None,
            ),
            (
                'XHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from xheap import XHeap;'
                    'heap = XHeap(values, key=lambda x: -x);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.push(values[i] + 1); i += 1',
                None,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range(0, {size} * 2, 2));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                    'heap = SortedList(values, key=lambda x: -x, load=100);'
                    'random.shuffle(values);'
                    'i = 0;'
                ),
                'heap.add(values[i] + 1); i += 1',
                None,
            ),
        ]


class RemovalHeapTimeCase(object):

    def time_remove(self):
        return [
            'remove',
            (
                'RemovalHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import RemovalHeap;'
                    'heap = RemovalHeap((-x, x) for x in values);'
                    'i = 0;'
                    'random.shuffle(values);'
                ),
                (
                    'heap.remove((-values[i], values[i]));'
                    'i += 1;'
                ),
                None,
            ),
            (
                'XHeap',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from xheap import XHeap;'
                    'heap = XHeap(values, key=lambda x: -x);'
                    'i = 0;'
                    'random.shuffle(values);'
                ),
                (
                    'heap.remove(values[i]);'
                    'i += 1;'
                ),
                None,
            ),
            (
                'SortedList',
                (
                    'import random;'
                    'random.seed(0);'
                    'values = list(range({size}));'
                    'random.shuffle(values);'
                    'from sortedcontainers import SortedList;'
                    'heap = SortedList(values, key=lambda x: -x, load=100);'
                    'i = 0;'
                    'random.shuffle(values);'
                ),
                (
                    'heap.remove(values[i]);'
                    'i += 1;'
                ),
                None,
            ),
        ]


initial_sizes = [10**3, 10**4, 10**5, 10**6]
repetitions = 5
def perform_time_configs(configs):
    for _, setup, stmt, number in configs:
        try:
            yield [min(repeat(stmt.format(size=size), setup.format(size=size), number=(number or size), repeat=repetitions)) for size in initial_sizes]
        except ImportError as exc:
            pass


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
