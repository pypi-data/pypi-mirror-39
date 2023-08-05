__all__ = [
	'counting', 'normalize',
    'CNV_multi', 'CNV_single'
]

from .bincount import counting
from .normalize import normalize
from .segment import CBS as segmentation
from .plots.genome import plot_genome

#pipeline
from .pipeline import CNV_multi, CNV_single