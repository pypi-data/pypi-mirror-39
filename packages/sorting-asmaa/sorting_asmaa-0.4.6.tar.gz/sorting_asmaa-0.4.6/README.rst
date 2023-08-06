Project Title
=============

sorting\_asmaa is a Python package that gives the user options to sort
different types of inputs. The package includes `K-way merge
sort <https://en.wikipedia.org/wiki/K-way_merge_algorithm>`__,
`introsort <https://en.wikipedia.org/wiki/Introsort>`__,\ `Bucket
sort <https://en.wikipedia.org/wiki/Bucket_sort>`__,\ `shell
sort <https://en.wikipedia.org/wiki/Shellsort>`__, and `Radix
sort <https://en.wikipedia.org/wiki/Radix_sort>`__. ## Getting Started
### Prerequisites

Before proceeding with the package installation, the following packages
are needed: `Math <https://docs.python.org/2/library/math.html>`__ and
`timeit <https://docs.python.org/2/library/timeit.html>`__ ###
Installing

On command prompt

::

    $ pip install sorting_asmaa

Usage
-----

To use shell sort,

::

    slist=[1,3,4,5] #add your list
    print(sorting_asmaa.shellsort_asmaa(slist))

To use k-way merge sort

::

    k=2 #add the value of k
    slist=[1,3,4,5] #add your list
    sorting_asmaa.kmerge_asmaa(slist)

To use bucket sort

::

    slist=[1,3,4,5] #add your list
    sorting_asmaa.bucketsort_asmaa(slist)

To use radix sort

::

    slist=[1,3,4,5] #add your non-negative input
    sorting_asmaa.radixsort_asmaa(slist)

To use intro sort

::

    slist=[1,3,4,5] #add your input
    sorting_asmaa.introsort_asmaa(slist)

Built With
----------

-  `Dillinger <https://dillinger.io/>`__ - Readme framework used

Authors
-------

-  **Asmaa Aly** - *Initial work* ## License

This project is licensed under the MIT License - see the
`LICENSE.md <LICENSE.md>`__ file for details
