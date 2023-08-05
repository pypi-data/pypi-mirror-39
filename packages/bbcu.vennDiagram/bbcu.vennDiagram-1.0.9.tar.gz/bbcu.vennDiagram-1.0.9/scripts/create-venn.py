#!/usr/bin/env python

import argparse
import itertools
import json
import os
from glob import glob
from shutil import copyfile

import pandas as pd
import scipy.stats as stats


class VennDiagram(object):
    def __init__(self, input_dir, output_dir, min_log_fc, max_pv, total_gene_numbers, package_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.min_log_fc = min_log_fc
        self.max_pv = max_pv
        self.total_gene_numbers = total_gene_numbers
        self.package_dir = package_dir
        self.filtered_genes = {}  # key is sample name, value is tuple of tuples ((Atnum,pv,log2FC), ...)
        self.samples_list = {}
        self.summary_json = []

    def read_file(self, input_file):
        file_name, extension = os.path.splitext(input_file)
        if extension == '.xlsx':
            xl = pd.ExcelFile(input_file)
            # print(xl.sheet_names)
            df = xl.parse('Sheet1')
        elif extension == '.csv':
            df = pd.read_csv(input_file)
        else:
            raise IOError('The extension \"%s\" of file %s is not valid. The input file must be csv or xlsx files.' % (
                extension, input_file))

        if df.shape[0] == 0:
            print 'The file %s is empty' % file_name
            return

        for index, row in df.iterrows():
            yield row

    def filter_files(self):
        print 'Start to filter the input files files'
        input_files = glob(os.path.join(self.input_dir, '*.xlsx'))
        input_files += glob(os.path.join(self.input_dir, '*.csv'))
        if not input_files:
            print 'No input file exists in %s folder. The input file name must be ended with csv or xlsx.'
        else:
            print 'The input files are: %s ' % (input_files)

        output_filtered_dir = os.path.join(self.output_dir, 'filtered_genes')
        os.makedirs(output_filtered_dir) if not os.path.isdir(output_filtered_dir) else None
        filtered_num = {}
        for input_file in input_files:
            full_file_name, extension = os.path.splitext(input_file)
            file_name = os.path.basename(full_file_name)
            with open(os.path.join(output_filtered_dir, file_name + '_filtered.csv'), 'w') as filtered_file:
                num = 0
                filtered_file.write('Atnum,pv,log2FC' + '\n')
                for row in self.read_file(input_file):
                    if row['pv'] <= self.max_pv and row['log2FC'] >= self.min_log_fc:
                        num += 1
                        filtered_file.write(','.join([str(row['Atnum']), str(row['pv']), str(row['log2FC'])]) + '\n')
                        if not file_name in self.filtered_genes:
                            self.filtered_genes[file_name] = [(row['Atnum'], row['pv'], row['log2FC'])]
                        else:
                            self.filtered_genes[file_name].append((row['Atnum'], row['pv'], row['log2FC']))
                filtered_num[file_name] = num

        for i, sample in enumerate(sorted(self.filtered_genes.keys())):
            self.samples_list[sample] = i
            self.summary_json.append({"label": sample, "sets": [i], "size": filtered_num[sample]})

    def find_intersections(self):
        output_intersection_dir = os.path.join(self.output_dir, 'intersections')
        os.makedirs(output_intersection_dir) if not os.path.isdir(output_intersection_dir) else None
        summary = {}
        for i in range(2, len(self.samples_list.keys()) + 1):
            for samples in itertools.combinations(self.samples_list.keys(), i):
                gene_lists = [set([details[0] for details in self.filtered_genes[sample]]) for sample in samples]
                intersected = set.intersection(*gene_lists)
                size_intersected = len(intersected)
                percent = float(size_intersected * 100) / sum([len(gene_list) for gene_list in gene_lists])
                if len(samples) == 2:
                    sam1num = len(self.filtered_genes[samples[0]])
                    sam2num = len(self.filtered_genes[samples[1]])
                    oddsratio, pvalue = stats.fisher_exact([[size_intersected, sam1num], [sam2num,
                                                                                          self.total_gene_numbers - (
                                                                                              sam1num + sam2num + size_intersected)]])
                stat = '%s (%s %%)' % (size_intersected, percent) if len(samples) > 2 else '%s (%s %%),%s,%s' % (
                    size_intersected, percent, pvalue, oddsratio)
                summary['_'.join([sample for sample in samples])] = stat
                self.summary_json.append({"label": " ".join(sorted([sample for sample in samples])),
                                          "sets": sorted([self.samples_list[sample] for sample in samples]),
                                          "size": size_intersected, "percent": "%.2f" % percent})
                with open(os.path.join(output_intersection_dir,
                                       '_'.join(samples) + '_intersected.csv'), 'w') as intersected_file:
                    intersected_file.write('Number of intersection: %s\n' % size_intersected)
                    intersected_file.write('Percent: %s\n' % percent)
                    intersected_file.write('Fisher test: pvalue: %s, oddsration: %s\n' % (pvalue, oddsratio)) if len(
                        samples) == 2 else None
                    intersected_file.write(
                        'Atnum,' + ','.join([sample + '_pv,' + sample + '_log2FC' for sample in samples]) + '\n')
                    for gene in intersected:
                        intersected_file.write(gene + ',')
                        for sample in samples:
                            for details in self.filtered_genes[sample]:
                                if details[0] == gene:
                                    intersected_file.write(','.join([str(detail) for detail in details[1:]]))
                        intersected_file.write('\n')
        with open(os.path.join(output_intersection_dir, 'summary_intersections.csv'), 'w') as summary_file:
            summary_file.write('Group,Intersection size, pvalue, oddsratio\n')
            for k, v in summary.items():
                summary_file.write(','.join([k, v]) + '\n')

        output_venn_dir = os.path.join(self.output_dir, 'venn-diagram')
        os.makedirs(output_venn_dir) if not os.path.isdir(output_venn_dir) else None
        copyfile(os.path.join(self.package_dir, 'venn-diagram.html'), os.path.join(output_venn_dir,'venn-diagram.html'))
        copyfile(os.path.join(self.package_dir, 'venn.js'), os.path.join(output_venn_dir, 'venn.js'))
        with open(os.path.join(output_venn_dir, 'intersections.jsonp'), 'w') as json_file:
            json_file.write("var sets = ")
        with open(os.path.join(output_venn_dir, 'intersections.jsonp'), 'a') as json_file:
            json.dump(self.summary_json, json_file)


def parse_args():
    help_txt = "Create report of counts in each step of pipeline for each sample"
    parser = argparse.ArgumentParser(description=help_txt)
    parser.add_argument('--input-dir', type=str,
                        help='Directory with input files. The file names must to to be sampleName.csv or sampleName.xlsx',
                        default=os.curdir, required=True)
    parser.add_argument('--output-dir', type=str, help='Name of existing output directory', default=os.curdir,
                        required=True)
    parser.add_argument('--min-log-fc', type=float,
                        help='Minimum absolut value of log fold change (for example 1.0 for fold change 2.0 or 0.5). Defauld: 1.0',
                        default=1.0, required=False)
    parser.add_argument('--max-p-value', type=float, help='Maximum p-value. Default: 0.05', default=0.05,
                        required=False)
    parser.add_argument('--total_gene_numbers', type=int,
                        help='Number of the total genes in transcriptome. Default: 30000', default=30000,
                        required=False)
    parser.add_argument('--package-dir', type=str,
                        help='Directory of this package. Need for copy the js files for the diagram',
                        default='/home/labs/fluhr/Collaboration/ve-venn-diagram/lib/python2.7/site-packages/vennDiagram',
                        required=False)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if not os.path.isdir(args.input_dir):
        raise IOError('No such input folder: %s' % args.input_dir)
    print 'Minimum fold change is %s, Maximum p-value is %s' % (args.min_log_fc, args.max_p_value)
    os.makedirs(args.output_dir) if not os.path.isdir(args.output_dir) else None
    vd = VennDiagram(args.input_dir, args.output_dir, args.min_log_fc, args.max_p_value, args.total_gene_numbers,
                     args.package_dir)
    vd.filter_files()
    vd.find_intersections()
