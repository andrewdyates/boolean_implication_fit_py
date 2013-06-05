from script_weak import *
import matrix_io as mio

D = mio.load("nice.may3.Eg.expr.gold.celegans.csv")
WEAK = main("nice.may3.Eg.expr.gold.celegans.csv")
print WEAK
print WEAK[3,6], WEAK[6,3]
r3 = np.array(D['M']>0.2,dtype=np.int)[3,]
r6 = np.array(D['M']>0.2,dtype=np.int)[6,]
print D['row_ids'][3], r3
print D['row_ids'][6], r6
print r3-r6
