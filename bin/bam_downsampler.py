#! /usr/bin/env python

import sys
import argparse

import bamreducers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='sample a random subset of alignments from a bam file')
    parser.add_argument('--seed', help='set seed. [91543]',
                        type=int, default=91543)
    parser.add_argument('-o', '--output',
                        help='specify an output file. By default, the bam is '
                             'output to stdout. ',
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('FACTOR',
                        help='factor to downsample by. for example, if 2 is '
                             'given, the output will contain approximately '
                             'half the input reads', type=float)
    parser.add_argument('BAM')

    args = parser.parse_args()

    bamreducers.BamReducer([
        bamreducers.BamDownSampler(args.FACTOR, args.seed)
    ]).filter_file(args.BAM, args.output)
