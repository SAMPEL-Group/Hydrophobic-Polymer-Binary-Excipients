import pandas as pd
import numpy as np
import seaborn as sns
import hdbscan
from numpy import savetxt
import MDAnalysis as md
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
import copy
from sklearn import preprocessing

font = "Helvetica"
hfont = {'fontname':'Helvetica'}
big = 36
medium = 28
small = 12
xsmall = 10
ms=12
lw=2

#%% Import Data
def open_files():
    dist = pd.read_table("./gyrate-{}-reus-{}-{}.xvg".format(title, idx, j), skipinitialspace=True, index_col=False, skiprows=27, sep=" ", names=['t', 'cv'])
    pmf = pd.read_table("../../avg-pmfs/average_pmf_{}.dat".format(title), skipinitialspace=True, index_col=False, skiprows=1, sep=" ", names=['r', 'p'])
    pmf.p = np.exp(-1*pmf.p)
    return dist, pmf

def binData(cvData, pdf):
    global lowerWalls
    outputCV, outputVal, outputErr = [], [], []
    lowerWalls = pdf.r - (0.5*(pdf.r[1] - pdf.r[0]))
    upperWalls = pdf.r + (0.5*(pdf.r[1] - pdf.r[0]))
    i=0
    for i in range(len(pdf)):
        currBin = cvData[(cvData.cv >= lowerWalls[i]) & (cvData.cv < upperWalls[i])]
        outputCV.append(pdf.r[i])
        outputVal.append(np.mean(currBin.cv))
        outputErr.append(np.std(currBin.cv))
    binnedData = pd.DataFrame(np.vstack((outputCV, outputVal, outputErr)).T, columns=["cv", "val", "stdv"])
    return binnedData

def unbiasData(cvData, pdf):
    binnedData = binData(cvData, pdf)
    binnedData = pd.concat((binnedData.val, binnedData.stdv, pdf.p, binnedData.cv), axis=1, ignore_index=True)
    binnedData.dropna(inplace=True)
    binnedData.rename(columns={0:"val", 1:"stdv", 2:"p", 3:"cv"}, inplace=True)
    reweightedData = np.sum(binnedData.val*binnedData.p) / np.sum(binnedData.p)
    reweightedErr = np.sum(binnedData.stdv*binnedData.p) / np.sum(binnedData.p)
    return binnedData, reweightedData, reweightedErr

def findWeights(cvData, pmf):
    cvData = dist
    indices = np.digitize(cvData.cv, lowerWalls[:-1])
    weights = []
    for x in indices:
        weights.append(pmf.p[x])
    weights = weights / np.sum(weights)
    return weights

titles=["0arg", "47arg", "93arg", "185arg",
        "47lys", "93lys", "185lys",
        "47glu", "93glu", "185glu",
        "48arg-glu", "94arg-glu", "186arg-glu",
        "48arg-lys", "94arg-lys", "186arg-lys",
        "48lys-glu", "94lys-glu", "186lys-glu"]
nR = 12
idx = 0

for title in titles:
    dfCat = pd.DataFrame()
    for j in range(1,4):
        for idx in range(0,nR):
            dist, pmf = open_files()
            lowerWalls = pmf.r - (0.5*(pmf.r[1] - pmf.r[0]))
            frameWeights = findWeights(dist, pmf)
            np.savetxt("../weights/{}-{}-{}-weights.dat".format(title, idx, j), frameWeights, fmt='%f', delimiter=' ')
        
            dist.reset_index(drop=True, inplace=True)
            dfCat = pd.concat((dfCat, dist), axis=0)
        
        dfCat.rename(columns={0:"cv"}, inplace=True)
        dist = dfCat
        
        binnedData, reweightedData, reweightedErr = unbiasData(dist, pmf)
        # print(np.round(reweightedData, 3), "+/-", np.round(reweightedErr, 2))
        frameWeights = findWeights(dist, pmf)
    
    #%% Plot
    fig, ax = plt.subplots(figsize=(9,6))
    
    cv_bins = np.linspace(dist.cv.min(), dist.cv.max(), 200)
    cv_hist, cv_edges = np.histogram(dist.cv, cv_bins)
    cv_hist = cv_hist / np.sum(cv_hist)
    plt.plot(cv_bins[:-1], cv_hist, color="firebrick", lw=3)
    
    cv_bins = np.linspace(dist.cv.min(), dist.cv.max(), 200)
    cv_hist, cv_edges = np.histogram(dist.cv, cv_bins, weights=frameWeights)
    cv_hist = cv_hist / np.sum(cv_hist)
    plt.plot(cv_bins[:-1], cv_hist, color="midnightblue", lw=3)
    
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    plt.xticks(fontsize=medium, **hfont)
    plt.yticks(fontsize=medium, **hfont)
    plt.xlabel(r'$R_{g}$ [nm]', **hfont, fontsize=big)
    plt.ylabel(r"P($R_{g}$)", **hfont, fontsize=big)
    # plt.ylim(0,0.1)
    plt.xlim(0.35,0.9)
    ax.tick_params(axis='both', which='both', direction='in', labelsize=medium)
    ax.tick_params(axis='both', which='major', length=6, width=2)
    ax.tick_params(axis='both', which='minor', length=4, width=2)
    plt.tight_layout()
    plt.savefig('figures/cv-reweight-{}.png'.format(title), dpi=300)
    plt.show()
