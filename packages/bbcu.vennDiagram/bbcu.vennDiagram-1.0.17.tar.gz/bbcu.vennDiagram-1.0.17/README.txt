Description
-----------

The script gets as input folder that contains separate file for each sample with 3 columns: gene name, p-value and log2 of fold change.
The script filter according p-value (default: <=0.05) and log2 fold change (default: >=1) and create venn-diagram between the groups.

The file names within the input folder should to be:

sample1.csv, sample2.csv ... (until 6 groups)
or
sample1.xlsx, sample2.xlsx ...

The files must to include the header line:
Atnum,pv,log2FC

You can see example of input and output files here:
venn-diagram-exmple


Run command
-----------
create-venn.py --input-dir YOUR-INPUT-FOLDER --output-dir YOUR-OUTPUT-DIR


You can see another optional parameters with the command (--min-log-fc, --max-p-value, --total_gene_numbers):
create-venn.py --help 


Python version
--------------

This project is currently using Python 2.7


Installation
------------

It is recommended to use **virtualenv** to create a clean python environment.

To install venn-diagram, use **pip**:

    pip install bbcu.venn-diagram


Credit
------

The plot of the venn made by:
https://github.com/benfred/venn.js



