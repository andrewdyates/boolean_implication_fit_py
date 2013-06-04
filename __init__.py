#!/usr/bin/python
from __future__ import division
import numpy as np

mse_f = lambda s, ss, n: ss - s**2/n

def stepfit(v):
  """Efficient algorithm for finding LSE step-up partition."""
  x = np.sort(v)
  xsq = x**2
  k, mse = -1, np.inf
  s_low, ss_low = 0, 0
  s_high, ss_high = np.sum(x), np.sum(xsq)
  n = len(v)
  for i in xrange(0,n-1):
    s_low += x[i]
    ss_low += xsq[i]
    s_high -= x[i]
    ss_high -= xsq[i]
    mse_i = mse_f(s_low, ss_low, i+1) + mse_f(s_high, ss_high, n-(i+1))
    if mse_i < mse:
      k, mse = i, mse_i
  thresh = (x[k]+x[k+1])/2
  return thresh, k


def M2thresh(M, Steps, b, z_th=3, err_th=0.1, d_th=1, r_th=1/3):
  """Convert matrix to low, interval, high enumeration."""
  # if d_th is None.... compute from formula in paper
  # convert entries of M into low, interval, high
  n = np.size(M,0)
  S = np.matrix(Steps).T
  H = np.matrix(M > (S+b))
  L = np.matrix(M < (S-b))
  U = ~(H|L)
  # counts per quadrant
  QLL = np.dot(L,L.T)
  QLH = np.dot(L,H.T)
  QHL = np.dot(H,L.T)
  QHH = np.dot(H,H.T)
  QU = np.dot(U,U.T)
  # get sparsity for each quad
  XL = QLL + QLH
  YL = QLL + QHL
  XH = QHL + QHH
  YH = QLH + QHH
  ALL = QLL + QLH + QHL + QHH

  def get_sparse(Q,X,Y):
    Exp = X*Y/ALL
    Z = ((Exp-Q) / np.sqrt(Exp)) > z_th
    Err = 0.5 * (Q/X + Q/Y) < err_th
    D = Q <= d_th
    return (Z & Err) | D

  SLL = get_sparse(QLL,XL,YL)
  SLH = get_sparse(QLH,XL,YH)
  SHL = get_sparse(QHL,XH,YL)
  SHH = get_sparse(QHL,XH,YH)

  # assign class enumerations
  CLS = np.ones((n,n))*4 # by default, assign all UNL
  CLS[~SLL & ~SLH & SHL & ~SHH] = 1
  CLS[~SLL & SLH & SHL & ~SHH] = 2
  CLS[~SLL & SLH & ~SHL & ~SHH] = 3
  CLS[~SLL & ~SLH & ~SHL & SHH] = 5
  CLS[SLL & ~SLH & ~SHL & SHH] = 6
  CLS[SLL & ~SLH & ~SHL & ~SHH] = 7
  CLS[QU > r_th*n] = 0
  
  return CLS
