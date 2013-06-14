#!/usr/bin/python
"""Compute all pairs boolean class.

SAMPLE USES:
python script.py fname=nice.may3.Eg.expr.gold.celegans.csv

python script.py fname=nice.may3.Eg.expr.gold.celegans.csv b=0.3

FNAME=$HOME/celegans/jun5.GSE2180.SCAN.select.tab
time python $HOME/code/boolean_implication_fit_py/script.py fname=$FNAME b=0.08797455 z_th=2.5
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
  print "Loading data..."
  D = mio.load(fname)
  print "Computing all pairs boolean class for a (%d x %d) data matrix (%d x %d result matrix)..." % \
      (D['M'].shape[0], D['M'].shape[1], D['M'].shape[0], D['M'].shape[0])
  CLS, steps, b = compute_all_bool(D['M'], **kwds)
  if 'z_th' in kwds:
    z = float(kwds['z_th'])
  else:
    z = 3.0
  fname_out = '%s.b%.4f.z%.2f.bool.tab' % (fname, b, z)
  print "Saving %s..." % (fname_out)
  mio.save(CLS, fname_out, fmt="%d", row_ids=D['row_ids'], col_ids=D['row_ids'])
  steps_fname = fname+".steps.txt"
  print "Saving high/low thresholds to %s in original row order..." % steps_fname
  open(steps_fname,"w").write("\n".join(("%f"%x for x in steps)))
  if pkl:
    fname_pkl_out = fname_out.rpartition('.')[0]+'.pkl'
    print "Saving %s..." % (fname_pkl_out)
    pickle.dump(CLS, open(fname_pkl_out,"w"), protocol=-1)

if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  print args
  main(**args)
