# CDCL based SAT Solver

import CNFparser
import sys

global lst, is_sat, n, m, ans, equ, ind, var, fst_equ, d, stk, dag, chooseVariable

def prepare():
    global lst, n, m, ans, equ, ind, var, fst_equ, d, dag
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
    d = [0 for i in range(n + 1)]
    ind = set([i for i in range(m)])
    dag = [set() for i in range(n + 1)]
    equ = []
    fst_equ = []
    var = dict()
    for i in range(-n, n + 1):
        var[i] = set()
    for i in range(m):
        now = set()
        for y in lst[i]:
            var[y].add(i)
            now.add(y)
        equ.append(now)
        tnow = set()
        for y in now:
            tnow.add(abs(y))
        fst_equ.append(tnow)

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

def setVariable(depth, v, lab, equ_modify, ind_modify, var_modify):
    global ans, equ, ind, var, d
    if v < 0:
        v, lab = -v, not lab
    d[v], ans[v] = depth, lab
    for x in var[v]:
        var_modify.append((v, x))
        equ_modify.append((x, v))
        equ[x].remove(v)
        if not equ[x]:
            ind_modify.append(x)
            ind.remove(x)
            continue
        if lab:
            ind_modify.append(x)
            ind.remove(x)
            for y in equ[x]:
                equ_modify.append((x, y))
                var_modify.append((y, x))
                var[y].remove(x)
            equ[x].clear()
    var[v].clear()

    for x in var[-v]:
        var_modify.append((-v, x))
        equ_modify.append((x, -v))
        equ[x].remove(-v)
        if not equ[x]:
            ind_modify.append(x)
            ind.remove(x)
            continue
        if not lab:
            ind_modify.append(x)
            ind.remove(x)
            for y in equ[x]:
                equ_modify.append((x, y))
                var_modify.append((y, x))
                var[y].remove(x)
            equ[x].clear()
    var[-v].clear()

def eliminateUnit(depth, equ_modify, ind_modify, var_modify, updSTK):
    global ans, equ, ind, var, dag
    lst = set()
    detm = dict()
    for i in ind:
        if len(equ[i]) == 1:
            x = equ[i].pop()
            equ[i].add(x)
            if x in lst:
                continue
            lst.add(x)
            detm[x] = i
            if -x in lst:
                tx = x if x > 0 else -x
                s = set()
                for t in fst_equ[i]:
                    if tx != t:
                        #if d[t] == depth:
                            #s = s.union(dag[t]) 
                        #else:
                            #s.add(t if not ans[t] else -t)
                        s = s.union(dag[t])
                for t in fst_equ[detm[-x]]:
                    if tx != t:
                        #if d[t] == depth:
                            #s = s.union(dag[t]) 
                        #else:
                            #s.add(t if not ans[t] else -t)
                        #for v in dag[t]:
                            #s.add(v)
                        s = s.union(dag[t])
                return False, True, s
    if not lst:
        return False, False, set()
    x = lst.pop()
    tx = x if x > 0 else -x
    updSTK.append(tx)
    for t in fst_equ[detm[x]]:
        if t != x:
            dag[tx] = dag[tx].union(dag[t])
    setVariable(depth, x, True, equ_modify, ind_modify, var_modify)
    return True, False, set()

def eliminatePure(depth, equ_modify, ind_modify, var_modify):
    global ans, equ, ind, var
    lst = set()
    for i in var:
        if i > 0:
            l1 = len(var[i])
            l2 = len(var[-i])
            if l1 > 0 and l2 == 0:
                lst.add(i)
            elif l1 == 0 and l2 > 0:
                lst.add(-i)
    if not lst:
        return False
    for x in lst:
        setVariable(depth, x, True, equ_modify, ind_modify, var_modify)
    return True
    
def chooseVariableflat():
    global var
    ret = 0
    maxn = -10
    for x in var:
        if x > 0:
            l1, l2 = len(var[x]), len(var[-x])
            if l1 > l2:
                s = l2 + l2
                v = x
            else:
                s = l1 + l1
                v = -x
            if s > maxn:
                maxn, ret = s, v
    return ret

