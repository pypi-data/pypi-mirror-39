def doTest(**kwargs):
    print(kwargs)
    doTest2(kwargs)

def doTest2(kwargs):
    print(kwargs)

doTest(a=1,b=2,c=3)
