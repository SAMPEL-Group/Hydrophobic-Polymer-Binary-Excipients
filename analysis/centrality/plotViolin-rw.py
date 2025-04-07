import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import rc
import math
from sklearn.neighbors import KernelDensity
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=False)

font = "Helvetica"
hfont = {'fontname':'Helvetica'}
big = 36
medium = 24
small = 12
xsmall = 10
ms=8
lw=2
cs=6

watTitle = ["0arg"]
argTitles = ["47arg", "93arg", "185arg"]
gluTitles = ["47glu", "93glu", "185glu"]
lysTitles = ["47lys", "93lys", "185lys"]
gdmTitles = ["47gdm", "93gdm", "185gdm"]
glyTitles = ["47gly", "93gly", "185gly"]
arggluTitles = ["48arg-glu", "94arg-glu", "186arg-glu"]
arglysTitles = ["48arg-lys", "94arg-lys", "186arg-lys"]
lysgluTitles = ["48lys-glu", "94lys-glu", "186lys-glu"]

watLabel = ["0.0 M"]
argLabels = ["0.25 M Arg", "0.5 M Arg", "1.0 M Arg"]
gluLabels = ["0.25 M Glu", "0.5 M Glu", "1.0 M Glu"]
lysLabels = ["0.25 M Lys", "0.5 M Lys", "1.0 M Lys"]
arggluLabels = ["0.25 M Arg/Glu", "0.5 M Arg/Glu", "1.0 M Arg/Glu"]
arglysLabels = ["0.25 M Arg/Lys", "0.5 M Arg/Lys", "1.0 M Arg/Lys"]
lysgluLabels = ["0.25 M Lys/Glu", "0.5 M Lys/Glu", "1.0 M Lys/Glu"]
    
watColor = ["black"]

argColors = list(pl.cm.Reds(np.linspace(0.3,1,len(argTitles))))
gluColors = list(pl.cm.Blues(np.linspace(0.3,1,len(gluTitles))))
lysColors = list(pl.cm.YlOrBr(np.linspace(0.3,1,len(lysTitles))))
gdmColors = list(pl.cm.Purples(np.linspace(0.3,1,len(gdmTitles))))
glyColors = list(pl.cm.Purples(np.linspace(0.3,1,len(glyTitles))))

lysgluColors = list(pl.cm.Greens(np.linspace(0.3,1,len(lysgluTitles))))
arggluColors = list(pl.cm.Purples(np.linspace(0.3,1,len(arggluTitles))))
arglysColors = list(pl.cm.Oranges(np.linspace(0.3,1,len(arglysTitles))))

titles = watTitle + argTitles + gluTitles + lysTitles + arggluTitles + arglysTitles + lysgluTitles
colors = watColor + argColors + gluColors + lysColors + arggluColors + arglysColors + lysgluColors
labels = watLabel + argLabels + gluLabels + lysLabels + arggluLabels + arglysLabels + lysgluLabels

label = "fragmentation-wat_f-seq"

runs = np.arange(1,4,1)
windows = np.arange(0,12,1)

def openFile():
    data = pd.read_csv("output/fragmentationThreshold-{}-reus-{}-{}.dat".format(title, window, run), sep=" ")
    # data = pd.read_csv("output/centrality-{}-reus-{}-{}.dat".format(title, window, run), sep=" ")
    rg = pd.read_table("../gyrate/gyrate-{}-reus-{}-{}.xvg".format(title, window, run), index_col=False, skipinitialspace=True, skiprows=27, sep=" ", names=['time','rg'])        
    rg = rg.set_index(np.arange(0, len(rg.rg), 1))
    
    weights = pd.read_table("../weights/{}-{}-{}-weights.dat".format(title, window, run), skiprows=0, skipinitialspace=True, sep=" ", names=['w'])
    weights.reset_index(drop=True, inplace=True)

    data = pd.concat((data, rg.rg, weights.w), axis=1)
    return data

import weighted
from matplotlib.cbook import violin_stats
from scipy import stats
from scipy.stats import gaussian_kde

def vdensity_with_weights(data, weights):
    ''' Outer function allows inner function access to weights. '''
    def vdensity(data, coords):
        ''' Custom weighted violin stats function '''
        # Gaussian KDE with weights
        weighted_cost = gaussian_kde(data, weights=weights)
        
        # Evaluate the KDE on the provided coords
        return weighted_cost(coords)

    return vdensity  # Return the function, not the result

