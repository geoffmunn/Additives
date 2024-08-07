#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from itertools import combinations

def main():
    
    length = 4
    current_set: list = []

    for i in range(1, length + 1):
        current_set.append(i)
    
    totals: dict = {}

    current_number = length

    # Go through the current set and check if every set of two numbers adds up to a unique number

    # For 2 combos, take the first number and check the others.
    while True:
        
        print ('----')

        set_combos = combinations(current_set, 2)
        for line in list(set_combos):
            total = sum(line)
            if total in totals:
                totals[total] += 1
            else:
                totals[total] = 1

        # Now go through the numbers to find the next one that doens't have a total of 2

        while True:
            current_number += 1
            if current_number in totals:
                if totals[current_number] < 2:
                    break
            else:
                break

        current_set.append(current_number)

        print ('total so far:', len(current_set))
        if len(current_set) >= 100:
            break

    # Now find the next number we can add

    print ('final set:', current_set)

    print (' 💯 Done!\n')

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()