#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 12:23:43 2018

@author: antony
"""

import glob
import numpy as np
import pandas as pd
import sys
import matplotlib
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import libplot

class _MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
    

class ExtGSEA(object):
    def __init__(self, ranked_gene_list, ranked_score, np=100, w=1):
        self.__w = w
        
        l = len(ranked_gene_list)
        
        rk = ranked_gene_list + ranked_gene_list
        rsc = np.concatenate((ranked_score, -ranked_score), axis=0)
        ix = np.argsort(rsc)[::-1]
        
        pn = np.concatenate((np.ones(l), -np.ones(l)), axis=0)
        
        self.__ranked_gene_list = rk[ix]
        self.__ranked_score = rsc[ix]
        self.__pn = pn[ix]
        
    def gsea(self, gs1, gs2):
        l = len(self.__ranked_gene_list)
        
        isgs = np.zeros(l)
        
        for i in range(0, l):
            if (self.__pn[i] > 0 and self.__ranked_gene_list[i] in gs1) or (self.__pn[i] < 0 and self.__ranked_gene_list[i] in gs2):
                isgs[i] = 1
        
        # Compute ES
        
        score_hit = np.cumsum(np.abs(self.__ranked_score * isgs) ** self.__w)
        score_hit = score_hit / score_hit[-1]
        score_miss = np.cumsum(1 - isgs)
        score_miss = score_miss / score_miss[-1]
        es_all = score_hit - score_miss
        es = np.max(es_all) - min(es_all)
        
        isen = np.zeros(l)
        
        if es < 0:
            ixpk = np.where(es_all == np.min(es_all))
            isen[ixpk:] = 1
            ledge = self.__ranked_gene_list[(np.where(isen == 1)[0]) | (np.where(isgs == 1)[0])]
            ledge = ledge[::-1]
        else:
            ixpk = np.where(es_all == np.max(es_all))
            isen[0:(ixpk + 1)] = 1
            ledge = self.__ranked_gene_list[(np.where(isen == 1)[0]) | (np.where(isgs == 1)[0])]
            
        if np > 0:
            bg = {}
            bg['es'] = np.zeros(np)
            
            for i in range(0, np):
                bg['isgs']  = isgs[np.random.permutation(l)];  
                bg['hit']   = np.cumsum((abs(self.__ranked_score * bg['isgs'])) ** self.__w)
                bg['hit']   = bg['hit'] / bg['hit'][-1]
                bg['miss']  = np.cumsum(1 - bg['isgs']);
                bg['miss']  = bg['miss'] / bg['miss'][-1]
                bg['all']   = bg['hit'] - bg['miss'];
                bg['es'][i] = max(bg['all']) + min(bg['all']);

            if es < 0:
                pv  = np.sum(bg['es'] <= es) / np
                nes = es / np.abs(np.mean(bg['es'][bg['es'] < 0]))
            else:
                pv  = np.sum(bg['es'] >= es) / np
                nes = es / np.abs(np.mean(bg['es'][bg['es'] > 0]))
        else:
            pv = -1
            nes = -1
                
        return es, nes, pv, ledge
                
        
        


def replot(gene_set, phenoPos, phenoNeg, ranking_file, hit_file, nes, pval, fdr):
    libplot.setup()
    
    matplotlib.rcParams['font.size'] = 14
    matplotlib.rcParams['mathtext.default'] = 'regular'
    
    dir=sys.argv[1]
    
    ranking_file=glob.glob(dir, 'ranked_gene_list')
    
    print(ranking_file)
    
    
    
    # import the rankings
    
    rank_data = pd.read_table(ranking_file, sep="\t", header=0, index_col=0)
    hit_data = pd.read_table(hit_file, sep="\t", header=0, index_col=0)
    
    
    
    
    
    #dataFrame of ranked matrix scores
    x = np.arange(rank_data.shape[0])
    
    # the rankings of every gene
    rankings = rank_data.iloc[:, 3].values
    
    # boost values to saturate colors
    heat_map_rankings = rankings * 2
    
    
    hit_ind = hit_data.iloc[:, 4].values
    RES = hit_data.iloc[:, 6].values
    
    x2 = hit_ind.tolist()
    y2 = RES.tolist()
    
    
    # plt.style.use('classic')
    # center color map at midpoint = 0
    norm = _MidpointNormalize(vmin=np.min(rankings), midpoint=0, vmax=np.max(rankings))
    
    
    if x2[0] != 0:
      x2.insert(0, 0)
      y2.insert(0, 0)
    
    if x2[len(x2) - 1] != rank_data.shape[0]:
      x2.append(rank_data.shape[0])
      y2.append(0)
    
    
    
    
    # figsize = (6,6)
    phenoP_label = phenoPos + ' (positively correlated)'
    phenoN_label = phenoNeg + ' (negatively correlated)'
    zero_score_ind = np.abs(rankings).argmin()
    z_score_label = 'Zero cross at ' + str(zero_score_ind)
    nes_label = 'NES: '+ "{:.3f}".format(float(nes))
    pval_label = 'Pval: '+ "{:.3f}".format(float(pval))
    fdr_label = 'FDR: '+ "{:.3f}".format(float(fdr))
    im_matrix = np.tile(heat_map_rankings, (2,1))
    
    # output truetype
    #plt.rcParams.update({'pdf.fonttype':42,'ps.fonttype':42})
    # in most case, we will have mangy plots, so do not display plots
    # It's also convinient to run this script on command line.
    
    # GSEA Plots
    gs = plt.GridSpec(16,1)
    # fig = plt.figure(figsize=figsize)
    fig = plt.figure(figsize=(10, 7))
    
    # Ranked Metric Scores Plot
    ax1 =  fig.add_subplot(gs[9:])
    
    ax1.fill_between(x, y1=rankings, y2=0, color='#2c5aa0')
    ax1.set_ylabel("Ranked list metric", fontsize=14)
        
    ax1.text(.05, .9, phenoP_label, color='red', horizontalalignment='left', verticalalignment='top',
      transform=ax1.transAxes)
    ax1.text(.95, .05, phenoN_label, color='Blue', horizontalalignment='right', verticalalignment='bottom',
      transform=ax1.transAxes)
    
    # the x coords of this transformation are data, and the y coord are axes
    trans1 = transforms.blended_transform_factory(ax1.transData, ax1.transAxes)
    ax1.vlines(zero_score_ind, 0, 1, linewidth=1, transform=trans1, linestyles='--', color='grey')
    ax1.text(zero_score_ind, 0.5, z_score_label,
             horizontalalignment='center',
             verticalalignment='center',
             transform=trans1)
    ax1.set_xlabel("Rank in Ordered Dataset", fontsize=14)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('dimgray')
    ax1.spines['bottom'].set_color('dimgray') #set_color('dimgray')
    #ax1.tick_params(axis='both', which='both', top='off', right='off', left='off')
    ax1.locator_params(axis='y', nbins=5)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda tick_loc,tick_num :  '{:.1f}'.format(tick_loc) ))
    
    # use round method to control float number
    # ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda tick_loc,tick_num :  round(tick_loc, 1) ))
    
    # gene hits
    ax2 = fig.add_subplot(gs[7:9], sharex=ax1)
    
    # the x coords of this transformation are data, and the y coord are axes
    trans2 = transforms.blended_transform_factory(ax2.transData, ax2.transAxes)
    ax2.vlines(hit_ind, 0, 1,linewidth=.5,transform=trans2)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='off', right='off', left='off', labelleft='off')
    
    # colormap
    ax3 =  fig.add_subplot(gs[8:10], sharex=ax1)
    ax3.imshow(im_matrix, aspect='auto', norm=norm, cmap=plt.cm.seismic, interpolation='none') # cm.coolwarm
    ax3.spines['top'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='off', right='off', left='off',labelleft='off')
    
    # Enrichment score plot
    ax4 = fig.add_subplot(gs[:8], sharex=ax1)
    ax4.plot(x2, y2, linewidth=4, color ='#2ca05a')
    ax4.tick_params(axis='both', which='both', color='dimgray')
    ax4.spines['left'].set_color('dimgray')
    ax4.spines['bottom'].set_visible(False) #set_color('dimgray')
    ax4.text(.1, .1, fdr_label, transform=ax4.transAxes)
    ax4.text(.1, .2, pval_label, transform=ax4.transAxes)
    ax4.text(.1, .3, nes_label, transform=ax4.transAxes)
    
    # the y coords of this transformation are data, and the x coord are axes
    trans4 = transforms.blended_transform_factory(ax4.transAxes, ax4.transData)
    ax4.hlines(0, 0, 1, linewidth=.5, transform=trans4, color='grey')
    ax4.set_ylabel("Enrichment score (ES)", fontsize=14)
    ax4.set_xlim(min(x), max(x))
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off')
    ax4.locator_params(axis='y', nbins=5)
    # FuncFormatter need two argment, I don't know why. this lambda function used to format yaxis tick labels.
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda tick_loc,tick_num :  '{:.1f}'.format(tick_loc)) )
    
    # fig adjustment
    fig.suptitle(gene_set, fontsize=16)
    fig.subplots_adjust(hspace=0)
    # fig.tight_layout()
    # plt.close(fig)
    gene_set = gene_set.replace('/','_').replace(":","_")
    
    out = '{}_{}.pdf'.format('gsea_plot', gene_set)
    
    fig.tight_layout(pad=2) #rect=[o, o, w, w])
    
    plt.savefig(out, dpi=600)
