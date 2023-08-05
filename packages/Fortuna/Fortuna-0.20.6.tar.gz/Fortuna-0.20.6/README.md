# Fortuna: Fast & Flexible Random Generators
Fortuna replaces some of the common functionality of Python's builtin Random module with specialized high performance functions. However, the true benefits of Fortuna are found in the class abstractions built on top of the core generators.

FlexCat is the crown jewel and the original driving force behind this entire project. FlexCat gives the user an easy way to build a categorized random value generator with configurable distribution patterns across two dimensions of data. FlexCat has nine unique distribution patterns to choose from.
```
I  Fortuna Core Functions
     a. Random Numbers
     b. Random Truth
     c. Random Sequence Values
     d. Random Table Values
     e. Utility Functions
II  Fortuna Abstraction Classes
     a. Random Cycle
     b. Quantum Monty
     c. Weighted Choice
     d. Flex Cat
III Test Suite
IV  Development Log
V   Legal Stuff... it's free and open.
```
## Fortuna Random Functions
### Random Numbers
`Fortuna.random_range(lo: int, hi: int) -> int`. Returns a random integer in range `[lo..hi]` inclusive. Up to 15x faster than `random.randint()`. Flat uniform distribution.

`Fortuna.random_below(num: int) -> int`. Returns a random integer in the exclusive range `[0..num)` for positive values of num. Flat uniform distribution.

`Fortuna.d(sides: int) -> int`. Represents a single die roll of a given size die.
Returns a random integer in the range `[1..sides]`. Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int`. Returns a random integer in range `[rolls..(rolls * sides)]`. The return value represents the sum of multiple rolls of the same size die. Geometric distribution based on the number and size of the dice rolled. Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns random integer in the range `[-N..N]` where `N = abs(num)`. Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns random integer in the range `[-N..N]` where `N = abs(num)`. Zero peak geometric distribution, triangle.

`Fortuna.plus_or_minus_curve(num: int, bounded: bool=True) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in the target range `[-num..num]`. If bounded is False, less than 0.1% of the results will fall outside the target range by up to +/- num. This will not change the overall shape of the distribution curve. Zero centered gaussian distribution, stretched bell curve: mean = 0, variance = num / pi.

