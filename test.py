from __init__ import *
import numpy as np
import matrix_io as mio

def main():
  v = np.array([1,2,3,4,5,6,7,8,9,10])
  H = np.matrix([[0,0,0,1],[1,1,1,0],[0,0,0,1]])
  L = np.matrix([[1,1,0,0],[0,0,0,1],[1,1,1,0]])
  print stepfit(v)
  D = mio.load("nice.may3.Eg.expr.gold.celegans.csv")
  M = D['M']
  Steps = []
  for row in M:
    Steps.append(stepfit(row)[0])
  b = 0.1726519*2
  CLS = M2thresh(M, Steps, b)
  print CLS
  

if __name__ == "__main__":
  main()
