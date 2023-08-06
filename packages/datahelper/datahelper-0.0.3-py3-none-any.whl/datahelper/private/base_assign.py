from itertools import zip_longest

from datahelper import pick
from datahelper.private.base_set import base_set
from datahelper.private.create import create


def base_assign(obj, paths, value):
    if not isinstance(obj, dict):
        return obj

    pathways = paths.split('.').copy()
    last_path = pathways[-1]
    tree = [obj]
    result = None

    for index, path in enumerate(pathways):
        parent = tree[index]
        [curr] = pick(parent, path)

        if not curr or isinstance(curr, (str, int)):
            curr = create(path)

        tree.append(curr)

    graph = list(zip_longest(pathways, tree, tree[1:]))
    graph = graph[:-1]

    while graph:
        path, parent, child = graph.pop()

        if path is last_path:
            result = base_set(parent, path, value)
            continue

        result = base_set(parent, path, result)

    return result


def main():
    data = {'a': 1, 'b': {'c': 3}}
    result = base_assign(data, 'a.b.c', {'d': 1})
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
