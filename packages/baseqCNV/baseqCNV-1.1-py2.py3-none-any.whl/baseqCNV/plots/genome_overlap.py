import os, sys
from baseq.mgt import get_config, run_cmd
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def plot_genome_overlap(bincount, cbs_path, figpath):
    """ Plot the copy number of whole genome.
    Usage:
    ::
        from baseq.cnv import plot_genome
        plot_genome("sample.norm.txt", "sample.segment.txt", "genome.png")
        #CNV.genome.sample.png

    .. image:: http://p8v379qr8.bkt.clouddn.com/Genome12.png
    """
    df = pd.read_table(bincount)

    #Plot The Dots...
    plt.figure(figsize=(10, 1.4))
    plt.margins(x=0, y=0)
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.gcf().subplots_adjust(left=0.03, right=0.97)
    plt.scatter(df.absstart, df.CN_ploidy, edgecolors='dodgerblue', s=1)

    #Plot Genomes
    df_chr_pos = df.groupby(by=["chr"]).agg({"absstart" : "first"})
    for idx, row in df_chr_pos.iterrows():
        plt.axvline(x=row['absstart'], color="grey")

    #Chr Name
    df_chr_pos = df.groupby(by=["chr"]).agg({"absstart": "mean", "start": "mean", "chr":"first"}).sort_values(by="absstart")
    df_chr_pos['offset'] = df_chr_pos.absstart - df_chr_pos.start
    labels = df_chr_pos.iloc[::2].chr.tolist()
    labels = [x.split("chr")[-1] for x in labels]
    plt.xticks(df_chr_pos.iloc[::2].absstart, labels)

    #Add Segs
    df_cbs = pd.read_table(cbs_path)
    for idx, row in df_cbs.iterrows():
        offset = df_chr_pos.loc[row['chrom'], 'offset']
        xmin = row['loc.start']+offset
        xmax = row['loc.end']+offset
        plt.plot([xmin, xmax], [row['CN'], row['CN']], color="red")

    print("[info] The fig path is {}".format(figpath))
    plt.savefig(figpath)