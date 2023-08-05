import random

import igraph as ig


def linear_treshold(graph: ig.Graph, initial_ids, param_value=None, depth=None):
    g = graph.copy()
    depth = depth or float('inf')

    if 'treshold' not in g.vertex_attributes():
        _apply_param(g, 'treshold', param_value)

    g.vs['influenced'] = False
    g.vs.select(id_in=initial_ids)['influenced'] = True
    influenced_ids = set(initial_ids)

    new_influenced = initial_ids
    i = 0
    while len(new_influenced) > 0 and i < depth:
        uninfluenced = g.vs.select(influenced=False)
        new_influenced = []

        for v in uninfluenced:
            inf_neigh = g.vs.select(g.neighbors(v, mode=ig.IN), influenced=True)
            es = g.es.select(_target=v['id'], _source_in=inf_neigh['id'])

            if inf_neigh and sum(es['weight']) >= v['treshold']:
                v['influenced'] = True
                new_influenced.append(v['id'])

        influenced_ids.update(new_influenced)
        i += 1

    return influenced_ids


def independent_cascade(graph: ig.Graph, initial_ids, param_value=None, depth=None, random_seed=None):
    if random_seed:
        random.seed(random_seed)
    g = graph.copy()
    depth = depth or float('inf')

    if 'treshold' not in g.vertex_attributes():
        _apply_param(g, 'treshold', param_value)

    g.vs['influenced'] = False
    g.vs['retired'] = False
    g.vs.select(id_in=initial_ids)['influenced'] = True
    influenced_ids = set(initial_ids)

    new_influenced = initial_ids
    i = 0
    while len(new_influenced) > 0 and i < depth:
        influencers = g.vs.select(new_influenced)
        new_influenced = []

        for v in influencers:
            healthy_neigh = g.vs.select(g.neighbors(v, mode=ig.OUT), influenced=False)

            for exposed in healthy_neigh:
                r = random.random()
                assert r is not None
                if r >= v['treshold']:
                    exposed['influenced'] = True
                    new_influenced.append(exposed['id'])

            v['retired'] = True

        influenced_ids.update(new_influenced)
        i += 1

    return influenced_ids


def _apply_param(g, param_name, value=None):
    if value is not None and not callable(value):
        g.vs[param_name] = value
    else:
        tresholdf = value or random.random
        g.vs[param_name] = [tresholdf() for _ in range(len(g.vs))]
