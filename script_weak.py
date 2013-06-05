#!/usr/bin/python
"""Compute all pairs boolean class.

USE:
python script_weak.py fname=nice.may3.Eg.expr.gold.celegans.csv 
"""
import sys
import matrix_io as mio
from __init__ import *
import cPickle as pickle


def main(fname=None, pkl=True, **kwds):
  assert fname
  if isinstance(pkl, basestring) and pkl.lower() in ('f','false','none'): pkl = False
  if 'err' in kwds: kwds['err'] = int(kwds['err'])
  if 'th' in kwds: kwds['th'] = float(kwds['th'])

  D = mio.load(fname)
  print "Computing all pairs weak boolean class..."
  WEAK = all_pairs_weak(D['M'], **kwds)
  print "Saving %s..." % (fname+'.weak.tab')
  mio.save(WEAK, fname+'.weak.tab', fmt="%d", row_ids=D['row_ids'], col_ids=D['row_ids'])
  if pkl:
    print "Saving %s..." % (fname+'.weak.pkl')
    pickle.dump(WEAK, open(fname+".weak.pkl","w"))
  return WEAK

if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  print args
  main(**args)
