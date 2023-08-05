#!python3
#distutils: language = c++
import random
from datetime import datetime


cdef extern from "Fortuna.hpp":
    int _random_range "random_range"(int, int)
    int _random_below "random_below"(int)
    int _d "d"(int)
    int _dice "dice"(int, int)
    int _min_max "min_max"(int, int, int)
    int _percent_true "percent_true"(int)
    int _plus_or_minus "plus_or_minus"(int)
    int _plus_or_minus_linear "plus_or_minus_linear"(int)
    int _plus_or_minus_curve "plus_or_minus_curve"(int, int)
    int _zero_flat "zero_flat"(int)
    int _zero_cool "zero_cool"(int)
    int _zero_extreme "zero_extreme"(int)
    int _max_cool "max_cool"(int)
    int _max_extreme "max_extreme"(int)
    int _mostly_middle "mostly_middle"(int)
    int _mostly_center "mostly_center"(int)
    int _fast_dice "fast_dice"(int, int)


def random_range(int lo, int hi) -> int:
    return _random_range(lo, hi)

def random_below(int num) -> int:
    return _random_below(num)

def d(int sides) -> int:
    return _d(sides)

def dice(int rolls, int sides) -> int:
    return _dice(rolls, sides)

def min_max(int n, int lo, int hi) -> int:
    return _min_max(n, lo, hi)

def percent_true(int num) -> bool:
    return _percent_true(_min_max(num, 0, 100)) == 1

def plus_or_minus(int num) -> int:
    return _plus_or_minus(num)

def plus_or_minus_linear(int num) -> int:
    return _plus_or_minus_linear(num)

def plus_or_minus_curve(int num, bounded=True) -> int:
    cdef int bound = 1 if bounded else 0
    return _plus_or_minus_curve(num, bound)

def zero_flat(int num) -> int:
    return _zero_flat(num)

def zero_cool(int num) -> int:
    return _zero_cool(num)

def zero_extreme(int num) -> int:
    return _zero_extreme(num)

def max_cool(int num) -> int:
    return _max_cool(num)

def max_extreme(int num) -> int:
    return _max_extreme(num)

def mostly_middle(int num) -> int:
    return _mostly_middle(num)

def mostly_center(int num) -> int:
    return _mostly_center(num)

