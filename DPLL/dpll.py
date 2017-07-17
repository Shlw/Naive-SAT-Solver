# DPLL based SAT Solver

import CNFparser
import sys

global lst, is_sat, n, m, ans, equ, ind, var

def prepare():
    global lst, n, m, ans, equ, ind, var

    tlst = lst
    lst = []
    m = len(tlst)
    for i in range(m):
        test = set() 
        flag = False
        for y in tlst[i]:
            test.add(y)
            if -y in test:
                flag = True
                break
        if not flag:
            lst.append(tlst[i])

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
        equ.append(now)
             
def setVariable(v, lab, equ_modify, ind_modify, var_modify): 
    global ans, equ, ind, var
    if v < 0:
        v = -v
        lab = not lab
    flag = False
    ans[v] = lab
    for x in var[v]:
        var_modify.append((v, x))
        equ_modify.append((x, v))
        equ[x].remove(v)
        if lab:
            ind_modify.append(x)
            ind.remove(x)
            for y in equ[x]:
                equ_modify.append((x, y))
                var_modify.append((y, x))
                var[y].remove(x)
            equ[x].clear()
            continue
        elif not equ[x]:
            flag = True
    var[v].clear()
    if flag:
        return True

    for x in var[-v]:
        var_modify.append((-v, x))
        equ_modify.append((x, -v))
        equ[x].remove(-v)
        if not lab:
            ind_modify.append(x)
            ind.remove(x)
            for y in equ[x]:
                equ_modify.append((x, y))
                var_modify.append((y, x))
                var[y].remove(x)
            equ[x].clear()
            continue
        elif not equ[x]:
            flag = True
    var[-v].clear()
    if flag:
        return True
    return False

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
        flag = setVariable(x, True, equ_modify, ind_modify, var_modify)
        if flag:
            return False, True
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
        setVariable(x, True, equ_modify, ind_modify, var_modify)

    return True
            
# choose the most frequently appeared variable 
def chooseVariable():
    global var
    ret = 0
    maxn = 0
    for x in var:
        if x > 0 and var[x]:
            #s = len(var[x]) + len(var[-x])
            l1 = len(var[x])
            l2 = len(var[-x])
            s = l1 + l2 #- abs(l1 - l2) 
            if s > maxn:
                maxn = s
                ret = x
    return ret

def undoChange(equ_modify, ind_modify, var_modify):
    global equ, ind, var
    for x, y in equ_modify:
        equ[x].add(y)
    for x, y in var_modify:
        var[x].add(y)
    for x in ind_modify:
        ind.add(x)

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
        undoChange(equ_modify, ind_modify, var_modify)
        return

    if not ind:
        is_sat = True
        return

    v = chooseVariable()
    
    vequ_modify = []
    vind_modify = []
    vvar_modify = []
    setVariable(v, True, vequ_modify, vind_modify, vvar_modify)
    dpll()
    if is_sat:
        return
    undoChange(vequ_modify, vind_modify, vvar_modify)


    vequ_modify = []
    vind_modify = []
    vvar_modify = []
    setVariable(v, False, vequ_modify, vind_modify, vvar_modify)
    dpll()
    if is_sat:
        return
    undoChange(vequ_modify, vind_modify, vvar_modify)

    undoChange(equ_modify, ind_modify, var_modify)
    
def check():
    global ans, lst, n
    for x in lst:
        flag = False
        for y in x:
            if y > 0:
                flag |= ans[y]
            else:
                flag |= not ans[-y]
        if not flag:
            return False
    return True

def main():
    global lst, is_sat, n, ans
    if len(sys.argv) == 1:
        n, lst = CNFparser.parse()
    elif len(sys.argv) == 2:
        n, lst = CNFparser.parse(sys.argv[1])
    else:
        print('Invalid Argv')
        return

    is_sat = False
    prepare()
    if n:
        dpll()

    if is_sat:
        print('s SATISFIABLE')
        #for i in range(1, n + 1):
            #print('x_%d = %d' % (i, ans[i]))
        #if not check():
            #print('Conflict')
    else:
        print('s UNSATISFIABLE')


if __name__ == '__main__':
    main()
