# Fortuna: Fast & Flexible Random Generators
Fortuna replaces much of the functionality of Python's Random module, often achieving 10x  better performance. However, the most interesting bits of Fortuna are found in the high-level abstractions like FlexCat and QuantumMonty.

The core functionality of Fortuna is based on the Mersenne Twister Algorithm by Makoto Matsumoto (松本 眞) and Takuji Nishimura (西村 拓士). Fortuna is not appropriate for cryptography of any kind, you have been warned. Fortuna employs hardware seeding exclusively.

Fortuna is designed, built and tested for MacOS X, it also happens to work out-of-the-box with many flavors of Linux. Installation: `pip3 install Fortuna` or download and build from source, if that's your thing.

Windows users can use `.../fortuna_extras/fortuna_pure.py` instead of trying to install or compile the extension. The pure Python implementation provides the same API and functionality but lacks the performance of the Fortuna extension.

## Documentation Table of Contents
```
I.   Fortuna Core Functions
        a. Random Number Functions
        b. Random Truth
        c. Random Sequence Values
        d. Random Table Values
        e. Utility Functions
II.  Fortuna Abstraction Classes
        a. Random Cycle
        b. Quantum Monty
        c. Weighted Choice
        d. Flex Cat
III. Test Suite
IV.  Development Log
V.   Legal Information
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

`Fortuna.flatten(itm: object) -> object`. Flatten will recursively unpack callable objects. If itm is not callable - flatten will return it, otherwise it recursively calls itm() and returns the result. Callable objects that require arguments are not supported.

`Fortuna.distribution_timer(func: staticmethod, call_sig=None, num_cycles=100000)`. The `func` arg is the callable object to be analyzed. `call_sig` is an optional label, this is useful for methods that don't have the `__qualname__` property. Optional arg `num_cycles` will set the total number invocations.

## Fortuna Random Classes
### Sequence Wrappers
#### Random Cycle: The Truffle Shuffle
Returns a random value from the sequence. Produces a uniform distribution with no consecutive duplicates and relatively few nearly-consecutive duplicates. Longer sequences will naturally push duplicates even farther apart. This behavior gives rise to output sequences that seem  less mechanical than other random sequences.

RandomCycle instances can return a list of samples rather than just one value, control the length of the list via the optional n_samples argument. By default n_samples=1.

RandomCycle will recursively unpack callable objects in the data set. Callable objects that require arguments are not supported. To disable this behavior pass the optional argument flat_map=False during instantiation. By default flat_map=True.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the input sequence.

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

QuantumMonty instances can return a list of samples rather than just one value, control the length of the list via the optional n_samples argument. By default n_samples=1.

QuantumMonty will recursively unpack callable objects in the data set. Callable objects that require arguments are not supported. To disable this behavior pass the optional argument flat_map=False during instantiation. By default flat_map=True.

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

WeightedChoice instances can return a list of samples rather than just one value, control the length of the list via the optional n_samples argument. By default n_samples=1.

WeightedChoice will recursively unpack callable objects in the data set. Callable objects that require arguments are not supported. To disable this behavior pass the optional argument flat_map=False during instantiation. By default flat_map=True.

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must have a weight and a value.
- Weights must be integers. A future release may allow weights to be floats.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check. As a result: non-unique values will have their probabilities logically accumulated.
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

FlexCat instances can return a list of samples rather than just one value, control the length of the list via the optional n_samples argument. By default n_samples=1.

FlexCat will recursively unpack callable objects in the data set. Callable objects that require arguments are not supported. To disable this behavior pass the optional argument flat_map=False during instantiation. By default flat_map=True.


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
    "Cat_A": (lambda: f"A1.{d(2)}", "A2", "A3", "A4", "A5"),
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
Fortuna 0.21.2 Sample Distribution and Performance Test Suite

Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 100000: Total time: 136.56 ms, Average time: 1366 nano
 1: 9.924%
 2: 10.073%
 3: 10.133%
 4: 10.096%
 5: 10.063%
 6: 9.961%
 7: 9.906%
 8: 10.031%
 9: 9.944%
 10: 9.869%

random_range(1, 10) x 100000: Total time: 8.27 ms, Average time: 83 nano
 1: 9.797%
 2: 10.174%
 3: 9.959%
 4: 10.11%
 5: 9.786%
 6: 9.956%
 7: 10.026%
 8: 10.05%
 9: 9.989%
 10: 10.153%

Base Case:
random.randrange(10) x 100000: Total time: 94.22 ms, Average time: 942 nano
 0: 9.982%
 1: 10.1%
 2: 9.985%
 3: 9.977%
 4: 10.043%
 5: 9.804%
 6: 10.051%
 7: 10.022%
 8: 10.049%
 9: 9.987%

random_below(10) x 100000: Total time: 8.1 ms, Average time: 81 nano
 0: 9.922%
 1: 9.967%
 2: 10.185%
 3: 9.961%
 4: 10.216%
 5: 10.025%
 6: 10.004%
 7: 9.823%
 8: 9.942%
 9: 9.955%

d(10) x 100000: Total time: 8.67 ms, Average time: 87 nano
 1: 9.971%
 2: 10.02%
 3: 9.992%
 4: 9.848%
 5: 10.033%
 6: 10.067%
 7: 9.966%
 8: 9.958%
 9: 10.035%
 10: 10.11%

dice(2, 6) x 100000: Total time: 10.91 ms, Average time: 109 nano
 2: 2.707%
 3: 5.59%
 4: 8.387%
 5: 11.053%
 6: 14.124%
 7: 16.548%
 8: 13.94%
 9: 11.131%
 10: 8.261%
 11: 5.521%
 12: 2.738%

plus_or_minus(5) x 100000: Total time: 7.82 ms, Average time: 78 nano
 -5: 9.217%
 -4: 9.085%
 -3: 8.996%
 -2: 9.064%
 -1: 9.068%
 0: 9.124%
 1: 9.075%
 2: 9.071%
 3: 9.004%
 4: 9.164%
 5: 9.132%

plus_or_minus_linear(5) x 100000: Total time: 11.43 ms, Average time: 114 nano
 -5: 2.695%
 -4: 5.489%
 -3: 8.451%
 -2: 11.082%
 -1: 13.837%
 0: 16.688%
 1: 14.006%
 2: 11.069%
 3: 8.378%
 4: 5.541%
 5: 2.764%

plus_or_minus_curve(5) x 100000: Total time: 12.74 ms, Average time: 127 nano
 -5: 0.189%
 -4: 1.146%
 -3: 4.415%
 -2: 11.327%
 -1: 20.302%
 0: 24.848%
 1: 20.411%
 2: 11.527%
 3: 4.451%
 4: 1.19%
 5: 0.194%

plus_or_minus_curve(5, bounded=False) x 100000: Total time: 13.32 ms, Average time: 133 nano
 -7: 0.001%
 -6: 0.033%
 -5: 0.197%
 -4: 1.101%
 -3: 4.413%
 -2: 11.465%
 -1: 20.264%
 0: 24.63%
 1: 20.439%
 2: 11.671%
 3: 4.372%
 4: 1.187%
 5: 0.196%
 6: 0.03%
 7: 0.001%

zero_flat(10) x 100000: Total time: 7.71 ms, Average time: 77 nano
 0: 9.095%
 1: 9.155%
 2: 8.968%
 3: 9.189%
 4: 9.195%
 5: 9.008%
 6: 9.091%
 7: 9.073%
 8: 9.233%
 9: 9.024%
 10: 8.969%

zero_cool(10) x 100000: Total time: 18.23 ms, Average time: 182 nano
 0: 16.45%
 1: 15.175%
 2: 13.893%
 3: 12.261%
 4: 10.575%
 5: 8.973%
 6: 7.51%
 7: 6.095%
 8: 4.584%
 9: 3.013%
 10: 1.471%

zero_extreme(10) x 100000: Total time: 19.86 ms, Average time: 199 nano
 0: 22.2%
 1: 21.123%
 2: 18.217%
 3: 14.385%
 4: 10.226%
 5: 6.477%
 6: 3.829%
 7: 2.06%
 8: 0.921%
 9: 0.399%
 10: 0.163%

max_cool(10) x 100000: Total time: 17.62 ms, Average time: 176 nano
 0: 1.506%
 1: 2.932%
 2: 4.561%
 3: 5.991%
 4: 7.572%
 5: 9.078%
 6: 10.637%
 7: 12.073%
 8: 13.745%
 9: 15.213%
 10: 16.692%

max_extreme(10) x 100000: Total time: 18.97 ms, Average time: 190 nano
 0: 0.156%
 1: 0.42%
 2: 0.987%
 3: 2.041%
 4: 3.789%
 5: 6.523%
 6: 10.303%
 7: 14.428%
 8: 18.024%
 9: 21.278%
 10: 22.051%

mostly_middle(10) x 100000: Total time: 12.12 ms, Average time: 121 nano
 0: 2.758%
 1: 5.51%
 2: 8.367%
 3: 11.206%
 4: 13.947%
 5: 16.557%
 6: 13.743%
 7: 11.164%
 8: 8.468%
 9: 5.633%
 10: 2.647%

mostly_center(10) x 100000: Total time: 13.15 ms, Average time: 132 nano
 0: 0.235%
 1: 1.172%
 2: 4.362%
 3: 11.378%
 4: 20.361%
 5: 24.628%
 6: 20.509%
 7: 11.488%
 8: 4.474%
 9: 1.162%
 10: 0.231%


Random Truth
-------------------------------------------------------------------------

percent_true(25) x 100000: Total time: 7.16 ms, Average time: 72 nano
 False: 74.784%
 True: 25.216%


Random Values from a Sequence
-------------------------------------------------------------------------

some_list = ('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')

Base Case:
random.choice(some_list) x 100000: Total time: 76.62 ms, Average time: 766 nano
 Alpha: 14.1%
 Beta: 14.275%
 Delta: 14.298%
 Eta: 14.357%
 Gamma: 14.317%
 Kappa: 14.31%
 Zeta: 14.343%

random_value(some_list) x 100000: Total time: 7.19 ms, Average time: 72 nano
 Alpha: 14.3%
 Beta: 14.369%
 Delta: 14.179%
 Eta: 14.181%
 Gamma: 14.442%
 Kappa: 14.215%
 Zeta: 14.314%

monty = Fortuna.QuantumMonty(some_list)

monty.mostly_flat() x 100000: Total time: 23.53 ms, Average time: 235 nano
 Alpha: 14.167%
 Beta: 14.195%
 Delta: 14.295%
 Eta: 14.306%
 Gamma: 14.295%
 Kappa: 14.257%
 Zeta: 14.485%

monty.mostly_flat(n_samples=8) -> ['Gamma', 'Kappa', 'Zeta', 'Gamma', 'Kappa', 'Delta', 'Delta', 'Eta']
monty.mostly_middle() x 100000: Total time: 29.25 ms, Average time: 292 nano
 Alpha: 6.25%
 Beta: 12.546%
 Delta: 18.946%
 Eta: 24.941%
 Gamma: 18.802%
 Kappa: 12.256%
 Zeta: 6.259%

monty.mostly_middle(n_samples=8) -> ['Gamma', 'Eta', 'Eta', 'Gamma', 'Kappa', 'Delta', 'Beta', 'Gamma']
monty.mostly_center() x 100000: Total time: 34.41 ms, Average time: 344 nano
 Alpha: 0.395%
 Beta: 5.347%
 Delta: 24.234%
 Eta: 39.846%
 Gamma: 24.404%
 Kappa: 5.331%
 Zeta: 0.443%

monty.mostly_center(n_samples=8) -> ['Gamma', 'Eta', 'Gamma', 'Delta', 'Delta', 'Eta', 'Eta', 'Delta']
monty.mostly_front() x 100000: Total time: 34.65 ms, Average time: 346 nano
 Alpha: 25.019%
 Beta: 21.315%
 Delta: 17.805%
 Eta: 14.326%
 Gamma: 10.723%
 Kappa: 7.255%
 Zeta: 3.557%

monty.mostly_front(n_samples=8) -> ['Beta', 'Delta', 'Kappa', 'Eta', 'Delta', 'Eta', 'Kappa', 'Kappa']
monty.mostly_back() x 100000: Total time: 35.48 ms, Average time: 355 nano
 Alpha: 3.578%
 Beta: 6.993%
 Delta: 10.604%
 Eta: 14.394%
 Gamma: 18.106%
 Kappa: 21.425%
 Zeta: 24.9%

monty.mostly_back(n_samples=8) -> ['Kappa', 'Gamma', 'Zeta', 'Kappa', 'Eta', 'Gamma', 'Beta', 'Gamma']
monty.mostly_first() x 100000: Total time: 38.27 ms, Average time: 383 nano
 Alpha: 34.048%
 Beta: 30.162%
 Delta: 20.054%
 Eta: 10.27%
 Gamma: 3.963%
 Kappa: 1.219%
 Zeta: 0.284%

monty.mostly_first(n_samples=8) -> ['Beta', 'Delta', 'Delta', 'Alpha', 'Eta', 'Alpha', 'Alpha', 'Gamma']
monty.mostly_last() x 100000: Total time: 39.31 ms, Average time: 393 nano
 Alpha: 0.259%
 Beta: 1.294%
 Delta: 4.014%
 Eta: 10.279%
 Gamma: 19.657%
 Kappa: 30.265%
 Zeta: 34.232%

monty.mostly_last(n_samples=8) -> ['Zeta', 'Kappa', 'Beta', 'Zeta', 'Delta', 'Zeta', 'Zeta', 'Delta']
monty.quantum_monty() x 100000: Total time: 60.54 ms, Average time: 605 nano
 Alpha: 11.559%
 Beta: 12.971%
 Delta: 15.986%
 Eta: 19.123%
 Gamma: 15.935%
 Kappa: 12.9%
 Zeta: 11.526%

monty.quantum_monty(n_samples=8) -> ['Beta', 'Delta', 'Beta', 'Delta', 'Kappa', 'Gamma', 'Zeta', 'Kappa']
monty.mostly_cycle() x 100000: Total time: 87.55 ms, Average time: 876 nano
 Alpha: 14.304%
 Beta: 14.331%
 Delta: 14.38%
 Eta: 14.274%
 Gamma: 14.207%
 Kappa: 14.275%
 Zeta: 14.229%

monty.mostly_cycle(n_samples=8) -> ['Delta', 'Beta', 'Eta', 'Alpha', 'Kappa', 'Gamma', 'Zeta', 'Delta']

random_cycle = Fortuna.RandomCycle(some_list)

random_cycle() x 100000: Total time: 78.6 ms, Average time: 786 nano
 Alpha: 14.28%
 Beta: 14.299%
 Delta: 14.226%
 Eta: 14.285%
 Gamma: 14.308%
 Kappa: 14.334%
 Zeta: 14.268%

random_cycle(n_samples=8) -> ['Alpha', 'Gamma', 'Eta', 'Delta', 'Zeta', 'Kappa', 'Beta', 'Alpha']


Random Values by Weighted Table
-------------------------------------------------------------------------

population = ('Apple', 'Banana', 'Cherry', 'Grape', 'Lime', 'Orange')
cum_weights = (7, 11, 13, 23, 26, 30)
rel_weights = (7, 4, 2, 10, 3, 4)

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 100000: Total time: 200.59 ms, Average time: 2006 nano
 Apple: 23.152%
 Banana: 13.281%
 Cherry: 6.683%
 Grape: 33.381%
 Lime: 10.108%
 Orange: 13.395%

Relative Base Case:
random.choices(pop, rel_weights) x 100000: Total time: 245.31 ms, Average time: 2453 nano
 Apple: 23.365%
 Banana: 13.336%
 Cherry: 6.647%
 Grape: 33.205%
 Lime: 10.156%
 Orange: 13.291%

cumulative_table = [(7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange')]

Fortuna.cumulative_weighted_choice(cumulative_table) x 100000: Total time: 15.11 ms, Average time: 151 nano
 Apple: 23.381%
 Banana: 13.301%
 Cherry: 6.751%
 Grape: 33.131%
 Lime: 10.086%
 Orange: 13.35%

cumulative_choice = CumulativeWeightedChoice(cumulative_table)

cumulative_choice() x 100000: Total time: 34.96 ms, Average time: 350 nano
 Apple: 23.122%
 Banana: 13.289%
 Cherry: 6.659%
 Grape: 33.414%
 Lime: 10.165%
 Orange: 13.351%

cumulative_choice(n_samples=8) -> ['Grape', 'Grape', 'Lime', 'Grape', 'Grape', 'Apple', 'Grape', 'Apple']

relative_choice = RelativeWeightedChoice(relative_table)

relative_choice() x 100000: Total time: 36.39 ms, Average time: 364 nano
 Apple: 23.306%
 Banana: 13.172%
 Cherry: 6.748%
 Grape: 33.275%
 Lime: 10.096%
 Orange: 13.403%

relative_choice(n_samples=8) -> ['Apple', 'Orange', 'Lime', 'Apple', 'Cherry', 'Banana', 'Grape', 'Grape']

Random Values by Category
-------------------------------------------------------------------------

flex_cat = FlexCat({'Cat_A': (<function <lambda> at 0x10a928d90>, 'A2', 'A3'), 'Cat_B': ('B1', 'B2', 'B3'), 'Cat_C': ('C1', 'C2', 'C3')}, y_bias='cycle', x_bias='cycle')

flex_cat('Cat_A') x 100000: Total time: 105.62 ms, Average time: 1056 nano
 A1.1: 8.423%
 A1.2: 8.253%
 A1.3: 8.227%
 A1.4: 8.423%
 A2: 33.325%
 A3: 33.349%

flex_cat('Cat_A', n_samples=8) -> ['A2', 'A1.4', 'A3', 'A2', 'A3', 'A1.3', 'A2', 'A3']

flex_cat('Cat_B') x 100000: Total time: 95.54 ms, Average time: 955 nano
 B1: 33.365%
 B2: 33.296%
 B3: 33.339%

flex_cat('Cat_B', n_samples=8) -> ['B3', 'B2', 'B1', 'B2', 'B3', 'B1', 'B2', 'B3']

flex_cat('Cat_C') x 100000: Total time: 89.9 ms, Average time: 899 nano
 C1: 33.323%
 C2: 33.304%
 C3: 33.373%

flex_cat('Cat_C', n_samples=8) -> ['C2', 'C1', 'C3', 'C2', 'C1', 'C3', 'C2', 'C1']

flex_cat() x 100000: Total time: 159.48 ms, Average time: 1595 nano
 A1.1: 2.729%
 A1.2: 2.82%
 A1.3: 2.758%
 A1.4: 2.805%
 A2: 11.112%
 A3: 11.13%
 B1: 11.103%
 B2: 11.141%
 B3: 11.103%
 C1: 11.09%
 C2: 11.099%
 C3: 11.11%

flex_cat(n_samples=8) -> ['C2', 'B2', 'A1.2', 'C1', 'B1', 'A2', 'C3', 'B3']

-------------------------------------------------------------------------
Total Test Time: 2.52 sec
```

