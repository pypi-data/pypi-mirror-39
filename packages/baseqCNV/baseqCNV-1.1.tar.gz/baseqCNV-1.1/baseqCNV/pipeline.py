import os, sys
import multiprocessing as mp

from .fastq_files import check
from .config import get_config
from .align import bowtie2_sort
from .bincount import counting
from .normalize import normalize
from .segment import CBS
from .process import run_cmd
from .plots.genome import plot_genome

def CNV_single(sample, genome, fq1, fq2, reads=1000000, config=""):
    """ Run the Copy number calling pipeline for single sample.

    It need 8 threads for alignment.
    ::
        from . import CNV_single
        CNV_single("Sample01", "hg19", "sample.1.fq.gz", "sample.2.fq.gz", reads=1000000)

    It will generate:
    ::
        Sample01
        |---Sample01.sort.bam
        |---Sample01.bam.stats

    """
    if not os.path.exists(sample):
        os.mkdir(sample)

    #Align using bowtie2
    bamfile = "{}/{}.bam".format(sample, sample)
    genome_path = get_config("CNV_ref_" + genome, "bowtie2_index", config)
    bowtie2_sort(fq1, fq2, bamfile, genome_path, reads=int(reads), 
        thread=8, config=config)

    #Count
    bincountfile = "{}/{}.bincount.txt".format(sample, sample)
    counting(genome, bamfile, bincountfile, config)

    #Normalize
    normed_path = "{}/{}.normed_count.txt".format(sample, sample)
    normalize(genome, bincountfile, normed_path, config)

    #Segmentation
    cbs_file = "{}/{}.segment.txt".format(sample, sample)
    CBS(normed_path, cbs_file)

    #Visualize
    figure_file = "{}/{}.genome.png".format(sample, sample)
    plot_genome(normed_path, cbs_file, figure_file)


def CNV_server(bincount, genome, dir, config=""):
    """ Run the analysis from bincounts submitted in the server;
    ::
        
    """

    if not os.path.exists(sample):
        os.mkdir(sample)

    #Normalize
    normed_path = "{}/{}.normed_count.txt".format(sample, sample)
    normalize(genome, bincountfile, normed_path, config)

    #Segmentation
    cbs_file = "{}/{}.segment.txt".format(sample, sample)
    CBS(normed_path, cbs_file)

    #Visualize
    figure_file = "{}/{}.genome.png".format(sample, sample)
    plot_genome(normed_path, cbs_file, figure_file)

def CNV_multi(samples, genome, reads=1000000, thread=4, config=""):
    """ Run the Copy number calling pipeline for multiple samples in parellel.
    ::
        from baseqCNV.pipeline import CNV_multi
        samples = [
                ['S01', 'S01.fq.gz', ''], 
                ['S02', 'S02.1.fq.gz', 'S02.2.fq.gz']
            ]
        CNV_multi(samples, "./CNV", thread=6)

        #Starting with a sample file
        from baseq.fastq import check
        samples = check(samplefile = "sample.txt")
        CNV_multi(samples, "hg19", reads=1000*1000, thread=6)

        #In the 
        baseq-CNV run_multiple -m sample.txt
    """
    pool = mp.Pool(processes=thread)
    results = []
    print("###", config)
    for sample in samples:
        results.append(pool.apply_async(CNV_single,
                                (sample[0], genome, sample[1], 
                                    sample[2], reads, config)))
    pool.close()
    pool.join()
    results = [x.get() for x in results]
