import sys
from typing import List, IO
import pysam
from .filters import AlignmentFilter


class BamReducer(object):
    def __init__(self, filters: List[AlignmentFilter] = None):
        self.filters: List[AlignmentFilter] = filters or []

    def add_filter(self, filter: AlignmentFilter):
        self.filters.append(filter)

    def output_processed_bam(self, in_bam_file: pysam.AlignmentFile,
                             out_bam_file: pysam.AlignmentFile) -> None:
        """ Filter an AlignmentFile """
        for aln in in_bam_file:
            if not any(f.filter_alignment(aln) for f in self.filters):
                out_bam_file.write(aln)

    def filter_bam(self, bam_file: pysam.AlignmentFile,
                   output_file: IO) -> None:
        """ Filter an AlignmentFile object and output a file object"""
        with pysam.AlignmentFile(output_file, 'wb', template=bam_file) as out:
            self.output_processed_bam(bam_file, out)

    def filter_file(self, in_file_name: str, output_file=sys.stdout) -> None:
        """ Filter a bam file by name and output it. """
        with pysam.AlignmentFile(in_file_name) as bf:
            self.filter_bam(bf, output_file)
