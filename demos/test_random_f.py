import random

def f1():
  print "1"
  functions.remove(f1)
def f2():
  print "2"
  functions.remove(f2)
def f3():
  print "3"
  functions.remove(f3)
def f4():
  print "4"
  functions.remove(f4)

functions = [f1,f2,f3,f4]

while functions != [] :
  random.choice(functions)()
