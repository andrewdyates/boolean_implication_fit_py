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
  print "Computing all pairs weak class for a (%d x %d) data matrix (%d x %d result matrix)..." % \
      (D['M'].shape[0], D['M'].shape[1], D['M'].shape[0], D['M'].shape[0])
  WEAK, err, th = compute_all_weak(D['M'], **kwds)
  print "Used parameters err=%d, cutoff th=%f" % (err, th)

  fname_out = "%s.err%d.th%.4f.weak.tab" % (fname, err, th)
  print "Saving %s..." % (fname_out)
  mio.save(WEAK, fname_out, fmt="%d", row_ids=D['row_ids'], col_ids=D['row_ids'])
  if pkl:
    fname_pkl_out = fname_out.rpartition('.')[0]+'.pkl'
    print "Saving %s..." % (fname_pkl_out)
    pickle.dump(WEAK, open(fname_pkl_out,"w"))
  return WEAK

if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  print args
  main(**args)
