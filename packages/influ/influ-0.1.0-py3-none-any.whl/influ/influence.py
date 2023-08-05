from heapq import heapify, heappop, heapreplace
from itertools import combinations, cycle, islice
from typing import Any, TypeVar

import igraph as ig
import numpy as np

from influ.model import linear_treshold, independent_cascade


class SeedFinder:

    def __init__(self, graph: ig.Graph, number=None, unit=None, random_seed=None):
        """
        Initiate instance of SeedFinder with some default values of parameters
        that will be used during choosing seeds.

        :param graph: graph to be analyzed
        :param number: value of number or percentage of seeds to choose
        :param unit: percent or number
        :param random_seed: value used as seed for random function to ensure repetitive results
        """

        self.graph = graph.copy()
        if 'id' not in self.graph.vertex_attributes():
            self.graph.vs['id'] = list(range(len(self.graph.vs)))
        self.graphs = self.graph.components().subgraphs()
        self.max_n = len(self.graph.vs)
        self.configure(number, unit, random_seed)

    def configure(self, number=None, unit=None, random_seed=None):
        """
        Calculates number of seeds to find.

        :param number: value of number or percentage of seeds to choose
        :param unit: 'percent' or 'number' - specifies how to calculates number of seeds to find
        :param random_seed: value used as seed for random function to ensure repetitive results
        :return: number of seeds to find
        """

        if None in (number, unit):
            if unit is not None and number is None:
                raise TypeError("'unit' cannot be specified without specifying number")

            if hasattr(self, 'n'):
                return self.n

        number = number or 5
        unit = unit or 'percent'

        if unit not in ('percent', 'number'):
            raise TypeError("'unit' must by 'percent' or 'number'!")

        if unit == 'percent':
            if number < 0 or 100 < number:
                raise TypeError("For 'percent' unit: 0 < numberof <= 100!")
            n = max(int(self.max_n * number / 100), 1)
        elif unit == 'number':
            if number < 0 or self.max_n < number or type(number) is not int:
                raise TypeError(
                    "for 'number' unit number must be positive integer not bigger than number of vertices in graph!")
            n = number

        self.n = n
        self.random_seed = random_seed

    def _postprocess_result(self, seeds):
        seeds = seeds[:self.n]
        if type(seeds) is not list:
            seeds = seeds.tolist()

        return seeds

    def merge_results(self, seed_lists):
        result = []
        pending = len(seed_lists)
        nexts = cycle(iter(elem).__next__ for elem in seed_lists)
        collected_seeds = 0

        while pending and collected_seeds < self.n:
            try:
                for next_v in nexts:
                    result.append(next_v())
                    collected_seeds += 1
                    if collected_seeds == self.n:
                        break
            except StopIteration:
                pending -= 1
                nexts = cycle(islice(nexts, pending))

        return result

    def by_indegree(self):
        """
        Return list of n first vertices indices sorted by their indegree.

        :return: list of vertices indices sorted by indegree
        """
        results = []
        for subgraph in self.graphs:
            indegree = np.array(subgraph.indegree())
            argi = np.argsort(-indegree).tolist()
            results.append(subgraph.vs.select(argi)['id'])

        print(results)
        return self.merge_results(results)

    def by_outdegree(self):
        """
        Return list of n first vertices indices sorted by their outdegree.

        :return: list of vertices indices sorted by outdegree
        """
        results = []
        for subgraph in self.graphs:
            outdegree = np.array(subgraph.outdegree())
            argi = np.argsort(-outdegree).tolist()
            results.append(subgraph.vs.select(argi)['id'])

        print(results)
        return self.merge_results(results)

    def by_degree(self):
        """
        Return list of n first vertices indices sorted by their degree.

        :return: list of vertices indices sorted by degree
        """
        results = []
        for subgraph in self.graphs:
            degree = np.array(subgraph.degree())
            argi = np.argsort(-degree).tolist()
            results.append(subgraph.vs.select(argi)['id'])

        print(results)
        return self.merge_results(results)

    def by_betweenness(self):
        """
        Return list of n first vertices indices sorted by their betweenness.

        :return: list of vertices indices sorted by betweenness
        """
        betweenness = np.array(self.graph.betweenness())
        return self._postprocess_result(np.argsort(-betweenness))

    def by_clustering_coefficient(self):
        """
        Return list of n first vertices indices sorted by their clustering coefficient (transitivity).
        IMPORTANT: in directed graph only mutual edges will be considered

        :return: list of vertices indices sorted by clustering coefficient
        """
        if self.graph.is_directed():
            mutual = np.where(self.graph.is_mutual())[0].tolist()
            g = self.graph.es.select(mutual).subgraph()
            g.to_undirected(combine_edges='first')
        else:
            g = self.graph
        transitivity = np.array(g.transitivity_local_undirected())
        return self._postprocess_result(np.argsort(-transitivity))

    def define_spread(self, model, param_value, depth):
        fcn = {
            'LT': linear_treshold,
            'IC': lambda *args, **kwargs: independent_cascade(*args, **kwargs, random_seed=self.random_seed)
        }.get(model)

        def spread(seeds):
            result = fcn(self.graph, initial_ids=seeds, param_value=param_value, depth=depth)
            return len(result)

        return spread

    def greedy(self, model='LT', param_value=None, depth=None):
        """
        Search for vertices indices that are the best seeds using greedy approach.

        :param model: model of social influence;
        currently only Linear Treshold (LT) and Independent Cascade (IC) are available
        :param param_value:
        :param depth: how many iterations will be in spreading simulations
        :return: list of ids of nodes considered as the best seeds
        """
        seeds = []
        candidates = self.graph.vs['id']
        spread = self.define_spread(model, param_value, depth)
        while len(seeds) < self.n:
            seeds.append(-1)
            scores = []
            for cand in candidates:
                seeds[-1] = cand
                scores.append(spread(seeds))
            best_candid = candidates[np.argmax(scores)]
            seeds[-1] = best_candid
            candidates.remove(best_candid)
        return self._postprocess_result(seeds)

    def brute_force(self, model='LT', param_value=None, depth=None):
        """
        Search for vertices indices that are the best seeds using brute force approach.

        :param model: model of social influence;
        currently only Linear Treshold (LT) and Independent Cascade (IC) are available
        :param param_value:
        :param depth: how many iterations will be in spreading simulations
        :return: list of ids vertices indices that are the best seeds
        """
        best_score = 0
        best_seeds = []

        spread = self.define_spread(model, param_value, depth)

        for seeds in combinations(self.graph.vs['id'], self.n):
            current_score = spread(seeds)
            if current_score > best_score:
                best_seeds = seeds
                best_score = current_score

        return list(best_seeds)

    def CELFpp(self, model='LT', param_value=None, depth=None):
        """
        Search for vertices indices that are the best seeds using CELF++ approach.

        :param model: model of social influence;
        currently only Linear Treshold (LT) and Independent Cascade (IC) are available
        :param param_value:
        :param depth: how many iterations will be in spreading simulations
        :return: list of ids of nodes considered as the best seeds
        """
        spread = self.define_spread(model, param_value, depth)

        seeds = []
        seeds_size = 0
        seeds_spread = 0
        heap = []
        last_seed = None
        curr_best = None
        curr_best_score = -1

        for vid in self.graph.vs['id']:
            mg1 = spread([vid])
            mg2 = spread([vid, curr_best]) if curr_best is not None else mg1
            heap.append(Vpp(vid, mg1=mg1, prev_best=curr_best, mg2=mg2, flag=0))

            if mg1 > curr_best_score:
                curr_best_score = mg1
                curr_best = vid

        heapify(heap)

        while seeds_size < self.n:
            u = heap[0]
            if u.flag == seeds_size:
                heappop(heap)
                seeds.append(u.vid)
                seeds_size += 1
                seeds_spread += u.mg1
                last_seed = u.vid
                continue
            elif u.prev_best == last_seed:
                u.mg1 = u.mg2
            else:
                u.mg1 = spread([*seeds, u.vid]) - seeds_spread
                u.prev_best = curr_best
                u.mg2 = spread([*seeds, curr_best, u.vid]) - seeds_spread
            u.flag = seeds_size

            if u.mg1 > curr_best_score:
                curr_best_score = u.mg1
                curr_best = u.vid
            heapreplace(heap, u)

        return self._postprocess_result(seeds)


