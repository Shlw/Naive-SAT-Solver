# DPLL based SAT Solver

import parser
import sys

global lst, is_sat, n, ans

def dpll():
    global lst, is_sat, n, ans
    if not lst:
        is_sat = True
        return


def main():
    global lst, is_sat, n, ans
    if len(sys.argv) == 1:
        n, lst = parser.parse()
    elif len(sys.argv) == 2:
        n, lst = parser.parse(sys.argv[1])
    else:
        print('Invalid Argv')
        return

    is_sat = False
    if n:
        ans = [0 for i in range(n + 1)]
        dpll()

    if is_sat:
        print('Satisfiable')
        for i in range(1, n + 1):
            print('x_%d = %d' % (i, ans[i]))
    else:
        print('Unsatisfiable')


if __name__ == '__main__':
    main()
