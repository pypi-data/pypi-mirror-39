# Fortuna: Fast & Flexible Random Generators
Fortuna replaces some of the functionality of Python's builtin Random module with specialized high performance functions, often achieving 10x performance. However, the more interesting bits of Fortuna are found in the high-level abstractions like FlexCat and QuantumMonty.

Fortuna is designed, built and tested for MacOS X, it also happens to work out-of-the-box with many flavors of Linux.

Mac and Linux Installation: `pip3 install Fortuna` or download and build from source, if that's your thing. Compilation procedures are far beyond the scope of this project.

Windows users can use `.../fortuna_extras/fortuna_pure.py` instead of trying to install or compile the extension. The pure Python implementation provides the same API and functionality but lacks the performance of the Fortuna extension.
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
```
## Fortuna Random Functions
### Random Numbers
`Fortuna.random_range(lo: int, hi: int) -> int`. Returns a random integer in range [lo..hi] inclusive. Up to 15x faster than `random.randint()`. Flat uniform distribution.

`Fortuna.random_below(num: int) -> int`. Returns a random integer in the exclusive range [0..num) for positive values of num. Flat uniform distribution.

`Fortuna.d(sides: int) -> int`. Represents a single die roll of a given size die.
Returns a random integer in the range [1..sides]. Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int`. Returns a random integer in range [X..Y] where X = rolls and Y = rolls * sides. The return value represents the sum of multiple rolls of the same size die. Geometric distribution based on the number and size of the dice rolled. Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in range [-num..num]. Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in range [-num..num]. Zero peak geometric distribution, up triangle.

