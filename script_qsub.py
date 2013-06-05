from qsub import *
import os, sys

PATH = os.path.abspath(os.path.dirname(__file__))

def main(nodes=1, ppn=12, hours=72, d="bool", dry=False, **kwds):
  nodes, ppn, hours = int(nodes), int(ppn), int(hours)
  Q = Qsub(jobname=kwds['fname']+"_"+d, n_nodes=nodes, n_ppn=ppn, hours=hours, work_dir=os.path.dirname(kwds['fname']), email=True)
  arg_str = " ".join(["%s=%s"%(k,v) for k,v in kwds.items()])
  if d == "bool":
    cmd = "python %s/script.py %s" % (PATH, arg_str)
  else:
    cmd = "python %s/script_weak.py %s" % (PATH, arg_str)
  print cmd
  Q.add(cmd)
  Q.submit(dry)
  print Q.script()
      
if __name__ == "__main__":
  args = dict([s.split('=') for s in sys.argv[1:]])
  print args
  main(**args)
