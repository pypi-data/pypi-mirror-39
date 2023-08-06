import random
from datetime import datetime


def analytic_continuation(func: staticmethod, num: int) -> int:
    if num < 0:
        return -func(-num)
    elif num == 0:
        return 0
    else:
        return func(num)


def random_range(lo: int, hi: int) -> int:
    if lo < hi:
        return random.randrange(lo, hi + 1)
    elif lo == hi:
        return lo
    else:
        return random_range(hi, lo)


def random_below(num: int) -> int:
    if num > 0:
        return random.randrange(0, num)
    else:
        return analytic_continuation(random_below, num)


def d(sides: int) -> int:
    if sides > 0:
        return random_range(1, sides)
    else:
        return analytic_continuation(d, sides)


def dice(rolls: int, sides: int) -> int:
    if rolls > 0:
        return sum(d(sides) for _ in range(rolls))
    elif rolls == 0:
        return 0
    else:
        return -dice(-rolls, sides)


def min_max(num: int, lo: int, hi: int) -> int:
    return min(max(num, lo), hi)


def percent_true(num: int) -> bool:
    return d(100) <= num


def plus_or_minus(num: int) -> int:
    return random_range(-num, num)


def plus_or_minus_linear(num: int) -> int:
    n = abs(num)
    return dice(2, n + 1) - (n + 2)


def plus_or_minus_curve(num: int, bounded: bool = True) -> int:
    def stretched_bell(x):
        pi = 3.14159265359
        return round(random.gauss(0.0, x / pi))
    n = abs(num)
    result = stretched_bell(n)
    while bounded and (result < -n or result > n):
        result = stretched_bell(n)
    return result


def zero_flat(num: int) -> int:
    return random_range(0, num)


def zero_cool(num: int) -> int:
    if num > 0:
        result = plus_or_minus_linear(num)
        while result < 0:
            result = plus_or_minus_linear(num)
        return result
    else:
        return analytic_continuation(zero_cool, num)


def zero_extreme(num: int) -> int:
    if num > 0:
        result = plus_or_minus_curve(num)
        while result < 0:
            result = plus_or_minus_curve(num)
        return result
    else:
        return analytic_continuation(zero_extreme, num)

    
def max_cool(num: int) -> int:
    if num > 0:
        return num - zero_cool(num)
    else:
        return analytic_continuation(max_cool, num)


def max_extreme(num: int) -> int:
    if num > 0:
        return num - zero_extreme(num)
    else:
        return analytic_continuation(max_extreme, num)


def mostly_middle(num: int) -> int:
    if num > 0:
        mid_point = num // 2
        if num % 2 == 0:
            return plus_or_minus_linear(mid_point) + mid_point
        elif percent_true(50):
            return max_cool(mid_point)
        else:
            return 1 + zero_cool(mid_point) + mid_point
    else:
        return analytic_continuation(mostly_middle, num)


def mostly_center(num: int) -> int:
    if num > 0:
        mid_point = num // 2
        if num % 2 == 0:
            return plus_or_minus_curve(mid_point) + mid_point
        elif percent_true(50):
            return max_extreme(mid_point)
        else:
            return 1 + zero_extreme(mid_point) + mid_point
    else:
        return analytic_continuation(mostly_center, num)