def custom_violin_stats(data, weights):
    # Get weighted median and mean
    median = weighted.quantile_1D(data, weights, 0.5)  # Replace with correct weighted quantile function
    mean, sumw = np.ma.average(data, weights=weights, returned=True)
    
    # Pass the custom KDE function to violin_stats
    density_func = vdensity_with_weights(data, weights)
    results = violin_stats(data, density_func)
    
    # Update result dictionary with custom statistics
    results[0][u"mean"] = mean
    results[0][u"median"] = median

    return results

def plotViolin(data, density, ls, fcolor):
    q1, m, q3 = np.percentile(data, [25, 50, 75])
    violins = ax.violin(density, positions=[j], showmeans=False)
    ax.scatter(j, m, marker='o', color='white', s=60, zorder=3)
    ax.vlines(j, q1, q3, color=colors[i], linestyle='-', lw=7)
    
    for v in violins['bodies']:
        v.set_facecolor(fcolor)
        v.set_edgecolor(colors[i])
        v.set_linewidth(3)
        v.set_linestyle(ls)
        v.set_alpha(0.5)
    
    for partname in ('cbars', 'cmins', 'cmaxes'):
        vp = violins[partname]
        vp.set_edgecolor(colors[i])
        vp.set_linewidth(1)
        vp.set_linestyle(ls)
        
### Plot centrality measures
i=0
j=0
x_list=[]
allData=[]
fig, ax = plt.subplots(figsize=(16,8))
for title in titles:
    catData=[]
    for run in runs:
        for window in windows:
            try:
                data = openFile()
                catData.append(data)
            except OSError:
                pass
            
    # x_list.append(j+0.5)
    x_list.append(j)
    catData = pd.concat(catData, axis=0)
    catData = catData.fillna(0)
    
    f, u = catData[catData.rg <= 0.6], catData[catData.rg > 0.6]
    
    # Truncate for fragmentation thresholds
    f = f[f.f>0.07]
    u = u[u.f>0.07]
    vpstats1 = custom_violin_stats(np.asarray(f.f), np.asarray(f.w))
    # plotViolin(f.watClose, f.w, '-', colors[i])
    plotViolin(f.f, vpstats1, '-', colors[i])
    # allData.append(f.watClose)
    j+=1    
    vpstats2 = custom_violin_stats(np.asarray(u.f), np.asarray(u.w))
    plotViolin(u.f, vpstats2, '--', "white")
    j+=1    
    i+=1
    
    delta = np.mean(f.f) - np.mean(u.f)
    print(title, np.round(delta,3))
    
#%%
plt.yticks(fontsize=medium, **hfont)
# plt.ylabel(r"$C^{Wat}_{c}$", **hfont, fontsize=big)
plt.ylabel(r"$f$", **hfont, fontsize=big)

ax.yaxis.set_major_locator(ticker.AutoLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

ax.tick_params(axis='both', which='both', direction='in', labelsize=medium)
ax.tick_params(axis='both', which='major', length=12, width=2)
ax.tick_params(axis='both', which='minor', length=8, width=2)

ax.set_xticks(x_list, labels, fontsize=medium, **hfont, rotation=30)
from matplotlib.ticker import FormatStrFormatter
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

for tick in ax.xaxis.get_majorticklabels():
    tick.set_horizontalalignment("right")

plt.tight_layout()

# plt.savefig('figures/{}.png'.format(label), transparent=True, dpi=300)

# #%% Compute Earth Mover Distance
# from scipy.stats import wasserstein_distance as WD
# from scipy.stats import ttest_ind

# earthMovers = []
# pList = []
# # ciList = []
# for i in range(len(allData)):
#     uVals = allData[0]
#     vVals = allData[i]
#     earthMovers.append(WD(uVals, vVals))
    
#     t, p = ttest_ind(uVals, vVals, equal_var=False)
    
#     # ciList.append(labels[i], ci)
#     if p < 0.05:
#         pList.append((labels[i], p))

# header = "title emd"
# emOutput = np.vstack((titles, np.round(earthMovers,3))).T
# from numpy import savetxt
# savetxt('output/emd/earthMovers-{}-wat.dat'.format(label), emOutput, header=header, fmt='%s', delimiter=' ')
