from .dvtDecimal import *


if __name__ == '__main__':
    f = dvtDecimal(-604, 260)
    print(f.fraction())
    f.dispResults()
    print(f.dotWrite(20))
    print(f.intPart)
    print(f.irrPart())
    print(f.repPart)
    print(f.repPartC())
    print(f.periodLen())
    print(f.gcd)
    print(f.initValues)
    print(f.simpValues)
    print(f.mixedF())
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(10, 3)
    h = f + g
    print(h.mixedF())
    print('###')
    i = f / g
    print(i.mixedF())
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(7, 5)
    h = f - g
    print(h.simpValues)
    print(h.sign)
    print(h.mixedF())
    print('###')
    f = dvtDecimal(1, 5)
    g = 5
    h = f * g
    h.dispResults()
    print(h.sign)
    print(h.mixedF())
    print(h.isDecimal())

    f = dvtDecimal(3.2587)
    f.dispResults()

    f = dvtDecimal('0123456789')
    print(f.simpValues)

    f = dvtDecimal(18,5)
    print(f.mixedF())
    f.tolerance=1e-10
    print(f.egyptFractions())
    f.tolerance = 1e-8
    print(f.egyptFractions(lim=5))
    print(f.egyptFractions(eF=4))
    print(f.intPart)
    print(f.egyptG2())
    
    f = dvtDecimal(5, 121)
    print(f.egyptFractions(eF=3, lim=1))
    print(f.tolerance)
    f.tolerance = 1e-30
    print(f.egyptFractions(eF=3))
    for i in range(100,110):
        f = dvtDecimal(1, i)
        a, b =f.egyptG2()
        #d, e, g = f.egyptFractions2(lim=1)[0]
        h, j, k = f.egyptFractions(lim=1)[0]
        print(f.initValues, b, j)

    h = dvtDecimal(1,200)
    print(h.egyptG2())
    print(h.egyptFractions())
    #print(h.egyptFractions2(lim=1))

    h = dvtDecimal(18,5)
    s = h.egyptFractions()
    print(s)
    s = h.egyptFractions(lim=5)
    print(s)
    s = h.egyptFractions(eF=4, lim=0)
    print(s)
    print(len(s))
    print(h.intPart)
    print(h.egyptG2())
    # s = set(tuple(i) for i in s)
    # t = h.egyptFractions2(lim='all')
    # t = set(tuple(i) for i in t)
    # print([ p in t for p in t^s])
