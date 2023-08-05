from Fortuna import *
from datetime import datetime
import random  # Base Cases - for comparison only


if __name__ == "__main__":
    t0 = datetime.now()
    print("\nFortuna 0.20.6 Sample Distribution and Performance Test Suite\n")

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
    print(f"flex_cat(cat_key='Cat_A', n_samples=5) -> {flex_cat(cat_key='Cat_A', n_samples=5)}")
    print(f"flex_cat(cat_key='Cat_B', n_samples=5) -> {flex_cat(cat_key='Cat_B', n_samples=5)}")
    print(f"flex_cat(cat_key='Cat_C', n_samples=5) -> {flex_cat(cat_key='Cat_C', n_samples=5)}")
    print(f"\n{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec\n")
