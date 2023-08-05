from subprocess import call
import os, sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.interpolate import interp1d
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

from .config import get_config
from .process import run_cmd

def normalize(genome, bincount, normed_path="sample.normedcount.txt", config=""):
    """Normalize the Raw bin counts with bin length and GC contents, also estimate the Ploidy.
    ::
        from baseq.cnv import normalize
        normalize("hg19", "bincounts.txt", "sample.normed_count.txt")

    This will generate two files:
    ::
        sample.normedcount.txt
        #'chr', 'start', 'absstart', 'CN_norm', 'CN_ploidy'
        sample.normedcount.txt.png

    Process:

    - Read the dynamicbin;
    - Aggregate the Bins into 500kb;
    - Normalize by bin length, normalize by bin number, log transform ('norm_counts_log');
    - Normalize by GC, normalize by bin number ('regress_by_GC');
    - Detect the Ploidy, by calculating the losses from CN 1.5-4;

    Output:
        GC_content_image: images
        Normalized bin counts (1M)
    """
    dynamic_bin = get_config("CNV_ref_"+genome, "dynamic_bin", config)
    df_counts = pd.read_table(bincount)
    df = pd.read_table(dynamic_bin)
    df['counts'] = df_counts['counts']

    print("[info] Aggregate the bins into 500kb...")

    df = df.groupby(df.index // 10).agg(
        {"chr":"first", "start": "mean", "absstart": "mean", "GC": "mean", "length" : "sum", "counts" : "sum"}
    )

    #Normalize by bin length
    df['norm_counts'] = df['counts']/df['length']
    df['norm_counts'] = df['norm_counts']/df['norm_counts'].mean()
    df['norm_counts_log'] = np.log(df.norm_counts + 0.01)

    #Normalize by GC content
    lowess = sm.nonparametric.lowess
    z = lowess(df.norm_counts_log, df.GC)
    f = interp1d(list(zip(*z))[0], list(zip(*z))[1], bounds_error = False)
    df['CN_norm'] = np.exp(df.norm_counts_log - f(df['GC']))-0.01
    df['CN_norm'] = df['CN_norm']/df['CN_norm'].mean()

    #plot GC correction...
    plt.figure(figsize=(10, 10))
    plt.subplot(2, 2, 1)
    plt.title('Raw Normalized Reads (500Kb)')
    plt.scatter(df.GC, df.norm_counts, facecolors='none', edgecolors='r')

    plt.subplot(2, 2, 2)
    plt.title('GC corrected (500Kb)')
    plt.scatter(df.GC, df.CN_norm, facecolors='none', edgecolors='b')

    #Peaks Detection
    plt.subplot(2, 2, 3)
    plt.title('Peaks')
    plt.hist(df.CN_norm, bins=300, density=True)

    #Peaks Detection..
    Ploidy_Lists = [x/40 for x in range(60, 240, 1)]
    SoS = []
    for ploidy in Ploidy_Lists:
        errors = round(df['CN_norm']*ploidy)-df['CN_norm']*ploidy
        SoS.append(sum([x*x for x in errors]))
    estimate_ploidy = Ploidy_Lists[SoS.index(min(SoS))]

    print("[info] The estimated plodity is {}".format(estimate_ploidy))
    plt.subplot(2, 2, 4)
    plt.title('Plodity Estimate: {}'.format(estimate_ploidy))
    plt.ylabel("Errors (Should be Minimized)")
    plt.xlabel("Ploidy")
    plt.plot(Ploidy_Lists, SoS)
    df['CN_ploidy'] =  df['CN_norm']*estimate_ploidy

    df_export = df[['chr', 'start', 'absstart', 'CN_norm', 'CN_ploidy']]
    print("[info] CN table write to {}".format(normed_path))
    df_export.to_csv(normed_path, sep="\t", float_format='%.2f', index=False)
    plt.savefig(normed_path + ".png")