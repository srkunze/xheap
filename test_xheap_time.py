# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from timeit import repeat


class HeapTimeCase(object):

    def time_init(self):
        return [
            (
                'heapq.heapify',
                'from heapq import heapify',
                'heapify(list(reversed(range({size}))))',
                1,
            ),
            (
                'Heap.__init__',
                'from xheap import Heap',
                'Heap(reversed(range({size})))',
                1,
            ),
        ]

    def time_pop(self):
        return [
            (
                'heapq.heappop',
                'from heapq import heapify, heappop; heap = list(reversed(range({size}))); heapify(heap)',
                'heappop(heap)',
                None,
            ),
            (
                'Heap.pop',
                'from xheap import Heap; heap = Heap(reversed(range({size})))',
                'heap.pop()',
                None,
            ),
        ]

    def time_push(self):
        return [
            (
                'heapq.heappush',
                'from heapq import heapify, heappush; heap = list(reversed(range({size}))); heapify(heap); i=0',
                'heappush(heap, i); i += 1',
                None,
            ),
            (
                'Heap.push',
                'from xheap import Heap; heap = Heap(reversed(range({size}))); i=0',
                'heap.push(i); i += 1',
                None,
            ),
        ]


initial_sizes = [10**2, 10**3, 10**4, 10**5, 10**6]
repetitions = 10000
def perform_time_configs(configs):
    for _, setup, stmt, number in configs:
        yield [min(repeat(stmt.format(size=size), setup.format(size=size), number=(number or size), repeat=repetitions)) for size in initial_sizes]


htc = HeapTimeCase()
config_methods = [getattr(htc, method) for method in dir(htc) if method.startswith('time_') and callable(getattr(htc, method))]
configs_list = [config_method() for config_method in config_methods]
align = max(len(c[0]) for cs in configs_list for c in cs)

for configs in configs_list:
    results = list(perform_time_configs(configs))

    baseline_config = configs[0]
    baseline_results = results[0]

    print(baseline_config[0].ljust(align), ' '.join('{:f}'.format(result) for result in baseline_results))

    for config, results in zip(configs[1:], results[1:]):
        print(config[0].ljust(align), ' '.join('{:f}'.format(result) for result in results))
        print('ratio'.ljust(align), ' '.join('{:7.4f}x'.format(result_after/result_before) for result_before, result_after in zip(baseline_results, results)))

    print('---------------------------------')