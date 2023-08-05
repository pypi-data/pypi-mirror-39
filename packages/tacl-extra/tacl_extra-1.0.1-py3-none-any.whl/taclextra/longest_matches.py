import collections
import fnmatch
import os

import pandas as pd

import tacl.constants


class LongestMatchesExtractor:

    def _compile_ngram_counts(self, input_dir):
        """Returns a dictionary mapping n-gram size to counts of n-grams at
        that size among all results files in `input_dir`."""
        counts = collections.defaultdict(int)
        count = 0
        for root, dirs, files in os.walk(input_dir):
            for name in fnmatch.filter(files, '*.csv'):
                counts = self._get_ngram_counts(os.path.join(root, name),
                                                counts)
                count += 1
        return counts

    def _compile_results(self, input_dir, min_size):
        """Returns results concatenated from every results file in
        `input_dir`, filtered for n-grams of `min_size` size or larger.

        :param input_dir: path to directory containing results files
        :type input_dir: `str`
        :param min_size: minimum n-gram size to extract
        :type min_size: `int`
        :rtype: `pandas.DataFrame`

        """
        full_results = pd.DataFrame(columns=tacl.constants.QUERY_FIELDNAMES)
        for root, dirs, files in os.walk(input_dir):
            for name in fnmatch.filter(files, '*.csv'):
                results = pd.read_csv(os.path.join(root, name),
                                      encoding='utf-8', na_filter=False)
                results = results[results[tacl.constants.SIZE_FIELDNAME]
                                  >= min_size]
                full_results = pd.concat([full_results, results],
                                         ignore_index=True)
        return full_results

    def extract(self, num_ngrams, input_dir, fh):
        counts = self._compile_ngram_counts(input_dir)
        min_size = self._get_minimum_size(counts, num_ngrams)
        results = self._compile_results(input_dir, min_size)
        results.to_csv(fh, encoding='utf-8', float_format='%d',
                       index=False)

    def _get_minimum_size(self, counts, num_ngrams):
        """Returns the minimum n-gram size such that the count of all n-grams
        of that size or higher is at least `num_ngrams`."""
        sizes = sorted(counts.keys(), reverse=True)
        count = 0
        for size in sizes:
            min_size = size
            count += counts[size]
            if count >= num_ngrams:
                break
        return min_size

    def _get_ngram_counts(self, path, counts):
        """Returns `counts` updated with the count of n-grams at each size in
        results file `path`.

        :param path: path to results file to get counts from
        :type path: `str`
        :param counts: mapping of n-grams to counts
        :type counts: `collections.defaultdict`

        """
        results = pd.read_csv(path, encoding='utf-8', na_filter=False)
        results.drop(columns=[tacl.constants.WORK_FIELDNAME,
                              tacl.constants.SIGLUM_FIELDNAME,
                              tacl.constants.COUNT_FIELDNAME,
                              tacl.constants.LABEL_FIELDNAME], inplace=True)
        results.drop_duplicates(inplace=True)
        grouped = results.groupby(tacl.constants.SIZE_FIELDNAME, sort=False)
        for size, group in grouped:
            counts[size] += len(group.index)
        return counts
