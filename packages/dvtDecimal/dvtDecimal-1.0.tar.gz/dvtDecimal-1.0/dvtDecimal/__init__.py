from .dvtDecimal import *


if __name__ == '__main__':
    f = dvtDecimal(-604, 260)
    print(eval(f.fraction))
    f.dispResults()
    print(f.dotWrite(20))
    print(f.intPart)
    print(f.irrPart)
    print(f.repPart)
    print(f.repPartC)
    print(f.periodLen)
    print(f.gcd)
    print(f.initValues)
    print(f.simpValues)
    print(f.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(10, 3)
    h = f + g
    print(h.mixedF)
    print('###')
    i = f / g
    print(i.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(7, 5)
    h = f - g
    print(h.simpValues)
    print(h.sign)
    print(h.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = 5
    h = f * g
    h.dispResults()
    print(h.sign)
    print(h.mixedF)
    print(h.isDecimal())

    f = dvtDecimal(3.2587)
    f.dispResults()

    f = dvtDecimal('0123456789')
    print(f.simpValues)

    f = dvtDecimal(18,5)
    print(f.mixedF)
    print(f.egyptFractions())
    print(f.egyptFractions(lim=5))
    print(f.egyptFractions(eF=4))
    print(f.intPart)
    print(f.egyptG2)
    
