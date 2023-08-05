#!/usr/bin/env python3

"""Script to extract the N largest n-grams (*very* roughly) from a set
of results files.

Operates by:

1. compiling a count of distinct n-grams (within each results file) at
   each size;

2. determining the largest size X that (in addition to all larger sizes)
   accounts for N n-grams; and

3. extracting all n-grams of size X or larger from the results files
   into a single results file.

The fuzziness of the number of results actually presented (rather than
being exactly N) is from two factors:

1. number 3 above, which means that if the Nth n-gram is of size S,
   then all n-grams of size equal to or greater than S are included; and

2. each n-gram is counted as many times as the number of results files
   it appears in.

"""

import argparse
import sys

from taclextra.largest_matches import LargestMatchesExtractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('num_ngrams', metavar='N', type=int,
                        help='Number of n-grams to show')
    parser.add_argument('input_dir', metavar='RESULTS_DIR',
                        help='Path to directory containing results files')
    args = parser.parse_args()
    extractor = LargestMatchesExtractor()
    extractor.extract(args.num_ngrams, args.input_dir, sys.stdout)
