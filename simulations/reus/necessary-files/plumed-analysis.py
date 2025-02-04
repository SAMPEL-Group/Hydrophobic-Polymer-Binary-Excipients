import plumed
import wham
import numpy as np

kBT=300*8.314462618*0.001

col=[]
for i in range(12):
	col.append(plumed.read_as_pandas("all_bias." + str(i)+".dat"))
	
bias=np.zeros((len(col[0]["restraint.bias"]),12))
for i in range(12):	
	bias[:,i]=col[i]["restraint.bias"][-len(bias):]

print(bias.shape)

w=wham.wham(bias,T=kBT)
#plt.plot(w["logW"])
#plt.show()
colvar=col[0]
colvar["logweights"]=w["logW"]
plumed.write_pandas(colvar,"bias_wham.dat")