def random_value(arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr[_random_below(size)]

def pop_random_value(list arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr.pop(_random_below(size))

def cumulative_weighted_choice(table):
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value

def fast_dice(int rolls, int sides) -> int:
    return _fast_dice(rolls, sides)


class RandomCycle:
    """ The Truffle Shuffle """
    __slots__ = ("data", "next", "size", "out_idx", "in_idx", "arr")

    def __init__(self, arr):
        self.arr = arr
        self.size = len(arr)
        assert self.size >= 3, f"Input Error, sequence length must be >= 3."
        self.data = list(arr)
        random.shuffle(self.data)
        self.next = self.data.pop()
        self.out_idx = len(self.data) - 1
        self.in_idx = len(self.data) - 2

    def __call__(self, n_samples: int = 1):
        if n_samples == 1:
            return self._cycle()
        else:
            return [self._cycle() for _ in range(n_samples)]

    def _cycle(self):
        result = self.next
        self.next = self.data.pop(max_extreme(self.out_idx))
        self.data.insert(zero_extreme(self.in_idx), result)
        return result

    def __repr__(self):
        return f"RandomCycle(\n\t{self.arr}\n)"


class QuantumMonty:
    __slots__ = ("data", "max_id", "random_cycle", "dispatch_methods", "monty_methods")

    def __init__(self, data):
        self.data = tuple(data)
        self.max_id = len(data) - 1
        self.random_cycle = RandomCycle(data)
        self.dispatch_methods = {
            "monty": self.quantum_monty,
            "cycle": self.mostly_cycle,
            "front": self.mostly_front,
            "middle": self.mostly_middle,
            "back": self.mostly_back,
            "first": self.mostly_first,
            "center": self.mostly_center,
            "last": self.mostly_last,
            "flat": self.mostly_flat,
        }
        self.monty_methods = (
            self.mostly_front,
            self.mostly_middle,
            self.mostly_back,
            self.mostly_first,
            self.mostly_center,
            self.mostly_last,
        )

    def __call__(self, n_samples: int = 1):
        return self.quantum_monty(n_samples)

    def __repr__(self):
        return f"QuantumMonty(\n\t{self.data}\n)"

    def dispatch(self, quantum_bias="monty"):
        return self.dispatch_methods[quantum_bias]

    def mostly_flat(self, n_samples: int = 1):
        if n_samples == 1:
            return random_value(self.data)
        else:
            return [random_value(self.data) for _ in range(n_samples)]

    def mostly_cycle(self, n_samples: int = 1):
        return self.random_cycle(n_samples)

    def mostly_front(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[zero_cool(self.max_id)]
        else:
            return [self.data[zero_cool(self.max_id)] for _ in range(n_samples)]

    def mostly_back(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[max_cool(self.max_id)]
        else:
            return [self.data[max_cool(self.max_id)] for _ in range(n_samples)]

    def mostly_middle(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[mostly_middle(self.max_id)]
        else:
            return [self.data[mostly_middle(self.max_id)] for _ in range(n_samples)]

    def mostly_first(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[zero_extreme(self.max_id)]
        else:
            return [self.data[zero_extreme(self.max_id)] for _ in range(n_samples)]

    def mostly_last(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[max_extreme(self.max_id)]
        else:
            return [self.data[max_extreme(self.max_id)] for _ in range(n_samples)]

    def mostly_center(self, n_samples: int = 1):
        if n_samples == 1:
            return self.data[mostly_center(self.max_id)]
        else:
            return [self.data[mostly_center(self.max_id)] for _ in range(n_samples)]

    def quantum_monty(self, n_samples: int = 1):
        if n_samples == 1:
            return random_value(self.monty_methods)()
        else:
            return [random_value(self.monty_methods)() for _ in range(n_samples)]


class WeightedChoice:
    __slots__ = ("data", "max_weight")

    def __call__(self, n_samples: int = 1):
        if n_samples == 1:
            return self.weighted_choice()
        else:
            return [self.weighted_choice() for _ in range(n_samples)]

    def weighted_choice(self):
        rand = random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value

    @staticmethod
    def _setup(weighted_table, is_cumulative, non_unique=False):
        size = len(weighted_table)
        assert size >= 1, f"Input Error, sequence length must be >= 1."
        if is_cumulative:
            assert size == len(set(w for w, _ in weighted_table)), "Cumulative Weights must be unique, because math."
        if non_unique:
            pass
        else:
            warn_non_unique = (
                "Sanity Check!",
                "  Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.",
                "  As a result: non-unique values will have their probabilities logically accumulated.",
                "  Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.",
            )
            assert size == len(set(v for _, v in weighted_table)), "\n".join(warn_non_unique)

    @staticmethod
    def _optimize(weighted_table, is_cumulative) -> list:
        if not is_cumulative:
            return sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        else:
            data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
            prev_weight = 0
            for w_pair in data:
                w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
            return sorted(data, key=lambda x: x[0], reverse=True)

    def _package(self, data) -> tuple:
        cum_weight = 0
        for w_pair in data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = data[-1][0]
        return tuple(tuple(itm) for itm in data)


class RelativeWeightedChoice(WeightedChoice):
    __slots__ = ("data", "max_weight", "weighted_table")

    def __init__(self, weighted_table, non_unique=False):
        self.weighted_table = weighted_table
        self._setup(weighted_table, is_cumulative=False, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=False)
        self.data = self._package(optimized_data)

    def __repr__(self):
        return f"RelativeWeightedChoice(\n\t{self.weighted_table}\n)"


class CumulativeWeightedChoice(WeightedChoice):
    __slots__ = ("data", "max_weight", "weighted_table")

    def __init__(self, weighted_table, non_unique=False):
        self.weighted_table = weighted_table
        self._setup(weighted_table, is_cumulative=True, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=True)
        self.data = self._package(optimized_data)

    def __repr__(self):
        return f"CumulativeWeightedChoice(\n\t{self.weighted_table}\n)"


class FlexCat:
    __slots__ = ("data", "cat_keys", "random_cat", "random_selection", "y_bias", "x_bias")

    def __init__(self, data, y_bias="front", x_bias="cycle"):
        self.data = data
        self.y_bias = y_bias
        self.x_bias = x_bias
        self.cat_keys = tuple(data.keys())
        self.random_cat = QuantumMonty(self.cat_keys).dispatch(y_bias)
        self.random_selection = {key: QuantumMonty(sequence).dispatch(x_bias) for key, sequence in data.items()}

    def _flex(self, cat_key: str):
        return self.random_selection[cat_key if cat_key else self.random_cat()]()

    def __call__(self, cat_key: str = "", n_samples: int = 1):
        if n_samples == 1:
            return self._flex(cat_key)
        else:
            return [self._flex(cat_key) for _ in range(n_samples)]

    def __repr__(self):
        return f"FlexCat(\n\t{self.data},\n\ty_bias='{self.y_bias}', x_bias='{self.x_bias}'\n)"


def distribution_timer(func: staticmethod, *args, call_sig=None, max_distribution=50, num_cycles=100000, **kwargs):
    start_time = datetime.now()
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    if call_sig:
        pass
    elif hasattr(func, "__qualname__"):
        if len(args) == 1:
            call_sig = f"{func.__qualname__}({args[0]})"
        else:
            call_sig = f"{func.__qualname__}{args}"
    else:
        call_sig = f"function(*args, **kwargs)"
    total_time_ms = round(total_time * 1000, 5)
    average_time_nano = round((total_time_ms / num_cycles) * 1000000, 2)
    print(f"{call_sig} x {num_cycles}: Total: {total_time_ms} ms, Average: {average_time_nano} nano")
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    unique_results = set(results)
    if len(unique_results) <= max_distribution:
        result_obj = {
            key: f"{results.count(key) / (num_cycles / 100)}%" for key in sorted(list(unique_results))
        }
        for key, val in result_obj.items():
            print(f" {key}: {val}")
    print("")


def analytic_continuation(func: staticmethod, num: int) -> int:
    if num < 0:
        return -func(-num)
    elif num == 0:
        return 0
    else:
        return func(num)
