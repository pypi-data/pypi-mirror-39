# mglcmdtools

## 1 Introduction

`mglcmdtools` is a collection of common cmd tools intended to be used in Python3 scripts. By Guanliang MENG, see https://github.com/linzhi2013/mglcmdtools.


## 2 Installation

    pip install mglcmdtools


## 3 Usage

    from mglcmdtools import rm_and_mkdir, runcmd, longStrings_not_match_shortStrings, read_fastaLike, read_fastaLike2, csv2dict, csv2tupe, split_fasta_to_equal_size


    rm_and_mkdir('Newdirectory')

    rm_and_mkdir('Newdirectory', force=True)


    cmd = 'ls -lhtr /'
    runcmd(cmd)

    runcmd(cmd, verbose=True)


    Long_strings = ['AABB', 'CCDD', 'EEFF']
    Short_strings = ['AA', 'EE']
    longStrings_not_match_shortStrings(Long_strings, Short_strings)
    # ['CCDD']


`seq.fa` file has following content:

    >scaffold512 Locus_1222_0 8.3 LINEAR length=1717 score=20.785
    COX2    2   649 45  643 +   4
    COX3    897 1691    18  784 +   4
    >C7676 18.0 length=1633 score=19.113
    DNA afd
    COX1    34  1580    12  1530    -   4
    >C7536 14.0 length=1185 score=13.529
    CYTB    178 1185    25  1008    +   4
    >scaffold619 Locus_1559_0 5.0 LINEAR length=803 score=3.515
    ND4 27  764 515 1185    +   2
    >scaffold367 Locus_808_0 4.6 LINEAR length=652 score=2.296
    ATP6    1   306 324 620 -   4
    AAA adfjkaj


Then read each record:

    for rec in read_fastaLike('seq.fa'):
        print('seqid line:', rec[0])
        print('sequence line 1:', rec[1])


function `csv2dict(file=None, header=None, nrows=None, index_col=0, rm_self=True, **kwargs)`:

    targeted file: a csv file containing a matrix.

    by default, assuming the csv file does not have header row, and the first column (index 0) is the row names.

    you must specify how many rows to be read.

    1. read data from a csv file into a pandas Dataframe;
    2. change the up triangular and low triangular to dictionary 'triu_dict' and 'tril_dict', respectively.

    Parameter:
        rm_self: remove the pair of self-to-self, default True.


    Return:
        (triu_dict, tril_dict)


function `csv2tupe(file=None, header=None, nrows=None, index_col=0, rm_self=True, **kwargs)`:

    targeted file: a csv file containing a matrix.

    by default, assuming the csv file does not have header row, and the first column (index 0) is the row names.

    you must specify how many rows to be read.

    1. read data from a csv file into a pandas Dataframe;
    2. change the up triangular and low triangular to LIST of tupes 'triu' and 'tril', respectively.

    Parameter:
        rm_self: remove the pair of self-to-self, default True.


    Return:
        (triu, tril)


function `split_fasta_to_equal_size(fastafile=None, tot_file_num=10, outdir='./')`:

    Split a fasta file to `tot_file_num` subfiles, and all subfiles have
    appropximately equal size.

    Return:
    A list of the subfiles' abspath


function `extend_ambiguous_dna(seq=None, get_a_random_seq=False)`:

    return a `map` iterator of all possible sequences given an ambiguous
    DNA input.

    if `get_a_random_seq=True`, return a randomly chosen sequence.

    the lower case or upper case of each base will be the same with input DNA.

    modified from:
    https://stackoverflow.com/questions/27551921/how-to-extend-ambiguous-dna-sequence


## 4 Author
Guanliang MENG

## 5 Citation
Currently I have no plan to publish `mglcmdtools`.







