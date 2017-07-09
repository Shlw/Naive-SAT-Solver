# Parse DIMACS-CNF Format
#
# Errors:
#   Multiple Parameter: 'p' occurred more than once
#   Not Number: encountered non-number when parsing
#   File Error: unable to read file
#   Invalid Argv: misusage
#   No Parameter: no 'p' occurred

import sys

def translate(s):
    return list(map(int, s.split()))

def formalize(lst):
    ret = [[]]
    n = 0
    for x in lst:
        if x:
            ret[n].append(x)
        else:
            ret.append([])
            n += 1
    while [] in ret:
        ret.remove([])
    return ret

def readfromconsole():
    lst = []
    n = 0
    visP = False
    while True:
        try:
            s = input()
            if not len(s):
                pass
            elif s[0] == '%':
                pass
            elif s[0] == 'c':
                pass
            elif s[0] == 'p':
                if visP:
                    print('Multiple Parameter')
                    lst = []
                    n = 0
                    break
                visP = True
                try:
                    n = int(s.split()[2])
                except:
                    print('Not Number')
                    lst = []
                    n = 0
                    break
            else:
                try:
                    lst += translate(s)
                except:
                    print('Not Number')
                    lst = []
                    n = 0
                    break
        except:
            break

    if not visP:
        print('No Parameter')
        return [0, []]
    else:
        return [n, formalize(lst)]

def readfromfile(filepath):
    lst = []
    n = 0
    visP = False
    try:
        f = open(filepath, 'r')
        for s in f.readlines():
            if not len(s):
                pass
            elif s[0] == '%':
                pass
            elif s[0] == 'c':
                pass
            elif s[0] == 'p':
                if visP:
                    print('Multiple Parameter')
                    lst = []
                    n = 0
                    break
                visP = True
                try:
                    n = int(s.split()[2])
                except:
                    print('Not Number')
                    lst = []
                    n = 0
                    break
            else:
                try:
                    lst += translate(s)
                except:
                    print('Not Number')
                    lst = []
                    n = 0
                    break
        f.close()
    except:
        print('File Error')
        return [0, []]

    if not visP:
        print('No Parameter')
        return [0, []]
    else:
        return [n, formalize(lst)]

def parse(filepath = ''):
    if filepath == '':
        ret = readfromconsole() 
    else:
        ret = readfromfile(filepath)
    return ret

def main():
    if len(sys.argv) == 1:
        a = parse()
    elif len(sys.argv) == 2:
        a = parse(sys.argv[1])
    else:
        a = 'Invalid Argv'
    print(a)

if __name__ == '__main__':
    main()
