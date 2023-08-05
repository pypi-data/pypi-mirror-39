import click, os, sys
from .fastq_files import check
from .config import get_config
from .align import bowtie2_sort

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

#Run the CNV pipeline for Lists of Samples
@cli.command(short_help = "Run the CNV pipeline for multiple samples in a file")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--thread', '-t', default=4, help="Samples run in parallel (4)")
@click.option('--genome', '-g', default='', help="Species hg19 or mm10")
@click.option('--config', '-c', default='', help="Config file")
def run_multiple(sample_file, genome, thread, config):
    from .pipeline import CNV_single, CNV_multi
    samples = check(sample_file)
    CNV_multi(samples, genome, thread = int(thread), config=config)

#Run BOWTIE2 Alignment
@cli.command(short_help="Alignment with bowtie2, Sorted and Index")
@click.option('--fq1', '-1', default='', help="Fastq 1")
@click.option('--fq2', '-2', default='', help="Fastq 2")
@click.option('--bamfile', '-o', default='baseqCNV.bowtie2.sort.bam', help="Output bamfile name (baseqCNV.bowtie2.sort.bam)")
@click.option('--reads', '-r', default='5000000', help="Numbers of reads")
@click.option('--thread', '-t', default=8, help="Numbers of Thread")
@click.option('--genome', '-g', default='hg19', help="Genome version : hg19/mm38")
@click.option('--config', '-c', default='', help="Configuration file")
def align(fq1, fq2, bamfile, genome, reads, thread, config):
    genome = get_config("CNV_ref_"+genome, "bowtie2_index", config)
    bowtie2_sort(fq1, fq2, bamfile, genome, reads=reads, thread=thread, config=config)

#Bin Counting
@cli.command(short_help="Couting reads in the bam file according to dynamic bins")
@click.option('--genome', '-g', default='hg19', help="Genome ID, like: hg19")
@click.option('--bamfile', '-i', default='', help="Bamfile path")
@click.option('--out', '-o', default='./sample.bincounts.txt', help="bin counts file path")
@click.option('--config', '-c', default='', help="Config file")
def bincount(genome, bamfile, out, config):
    from .bincount import counting
    counting(genome, bamfile, out, config)

#Run Normalization
@cli.command(short_help="Normalize the reads to Depth and GC content")
@click.option('--genome', '-g', default='', help="genome")
@click.option('--bincount', '-i', default='', help="bin count file")
@click.option('--out', '-o', default="./sample.norm_GC.txt", help="normalized bin counts")
@click.option('--config', '-c', default='', help="Config file")
def normalize(genome, bincount, out, config):
    from .normalize import normalize
    normalize(genome, bincount, out, config)

#Run CBS
@cli.command(short_help="Run Circular Binary Segmentation")
@click.option('--count_file', '-i', default='', help="Normalized bin count file")
@click.option('--out', '-o', default='./', help="CBS file...")
def CBS(count_file, out):
    from .segment import CBS
    CBS(count_file, out)

#Run Plot Genomes.
@cli.command(short_help="Generate the genome CNV's plot")
@click.option('--counts', '-i', default='', help="Normalized bin count file")
@click.option('--countlists', '-l', default='', help="Lists of normalized bin count file")
@click.option('--cbs', '-c', default='', help="CBS File, Genrated from run_CBS command")
@click.option('--out', '-o', default='./baseqcnv.png', help="The Path of Generated Figure")
def plotgenome(counts, countlists, cbs, out):
    from .plots.genome import plot_genome, plot_genome_multiple
    if not countlists:
        plot_genome(counts, cbs, out)
    else:
        plot_genome_multiple(countlists, cbs, out)