## Fortuna Development Log
##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Major feature release.
- The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
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

##### Dice 0.1.x - 0.9.x
- Experimental Phase

## Legal Information
Fortuna © 2018 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>

```
License
-------

THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE
COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE"). THE WORK IS PROTECTED BY
COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS
AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.

BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO BE
BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT THIS LICENSE MAY BE
CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED HERE
IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.

1. Definitions

  a. "Adaptation" means a work based upon the Work, or upon the Work and other
  pre-existing works, such as a translation, adaptation, derivative work,
  arrangement of music or other alterations of a literary or artistic work, or
  phonogram or performance and includes cinematographic adaptations or any
  other form in which the Work may be recast, transformed, or adapted
  including in any form recognizably derived from the original, except that a
  work that constitutes a Collection will not be considered an Adaptation for
  the purpose of this License. For the avoidance of doubt, where the Work is a
  musical work, performance or phonogram, the synchronization of the Work in
  timed-relation with a moving image ("synching") will be considered an
  Adaptation for the purpose of this License.

  b. "Collection" means a collection of literary or artistic works, such as
  encyclopedias and anthologies, or performances, phonograms or broadcasts, or
  other works or subject matter other than works listed in Section 1(f) below,
  which, by reason of the selection and arrangement of their contents,
  constitute intellectual creations, in which the Work is included in its
  entirety in unmodified form along with one or more other contributions, each
  constituting separate and independent works in themselves, which together
  are assembled into a collective whole. A work that constitutes a Collection
  will not be considered an Adaptation (as defined above) for the purposes of
  this License.

  c. "Distribute" means to make available to the public the original and
  copies of the Work or Adaptation, as appropriate, through sale or other
  transfer of ownership.

  d. "Licensor" means the individual, individuals, entity or entities that
  offer(s) the Work under the terms of this License.

  e. "Original Author" means, in the case of a literary or artistic work, the
  individual, individuals, entity or entities who created the Work or if no
  individual or entity can be identified, the publisher; and in addition (i)
  in the case of a performance the actors, singers, musicians, dancers, and
  other persons who act, sing, deliver, declaim, play in, interpret or
  otherwise perform literary or artistic works or expressions of folklore;
  (ii) in the case of a phonogram the producer being the person or legal
  entity who first fixes the sounds of a performance or other sounds; and,
  (iii) in the case of broadcasts, the organization that transmits the
  broadcast.

  f. "Work" means the literary and/or artistic work offered under the terms of
  this License including without limitation any production in the literary,
  scientific and artistic domain, whatever may be the mode or form of its
  expression including digital form, such as a book, pamphlet and other
  writing; a lecture, address, sermon or other work of the same nature; a
  dramatic or dramatico-musical work; a choreographic work or entertainment in
  dumb show; a musical composition with or without words; a cinematographic
  work to which are assimilated works expressed by a process analogous to
  cinematography; a work of drawing, painting, architecture, sculpture,
  engraving or lithography; a photographic work to which are assimilated works
  expressed by a process analogous to photography; a work of applied art; an
  illustration, map, plan, sketch or three-dimensional work relative to
  geography, topography, architecture or science; a performance; a broadcast;
  a phonogram; a compilation of data to the extent it is protected as a
  copyrightable work; or a work performed by a variety or circus performer to
  the extent it is not otherwise considered a literary or artistic work.

  g. "You" means an individual or entity exercising rights under this License
  who has not previously violated the terms of this License with respect to
  the Work, or who has received express permission from the Licensor to
  exercise rights under this License despite a previous violation.

  h. "Publicly Perform" means to perform public recitations of the Work and to
  communicate to the public those public recitations, by any means or process,
  including by wire or wireless means or public digital performances; to make
  available to the public Works in such a way that members of the public may
  access these Works from a place and at a place individually chosen by them;
  to perform the Work to the public by any means or process and the
  communication to the public of the performances of the Work, including by
  public digital performance; to broadcast and rebroadcast the Work by any
  means including signs, sounds or images.

  i. "Reproduce" means to make copies of the Work by any means including
  without limitation by sound or visual recordings and the right of fixation
  and reproducing fixations of the Work, including storage of a protected
  performance or phonogram in digital form or other electronic medium.

2. Fair Dealing Rights. Nothing in this License is intended to reduce, limit,
or restrict any uses free from copyright or rights arising from limitations or
exceptions that are provided for in connection with the copyright protection
under copyright law or other applicable laws.

3. License Grant. Subject to the terms and conditions of this License,
Licensor hereby grants You a worldwide, royalty-free, non-exclusive, perpetual
(for the duration of the applicable copyright) license to exercise the rights
in the Work as stated below:

  a. to Reproduce the Work, to incorporate the Work into one or more
  Collections, and to Reproduce the Work as incorporated in the Collections;

  b. to create and Reproduce Adaptations provided that any such Adaptation,
  including any translation in any medium, takes reasonable steps to clearly
  label, demarcate or otherwise identify that changes were made to the
  original Work. For example, a translation could be marked "The original work
  was translated from English to Spanish," or a modification could indicate
  "The original work has been modified.";

  c. to Distribute and Publicly Perform the Work including as incorporated in
  Collections; and,

  d. to Distribute and Publicly Perform Adaptations.

The above rights may be exercised in all media and formats whether now known
or hereafter devised. The above rights include the right to make such
modifications as are technically necessary to exercise the rights in other
media and formats. Subject to Section 8(f), all rights not expressly granted
by Licensor are hereby reserved, including but not limited to the rights set
forth in Section 4(d).

4. Restrictions. The license granted in Section 3 above is expressly made
subject to and limited by the following restrictions:

  a. You may Distribute or Publicly Perform the Work only under the terms of
  this License. You must include a copy of, or the Uniform Resource Identifier
  (URI) for, this License with every copy of the Work You Distribute or
  Publicly Perform. You may not offer or impose any terms on the Work that
  restrict the terms of this License or the ability of the recipient of the
  Work to exercise the rights granted to that recipient under the terms of the
  License. You may not sublicense the Work. You must keep intact all notices
  that refer to this License and to the disclaimer of warranties with every
  copy of the Work You Distribute or Publicly Perform. When You Distribute or
  Publicly Perform the Work, You may not impose any effective technological
  measures on the Work that restrict the ability of a recipient of the Work
  from You to exercise the rights granted to that recipient under the terms of
  the License. This Section 4(a) applies to the Work as incorporated in a
  Collection, but this does not require the Collection apart from the Work
  itself to be made subject to the terms of this License. If You create a
  Collection, upon notice from any Licensor You must, to the extent
  practicable, remove from the Collection any credit as required by Section
  4(c), as requested. If You create an Adaptation, upon notice from any
  Licensor You must, to the extent practicable, remove from the Adaptation any
  credit as required by Section 4(c), as requested.

  b. You may not exercise any of the rights granted to You in Section 3 above
  in any manner that is primarily intended for or directed toward commercial
  advantage or private monetary compensation. The exchange of the Work for
  other copyrighted works by means of digital file-sharing or otherwise shall
  not be considered to be intended for or directed toward commercial advantage
  or private monetary compensation, provided there is no payment of any
  monetary compensation in connection with the exchange of copyrighted works.

  c. If You Distribute, or Publicly Perform the Work or any Adaptations or
  Collections, You must, unless a request has been made pursuant to Section
  4(a), keep intact all copyright notices for the Work and provide, reasonable
  to the medium or means You are utilizing: (i) the name of the Original
  Author (or pseudonym, if applicable) if supplied, and/or if the Original
  Author and/or Licensor designate another party or parties (e.g., a sponsor
  institute, publishing entity, journal) for attribution ("Attribution
  Parties") in Licensor's copyright notice, terms of service or by other
  reasonable means, the name of such party or parties; (ii) the title of the
  Work if supplied; (iii) to the extent reasonably practicable, the URI, if
  any, that Licensor specifies to be associated with the Work, unless such URI
  does not refer to the copyright notice or licensing information for the
  Work; and, (iv) consistent with Section 3(b), in the case of an Adaptation,
  a credit identifying the use of the Work in the Adaptation (e.g., "French
  translation of the Work by Original Author," or "Screenplay based on
  original Work by Original Author"). The credit required by this Section 4(c)
  may be implemented in any reasonable manner; provided, however, that in the
  case of a Adaptation or Collection, at a minimum such credit will appear, if
  a credit for all contributing authors of the Adaptation or Collection
  appears, then as part of these credits and in a manner at least as prominent
  as the credits for the other contributing authors. For the avoidance of
  doubt, You may only use the credit required by this Section for the purpose
  of attribution in the manner set out above and, by exercising Your rights
  under this License, You may not implicitly or explicitly assert or imply any
  connection with, sponsorship or endorsement by the Original Author, Licensor
  and/or Attribution Parties, as appropriate, of You or Your use of the Work,
  without the separate, express prior written permission of the Original
  Author, Licensor and/or Attribution Parties.

  d. For the avoidance of doubt:

    i. Non-waivable Compulsory License Schemes. In those jurisdictions in
    which the right to collect royalties through any statutory or compulsory
    licensing scheme cannot be waived, the Licensor reserves the exclusive
    right to collect such royalties for any exercise by You of the rights
    granted under this License;

    ii. Waivable Compulsory License Schemes. In those jurisdictions in which
    the right to collect royalties through any statutory or compulsory
    licensing scheme can be waived, the Licensor reserves the exclusive right
    to collect such royalties for any exercise by You of the rights granted
    under this License if Your exercise of such rights is for a purpose or use
    which is otherwise than noncommercial as permitted under Section 4(b) and
    otherwise waives the right to collect royalties through any statutory or
    compulsory licensing scheme; and,

    iii. Voluntary License Schemes. The Licensor reserves the right to collect
    royalties, whether individually or, in the event that the Licensor is a
    member of a collecting society that administers voluntary licensing
    schemes, via that society, from any exercise by You of the rights granted
    under this License that is for a purpose or use which is otherwise than
    noncommercial as permitted under Section 4(c).

  e. Except as otherwise agreed in writing by the Licensor or as may be
  otherwise permitted by applicable law, if You Reproduce, Distribute or
  Publicly Perform the Work either by itself or as part of any Adaptations or
  Collections, You must not distort, mutilate, modify or take other derogatory
  action in relation to the Work which would be prejudicial to the Original
  Author's honor or reputation. Licensor agrees that in those jurisdictions
  (e.g. Japan), in which any exercise of the right granted in Section 3(b) of
  this License (the right to make Adaptations) would be deemed to be a
  distortion, mutilation, modification or other derogatory action prejudicial
  to the Original Author's honor and reputation, the Licensor will waive or
  not assert, as appropriate, this Section, to the fullest extent permitted by
  the applicable national law, to enable You to reasonably exercise Your right
  under Section 3(b) of this License (right to make Adaptations) but not
  otherwise.

5. Representations, Warranties and Disclaimer

UNLESS OTHERWISE MUTUALLY AGREED TO BY THE PARTIES IN WRITING, LICENSOR OFFERS
THE WORK AS-IS AND MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND
CONCERNING THE WORK, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE, INCLUDING,
WITHOUT LIMITATION, WARRANTIES OF TITLE, MERCHANTIBILITY, FITNESS FOR A
PARTICULAR PURPOSE, NONINFRINGEMENT, OR THE ABSENCE OF LATENT OR OTHER
DEFECTS, ACCURACY, OR THE PRESENCE OF ABSENCE OF ERRORS, WHETHER OR NOT
DISCOVERABLE. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF IMPLIED
WARRANTIES, SO SUCH EXCLUSION MAY NOT APPLY TO YOU.

6. Limitation on Liability. EXCEPT TO THE EXTENT REQUIRED BY APPLICABLE LAW,
IN NO EVENT WILL LICENSOR BE LIABLE TO YOU ON ANY LEGAL THEORY FOR ANY
SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE OR EXEMPLARY DAMAGES ARISING OUT
OF THIS LICENSE OR THE USE OF THE WORK, EVEN IF LICENSOR HAS BEEN ADVISED OF
THE POSSIBILITY OF SUCH DAMAGES.

7. Termination

  a. This License and the rights granted hereunder will terminate
  automatically upon any breach by You of the terms of this License.
  Individuals or entities who have received Adaptations or Collections from
  You under this License, however, will not have their licenses terminated
  provided such individuals or entities remain in full compliance with those
  licenses. Sections 1, 2, 5, 6, 7, and 8 will survive any termination of this
  License.

  b. Subject to the above terms and conditions, the license granted here is
  perpetual (for the duration of the applicable copyright in the Work).
  Notwithstanding the above, Licensor reserves the right to release the Work
  under different license terms or to stop distributing the Work at any time;
  provided, however that any such election will not serve to withdraw this
  License (or any other license that has been, or is required to be, granted
  under the terms of this License), and this License will continue in full
  force and effect unless terminated as stated above.

8. Miscellaneous

  a. Each time You Distribute or Publicly Perform the Work or a Collection,
  the Licensor offers to the recipient a license to the Work on the same terms
  and conditions as the license granted to You under this License.

  b. Each time You Distribute or Publicly Perform an Adaptation, Licensor
  offers to the recipient a license to the original Work on the same terms and
  conditions as the license granted to You under this License.

  c. If any provision of this License is invalid or unenforceable under
  applicable law, it shall not affect the validity or enforceability of the
  remainder of the terms of this License, and without further action by the
  parties to this agreement, such provision shall be reformed to the minimum
  extent necessary to make such provision valid and enforceable.

  d. No term or provision of this License shall be deemed waived and no breach
  consented to unless such waiver or consent shall be in writing and signed by
  the party to be charged with such waiver or consent.

  e. This License constitutes the entire agreement between the parties with
  respect to the Work licensed here. There are no understandings, agreements
  or representations with respect to the Work not specified here. Licensor
  shall not be bound by any additional provisions that may appear in any
  communication from You. This License may not be modified without the mutual
  written agreement of the Licensor and You.

  f. The rights granted under, and the subject matter referenced, in this
  License were drafted utilizing the terminology of the Berne Convention for
  the Protection of Literary and Artistic Works (as amended on September 28,
  1979), the Rome Convention of 1961, the WIPO Copyright Treaty of 1996, the
  WIPO Performances and Phonograms Treaty of 1996 and the Universal Copyright
  Convention (as revised on July 24, 1971). These rights and subject matter
  take effect in the relevant jurisdiction in which the License terms are
  sought to be enforced according to the corresponding provisions of the
  implementation of those treaty provisions in the applicable national law. If
  the standard suite of rights granted under applicable copyright law includes
  additional rights not granted under this License, such additional rights are
  deemed to be included in the License; this License is not intended to
  restrict the license of any rights under applicable law.
```
