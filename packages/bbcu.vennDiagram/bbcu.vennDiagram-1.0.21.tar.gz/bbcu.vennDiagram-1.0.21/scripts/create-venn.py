#!/usr/bin/env python

import argparse
import itertools
import json
import os
import sys
from glob import glob
from shutil import copyfile

import numpy as np
import pandas as pd
import scipy.stats



JS_VENN_NAME = 'venn.v1.js'
JS_D3_NAME = 'd3.v4.js'
WISLOGO = 'wis_logo_heb_v1.png'

class VennDiagram(object):
    def __init__(self, input_dir, output_dir, min_log_fc, max_log_fc, min_pv, max_pv, total_gene_numbers, package_dir,
                 js_venn_name, js_d3_name, wislogo):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.min_log_fc = min_log_fc
        self.max_log_fc = max_log_fc
        self.min_pv = min_pv
        self.max_pv = max_pv
        self.total_gene_numbers = total_gene_numbers
        self.package_dir = package_dir
        self.js_venn_name, self.js_d3_name = js_venn_name, js_d3_name
        self.wislogo = wislogo
        self.filtered_genes = {}  # key is sample name, value is tuple of tuples ((Atnum,pv,log2FC), ...)
        self.samples_list = {}
        self.summary_json = []
        self.summary = {}

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
        print 'Start to filter the input files'
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
                    if row['pv'] <= self.max_pv and row['pv'] >= self.min_pv and row['log2FC'] >= self.min_log_fc and \
                                    row['log2FC'] <= self.max_log_fc:
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
            self.summary[sample] = str(filtered_num[sample])

    def percents_string(self, samples, percents, delimiter):
        return delimiter.join(["%s (%.2f%%)" % (sample, percent) for sample, percent in zip(samples, percents)])

    def find_intersections(self):
        print 'Start to find intersections'
        output_intersection_dir = os.path.join(self.output_dir, 'intersections')
        os.makedirs(output_intersection_dir) if not os.path.isdir(output_intersection_dir) else None
        for i in range(2, len(self.samples_list.keys()) + 1):
            for samples in itertools.combinations(self.samples_list.keys(), i):
                samples = sorted(samples)
                gene_lists = [set([details[0] for details in self.filtered_genes[sample]]) for sample in samples]
                intersected = set.intersection(*gene_lists)
                size_intersected = len(intersected)
                percents = [float(size_intersected * 100) / len(gene_list) for gene_list in gene_lists]
                if len(samples) == 2:
                    sam1num = len(self.filtered_genes[samples[0]])
                    sam2num = len(self.filtered_genes[samples[1]])
                    expected = (size_intersected + sam1num) * float(
                        size_intersected + sam2num) / self.total_gene_numbers
                    freq_matrix = np.array([[size_intersected, sam1num], [sam2num, self.total_gene_numbers - (
                    sam1num + sam2num + size_intersected)]])
                    test_type = None
                    if (size_intersected > 500):  # chi2 test
                        try:
                            test_type = 'Chi2 test'
                            statistic_type = 'Chi2'
                            statistic, pvalue, dof, chi2_expected = scipy.stats.chi2_contingency(freq_matrix)
                        except Exception as e:
                            test_type = 'No valid Chi2 test'
                            statistic = ''
                            pvalue = ''
                            print "Cannot do Chi2 test because: %s" % str(e)
                    else:  # fisher test
                        try:
                            test_type = 'Fisher test'
                            statistic_type = 'oddsratio'
                            statistic, pvalue = scipy.stats.fisher_exact(freq_matrix)
                        except Exception as e:
                            test_type = 'No valid Fisher test'
                            statistic = ''
                            pvalue = ''
                            print "Cannot do Fisher test because: %s" % str(e)
                            # print size_intersected, sam1num, sam2num,self.total_gene_numbers

                stat = '%s,%s' % (size_intersected, self.percents_string(samples, percents, ';')) if len(
                    samples) > 2 else '%s,%s,%s,%s,%s' % (
                size_intersected, self.percents_string(samples, percents, ';'), pvalue, statistic, expected)
                self.summary['_'.join([sample for sample in samples])] = stat
                self.summary_json.append({"label": "(" + ",".join([sample for sample in samples]) + ")",
                                          "sets": [self.samples_list[sample] for sample in samples],
                                          "expected": '%.4f' % expected,
                                          "size": size_intersected,
                                          "percent": "%s" % self.percents_string(samples, percents, ',')})
                with open(os.path.join(output_intersection_dir,
                                       '_'.join(samples) + '_intersected.csv'), 'w') as intersected_file:
                    intersected_file.write('Number of intersection: %s\n' % size_intersected)
                    intersected_file.write('Percent: %s\n' % self.percents_string(samples, percents, ';'))
                    intersected_file.write('%s: pvalue: %s, %s: %s, expected: %s\n' % (
                    test_type, pvalue, statistic_type, statistic, expected)) if len(
                        samples) == 2 else None
                    intersected_file.write(
                        'Atnum,' + ','.join([sample + '_pv,' + sample + '_log2FC' for sample in samples]) + '\n')
                    for gene in intersected:
                        intersected_file.write(gene + ',')
                        for sample in samples:
                            for details in self.filtered_genes[sample]:
                                if details[0] == gene:
                                    intersected_file.write(','.join([str(detail) for detail in details[1:]]))
                                    intersected_file.write(',')
                        intersected_file.write('\n')
        with open(os.path.join(output_intersection_dir, 'summary_intersections.csv'), 'w') as summary_file:
            summary_file.write('Group,Intersection size, percent (per sample),pvalue, %s, expected\n' %statistic_type)
            for k, v in self.summary.items():
                summary_file.write(','.join([k, v]) + '\n')

        output_venn_dir = os.path.join(self.output_dir, 'venn-diagram')
        os.makedirs(output_venn_dir) if not os.path.isdir(output_venn_dir) else None
        copyfile(os.path.join(self.package_dir, 'venn-diagram.html'),
                 os.path.join(output_venn_dir, 'venn-diagram.html'))
        copyfile(os.path.join(self.package_dir, self.js_venn_name), os.path.join(output_venn_dir, self.js_venn_name))
        copyfile(os.path.join(self.package_dir, self.js_d3_name), os.path.join(output_venn_dir, self.js_d3_name))
        copyfile(os.path.join(self.package_dir, self.wislogo), os.path.join(output_venn_dir, self.wislogo))
        with open(os.path.join(output_venn_dir, 'intersections.jsonp'), 'w') as json_file:
            json_file.write("var sets = ")
        with open(os.path.join(output_venn_dir, 'intersections.jsonp'), 'a') as json_file:
            json.dump(self.summary_json, json_file)


