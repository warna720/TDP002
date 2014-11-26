#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""5a_________________________________________________________________"""

from functools import reduce

plus = lambda x1, x2: x1 + x2
times = lambda x1, x2: x1 * x2

operations = [plus, times]
for fn in operations: print(reduce(fn, range(1, 513))); print("\n"*2)



from fractions import gcd
def lcm(numbers):
    return int(reduce(lambda x, y: (x * y)/gcd(x, y), numbers, 1))

print(lcm(range(1, 101)), "\n"*2)


"""5b_________________________________________________________________"""

db = [
    {'name': 'Jakob', 'position': 'assistant'},
    {'name': 'Åke', 'position': 'assistant'},
    {'name': 'Ola', 'position': 'examiner'},
    {'name': 'Henrik', 'position': 'assistant'}
    ]


def dbsearch(db, column, value):
    return ([worker for worker in db if worker[column] == value])

"""5c_________________________________________________________________"""

def contains(needle, haystack):
    return bool([word for word in haystack if needle == word])


"""5d_________________________________________________________________"""

#See corresponding file

"""5e_________________________________________________________________"""

#Different ways to do this
#generate_list = lambda op, amount: list(map(op, range(1, amount + 1)))

#Uses the function at every index in list
def generate_list(op, amount):
    return list(map(op, range(1, amount + 1)))

"""5f_________________________________________________________________"""

#Different ways to do this
#partial = lambda op, amount: lambda x: op(amount, x)

#Returns lambda function with op as the fn and amount as first arg
def partial(op, amount):
    return lambda x: op(amount, x)

"""5h_________________________________________________________________"""

#Different ways to do this
#compose = lambda first_op, second_op: lambda x: first_op(second_op(x))

#Returns lambda function with second function as argument
#to first function and x as argument to second function
def compose(first_op, second_op):
    return lambda x: first_op(second_op(x))

"""5g_________________________________________________________________"""

#Different ways to do this
#make_filter_map = lambda first_filter, second_filter: compose(list, compose(partial(filter, first_filter), partial(map, second_filter)))


def make_filter_map(first_filter, second_filter):
    #s = map func with second_filter as first arg and x as second arg
    #f = filter func with first_filter as first arg and x as second arg
    #First compose = function with s as argument to f and x as argument to s
    #Second compose = first compose as arg to list
    
    s = partial(map, second_filter)
    f = partial(filter, first_filter)

    return compose(list, compose(f, s))

