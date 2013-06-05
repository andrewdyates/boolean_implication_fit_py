#!/usr/bin/python
"""Compute all pairs boolean class.

USE:
python script.py fname=nice.may3.Eg.expr.gold.celegans.csv b=0.3
"""
import sys
import matrix_io as mio
from __init__ import *
import cPickle as pickle


def main(fname=None, pkl=True, **kwds):
  assert fname
  if isinstance(pkl, basestring) and pkl.lower() in ('f','false','none'): pkl = False
  if 'b' in kwds: kwds['b'] = float(kwds['b'])
  if 'z_th' in kwds: kwds['z_th'] = float(kwds['z_th'])
  if 'err_th' in kwds: kwds['err_th'] = float(kwds['err_th'])
  if 'd_th' in kwds: kwds['d_th'] = float(kwds['d_th'])
  if 'r_th' in kwds: kwds['r_th'] = float(kwds['r_th'])
  D = mio.load(fname)
  print "Computing all pairs boolean class..."
  CLS = compute_all(D['M'], **kwds)
  print "Saving %s..." % (fname+'.bool.tab')
  mio.save(CLS, fname+'.bool.tab', fmt="%d", row_ids=D['row_ids'], col_ids=D['row_ids'])
  if pkl:
    print "Saving %s..." % (fname+'.bool.pkl')
    pickle.dump(CLS, open(fname+".bool.pkl","w"))

if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  print args
  main(**args)
