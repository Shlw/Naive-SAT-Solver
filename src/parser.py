# parse DIMACS-CNF format
import sys

def translate(s):
    return list(map(int,s.split()))

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
    while True:
        try:
            s = input()
            if not len(s):
                pass
            elif s[0] == 'c':
                pass
            elif s[0] == 'p':
                pass
            else:
                try:
                    lst += translate(s)
                except:
                    print('Not Number')
                    lst = []
                    break
        except:
            break
    return formalize(lst)

def readfromfile(filepath):
    lst = []
    try:
        f = open(filepath, 'r')
        for s in f.readlines():
            if not len(s):
                pass
            elif s[0] == 'c':
                pass
            elif s[0] == 'p':
                pass
            else:
                try:
                    lst += translate(s)
                except:
                    print('Not Number')
                    lst = []
                    break
        f.close()
    except:
        print('File Error')
        return []
    return formalize(lst)

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
        a = 'Incorrect Parameter Number'
    print(a)

if __name__ == '__main__':
    main()
