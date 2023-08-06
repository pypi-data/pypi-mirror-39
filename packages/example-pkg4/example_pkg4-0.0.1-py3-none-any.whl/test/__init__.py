from example_pkg4 import TestClass, TestClass2
from example_pkg4.compo1 import Compo1, Compo1_1
from example_pkg4.compo2 import Compo1_2, Compo2

a = TestClass()
b = TestClass2()
c = Compo1()
d = Compo1_1()
e = Compo2()
f = Compo2()
print(a.testFunc())
print(a.testFunc2())
print(b.testFunc())
print(c.testFunc())
print(d.testFunc())
print(e.testFunc())