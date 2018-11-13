import random
import array
import abc

import pysam
from typing import Dict, List


class AlignmentFilter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def filter_alignment(self, aln: pysam.AlignedSegment) -> bool:
        pass


class BamDownSampler(AlignmentFilter):
    def __init__(self, factor, seed=91543):
        self.threshold: float = 1 / factor
        random.seed(seed)

    def filter_alignment(self, _) -> bool:
        return random.random() > self.threshold


class BamTagStripper(AlignmentFilter):
    def __init__(self, exclude: List[str] = None):
        self.exclude = set(exclude or [])

    def filter_alignment(self, aln: pysam.AlignedSegment) -> bool:
        for tag in aln.get_tags():
            if tag[0] not in self.exclude:
                aln.set_tag(tag[0], None)
        return False


class BamQualityRemover(AlignmentFilter):
    def filter_alignment(self, aln: pysam.AlignedSegment) -> bool:
        aln.query_qualities = array.array('B', [0] * len(aln.query_sequence))
        return False


class SJChromValidator(object):
    def __init__(self):
        self.sjs = dict()

    def add(self, start: int, end: int):
        self.sjs.setdefault(start, set()).add(end)

    def contains(self, start, end):
        if int(start) in self.sjs and int(end) in self.sjs[start]:
            return True
        else:
            return False

    def filter_alignment(self, aln: pysam.AlignedSegment) -> bool:
        position = aln.reference_start
        for op, length in aln.cigartuples:
            if op == 3:
                if not self.contains(position + 1, position + length):
                    return True
            if op in [0, 2, 3, 7, 8]:
                position += length
        return False


class SJValidator(AlignmentFilter):
    def __init__(self):
        self.cvs: Dict[str, SJChromValidator] = dict()

    @classmethod
    def from_sjout(cls, file_name: str):
        sjv = SJValidator()
        with open(file_name) as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) < 3:
                    raise (ValueError,
                           'Invalid format for splice junction file. Offending '
                           'line:\n' + line)
                chrom, start, end = fields[:3]
                sjv.cvs.setdefault(chrom, SJChromValidator()).add(int(start),
                                                                  int(end))

    def filter_alignment(self, aln: pysam.AlignedSegment):
        return aln.reference_name not in self.cvs or \
               self.cvs[aln.reference_name].filter_alignment(aln)

