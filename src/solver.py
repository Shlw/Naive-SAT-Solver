# DPLL based SAT Solver

import parser
import sys

global lst, is_sat, n, m, ans, equ, ind, var, cftInClause

def prepare():
    global lst, n, m, ans, equ, ind, var, cftInClause
    m = len(lst)
    ans = [0 for i in range(n + 1)]
    ind = set([i for i in range(m)])
    equ = []
    var = dict()
    for i in range(-n, n + 1):
        var[i] = set();
    for i in range(m):
        now = set()
        for y in lst[i]:
            var[y].add(i)
            now.add(y)
            if -y in now:
                cftInClause = True
                return
        equ.append(now)
    #print(ind)
    #print(equ)
    #print(var)

def eliminateUnit(equ_modify, ind_modify, var_modify):
    global ans, equ, ind, var
    lst = set()
    for i in ind:
        if len(equ[i]) == 1:
            x = equ[i].pop()
            equ[i].add(x)
            lst.add(x)
            if -x in lst:
                return False, True
    if not lst:
        return False, False
    for x in lst:
        if x > 0:
            ans[x] = True
        else:
            ans[-x] = False
        # remove those true clause
        for y in var[x]:
            var_modify.append((x, y))
            equ_modify.append((y, x))
            equ[y].remove(x)
            ind_modify.append(y)
            ind.remove(y)
        var[x].clear()

        # modify those opposite literal
        for y in var[-x]:
            var_modify.append((-x, y))
            equ_modify.append((y, -x))
            equ[y].remove(-x)
        var[-x].clear()
    return True, False


def eliminatePure(equ_modify, ind_modify, var_modify):
    global ans, equ, ind, var
    lst = set()
    for i in var:
        if len(var[i]) > 0 and len(var[-i]) == 0:
            lst.add(i)
    if not lst:
        return False
    for x in lst:
        if x > 0:
            ans[x] = True
        else:
            ans[-x] = False
        for y in var[x]:
            var_modify.append((x, y))
            equ_modify.append((y, x))
            equ[y].remove(x)
            if y in ind:
                ind_modify.append(y)
                ind.remove(y)
        var[x].clear()
    return True
            
# choose the most frequent variable 
def chooseVariable():
    global var
    ret = 0
    maxn = 0
    for x in var:
        if x > 0 and var[x]:
            s = len(var[x]) + len(var[-x])
            if s > maxn:
                maxn = s
                ret = x
    return ret
             
def setVariable(v, lab, vequ_modify, vind_modify, vvar_modify): 
    global ans, equ, ind, var
    ans[v] = lab
    for x in var[v]:
        vvar_modify.append((v, x))
        vequ_modify.append((x, v))
        equ[x].remove(v)
        if lab:
            vind_modify.append(x)
            ind.remove(x)
    var[v].clear()

    for x in var[-v]:
        vvar_modify.append((-v, x))
        vequ_modify.append((x, -v))
        equ[x].remove(-v)
        if not lab:
            vind_modify.append(x)
            ind.remove(x)
    var[-v].clear()

def undoChange(equ_mod, ind_mod, var_mod):
    global equ, ind, var
    for x, y in equ_mod:
        equ[x].add(y)
    for x, y in var_mod:
        var[x].add(y)
    for x in ind_mod:
        ind.append(x)

def dpll():
    global is_sat, n, ans, equ, ind, var
    if not ind:
        is_sat = True
        return

    equ_modify = [] 
    ind_modify = []
    var_modify = []
    flag = True
    conflict = False

    while flag:
        flag, conflict = eliminateUnit(equ_modify, ind_modify, var_modify)
        if conflict:
            break
        flag |= eliminatePure(equ_modify, ind_modify, var_modify)

    if conflict:
        undoAllChange(equ_modify, ind_modify, var_modify)
        return

    if not ind:
        is_sat = True
        return

    v = chooseVariable()
    
    vequ_modify = []
    vind_modify = []
    vvar_modify = []
    setVariable(v, 1, vequ_modify, vind_modify, vvar_modify)
    dpll()
    if is_sat:
        return
    undoChange(vequ_modify, vind_modify, vvar_modify)


    vequ_modify = []
    vind_modify = []
    vvar_modify = []
    setVariable(v, 0, vequ_modify, vind_modify, vvar_modify)
    dpll()
    if is_sat:
        return
    undoChange(vequ_modify, vind_modify, vvar_modify)

    undoChange(equ_modify, ind_modify, var_modify)

def main():
    global lst, is_sat, n, ans, cftInClause
    if len(sys.argv) == 1:
        n, lst = parser.parse()
    elif len(sys.argv) == 2:
        n, lst = parser.parse(sys.argv[1])
    else:
        print('Invalid Argv')
        return

    is_sat = False
    cftInClause = False
    if n:
        prepare()
        if not cftInClause: 
            dpll()

    if is_sat:
        print('Satisfiable')
        for i in range(1, n + 1):
            print('x_%d = %d' % (i, ans[i]))
    else:
        print('Unsatisfiable')


if __name__ == '__main__':
    main()
