import plumed
import wham
import matplotlib.pyplot as plt
import numpy as np

fes_rg=plumed.read_as_pandas("fes_rg.dat").replace([np.inf, -np.inf], np.nan).dropna()
min=np.min(fes_rg.ffrg)
fes_rg.ffrg = fes_rg.ffrg - min
plt.plot(fes_rg.rg,fes_rg.ffrg/2.4943387854)
plt.xlim((0.35,0.9))
plt.ylim((-0.1,1.75))
plt.xlabel("rg [nm]")
plt.ylabel("$W(rg) [kT]$")
plt.show()
plt.savefig('rg-wham.svg', transparent=True)

plt.clf()
histo_rg=plumed.read_as_pandas("histo.dat").replace([np.inf, -np.inf], np.nan).dropna()
plt.plot(histo_rg.rg,histo_rg.hhrg)
#plt.xlim((0.35,0.9))
#plt.ylim((-0.1,2))
plt.xlabel("rg [nm]")
plt.ylabel("P(rg)")
plt.show()
plt.savefig('histo.svg', transparent=True)

plt.clf()
#for i in range(12):
#	histo_rg=plumed.read_as_pandas("histo_{}.dat".format(i)).replace([np.inf, -np.inf], np.nan).dropna()
#	plt.plot(histo_rg.rg,histo_rg.hhrg)
#plt.xlim((0.35,0.9))
#plt.ylim((-0.1,2))
#plt.xlabel("rg [nm]")
#plt.ylabel("P(rg)")
#plt.show()
#plt.savefig('histo_all.svg', transparent=True)


