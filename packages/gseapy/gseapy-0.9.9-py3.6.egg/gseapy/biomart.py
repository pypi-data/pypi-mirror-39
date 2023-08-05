#! bin/env python

"""biomart

Query biomart from the command line.

Usage:
    biomart [--mart=MART] [--dataset=DATA] --mergecol=COL... --intype=IN... --outtype=OUT... [--noheader] FILE
    biomart [--mart=MART] [--dataset=DATA] --intype=IN --outtype=OUT
    biomart --list-marts
    biomart [--mart=MART] --list-datasets
    biomart [--mart=MART] [--dataset=DATASET] --list-attributes

Arguments:
    FILE                   file with COL(s) to join mart data on (- for STDIN)
    -i IN --intype=IN      the datatype in the column to merge on
    -o OUT --outtype=OUT   the datatype to get (joining on value COL)
    -c COL --mergecol=COL  name or number of the column to join on in FILE

Note:
    Required args --intype, --outtype and --mergecol must be equal in number.

Options:
    -h      --help          show this message
    -m MART --mart=MART     which mart to use [default: ENSEMBL_MART_ENSEMBL]
    -d DATA --dataset=DATA  which dataset to use [default: hsapiens_gene_ensembl]
    -n --noheader           the input data does not contain a header (must
                            use integers to denote COL)

Lists:
    --list-marts       show all available marts
    --list-datasets    show all available datasets for MART
    --list-attributes  show all kinds of data available for MART and DATASET


Example:
biomart -d rnorvegicus_gene_ensembl  -i external_gene_name -o go_id | shuf -n 10
"""





