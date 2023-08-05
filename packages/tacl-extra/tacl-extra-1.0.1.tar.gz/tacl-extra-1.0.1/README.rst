tacl-extra
==========

tacl-extra provides scripts and libraries that make use of the `TACL`_
software.

Scripts provided are:

* **int-all**: Generates extended and reduced intersect results files
  for every pair of texts in a supplied corpus.
* **jitc**: Generates an HTML report showing the amount of overlap
  between a set of works, ignoring those parts that overlap with
  works in a second set of works.
* **lifetime**: Generates results data and a report showing the
  lifetime of n-grams that come into or fall out of use in a group of
  corpora.
* **paternity**: Generates a series of results files giving the
  n-grams in common between one corpus and each work in a second
  corpus, that are not present in a third corpus.

The actual work of the scripts is done in library code that can be
imported and used by other code.

The code is developed at https://github.com/ajenhl/tacl-extra/ and the
documentation is available at
http://tacl-extra.readthedocs.io/en/latest/.


.. _TACL: https://github.com/ajenhl/tacl/
