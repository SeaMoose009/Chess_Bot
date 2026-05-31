import timeit
a = '''
from math import sqrt
def example():
    mylist = [sqrt(x) for x in range(100)]
'''
t = timeit.timeit(a, number=1000000) * 1e3
print(round(t, 3), "ms")