V = TypeVar("V", bound="Vpp")


class Vpp:
    """Store vertex id with additional properties required in CELF++ algorithm"""

    def __init__(self, vid: Any, mg1: int, prev_best: Any, mg2: int, flag: int) -> None:
        self.vid = vid
        self.mg1 = mg1
        self.prev_best = prev_best
        self.mg2 = mg2
        self.flag = flag

    def __eq__(self, o: V) -> bool:
        return (type(self) == type(o)
                and self.vid == o.vid
                and self.mg1 == o.mg1
                and self.prev_best == o.prev_best
                and self.mg2 == o.mg2
                and self.flag == o.flag)

    def __ne__(self, o: V) -> bool:
        return (type(self) != type(o)
                or self.vid != o.vid
                or self.mg1 != o.mg1
                or self.prev_best != o.prev_best
                or self.mg2 != o.mg2
                or self.flag != o.flag)

    def __str__(self) -> str:
        return f'Vpp({self.vid})'

    def __lt__(self, other) -> bool:
        return self.mg1 > other.mg1

    def __le__(self, other) -> bool:
        return self.mg1 >= other.mg1

    def __gt__(self, other) -> bool:
        return self.mg1 < other.mg1

    def __ge__(self, other) -> bool:
        return self.mg1 >= other.mg1