`Fortuna.zero_flat(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Flat uniform distribution.

`Fortuna.zero_cool(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Zero peak, geometric distribution, half triangle.

`Fortuna.zero_extreme(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Zero peak, gaussian distribution, half bell curve: mean = 0, variance = num / pi.

`Fortuna.max_cool(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Max peak (num), geometric distribution, half triangle.

`Fortuna.max_extreme(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Max peak (num), gaussian distribution, half bell curve: mean = num, variance = num / pi.

`Fortuna.mostly_middle(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Middle peak (num / 2), geometric distribution, half triangle.

`Fortuna.mostly_center(num: int) -> int`. Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. Middle peak (num / 2), gaussian distribution, bell curve: mean = num / 2, variance = num / pi.

### Random Truth
`Fortuna.percent_true(num: int) -> bool`. Always returns False if num is 0 or less, always returns True if num is 100 or more. Any value of num in range `[1..99]` will produce True or False. Returns a random Bool based on the probability of True as a percentage.

### Random Sequence Values
`Fortuna.random_value(arr) -> value`. Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. Up to 10x faster than random.choice().

`Fortuna.pop_random_value(arr: list) -> value`. Returns and removes a random value from a sequence list, uniform distribution, destructive. Not included in the test suite due to it's destructive nature. This is the only destructive function in the module, use with care. It will raise an error if the list is empty.

### Random Table Values
`Fortuna.cumulative_weighted_choice(table) -> value`. Core function for the WeightedChoice base class. Produces a custom distribution of values based on cumulative weights. Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. Weights must be unique positive integers. See WeightedChoice class for a more comprehensive solution that verifies and optimizes the table. Up to 15x faster than random.choices()

### Utility Functions
`Fortuna.min_max(num: int, lo: int, hi: int) -> int`. Used to force a number in to the range `[lo..hi]`. Returns num if it is already in the proper range. Returns lo if num is less than lo. Returns hi if num is greater than hi.

`Fortuna.analytic_continuation(func: staticmethod, num: int) -> int`. Used to map a positive only function to the negative number line for complete input domain coverage. The "C" version of this function is used throughout the Fortuna extension. The function to be analytically continued must take an integer as input and return an integer.

## Fortuna Random Classes
### Sequence Wrappers
#### Random Cycle: The Truffle Shuffle
Returns a random value from the sequence. Produces a uniform distribution with no consecutive duplicates and relatively few nearly-consecutive duplicates. Longer sequences will naturally push duplicates even farther apart. This behavior gives rise to output sequences that seem much less mechanical than other random value sequences.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the sequence.

```python
from Fortuna import RandomCycle


random_cycle = RandomCycle(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])

random_cycle()  # returns a random value, cycled uniform distribution.
random_cycle(n_samples=10)  # returns a list of 10 random values, cycled uniform distribution.
```

#### The Quantum Monty
A set of strategies for producing random values from a sequence where the probability
of each value is based on the monty you choose. For example: the mostly_front monty
produces random values where the beginning of the sequence is geometrically more common than the back. The Quantum Monty Algorithm results from overlapping the probability waves of six of the other eight methods. The distribution it produces is a gentle curve with a bump in the middle.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may vary slightly.

```python
from Fortuna import QuantumMonty


quantum_monty = QuantumMonty(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])

# Each of the following methods will return a random value from the sequence.
quantum_monty.mostly_front()    # Mostly from the front of the list (geometric descending)
quantum_monty.mostly_middle()   # Mostly from the middle of the list (geometric pyramid)
quantum_monty.mostly_back()     # Mostly from the back of the list (geometric ascending)
quantum_monty.mostly_first()    # Mostly from the very front of the list (stretched gaussian descending)
quantum_monty.mostly_center()   # Mostly from the very center of the list (stretched gaussian bell curve)
quantum_monty.mostly_last()     # Mostly from the very back of the list (stretched gaussian ascending)
quantum_monty.quantum_monty()   # Quantum Monty Algorithm. Overlapping probability waves.
quantum_monty.mostly_flat()     # Uniform flat distribution (see Fortuna.random_value)
quantum_monty.mostly_cycle()    # Cycled uniform flat distribution (see RandomCycle)

# Each of the methods can return a list of values as follows:
quantum_monty.mostly_cycle(n_samples=10)    # Returns a list of 10 random samples.
```

### Table & Dictionary Wrappers
#### Weighted Choice: Custom Rarity
Two strategies for selecting random values from a sequence where rarity counts. Both produce a custom distribution of values based on the weights of the values. Up to 10x faster than random.choices()

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must have a weight and a value.
- Weights must be integers. A future release may allow weights to be floats.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.
As a result: non-unique values will have their probabilities logically accumulated.
Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance.
The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

##### Cumulative Weight Strategy
_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cumulative_weighted_choice = CumulativeWeightedChoice((
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
))

cumulative_weighted_choice()  # returns a weighted random value
cumulative_weighted_choice(n_samples=10)  # returns a list of 10 weighted random values
```

##### Relative Weight Strategy

```python
from Fortuna import RelativeWeightedChoice


relative_weighted_choice = RelativeWeightedChoice((
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
))

relative_weighted_choice()  # returns a weighted random value
relative_weighted_choice(n_samples=10)  # returns a list of 10 weighted random values
```

#### FlexCat
FlexCat wraps a dictionary of keyed sequences, and takes two optional keyword arguments, y_bias and x_bias. The Y axis keys are accessed directly at call time, or randomized with one of the QuantumMonty methods specified by y_bias. The X axis sequences are always randomized with one of the QuantumMonty methods, specified by x_bias.

By default FlexCat will use `y_bias="front"` and `x_bias="cycle"` if not specified at initialization. This will make the top of the data structure geometrically more common than the bottom, and it produces a flat cycled distribution for each category independently. The name FlexCat is short for flexible category sequence value generator.

FlexCat requires at least three keyed sequence categories each with at least 3 values. Although FlexCat data need not be square, the minimum size is 3x3.

Options for X & Y bias: _See QuantumMonty for details about each of these._
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, stretched gaussian descending
- center, stretched gaussian bell curve
- last, stretched gaussian ascending
- flat, uniform flat
- cycle, cycled uniform flat
- monty, Quantum Monty Algorithm

```python
from Fortuna import FlexCat


flex_cat = FlexCat({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}, y_bias="cycle", x_bias="cycle")

flex_cat()          # returns random value from a random category

flex_cat("Cat_A")   # returns random value from "Cat_A"
flex_cat("Cat_B")   # returns random value from "Cat_B"
flex_cat("Cat_C")   # returns random value from "Cat_C"

flex_cat(n_samples=10)              # returns a list of 10 random values
flex_cat("Cat_A", n_samples=10)     # returns a list of 10 random values from "Cat_A"
```

## Fortuna Test Suite
#### Testbed:
- **Software** _macOS 10.14.1, Python 3.7.1, Fortuna_
- **Hardware** _Intel 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD_

```
Fortuna 0.20.6 Sample Distribution and Performance Test Suite

Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 100000: Total: 130.574 ms, Average: 1305.74 nano
 1: 10.074%
 2: 9.966%
 3: 10.015%
 4: 10.087%
 5: 10.021%
 6: 9.979%
 7: 10.03%
 8: 9.945%
 9: 9.888%
 10: 9.995%

random_range(1, 10) x 100000: Total: 8.178 ms, Average: 81.78 nano
 1: 10.137%
 2: 9.894%
 3: 9.952%
 4: 9.992%
 5: 10.097%
 6: 9.993%
 7: 9.846%
 8: 9.985%
 9: 10.281%
 10: 9.823%

Base Case:
random.randrange(10) x 100000: Total: 91.247 ms, Average: 912.47 nano
 0: 9.934%
 1: 9.99%
 2: 10.015%
 3: 9.997%
 4: 10.119%
 5: 9.91%
 6: 10.112%
 7: 9.876%
 8: 9.933%
 9: 10.114%

random_below(10) x 100000: Total: 7.907 ms, Average: 79.07 nano
 0: 10.085%
 1: 9.984%
 2: 9.899%
 3: 9.857%
 4: 9.971%
 5: 9.965%
 6: 10.154%
 7: 10.229%
 8: 10.008%
 9: 9.848%

d(10) x 100000: Total: 8.013 ms, Average: 80.13 nano
 1: 10.182%
 2: 10.001%
 3: 10.153%
 4: 9.878%
 5: 10.015%
 6: 9.871%
 7: 10.147%
 8: 9.789%
 9: 9.89%
 10: 10.074%

dice(2, 6) x 100000: Total: 10.479 ms, Average: 104.79 nano
 2: 2.754%
 3: 5.631%
 4: 8.491%
 5: 11.086%
 6: 13.845%
 7: 16.565%
 8: 13.767%
 9: 11.041%
 10: 8.377%
 11: 5.564%
 12: 2.879%

plus_or_minus(5) x 100000: Total: 7.716 ms, Average: 77.16 nano
 -5: 9.203%
 -4: 9.193%
 -3: 9.118%
 -2: 9.248%
 -1: 8.979%
 0: 9.121%
 1: 9.036%
 2: 9.168%
 3: 8.994%
 4: 8.955%
 5: 8.985%

plus_or_minus_linear(5) x 100000: Total: 10.249 ms, Average: 102.49 nano
 -5: 2.798%
 -4: 5.472%
 -3: 8.328%
 -2: 11.079%
 -1: 13.776%
 0: 16.887%
 1: 14.004%
 2: 11.088%
 3: 8.468%
 4: 5.455%
 5: 2.645%

plus_or_minus_curve(5) x 100000: Total: 12.045 ms, Average: 120.45 nano
 -5: 0.205%
 -4: 1.158%
 -3: 4.379%
 -2: 11.729%
 -1: 20.196%
 0: 24.719%
 1: 20.293%
 2: 11.592%
 3: 4.44%
 4: 1.13%
 5: 0.159%

plus_or_minus_curve(5, bounded=False) x 100000: Total: 13.082 ms, Average: 130.82 nano
 -7: 0.003%
 -6: 0.028%
 -5: 0.215%
 -4: 1.135%
 -3: 4.378%
 -2: 11.449%
 -1: 20.479%
 0: 24.518%
 1: 20.473%
 2: 11.377%
 3: 4.532%
 4: 1.178%
 5: 0.206%
 6: 0.027%
 7: 0.002%

zero_flat(10) x 100000: Total: 7.503 ms, Average: 75.03 nano
 0: 9.151%
 1: 8.952%
 2: 9.053%
 3: 9.143%
 4: 9.179%
 5: 9.03%
 6: 9.1%
 7: 9.286%
 8: 8.978%
 9: 9.092%
 10: 9.036%

zero_cool(10) x 100000: Total: 16.885 ms, Average: 168.85 nano
 0: 16.588%
 1: 15.124%
 2: 13.679%
 3: 12.075%
 4: 10.606%
 5: 9.107%
 6: 7.625%
 7: 6.073%
 8: 4.511%
 9: 3.06%
 10: 1.552%

zero_extreme(10) x 100000: Total: 18.569 ms, Average: 185.69 nano
 0: 22.292%
 1: 21.177%
 2: 18.181%
 3: 14.34%
 4: 10.101%
 5: 6.543%
 6: 3.833%
 7: 1.989%
 8: 0.973%
 9: 0.408%
 10: 0.163%

max_cool(10) x 100000: Total: 16.728 ms, Average: 167.28 nano
 0: 1.495%
 1: 3.068%
 2: 4.443%
 3: 6.052%
 4: 7.615%
 5: 9.248%
 6: 10.695%
 7: 11.867%
 8: 13.741%
 9: 15.236%
 10: 16.54%

max_extreme(10) x 100000: Total: 18.431 ms, Average: 184.31 nano
 0: 0.144%
 1: 0.438%
 2: 0.994%
 3: 2.022%
 4: 3.895%
 5: 6.617%
 6: 10.105%
 7: 14.214%
 8: 18.263%
 9: 21.056%
 10: 22.252%

mostly_middle(10) x 100000: Total: 10.521 ms, Average: 105.21 nano
 0: 2.706%
 1: 5.622%
 2: 8.353%
 3: 11.09%
 4: 13.966%
 5: 16.489%
 6: 13.923%
 7: 11.006%
 8: 8.378%
 9: 5.594%
 10: 2.873%

mostly_center(10) x 100000: Total: 12.085 ms, Average: 120.85 nano
 0: 0.218%
 1: 1.15%
 2: 4.458%
 3: 11.371%
 4: 20.397%
 5: 24.565%
 6: 20.495%
 7: 11.507%
 8: 4.458%
 9: 1.178%
 10: 0.203%


Random Truth
-------------------------------------------------------------------------

percent_true(25) x 100000: Total: 7.091 ms, Average: 70.91 nano
 False: 75.263%
 True: 24.737%


Random Values from a Sequence
-------------------------------------------------------------------------

some_list = ('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')

Base Case:
random.choice(some_list) x 100000: Total: 73.907 ms, Average: 739.07 nano
 Alpha: 14.649%
 Beta: 14.129%
 Delta: 14.336%
 Eta: 14.151%
 Gamma: 14.25%
 Kappa: 14.323%
 Zeta: 14.162%

random_value(some_list) x 100000: Total: 6.846 ms, Average: 68.46 nano
 Alpha: 14.14%
 Beta: 14.215%
 Delta: 14.298%
 Eta: 14.421%
 Gamma: 14.364%
 Kappa: 14.228%
 Zeta: 14.334%

monty = Fortuna.QuantumMonty(
	('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')
)

monty.mostly_flat() x 100000: Total: 13.357 ms, Average: 133.57 nano
 Alpha: 14.544%
 Beta: 14.32%
 Delta: 14.087%
 Eta: 14.146%
 Gamma: 14.369%
 Kappa: 14.32%
 Zeta: 14.214%

monty.mostly_middle() x 100000: Total: 18.938 ms, Average: 189.38 nano
 Alpha: 6.166%
 Beta: 12.499%
 Delta: 18.846%
 Eta: 25.061%
 Gamma: 18.645%
 Kappa: 12.574%
 Zeta: 6.209%

monty.mostly_center() x 100000: Total: 21.856 ms, Average: 218.56 nano
 Alpha: 0.487%
 Beta: 5.35%
 Delta: 24.245%
 Eta: 39.913%
 Gamma: 24.316%
 Kappa: 5.285%
 Zeta: 0.404%

monty.mostly_front() x 100000: Total: 25.156 ms, Average: 251.56 nano
 Alpha: 24.917%
 Beta: 21.529%
 Delta: 17.95%
 Eta: 14.209%
 Gamma: 10.719%
 Kappa: 7.197%
 Zeta: 3.479%

monty.mostly_back() x 100000: Total: 23.854 ms, Average: 238.54 nano
 Alpha: 3.585%
 Beta: 7.178%
 Delta: 10.653%
 Eta: 14.169%
 Gamma: 17.906%
 Kappa: 21.438%
 Zeta: 25.071%

monty.mostly_first() x 100000: Total: 27.294 ms, Average: 272.94 nano
 Alpha: 34.36%
 Beta: 29.884%
 Delta: 19.956%
 Eta: 10.302%
 Gamma: 4.045%
 Kappa: 1.148%
 Zeta: 0.305%

monty.mostly_last() x 100000: Total: 28.348 ms, Average: 283.48 nano
 Alpha: 0.297%
 Beta: 1.234%
 Delta: 4.031%
 Eta: 10.311%
 Gamma: 19.694%
 Kappa: 30.101%
 Zeta: 34.332%

monty.quantum_monty() x 100000: Total: 35.756 ms, Average: 357.56 nano
 Alpha: 11.479%
 Beta: 12.845%
 Delta: 16.006%
 Eta: 19.094%
 Gamma: 15.938%
 Kappa: 12.872%
 Zeta: 11.766%

monty.mostly_cycle() x 100000: Total: 81.999 ms, Average: 819.99 nano
 Alpha: 14.304%
 Beta: 14.273%
 Delta: 14.284%
 Eta: 14.295%
 Gamma: 14.299%
 Kappa: 14.263%
 Zeta: 14.282%

monty.mostly_flat(n_samples=5) -> ['Gamma', 'Gamma', 'Eta', 'Beta', 'Zeta']
monty.mostly_middle(n_samples=5) -> ['Eta', 'Gamma', 'Zeta', 'Kappa', 'Eta']
monty.mostly_center(n_samples=5) -> ['Delta', 'Delta', 'Gamma', 'Delta', 'Delta']
monty.mostly_front(n_samples=5) -> ['Delta', 'Alpha', 'Delta', 'Beta', 'Beta']
monty.mostly_back(n_samples=5) -> ['Delta', 'Gamma', 'Kappa', 'Gamma', 'Kappa']
monty.mostly_first(n_samples=5) -> ['Delta', 'Alpha', 'Beta', 'Delta', 'Delta']
monty.mostly_last(n_samples=5) -> ['Beta', 'Zeta', 'Kappa', 'Kappa', 'Kappa']
monty.mostly_cycle(n_samples=5) -> ['Zeta', 'Alpha', 'Delta', 'Gamma', 'Beta']

random_cycle = Fortuna.RandomCycle(
	('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')
)

random_cycle() x 100000: Total: 72.645 ms, Average: 726.45 nano
 Alpha: 14.278%
 Beta: 14.29%
 Delta: 14.27%
 Eta: 14.259%
 Gamma: 14.357%
 Kappa: 14.234%
 Zeta: 14.312%

random_cycle(n_samples=5) -> ['Kappa', 'Delta', 'Beta', 'Alpha', 'Zeta']


Random Values by Weighted Table
-------------------------------------------------------------------------

population = ('Apple', 'Banana', 'Cherry', 'Grape', 'Lime', 'Orange')
cum_weights = (7, 11, 13, 23, 26, 30)
rel_weights = (7, 4, 2, 10, 3, 4)

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 100000: Total: 187.335 ms, Average: 1873.35 nano
 Apple: 23.274%
 Banana: 13.498%
 Cherry: 6.649%
 Grape: 33.302%
 Lime: 9.972%
 Orange: 13.305%

Relative Base Case:
random.choices(pop, rel_weights) x 100000: Total: 224.429 ms, Average: 2244.29 nano
 Apple: 23.188%
 Banana: 13.404%
 Cherry: 6.651%
 Grape: 33.256%
 Lime: 10.123%
 Orange: 13.378%

cumulative_table = ((7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange'))

Fortuna.cumulative_weighted_choice(cumulative_table) x 100000: Total: 14.26 ms, Average: 142.6 nano
 Apple: 23.268%
 Banana: 13.322%
 Cherry: 6.68%
 Grape: 33.399%
 Lime: 10.004%
 Orange: 13.327%

cumulative_choice = CumulativeWeightedChoice(
	((7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange'))
)

cumulative_choice() x 100000: Total: 29.628 ms, Average: 296.28 nano
 Apple: 23.365%
 Banana: 13.11%
 Cherry: 6.746%
 Grape: 33.368%
 Lime: 10.079%
 Orange: 13.332%

cumulative_choice(n_samples=5) -> ['Grape', 'Cherry', 'Lime', 'Grape', 'Banana']

relative_choice = RelativeWeightedChoice(
	((7, 'Apple'), (4, 'Banana'), (2, 'Cherry'), (10, 'Grape'), (3, 'Lime'), (4, 'Orange'))
)

relative_choice() x 100000: Total: 30.211 ms, Average: 302.11 nano
 Apple: 23.345%
 Banana: 13.248%
 Cherry: 6.491%
 Grape: 33.547%
 Lime: 10.019%
 Orange: 13.35%

relative_choice(n_samples=5) -> ['Orange', 'Apple', 'Orange', 'Grape', 'Cherry']

Random Values by Category
-------------------------------------------------------------------------

flex_cat = FlexCat(
	{'Cat_A': ('A1', 'A2', 'A3'), 'Cat_B': ('B1', 'B2', 'B3'), 'Cat_C': ('C1', 'C2', 'C3')},
	y_bias='front', x_bias='back'
)

flex_cat('Cat_A') x 100000: Total: 41.606 ms, Average: 416.06 nano
 A1: 16.59%
 A2: 33.369%
 A3: 50.041%

flex_cat('Cat_B') x 100000: Total: 41.361 ms, Average: 413.61 nano
 B1: 16.912%
 B2: 33.201%
 B3: 49.887%

flex_cat('Cat_C') x 100000: Total: 40.988 ms, Average: 409.88 nano
 C1: 16.513%
 C2: 33.429%
 C3: 50.058%

flex_cat() x 100000: Total: 61.87 ms, Average: 618.7 nano
 A1: 8.397%
 A2: 16.647%
 A3: 25.148%
 B1: 5.392%
 B2: 11.299%
 B3: 16.477%
 C1: 2.786%
 C2: 5.652%
 C3: 8.202%

flex_cat(n_samples=5) -> ['A3', 'C3', 'C3', 'A3', 'A3']
flex_cat(cat_key='Cat_A', n_samples=5) -> ['A3', 'A3', 'A3', 'A3', 'A3']
flex_cat(cat_key='Cat_B', n_samples=5) -> ['B3', 'B1', 'B3', 'B3', 'B3']
flex_cat(cat_key='Cat_C', n_samples=5) -> ['C2', 'C3', 'C1', 'C2', 'C1']

-------------------------------------------------------------------------
Total Test Time: 2.06 sec

```

## Fortuna Development Log
##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can return a list of samples rather than just one,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can return a list of samples rather than just one,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can return a list of samples rather than just one,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can return a list of samples rather than just one,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random.choices()
- Added Base Case for randint_dice()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna


## Legal Stuff
Fortuna :: Copyright (c) 2018 Broken aka Robert W. Sharp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

This README.md file shall be included in all copies or portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
