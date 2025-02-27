#!/usr/bin/env python

import os
import sys
import errno
import argparse

def parse_args(args=None):
    Description = 'Reformat nf-core/viralrecon samplesheet file and check its contents.'
    Epilog = """Example usage: python check_samplesheet.py <FILE_IN> <FILE_OUT>"""

    parser = argparse.ArgumentParser(description=Description, epilog=Epilog)
    parser.add_argument('-FILE_IN', required = True, help="Input samplesheet file.")
    parser.add_argument('-FILE_OUT', required = False, help="Output file.", default = '')
    return parser.parse_args(args)


def make_dir(path):
    if not len(path) == 0:
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


def print_error(error,line):
    print("ERROR: Please check samplesheet -> {}\nLine: '{}'".format(error,line.strip()))
    sys.exit(1)


def check_samplesheet(FileIn,FileOut):
    ## Check header
    HEADER = ['sample', 'fastq_1', 'fastq_2', 'fasta']
    print("HEADER: ", HEADER, '\n')
    fin = open(FileIn,'r')
    header = fin.readline().strip().split(',')
    print("header: ", header, '\n')
    if header != HEADER:
        print("ERROR: Please check samplesheet header -> {} != {}".format(','.join(header),','.join(HEADER)))
        sys.exit(1)

    sampleRunDict = {}
    while True:
        print("inside while", '\n')
        line = fin.readline()
        if line:
            print("inside if line", '\n')
            lspl = [x.strip() for x in line.strip().split(',')]

            ## Check valid number of columns per row
            if len(lspl) != len(header):
                print_error("Invalid number of columns (minimum = {})!".format(len(header)),line)

            numCols = len([x for x in lspl if x])
            if numCols < 2:
                print_error("Invalid number of populated columns (minimum = 2)!",line)

            ## Check sample name entries
            sample,fastQFiles,fastaFile = lspl[0],lspl[1:3],lspl[3]
            print("fastaFile: ", fastaFile, '\n')
            if sample:
                if sample.find(' ') != -1:
                    print_error("Sample entry contains spaces!",line)
            else:
                print_error("Sample entry has not been specified!",line)

            ## Check FastQ file extension
            for fastq in fastQFiles:
                if fastq:
                    if fastq.find(' ') != -1:
                        print_error("FastQ file contains spaces!",line)
                    if fastq[-9:] != '.fastq.gz' and fastq[-6:] != '.fq.gz':
                        print_error("FastQ file does not have extension '.fastq.gz' or '.fq.gz'!",line)


            ## Check Fasta file extension  ###
            if fastaFile:
                if fastaFile.find(' ') != -1:
                    print_error("Fasta file contains spaces!",line)

                fasta_extensions = [".fasta", ".fasta.gz", ".fa", ".fa.gz", ".fna", ".fna.gz", ".ffn", ".ffn.gz", ".faa", ".faa.gz", ".frn", ".frn.gz"]
                is_fasta = False
                for extension in fasta_extensions:
                    if fastaFile.endswith(extension):
                        is_fasta = True
                        break

                if not is_fasta:
                    print_error("Fasta file, " + fastaFile + " does not have a correct fasta extension: " + fasta_extensions)



            ## Extract sample info
            sample_info = []                                                ## [single_end, is_sra, is_ftp, fastq_1, fastq_2, md5_1, md5_2, is_fasta] //// ## [single_end, is_sra, is_ftp, fastq_1, fastq_2, md5_1, md5_2, is_ncbi, is_fasta]
            fastq_1,fastq_2 = fastQFiles

            #if fastq_1 or fastq_2: ## DIFF
            if sample and fastq_1 and fastq_2:                              ## Paired-end short reads
                sample_info = ['0', '0', '0', fastq_1, fastq_2, '', '', '0', '0', '']
            elif sample and fastq_1 and not fastq_2:                        ## Single-end short reads
                sample_info = ['1', '0', '0', fastq_1, fastq_2, '', '', '0', '0', '']
            elif sample and fastaFile:
                sample_info = ['0', '0', '0', '', '', '', '', '0', '1', fastaFile]
            else:
                print_error("Invalid combination of columns provided!",line)

            if sample not in sampleRunDict:
                sampleRunDict[sample] = [sample_info]
            else:
                if sample_info in sampleRunDict[sample]:
                    print_error("Samplesheet contains duplicate rows!",line)
                else:
                    sampleRunDict[sample].append(sample_info)


            ## Extract sample info (Fasta)
            #sample_info = []                                                ## [is_id, fasta]

            #if fastaFile:
            #    if sample and fastaFile:                              ## Paired-end short reads
            #        sample_info = ['0', fastaFile]

            #    if sample not in sampleRunDict:
            #        sampleRunDict[sample] = [sample_info]
            #    else:
            #        if sample_info in sampleRunDict[sample]:
            #            print_error("Samplesheet contains duplicate rows!",line)
            #        else:
            #            sampleRunDict[sample].append(sample_info)

            """

            ## Extract sample info (Fastq)
            sample_info = []                                                ## [single_end, is_sra, is_ftp, fastq_1, fastq_2, md5_1, md5_2]
            fastq_1,fastq_2 = fastQFiles

            if fastq_1 or fastq_2: ## DIFF
                if sample and fastq_1 and fastq_2:                              ## Paired-end short reads
                    sample_info = ['0', '0', '0', fastq_1, fastq_2, '', '', 0]
                elif sample and fastq_1 and not fastq_2:                        ## Single-end short reads
                    sample_info = ['1', '0', '0', fastq_1, fastq_2, '', '', 0]
                else:
                    print_error("Invalid combination of columns provided!",line)

                if sample not in sampleRunDict:
                    sampleRunDict[sample] = [sample_info]
                else:
                    if sample_info in sampleRunDict[sample]:
                        print_error("Samplesheet contains duplicate rows!",line)
                    else:
                        sampleRunDict[sample].append(sample_info)


            ## Extract sample info (Fasta)
            sample_info = []                                                ## [is_id, fasta]

            if fastaFile:
                if sample and fastaFile:                              ## Paired-end short reads
                    sample_info = ['0', fastaFile]

                if sample not in sampleRunDict:
                    sampleRunDict[sample] = [sample_info]
                else:
                    if sample_info in sampleRunDict[sample]:
                        print_error("Samplesheet contains duplicate rows!",line)
                    else:
                        sampleRunDict[sample].append(sample_info)
            """


        else:
            fin.close()
            break


    ##if not fastaFile: ###
    ## Write validated samplesheet with appropriate columns
    if len(sampleRunDict) > 0:
        OutDir = os.path.dirname(FileOut)
        make_dir(OutDir)
        fout = open(FileOut,'w')
        fout.write(','.join(['sample_id', 'single_end', 'is_sra', 'is_ftp', 'fastq_1', 'fastq_2', 'md5_1', 'md5_2', 'is_ncbi', 'is_fasta', 'fasta']) + '\n')
        for sample in sorted(sampleRunDict.keys()):

            ## Check that multiple runs of the same sample are of the same datatype
            ##if not all(x[:2] == sampleRunDict[sample][0][:2] for x in sampleRunDict[sample]):
                ##  print_error("Multiple runs of a sample must be of the same datatype","Sample: {}".format(sample))

            for idx,val in enumerate(sampleRunDict[sample]):
                fout.write(','.join(["{}_T{}".format(sample,idx+1)] + val) + '\n')
        fout.close()

    """
    else:
        ## Write validated samplesheet with appropriate columns
        if len(sampleRunDict) > 0:
            OutDir = os.path.dirname(FileOut)
            make_dir(OutDir)
            fout = open(FileOut,'w')
            fout.write(','.join(['sample_id', 'is_id', 'fasta']) + '\n')
            for sample in sorted(sampleRunDict.keys()):

                ## Check that multiple runs of the same sample are of the same datatype
                ##if not all(x[:2] == sampleRunDict[sample][0][:2] for x in sampleRunDict[sample]):
                  ##  print_error("Multiple runs of a sample must be of the same datatype","Sample: {}".format(sample))

                for idx,val in enumerate(sampleRunDict[sample]):
                    fout.write(','.join(["{}_T{}".format(sample,idx+1)] + val) + '\n')
            fout.close()
            print("Archivo fasta escrito") ## borrar
    """

def main(args=None):
    args = parse_args(args)
    check_samplesheet(args.FILE_IN,args.FILE_OUT)


if __name__ == '__main__':
    sys.exit(main())
