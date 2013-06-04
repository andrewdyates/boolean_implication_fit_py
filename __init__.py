#!/usr/bin/python
from __future__ import division
import numpy as np

mse_f = lambda s, ss, n: ss - s**2/n

def compute_all(M, b=None, **kwds):
  """Compute all-pairs bool, return CLS matrix."""
  steps = []
  for row in M:
    steps.append(stepfit(row)[0])
  if b is None:
    stds = np.std(M,1)
    b = np.percentile(stds, 3)*2
  CLS = all_pairs_bool(M, steps, b, **kwds)
  return CLS
  

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


def all_pairs_bool(M, Steps, b, z_th=3, err_th=0.1, d_th=1, r_th=2/3):
  """Compute all-pairs boolean enumeration.

  0:NA, 1:YX, 2:PC, 3:XY, 4:UNL, 5:MX, 6:NC, 7:OR
  """
  # if d_th is None.... compute from formula in paper
  # convert entries of M into low, interval, high
  m, n = np.size(M,0), np.size(M,1)
  S = np.matrix(Steps).T
  H = np.matrix(M > (S+b), dtype=np.int)
  L = np.matrix(M < (S-b), dtype=np.int)
  # counts per quadrant
  QLL = np.dot(L,L.T)
  QLH = np.dot(L,H.T)
  QHL = np.dot(H,L.T)
  QHH = np.dot(H,H.T)

  # get sparsity for each quad
  XL = np.array(QLL + QLH)
  YL = np.array(QLL + QHL)
  XH = np.array(QHL + QHH)
  YH = np.array(QLH + QHH)
  ALL = QLL + QLH + QHL + QHH

  def get_sparse(Q,X,Y):
    Exp = (X*Y)/ALL
    Z = ((Exp-Q) / np.sqrt(Exp)) > z_th # similar to chi-squared
    Err = 0.5 * (Q/X + Q/Y) < err_th
    D = Q <= d_th
    return (Z & Err) | D

  SLL = get_sparse(QLL,XL,YL)
  SLH = get_sparse(QLH,XL,YH)
  SHL = get_sparse(QHL,XH,YL)
  SHH = get_sparse(QHH,XH,YH)

  # assign class enumerations
  CLS = np.ones((m,m), dtype=np.int)*4 # by default, assign all UNL
  CLS[~SLL & ~SLH & SHL & ~SHH] = 3    # note: X and Y swapped for actual X/Y "scatterplot" mapping
  CLS[~SLL & SLH & SHL & ~SHH] = 2
  CLS[~SLL & SLH & ~SHL & ~SHH] = 1
  CLS[~SLL & ~SLH & ~SHL & SHH] = 5
  CLS[SLL & ~SLH & ~SHL & SHH] = 6
  CLS[SLL & ~SLH & ~SHL & ~SHH] = 7
  CLS[ALL < (1-r_th)*n] = 0
  return CLS