`Fortuna.plus_or_minus_curve(num: int, bounded: bool=True) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in range [-num..num]. If bounded is False, less than 0.1% of the results will fall outside the target range by up to +/- num. This will not change the overall shape of the distribution curve. Zero peak gaussian distribution, stretched bell curve: mean = 0, variance = num / pi.

`Fortuna.zero_flat(num: int) -> int`. Returns a random integer in range [0..num]. Flat uniform distribution.

`Fortuna.zero_cool(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, geometric distribution, half triangle.

`Fortuna.zero_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, gaussian distribution, half bell curve: mean = 0, variance = num / pi.

`Fortuna.max_cool(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), geometric distribution, half triangle.

`Fortuna.max_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), gaussian distribution, half bell curve: mean = num, variance = num / pi.

`Fortuna.mostly_middle(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), geometric distribution, up triangle. Ranges that span an even number of values will have two dominant values in the middle, this will guarantee that the probability distribution is always symmetrical.

`Fortuna.mostly_center(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), gaussian distribution, bell curve: mean = num / 2, variance = num / pi.

### Random Truth
`Fortuna.percent_true(num: int) -> bool`. Always returns False if num is 0 or less, always returns True if num is 100 or more. Any value of num in range [1..99] will produce True or False based on the value of num - the probability of True as a percentage.

### Random Sequence Values
`Fortuna.random_value(arr) -> value`. Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. Up to 10x faster than random.choice().

`Fortuna.pop_random_value(arr: list) -> value`. Returns and removes a random value from a sequence list, uniform distribution, destructive. Not included in the test suite due to it's destructive nature. This is the only destructive function in the module, use with care. It will raise an error if the list is empty.

### Random Table Values
`Fortuna.cumulative_weighted_choice(table) -> value`. Core function for the WeightedChoice base class. Produces a custom distribution of values based on cumulative weights. Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. Weights must be unique positive integers. See WeightedChoice class for a more comprehensive solution that verifies and optimizes the table. Up to 15x faster than random.choices()

### Utility Functions
`Fortuna.min_max(num: int, lo: int, hi: int) -> int`. Used to force a number in to the range [lo..hi]. Returns num if it is already in the proper range. Returns lo if num is less than lo. Returns hi if num is greater than hi.

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
FlexCat wraps a dictionary of sequences. When the primary method is called it returns a random value from one of the sequences. It takes two optional keyword arguments to specify the algorithms used to make random selections.

By default, FlexCat will use y_bias="front" and x_bias="cycle", this will make the top of the data structure geometrically more common than the bottom and cycle the sequences. This config is known as Top Cat, it produces a descending-step cycled distribution for the data. Many other combinations are possible (9 algorithms, 2 dimensions = 81 configs).

FlexCat requires a dict with at least three sequences with at least 3 values each. Even though the total value limit is much higher, data sets with more than one million values are not recommended for all platforms.

FlexCat generally works best if all sequences in a set are sufficiently large and close to the same size, this is not enforced. Values in a shorter sequence will naturally be more common, since probability balancing between categories is not considered. For example: in a flat/flat set where it might be expected that all values have equal probability (and they would, given sequences with equal length). However, values in a sequence half the size of the others in the set would have exactly double the probability of the other items. This effect scales with the size delta and affects all nine methods. Cross category balancing might be considered for a future release.

Algorithm Options: _See QuantumMonty & RandomCycle for more details._
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, stretched gaussian descending
- center, stretched gaussian bell
- last, stretched gaussian ascending
- flat, uniform flat
- cycle, RandomCycle uniform flat
- monty, The Quantum Monty

```python
from Fortuna import FlexCat


flex_cat = FlexCat({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}, y_bias="cycle", x_bias="cycle")

flex_cat()          # returns a random value from a random category

flex_cat("Cat_A")   # returns a random value from "Cat_A"
flex_cat("Cat_B")   #                             "Cat_B"
flex_cat("Cat_C")   #                             "Cat_C"

flex_cat(n_samples=10)              # returns a list of 10 random values
flex_cat("Cat_A", n_samples=10)     # returns a list of 10 random values from "Cat_A"
```

## Fortuna Test Suite
#### Testbed:
- **Software** _macOS 10.14.1, Python 3.7.1, Fortuna Beta_
- **Hardware** _Intel 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD_

```
Fortuna 0.20.10 Sample Distribution and Performance Test Suite

Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 100000: Total: 151.949 ms, Average: 1519.49 nano
 1: 10.016%
 2: 10.031%
 3: 10.172%
 4: 9.959%
 5: 10.04%
 6: 10.061%
 7: 9.817%
 8: 9.957%
 9: 10.045%
 10: 9.902%

random_range(1, 10) x 100000: Total: 10.143 ms, Average: 101.43 nano
 1: 9.951%
 2: 10.028%
 3: 9.992%
 4: 10.166%
 5: 9.83%
 6: 10.163%
 7: 10.114%
 8: 9.973%
 9: 9.852%
 10: 9.931%

Base Case:
random.randrange(10) x 100000: Total: 107.543 ms, Average: 1075.43 nano
 0: 9.985%
 1: 10.123%
 2: 9.87%
 3: 9.945%
 4: 10.023%
 5: 10.052%
 6: 10.002%
 7: 9.938%
 8: 9.989%
 9: 10.073%

random_below(10) x 100000: Total: 11.295 ms, Average: 112.95 nano
 0: 9.992%
 1: 10.127%
 2: 9.989%
 3: 9.938%
 4: 9.866%
 5: 10.023%
 6: 9.907%
 7: 10.174%
 8: 9.923%
 9: 10.061%

d(10) x 100000: Total: 10.568 ms, Average: 105.68 nano
 1: 9.843%
 2: 9.991%
 3: 10.169%
 4: 9.949%
 5: 10.046%
 6: 10.027%
 7: 10.13%
 8: 9.997%
 9: 9.958%
 10: 9.89%

dice(2, 6) x 100000: Total: 11.401 ms, Average: 114.01 nano
 2: 2.748%
 3: 5.584%
 4: 8.496%
 5: 10.987%
 6: 13.781%
 7: 16.579%
 8: 13.877%
 9: 11.217%
 10: 8.372%
 11: 5.601%
 12: 2.758%

plus_or_minus(5) x 100000: Total: 8.655 ms, Average: 86.55 nano
 -5: 8.907%
 -4: 9.058%
 -3: 9.159%
 -2: 9.186%
 -1: 9.052%
 0: 9.109%
 1: 9.191%
 2: 9.111%
 3: 9.111%
 4: 9.219%
 5: 8.897%

plus_or_minus_linear(5) x 100000: Total: 12.08 ms, Average: 120.8 nano
 -5: 2.781%
 -4: 5.422%
 -3: 8.419%
 -2: 11.142%
 -1: 13.743%
 0: 16.761%
 1: 13.928%
 2: 11.154%
 3: 8.356%
 4: 5.532%
 5: 2.762%

plus_or_minus_curve(5) x 100000: Total: 12.639 ms, Average: 126.39 nano
 -5: 0.209%
 -4: 1.14%
 -3: 4.343%
 -2: 11.519%
 -1: 20.612%
 0: 24.666%
 1: 20.172%
 2: 11.595%
 3: 4.378%
 4: 1.172%
 5: 0.194%

plus_or_minus_curve(5, bounded=False) x 100000: Total: 12.454 ms, Average: 124.54 nano
 -7: 0.004%
 -6: 0.028%
 -5: 0.183%
 -4: 1.184%
 -3: 4.379%
 -2: 11.453%
 -1: 20.56%
 0: 24.788%
 1: 20.086%
 2: 11.552%
 3: 4.373%
 4: 1.184%
 5: 0.201%
 6: 0.023%
 7: 0.002%

zero_flat(10) x 100000: Total: 7.149 ms, Average: 71.49 nano
 0: 9.184%
 1: 8.991%
 2: 9.264%
 3: 9.02%
 4: 9.071%
 5: 9.154%
 6: 8.946%
 7: 9.082%
 8: 9.002%
 9: 9.317%
 10: 8.969%

zero_cool(10) x 100000: Total: 17.182 ms, Average: 171.82 nano
 0: 16.764%
 1: 15.108%
 2: 13.457%
 3: 12.183%
 4: 10.734%
 5: 9.108%
 6: 7.698%
 7: 6.029%
 8: 4.533%
 9: 2.883%
 10: 1.503%

zero_extreme(10) x 100000: Total: 20.103 ms, Average: 201.03 nano
 0: 22.115%
 1: 21.136%
 2: 18.363%
 3: 14.449%
 4: 10.089%
 5: 6.503%
 6: 3.794%
 7: 1.992%
 8: 0.981%
 9: 0.416%
 10: 0.162%

max_cool(10) x 100000: Total: 18.12 ms, Average: 181.2 nano
 0: 1.508%
 1: 3.01%
 2: 4.442%
 3: 6.15%
 4: 7.62%
 5: 9.019%
 6: 10.81%
 7: 12.075%
 8: 13.502%
 9: 15.238%
 10: 16.626%

max_extreme(10) x 100000: Total: 19.333 ms, Average: 193.33 nano
 0: 0.143%
 1: 0.416%
 2: 1.062%
 3: 2.026%
 4: 3.736%
 5: 6.506%
 6: 10.065%
 7: 13.905%
 8: 18.382%
 9: 21.44%
 10: 22.319%

mostly_middle(10) x 100000: Total: 10.452 ms, Average: 104.52 nano
 0: 2.784%
 1: 5.444%
 2: 8.293%
 3: 11.037%
 4: 13.84%
 5: 16.87%
 6: 14.014%
 7: 11.223%
 8: 8.284%
 9: 5.453%
 10: 2.758%

mostly_center(10) x 100000: Total: 12.412 ms, Average: 124.12 nano
 0: 0.212%
 1: 1.199%
 2: 4.42%
 3: 11.462%
 4: 20.364%
 5: 24.591%
 6: 20.399%
 7: 11.596%
 8: 4.422%
 9: 1.151%
 10: 0.184%


Random Truth
-------------------------------------------------------------------------

percent_true(25) x 100000: Total: 7.087 ms, Average: 70.87 nano
 False: 75.069%
 True: 24.931%


Random Values from a Sequence
-------------------------------------------------------------------------

some_list = ('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')

Base Case:
random.choice(some_list) x 100000: Total: 77.314 ms, Average: 773.14 nano
 Alpha: 14.453%
 Beta: 14.449%
 Delta: 14.195%
 Eta: 14.218%
 Gamma: 14.25%
 Kappa: 14.377%
 Zeta: 14.058%

random_value(some_list) x 100000: Total: 7.494 ms, Average: 74.94 nano
 Alpha: 14.255%
 Beta: 14.23%
 Delta: 14.161%
 Eta: 14.232%
 Gamma: 14.296%
 Kappa: 14.337%
 Zeta: 14.489%

monty = Fortuna.QuantumMonty(
	('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')
)

monty.mostly_flat() x 100000: Total: 13.187 ms, Average: 131.87 nano
 Alpha: 14.217%
 Beta: 14.44%
 Delta: 14.171%
 Eta: 14.393%
 Gamma: 14.265%
 Kappa: 14.22%
 Zeta: 14.294%

monty.mostly_middle() x 100000: Total: 19.174 ms, Average: 191.74 nano
 Alpha: 6.387%
 Beta: 12.496%
 Delta: 18.661%
 Eta: 24.948%
 Gamma: 18.717%
 Kappa: 12.554%
 Zeta: 6.237%

monty.mostly_center() x 100000: Total: 22.102 ms, Average: 221.02 nano
 Alpha: 0.463%
 Beta: 5.408%
 Delta: 24.146%
 Eta: 40.188%
 Gamma: 24.06%
 Kappa: 5.305%
 Zeta: 0.43%

monty.mostly_front() x 100000: Total: 24.444 ms, Average: 244.44 nano
 Alpha: 24.954%
 Beta: 21.543%
 Delta: 17.989%
 Eta: 14.279%
 Gamma: 10.61%
 Kappa: 7.075%
 Zeta: 3.55%

monty.mostly_back() x 100000: Total: 23.249 ms, Average: 232.49 nano
 Alpha: 3.529%
 Beta: 7.18%
 Delta: 10.57%
 Eta: 14.438%
 Gamma: 17.942%
 Kappa: 21.371%
 Zeta: 24.97%

monty.mostly_first() x 100000: Total: 28.199 ms, Average: 281.99 nano
 Alpha: 34.479%
 Beta: 29.989%
 Delta: 19.894%
 Eta: 10.21%
 Gamma: 3.996%
 Kappa: 1.155%
 Zeta: 0.277%

monty.mostly_last() x 100000: Total: 28.93 ms, Average: 289.3 nano
 Alpha: 0.259%
 Beta: 1.19%
 Delta: 4.046%
 Eta: 10.209%
 Gamma: 20.181%
 Kappa: 29.985%
 Zeta: 34.13%

monty.quantum_monty() x 100000: Total: 38.43 ms, Average: 384.3 nano
 Alpha: 11.802%
 Beta: 13.027%
 Delta: 15.93%
 Eta: 19.06%
 Gamma: 15.838%
 Kappa: 12.763%
 Zeta: 11.58%

monty.mostly_cycle() x 100000: Total: 81.616 ms, Average: 816.16 nano
 Alpha: 14.23%
 Beta: 14.244%
 Delta: 14.325%
 Eta: 14.301%
 Gamma: 14.34%
 Kappa: 14.271%
 Zeta: 14.289%

monty.mostly_flat(n_samples=5) -> ['Alpha', 'Alpha', 'Delta', 'Eta', 'Delta']
monty.mostly_middle(n_samples=5) -> ['Gamma', 'Beta', 'Delta', 'Eta', 'Gamma']
monty.mostly_center(n_samples=5) -> ['Delta', 'Delta', 'Delta', 'Delta', 'Eta']
monty.mostly_front(n_samples=5) -> ['Alpha', 'Alpha', 'Beta', 'Beta', 'Gamma']
monty.mostly_back(n_samples=5) -> ['Zeta', 'Zeta', 'Zeta', 'Eta', 'Zeta']
monty.mostly_first(n_samples=5) -> ['Alpha', 'Delta', 'Eta', 'Eta', 'Beta']
monty.mostly_last(n_samples=5) -> ['Kappa', 'Zeta', 'Zeta', 'Eta', 'Gamma']
monty.mostly_cycle(n_samples=5) -> ['Kappa', 'Beta', 'Delta', 'Zeta', 'Alpha']

random_cycle = Fortuna.RandomCycle(
	('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')
)

random_cycle() x 100000: Total: 82.398 ms, Average: 823.98 nano
 Alpha: 14.329%
 Beta: 14.291%
 Delta: 14.221%
 Eta: 14.231%
 Gamma: 14.346%
 Kappa: 14.288%
 Zeta: 14.294%

random_cycle(n_samples=5) -> ['Delta', 'Alpha', 'Delta', 'Zeta', 'Eta']


Random Values by Weighted Table
-------------------------------------------------------------------------

population = ('Apple', 'Banana', 'Cherry', 'Grape', 'Lime', 'Orange')
cum_weights = (7, 11, 13, 23, 26, 30)
rel_weights = (7, 4, 2, 10, 3, 4)

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 100000: Total: 189.873 ms, Average: 1898.73 nano
 Apple: 23.423%
 Banana: 13.183%
 Cherry: 6.794%
 Grape: 33.276%
 Lime: 10.017%
 Orange: 13.307%

Relative Base Case:
random.choices(pop, rel_weights) x 100000: Total: 236.992 ms, Average: 2369.92 nano
 Apple: 23.392%
 Banana: 13.329%
 Cherry: 6.709%
 Grape: 33.348%
 Lime: 9.977%
 Orange: 13.245%

cumulative_table = ((7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange'))

Fortuna.cumulative_weighted_choice(cumulative_table) x 100000: Total: 15.473 ms, Average: 154.73 nano
 Apple: 23.358%
 Banana: 13.396%
 Cherry: 6.691%
 Grape: 33.318%
 Lime: 9.949%
 Orange: 13.288%

cumulative_choice = CumulativeWeightedChoice(
	((7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange'))
)

cumulative_choice() x 100000: Total: 30.786 ms, Average: 307.86 nano
 Apple: 23.146%
 Banana: 13.441%
 Cherry: 6.689%
 Grape: 33.482%
 Lime: 10.017%
 Orange: 13.225%

cumulative_choice(n_samples=5) -> ['Orange', 'Orange', 'Cherry', 'Apple', 'Grape']

relative_choice = RelativeWeightedChoice(
	((7, 'Apple'), (4, 'Banana'), (2, 'Cherry'), (10, 'Grape'), (3, 'Lime'), (4, 'Orange'))
)

relative_choice() x 100000: Total: 30.053 ms, Average: 300.53 nano
 Apple: 23.278%
 Banana: 13.385%
 Cherry: 6.684%
 Grape: 33.294%
 Lime: 9.933%
 Orange: 13.426%

relative_choice(n_samples=5) -> ['Grape', 'Grape', 'Grape', 'Grape', 'Grape']

Random Values by Category
-------------------------------------------------------------------------

flex_cat = FlexCat(
	{'Cat_A': ('A1', 'A2', 'A3'), 'Cat_B': ('B1', 'B2', 'B3'), 'Cat_C': ('C1', 'C2', 'C3')},
	y_bias='front', x_bias='back'
)

flex_cat('Cat_A') x 100000: Total: 40.734 ms, Average: 407.34 nano
 A1: 16.608%
 A2: 33.297%
 A3: 50.095%

flex_cat('Cat_B') x 100000: Total: 39.236 ms, Average: 392.36 nano
 B1: 16.725%
 B2: 33.189%
 B3: 50.086%

flex_cat('Cat_C') x 100000: Total: 42.862 ms, Average: 428.62 nano
 C1: 16.581%
 C2: 33.502%
 C3: 49.917%

flex_cat() x 100000: Total: 64.38 ms, Average: 643.8 nano
 A1: 8.334%
 A2: 16.446%
 A3: 25.143%
 B1: 5.538%
 B2: 11.235%
 B3: 16.504%
 C1: 2.83%
 C2: 5.6%
 C3: 8.37%

flex_cat(n_samples=5) -> ['C3', 'B2', 'C1', 'A3', 'A3']
flex_cat('Cat_A', n_samples=5) -> ['A3', 'A1', 'A2', 'A3', 'A3']
flex_cat('Cat_B', n_samples=5) -> ['B1', 'B3', 'B2', 'B1', 'B1']
flex_cat('Cat_C', n_samples=5) -> ['C1', 'C2', 'C3', 'C2', 'C3']

-------------------------------------------------------------------------
Total Test Time: 2.17 sec

```

## Fortuna Development Log
##### Fortuna 0.20.7
- Documentation updated for clarity.

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
