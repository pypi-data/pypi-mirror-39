from abc import ABCMeta, abstractmethod

from copy import deepcopy

from itertools import product

from numbers import Real

from typing import Any, Dict, Iterator, List


class Variation(metaclass=ABCMeta):

    @abstractmethod
    def expand(self) -> List[Any]:
        """ Expands the variation to a list of values. """


class RangeVariation(Variation):

    def __init__(self, min_val: Real, max_val: Real, step: Real) -> None:
        self._min = min_val
        self._max = max_val
        self._step = step

    def expand(self) -> List[Any]:
        """ Expands the variation to a list of values. """
        values = []
        i = self._min
        while i < self._max:
            values.append(i)
            i += self._step
        values.append(self._max)

        return values


class ValuesVariation(Variation):

    def __init__(self, values: List[Any]) -> None:
        self._values = values

    def expand(self) -> List[Any]:
        return self._values


def explode_variations(base_data: Dict[str, Any], variations: Dict[str, Variation]) -> Iterator[Dict[Any, Any]]:
    """ Blows up variations into a list from a range dict and some default parameters. """
    keys = []  # Preserve order
    value_ranges = []
    for k, var_object in variations.items():
        keys.append(k)
        value_ranges.append(var_object.expand())

    combined = list(product(*value_ranges))
    for combination in combined:
        copied = deepcopy(base_data)
        for i, v in enumerate(combination):
            k = keys[i]
            subsect = copied
            while '.' in k:
                prefix, rest = k.split('.', 1)
                k = rest
                subsect = subsect[prefix]
            subsect[k] = v
        yield copied
