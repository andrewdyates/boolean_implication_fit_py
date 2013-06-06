#!/usr/bin/python
from __future__ import division
import numpy as np

mse_f = lambda s, ss, n: ss - s**2/n

def compute_all_bool(M, b=None, **kwds):
  """Compute all-pairs bool, return all relevant results."""
  print "Computing high/low thresholds using adaptive regression..."
  steps = []
  for row in M:
    steps.append(stepfit(row)[0])
  if b is None:
    stds = np.std(M,1)
    b = np.percentile(stds, 3)*2
    print "Computed signal 2*std to be %f" % b
  else:
    print "Using provided signal 2*std, %f" % b
  print "Computing boolean implications..."
  CLS = all_pairs_bool(M, steps, b, **kwds)
  return CLS, steps, b

def compute_all_weak(M, err=1, th=0.2, debug=False):
  """Compute all-pairs weak, return all relevant results."""
  WEAK = all_pairs_weak(M, err, th, debug)
  return WEAK, err, th

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
  # set zero values in X, Y margins to -1 to avoid division by zero.
  # any such entry will be assigned "4" class unless assigned "0" class.
  BAD_MARGIN = (XL==0)|(YL==0)|(XH==0)|(YH==0)
  TOO_FEW = ALL < (1-r_th)*n
  XL[BAD_MARGIN] = 1
  YL[BAD_MARGIN] = 1
  XH[BAD_MARGIN] = 1
  YH[BAD_MARGIN] = 1
  YH[BAD_MARGIN] = 1
  ALL[TOO_FEW] = 1 # includes 0 case

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
  CLS[BAD_MARGIN] = 4
  CLS[TOO_FEW] = 0
  return CLS

def all_pairs_weak(M, err=1, th=0.2, debug=False):
  """Compute all-pairs weak enumeration.
  0:NC, 1:AND, 2:RN4C, 3: CN4R, 4:XOR, 5:MIX
  """
  t = np.transpose
  m,n = M.shape
  B = np.array(M>=th,dtype=np.int)
  BN = np.array(M<th,dtype=np.int)
  AND_B = np.dot(B,t(B))
  N = np.dot(BN,t(BN))*-1 + n      # number of entries where at least one bit is on
  RN4C_B = N - np.dot(BN,t(B))
  CN4R_B = N - np.dot(B,t(BN))
  XOR_B = RN4C_B + CN4R_B - 2*AND_B
  RN4C_O = RN4C_B - AND_B
  CN4R_O = CN4R_B - AND_B
  if debug:
    print "AND errors"
    print N-AND_B
    print "RN4C_B errors"
    print N-RN4C_B
    print "CN4R_B errors"
    print N-CN4R_B
    print "XOR errors"
    print N-XOR_B

  W = np.ones((m,m), dtype=np.int)*5
  W[N-AND_B <= err] = 1
  W[N-XOR_B <= err] = 4
  W[(N-RN4C_B <= err) & (RN4C_O >= err+1)] = 2
  W[(N-CN4R_B <= err) & (CN4R_O >= err+1)] = 3
  return W
  
