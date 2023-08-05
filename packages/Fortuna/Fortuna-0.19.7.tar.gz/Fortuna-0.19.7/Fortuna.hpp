//  Fortuna.hpp
//  Copyright © 2018 Robert Sharp. All rights reserved.
#pragma once
#include <random>       // std::random_device, std::mt19937_64, std::uniform_int_distribution, std::normal_distribution
#include <functional>   // std::function
#include <algorithm>    // std::min, std::max
#include <stdlib.h>     // std::abs


namespace RNG {
    static std::random_device hardware_seed;
    static std::mt19937_64 generator(hardware_seed());
}

int random_range(int lo, int hi) {
    if (lo < hi) {
        std::uniform_int_distribution<int> distribution(lo, hi);
        return distribution(RNG::generator);
    }
    else if (hi == lo) return hi;
    else return random_range(hi, lo);
}

int analytic_continuation(const std::function<int(int)> & func, int num) {
    if (num < 0) return -func(-num);
    else if (num == 0) return 0;
    else return func(num);
}

int random_below(int size) {
    if (size > 0) return random_range(0, size - 1);
    else return analytic_continuation(random_below, size);
}

int d(int sides) {
    if (sides > 0) return random_range(1, sides);
    else return analytic_continuation(d, sides);
}

int dice(int rolls, int sides) {
    if (rolls > 0) {
        int total = 0;
        for (int i=0; i<rolls; ++i) total += d(sides);
        return total;
    }
    else if (rolls == 0) return 0;
    else return -dice(-rolls, sides);
}

bool percent_true(int num) {
    return d(100) <= num;
}

int min_max(int target, int lo, int hi) {
    if (lo < hi) return std::min(std::max(target, lo), hi);
    else if (lo == hi) return hi;
    else return min_max(target, hi, lo);
}

int plus_or_minus(int num) {
    return random_range(-num, num);
}

int plus_or_minus_linear(int num) {
    const int n = std::abs(num);
    return dice(2, n + 1) - (n + 2);
}

int stretched_bell(int num) {
    const double PI = 3.14159265359;
    std::normal_distribution<double> distribution(0.0, num / PI);
    return round(distribution(RNG::generator));
}

int plus_or_minus_curve(int num, int bounded=1) {
    const int n = std::abs(num);
    int result = stretched_bell(n);
    if (bounded == 0) return result;
    while (result < -n or result > n) { result = stretched_bell(n); };
    return result;
}

int zero_flat(int num) {
    return random_range(0, num);
}

int zero_cool(int num) {
    if (num > 0) {
        int result;
        do { result = plus_or_minus_linear(num); } while (result < 0);
        return result;
    } else return analytic_continuation(zero_cool, num);
}

int zero_extreme(int num) {
    if (num > 0) {
        int result;
        do { result = plus_or_minus_curve(num); } while (result < 0);
        return result;
    } else return analytic_continuation(zero_extreme, num);
}

int max_cool(int num) {
    if (num > 0) return num - zero_cool(num);
    else return analytic_continuation(max_cool, num);
}

int max_extreme(int num) {
    if (num > 0) return num - zero_extreme(num);
    else return analytic_continuation(max_extreme, num);
}

int mostly_middle(int num) {
    if (num > 0) {
        const int mid_point = num / 2;
        if (num % 2 == 0) return plus_or_minus_linear(mid_point) + mid_point;
        else if (percent_true(50)) return max_cool(mid_point);
        else return 1 + zero_cool(mid_point) + mid_point;
    } else return analytic_continuation(mostly_middle, num);
}

int mostly_center(int num) {
    if (num > 0) {
        const int mid_point = num / 2;
        if (num % 2 == 0) return plus_or_minus_curve(mid_point) + mid_point;
        else if (percent_true(50)) return max_extreme(mid_point);
        else return 1 + zero_extreme(mid_point) + mid_point;
    } else return analytic_continuation(mostly_center, num);
}

int fast_dice(int rolls, int sides) {
    int total = rolls;
    for (auto i=0; i<rolls; ++i) total += rand() % sides;
    return total;
}
