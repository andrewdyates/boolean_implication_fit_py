from __init__ import *
import numpy as np

def main():
  v = np.array([1,2,3,4,5,6,7,8,9,10])
  H = np.matrix([[0,0,0,1],[1,1,1,0],[0,0,0,1]])
  L = np.matrix([[1,1,0,0],[0,0,0,1],[1,1,1,0]])
  print stepfit(v)

if __name__ == "__main__":
  main()