def parse_args():
    help_txt = "Create report of counts in each step of pipeline for each sample"
    parser = argparse.ArgumentParser(description=help_txt)
    parser.add_argument('--input-dir', metavar='path', type=str,
                        help='Directory with input files. The file names must to to be sampleName.csv or sampleName.xlsx',
                        default=os.curdir, required=True)
    parser.add_argument('--output-dir', metavar='path', type=str, help='Name of existing output directory',
                        default=os.curdir,
                        required=True)
    parser.add_argument('--min-log-fc', metavar='1.0', type=float,
                        help='Minimum absolut value of log fold change (for example 1.0 for fold change 2 or 1/2). Defauld: 1.0',
                        default=1.0, required=False)
    parser.add_argument('--max-log-fc', metavar='100000000000000000.0', type=float,
                        help='Maximum absolut value of log fold change (for example 7.0 for fold change 128 or 1/128). Defauld: 100000000000000000.0',
                        default=sys.float_info.max, required=False)
    parser.add_argument('--min-p-value', metavar='0.0', type=float, help='Minimum p-value. Default: 0.0', default=0.0,
                        required=False)
    parser.add_argument('--max-p-value', metavar='0.05', type=float, help='Maximum p-value. Default: 0.05',
                        default=0.05,
                        required=False)
    parser.add_argument('--total_gene_numbers', metavar='30000', type=int,
                        help='Number of the total genes in transcriptome. Default: 30000', default=30000,
                        required=False)
    parser.add_argument('--package-dir', metavar='path', type=str,
                        help='Directory of this package. Need for copy the js files for the diagram',
                        default='/home/labs/fluhr/Collaboration/ve-venn-diagram/lib/python2.7/site-packages/vennDiagram',
                        required=False)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if not os.path.isdir(args.input_dir):
        raise IOError('No such input folder: %s' % args.input_dir)
    print 'Minimum fold change is %s, Maximum fold change is %s, Minimum p-value is %s, Maximum p-value is %s' % (
    args.min_log_fc, args.max_log_fc, args.min_p_value, args.max_p_value)
    os.makedirs(args.output_dir) if not os.path.isdir(args.output_dir) else None
    with open(os.path.join(args.output_dir, 'log.txt'), 'w') as log:
        log.write('Parameters:\n')
        log.write('Input directory: %s\n' % (args.input_dir))
        log.write('Output directory: %s\n' % (args.output_dir))
        log.write('Minimum fold change: %s\n' % (args.min_log_fc))
        log.write('Maximum fold change: %s\n' % (args.max_log_fc))
        log.write('Minimum p-value: %s\n' % (args.min_p_value))
        log.write('Maximum p-value: %s\n' % (args.max_p_value))
        log.write('Total gene numbers: %s\n' % (args.total_gene_numbers))
        log.write('Package directory: %s\n' % (args.package_dir))

    vd = VennDiagram(args.input_dir, args.output_dir, float(args.min_log_fc), float(args.max_log_fc),
                     float(args.min_p_value), float(args.max_p_value), args.total_gene_numbers,
                     args.package_dir, JS_VENN_NAME, JS_D3_NAME, WISLOGO)
    vd.filter_files()
    vd.find_intersections()
    print 'Run ended. See results in output folder: %s' % args.output_dir
