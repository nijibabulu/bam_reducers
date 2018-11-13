#! /usr/bin/env python

import argparse
import pysam


def write_bam(bam_file, aln_iter, split_length, output_prefix, output_id):
    aln_count = 0
    with pysam.AlignmentFile('{}.{}.bam'.format(output_prefix, output_id),
                             mode='wb', template=bam_file) as out:
        while aln_count < split_length:
            try:
                out.write(aln_iter.__next__())
                aln_count += 1
            except:
                return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('SPLIT_LENGTH', help='number of alignments per file',
                        type=int)
    parser.add_argument('BAM', help='input bam file')
    parser.add_argument('OUTPUT_PREFIX',
                        help='first part of the output file name')
    args = parser.parse_args()

    count = 0
    with pysam.AlignmentFile(args.BAM) as bf:
        iter = bf.fetch()
        while write_bam(bf, iter, args.SPLIT_LENGTH, args.OUTPUT_PREFIX, count):
            count += 1
