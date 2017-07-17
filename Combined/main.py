# SAT Solver 
# Specify different kinds of dataset

import dpll
import cdcl
import sys

def main():
    if len(sys.argv) == 1:
        dpll.solve()
    elif len(sys.argv) == 2:
        # ii, aim, pret dataset
        if 'ii' in sys.argv[1] or 'aim' in sys.argv[1] or 'pret' in sys.argv[1]:
            cdcl.solve(0, sys.argv[1])
            return
        # flat dataset
        if 'flat' in sys.argv[1]:
            cdcl.solve(1, sys.argv[1])
            return
        # uf, uuf, sw, hole dataset
        if 'uf' in sys.argv[1] or 'uuf' in sys.argv[1] or 'sw' in sys.argv[1] or 'hole' in sys.argv[1]:
            dpll.solve(sys.argv[1])
            return
        if 'unsat' in sys.argv[1]:
            cdcl.solve(0, sys.argv[1])
            return
        dpll.solve(sys.argv[1])
    else:
        print('Invalid Argv')
        return

if __name__ == '__main__':
    main()