def chooseVariableother():
    global var
    ret = 0
    maxn = -10
    for x in var:
        if x > 0:
            l1, l2 = len(var[x]), len(var[-x])
            s = l1 + l2
            if l1 > l2:
                v = x
            else:
                v = -x
            if s > maxn:
                maxn, ret = s, v
    return ret

def undoChange(equ_modify, ind_modify, var_modify, updSTK):
    global equ, ind, var, dag
    for x, y in equ_modify:
        equ[x].add(y)
    for x, y in var_modify:
        var[x].add(y)
    for x in ind_modify:
        ind.add(x)
    for x in updSTK:
        dag[x].clear()

def propagation(depth, equ_modify, ind_modify, var_modify, updSTK):
    flag = True
    conflict = False
    while flag:
        flag, conflict, s = eliminateUnit(depth, equ_modify, ind_modify, var_modify, updSTK)
        if conflict:
            return True, s
        flag |= eliminatePure(depth, equ_modify, ind_modify, var_modify)
    return False, set()

def clauseLearning(cls):
    global d, stk, equ, ind, var
    maxn, tmaxn = 0, 0
    cur = len(equ) 
    fst_equ.append(set())
    equ.append(set())
    ind.add(cur)
    for x in cls:
        fst_equ[cur].add(x if x > 0 else -x)
        tx = x if x > 0 else -x
        dcur = d[tx]
        if dcur > maxn:
            maxn, tmaxn = dcur, maxn
        else:
            tmaxn = max(tmaxn, dcur)
    for x in cls:
        tx = x if x > 0 else -x
        dcur = d[tx]
        if dcur == maxn:
            equ[cur].add(x)
            var[x].add(cur)
        else:
            stk[dcur][1].append((cur, x)) #equ_modify
            stk[dcur][3].append((x, cur)) #var_modify
    return tmaxn

def cdcl():
    global stk, ind, var, equ, dag, is_sat, n, chooseVariable
    stk = [[[0, True], [], [], [], []] for i in range(n + 1)]
    tail = 0
    conflict, s = propagation(0, stk[0][1], stk[0][2], stk[0][3], stk[0][4])
    if conflict:
        return
    jumpflag = False
    while tail >= 0:
        if not ind:
            is_sat = True
            return
        if not jumpflag:
            tail += 1
            v = chooseVariable()
            lab = True
            if v < 0:
                v, lab = -v, False
                dag[v] = set([v])
            else:
                dag[v] = set([-v])
            stk[tail][0][0] = v
            setVariable(tail, v, lab, stk[tail][1], stk[tail][2], stk[tail][3])
        else:
            jumpflag = False
        conflict, s = propagation(tail, stk[tail][1], stk[tail][2], stk[tail][3], stk[tail][4])
        if not conflict:
            continue
        if not tail:
            return
        jumpto = clauseLearning(s)
        jumpflag = True
        while tail > jumpto:
            undoChange(stk[tail][1], stk[tail][2], stk[tail][3], stk[tail][4])
            stk[tail][1].clear()
            stk[tail][2].clear()
            stk[tail][3].clear()
            stk[tail][4].clear()
            dag[stk[tail][0][0]].clear()
            tail -= 1

def solve(cases, st = ''):
    global lst, is_sat, n, ans, ind, chooseVariable
    if cases == 0:
        chooseVariable = chooseVariableother
    else:
        chooseVariable = chooseVariableflat
    
    if st == '':
        n, lst = CNFparser.parse()
    else:
        n, lst = CNFparser.parse(st)

    is_sat = False
    prepare()
    if not ind:
        is_sat = True
    elif n:
       cdcl() 

    if is_sat:
        print('s SATISFIABLE')
        #for i in range(1, n + 1):
            #print('x %d = %d' % (i, ans[i]))
        #if not check():
            #print('Conflict')
    else:
        print('s UNSATISFIABLE')


def main():
    if len(sys.argv) == 1:
        solve()
    elif len(sys.argv) == 2:
        solve(sys.argv[1])
    else:
        print('Invalid Argv')
        return


if __name__ == '__main__':
    main()
