#! /usr/bin/env python

import sys
import argparse

import bamreducers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='reduce a BAM file by stripping some information which '
                    'is not necessary for display.')
    parser.add_argument('BAM')
    parser.add_argument('--preserve-quals', action='store_true',
                        help='preserve the quality values (default behavior is '
                             'convert all quality values to 0')
    parser.add_argument('--preserve-attr', action='append', default=[],
                        metavar="ATTR",
                        help='preserve the attribute (default behavior is '
                             'to remove all attributes. A "*" preserves all '
                             'attributes'),
    parser.add_argument('--sj-file', help='include a STAR splice junction '
                                          'file to filter spliced reads by')
    parser.add_argument('--down-sample', metavar='FACTOR', type=float,
                        dest='factor',
                        help='Take a random subset of reads. FACTOR Is a '
                             'factor to downsample by. for example, if 2 is '
                             'given, the output will contain approximately '
                             'half the input reads')
    parser.add_argument('--seed', type=int, default=91543,
                        help='random seed for down sampling [default: 91543]')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='output file [default: stdout]')

    args = parser.parse_args()

    reducer = bamreducers.BamReducer()
    if args.factor:
        reducer.add_filter(bamreducers.BamDownSampler(args.factor, args.seed))
    if "*" not in args.preserve_attr:
        reducer.add_filter(bamreducers.BamTagStripper(exclude=args.preserve_attr))
    if not args.preserve_quals:
        reducer.add_filter(bamreducers.BamQualityRemover())
    if args.sj_file:
        reducer.add_filter(bamreducers.SJValidator.from_sjout(args.sj_file))
    reducer.filter_file(args.BAM, args.output)
