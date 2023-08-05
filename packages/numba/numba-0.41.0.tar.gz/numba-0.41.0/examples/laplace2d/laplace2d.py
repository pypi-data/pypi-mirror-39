#!/usr/bin/env python
from __future__ import print_function

import sys
import time

import numpy as np


def jacobi_relax_core(A, Anew):
    error = 0.0
    n = A.shape[0]
    m = A.shape[1]

    for j in range(1, n - 1):
        for i in range(1, m - 1):
            Anew[j, i] = 0.25 * ( A[j, i + 1] + A[j, i - 1] \
                                + A[j - 1, i] + A[j + 1, i])
            error = max(error, abs(Anew[j, i] - A[j, i]))
    return error


def main():
    argv = sys.argv[1:]
    if len(argv) == 1:
        [iter_max] = argv
        iter_max = int(iter_max)
    else:
        print('Using default max number of iteration to 2 due to long run time.')
        print('Override by passing a cmdline arg: python {} <max_iter>'.format(__file__))
        iter_max = 1000

    NN = 3000
    NM = 3000

    A = np.zeros((NN, NM), dtype=np.float64)
    Anew = np.zeros((NN, NM), dtype=np.float64)

    n = NN
    m = NM

    tol = 1.0e-6
    error = 1.0

    for j in range(n):
        A[j, 0] = 1.0
        Anew[j, 0] = 1.0

    print("Jacobi relaxation Calculation: %d x %d mesh" % (n, m))

    timer = time.time()
    iter = 0

    while error > tol and iter < iter_max:
        error = jacobi_relax_core(A, Anew)

        # swap A and Anew
        tmp = A
        A = Anew
        Anew = tmp

        if iter % 100 == 0:
            print("%5d, %0.6f (elapsed: %f s)" % (iter, error, time.time()-timer))

        iter += 1

    runtime = time.time() - timer
    print(" total: %f s" % runtime)

if __name__ == '__main__':
    main()
