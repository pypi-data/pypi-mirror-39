from .config import get_config
from .process import run_cmd

def bowtie2_sort(fq1, fq2, bamfile, genome, reads=10*1000*1000, thread=8, config=""):
    """
    Align the fastq reads using bowtie2 and sort the bam file into a sorted.bam file.
    ::
        from baseqCNV.align import bowtie2_sort

        #for single reads
        bowtie2_sort("read.1.fq.gz", "", "sample.bam", "hg38")

        #for multiple reads
        bowtie2_sort("read.1.fq.gz", "read.2.fq.gz", "sample.bam", "hg38")

    Result Files:
    ::
        sample.bam
        sample.bam.stats
    """

    bowtie2 = get_config("CNV", "bowtie2", config)
    samtools = get_config("CNV", "samtools", config)

    bowtie2_ref = genome
    samfile = bamfile+".sam"
    bamfile = bamfile
    statsfile = bamfile+".stat"

    print("[info] Bamfile Path : {}".format(bamfile))

    #Run Bowtie
    if fq1 and fq2:
        bowtie_cmd = [bowtie2, '-p', str(thread), '-x', bowtie2_ref, '-u', str(reads), '-1', fq1, '-2', fq2, '>', samfile]
    else:
        bowtie_cmd = [bowtie2, '-p', str(thread), '-x', bowtie2_ref, '-u', str(reads), '-U', fq1, '>', samfile]
    
    run_cmd("Bowtie2 Alignment To The Genome ...", " ".join(bowtie_cmd))

    #Sort The Bam Files...
    samtools_sort = [
        [samtools, 'view -bS', samfile, ">", bamfile+".preSort.bam"],
        [samtools, 'sort -@ 8', bamfile+".preSort.bam", '-o', bamfile],
        [samtools, "index", bamfile],
        ["rm", samfile],
        ["rm", bamfile+".preSort.bam"]
    ]

    cmd = ";".join([" ".join(line) for line in samtools_sort])
    run_cmd("Samtools Sort", cmd)

    #run flagstats
    cmd_stats = [samtools, "flagstat", bamfile, ">", statsfile]
    run_cmd("Samtools Stats", " ".join(cmd_stats))

    return bamfile