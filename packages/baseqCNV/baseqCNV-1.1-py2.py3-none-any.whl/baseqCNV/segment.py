import os, sys
from pathlib import Path
from .command import run_cmd

HERE = Path(__file__).parent 

def CBS(infile, segment_file):
    """ Run DNACopy.R file, depends on the R package DNAcopy.
    ::
        CBS("bincounts_norm.txt", "sample.segment.txt")
    
    Results:
    ::
        #outfile.txt
        #ID	chrom	loc.start	loc.end	num.mark	seg.mean	CN
    """
    script = Path(HERE, "src/DNACopy.R")
    cmd = "Rscript {} {} {}".format(script, infile, segment_file)
    try:
        run_cmd("Normalize ", cmd)
        print("[info] Segment file write to {}".format(segment_file))
    except:
        sys.exit("[error] Failed to run the CBS Rscript ...")

if __name__ == "__main__":
    print(HERE, Path(HERE, "src/DNACopy.R"))