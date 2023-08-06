from .dvtDecimal import *


if __name__ == '__main__':
    # f = dvtDecimal(-604, 260)
    # print(eval(f.fraction))
    # f.dispResults()
    # print(f.dotWrite(20))
    # print(f.intPart)
    # print(f.irrPart)
    # print(f.repPart)
    # print(f.repPartC)
    # print(f.periodLen)
    # print(f.gcd)
    # print(f.initValues)
    # print(f.simpValues)
    # print(f.mixedF)
    # print('###')
    # f = dvtDecimal(1, 5)
    # g = dvtDecimal(10, 3)
    # h = f + g
    # print(h.mixedF)
    # print('###')
    # i = f / g
    # print(i.mixedF)
    # print('###')
    # f = dvtDecimal(1, 5)
    # g = dvtDecimal(7, 5)
    # h = f - g
    # print(h.simpValues)
    # print(h.sign)
    # print(h.mixedF)
    # print('###')
    # f = dvtDecimal(1, 5)
    # g = 5
    # h = f * g
    # h.dispResults()
    # print(h.sign)
    # print(h.mixedF)
    # print(h.isDecimal())

    # f = dvtDecimal(3.2587)
    # f.dispResults()

    # f = dvtDecimal('0123456789')
    # print(f.simpValues)

    # f = dvtDecimal(18,5)
    # print(f.mixedF)
    # f.tolerance=1e-10
    # print(f.egyptFractions())
    # f.tolerance = 1e-8
    # print(f.egyptFractions(lim=5))
    # print(f.egyptFractions(eF=4))
    # print(f.intPart)
    # print(f.egyptG2)
    
    # f = dvtDecimal(5, 121)
    # print(f.egyptFractions(eF=5))
    # print(f.tolerance)
    # f.tolerance = 1e-30
    # print(f.egyptFractions(eF=5))
    for i in range(2,101):
        f = dvtDecimal(1, i)
        a, b =f.egyptG2
        d, e, g = f.egyptFractions(lim=1)[0]
        if b!=e-1: print(f.initValues, b, e)

    h = dvtDecimal(1,26)
    print(h.egyptG2)
    print(h.egyptFractions())