def random_value(arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr[random_below(size)]


def pop_random_value(arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr.pop(random_below(size))


def cumulative_weighted_choice(table):
    max_weight = table[-1][0]
    rand = random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


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


def distribution_timer(func: staticmethod, *args, call_sig=None, max_distribution=50, num_cycles=10000, **kwargs):
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
    total_time_ms = round(total_time * 1000.0, 2)
    average_time_nano = round((total_time_ms / num_cycles) * 1000000)
    print(f"{call_sig} x {num_cycles}: Total time: {total_time_ms} ms, Average time: {average_time_nano} nano")
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


if __name__ == "__main__":
    t0 = datetime.now()
    print("\nFortuna Pure 0.20.7 Sample Distribution and Performance Test Suite\n")

    print("Random Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10)
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random_below, 10)
    distribution_timer(d, 10)
    distribution_timer(dice, 2, 6)
    distribution_timer(plus_or_minus, 5)
    distribution_timer(plus_or_minus_linear, 5)
    distribution_timer(plus_or_minus_curve, 5)
    distribution_timer(plus_or_minus_curve, 5, bounded=False, call_sig="plus_or_minus_curve(5, bounded=False)"),
    distribution_timer(zero_flat, 10)
    distribution_timer(zero_cool, 10)
    distribution_timer(zero_extreme, 10)
    distribution_timer(max_cool, 10)
    distribution_timer(max_extreme, 10)
    distribution_timer(mostly_middle, 10)
    distribution_timer(mostly_center, 10)

    print("\nRandom Truth")
    print(f"{'-' * 73}\n")
    distribution_timer(percent_true, 25)

    print("\nRandom Values from a Sequence")
    print(f"{'-' * 73}\n")
    some_list = ("Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta")
    print(f"some_list = {some_list}\n")
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="random_value(some_list)")
    monty = QuantumMonty(some_list)
    print(f"monty = Fortuna.{monty}\n")
    distribution_timer(monty.mostly_flat, call_sig="monty.mostly_flat()")
    distribution_timer(monty.mostly_middle, call_sig="monty.mostly_middle()")
    distribution_timer(monty.mostly_center, call_sig="monty.mostly_center()")
    distribution_timer(monty.mostly_front, call_sig="monty.mostly_front()")
    distribution_timer(monty.mostly_back, call_sig="monty.mostly_back()")
    distribution_timer(monty.mostly_first, call_sig="monty.mostly_first()")
    distribution_timer(monty.mostly_last, call_sig="monty.mostly_last()")
    distribution_timer(monty.quantum_monty, call_sig="monty.quantum_monty()")
    distribution_timer(monty.mostly_cycle, call_sig="monty.mostly_cycle()")

    print(f"monty.mostly_flat(n_samples=5) -> {monty.mostly_flat(n_samples=5)}")
    print(f"monty.mostly_middle(n_samples=5) -> {monty.mostly_middle(n_samples=5)}")
    print(f"monty.mostly_center(n_samples=5) -> {monty.mostly_center(n_samples=5)}")
    print(f"monty.mostly_front(n_samples=5) -> {monty.mostly_front(n_samples=5)}")
    print(f"monty.mostly_back(n_samples=5) -> {monty.mostly_back(n_samples=5)}")
    print(f"monty.mostly_first(n_samples=5) -> {monty.mostly_first(n_samples=5)}")
    print(f"monty.mostly_last(n_samples=5) -> {monty.mostly_last(n_samples=5)}")
    print(f"monty.mostly_cycle(n_samples=5) -> {monty.mostly_cycle(n_samples=5)}\n")

    random_cycle = RandomCycle(some_list)
    print(f"random_cycle = Fortuna.{random_cycle}\n")
    distribution_timer(random_cycle, call_sig="random_cycle()")
    print(f"random_cycle(n_samples=5) -> {random_cycle(n_samples=5)}\n")

    print("\nRandom Values by Weighted Table")
    print(f"{'-' * 73}\n")
    population = ("Apple", "Banana", "Cherry", "Grape", "Lime", "Orange")
    cum_weights = (7, 11, 13, 23, 26, 30)
    rel_weights = (7, 4, 2, 10, 3, 4)
    print(f"population = {population}")
    print(f"cum_weights = {cum_weights}")
    print(f"rel_weights = {rel_weights}\n")
    distribution_timer(
        random.choices, population, cum_weights=cum_weights,
        call_sig="Cumulative Base Case:\nrandom.choices(pop, cum_weights=cum_weights)"
    )
    distribution_timer(
        random.choices, population, rel_weights,
        call_sig="Relative Base Case:\nrandom.choices(pop, rel_weights)"
    )
    cumulative_table = (
        (7, "Apple"),
        (11, "Banana"),
        (13, "Cherry"),
        (23, "Grape"),
        (26, "Lime"),
        (30, "Orange"),
    )
    print(f"cumulative_table = {cumulative_table}\n")
    distribution_timer(
        cumulative_weighted_choice, cumulative_table,
        call_sig="Fortuna.cumulative_weighted_choice(cumulative_table)"
    )
    cumulative_choice = CumulativeWeightedChoice(cumulative_table)
    print(f"cumulative_choice = {cumulative_choice}\n")
    distribution_timer(cumulative_choice, call_sig="cumulative_choice()")
    print(f"cumulative_choice(n_samples=5) -> {cumulative_choice(n_samples=5)}\n")

    relative_table = (
        (7, "Apple"),
        (4, "Banana"),
        (2, "Cherry"),
        (10, "Grape"),
        (3, "Lime"),
        (4, "Orange"),
    )
    relative_choice = RelativeWeightedChoice(relative_table)
    print(f"relative_choice = {relative_choice}\n")
    distribution_timer(relative_choice, call_sig="relative_choice()")
    print(f"relative_choice(n_samples=5) -> {relative_choice(n_samples=5)}\n")

    print("Random Values by Category")
    print(f"{'-' * 73}\n")
    flex_cat = FlexCat(
        {'Cat_A': ('A1', 'A2', 'A3'), 'Cat_B': ('B1', 'B2', 'B3'), 'Cat_C': ('C1', 'C2', 'C3')},
        y_bias='front', x_bias='back'
    )
    print(f"flex_cat = {flex_cat}\n")
    for cat in flex_cat.cat_keys:
        distribution_timer(flex_cat, cat, call_sig=f"flex_cat('{cat}')")
    distribution_timer(flex_cat, call_sig="flex_cat()")
    print(f"flex_cat(n_samples=5) -> {flex_cat(n_samples=5)}")
    print(f"flex_cat('Cat_A', n_samples=5) -> {flex_cat('Cat_A', n_samples=5)}")
    print(f"flex_cat('Cat_B', n_samples=5) -> {flex_cat('Cat_B', n_samples=5)}")
    print(f"flex_cat('Cat_C', n_samples=5) -> {flex_cat('Cat_C', n_samples=5)}")
    print(f"\n{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec\n")
