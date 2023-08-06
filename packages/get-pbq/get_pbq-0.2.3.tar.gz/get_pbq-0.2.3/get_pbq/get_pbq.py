from Bio import SeqIO
import os
import gzip
import argparse

def main(input_path=None):
    if not input_path:
        parser = argparse.ArgumentParser(
            description='Annotation pipeline for Oxford Nanopore sequences.',
            add_help=True)
        parser.add_argument(
            '-i', '--input', metavar="file", type=str, action='store',
            dest='input', required=True,
            help=('Input file in fastq or fastq.gz format.'))
        args = parser.parse_args()
        input_path = args.input
    filename, file_extension = os.path.splitext(input_path)
    qscore_count = [0 for i in range(43)]
    qscore_count = {}
    total = 0
    if file_extension == '.gz':
        with gzip.open(path, "rt") as input_path:
            for record in SeqIO.parse(input_path, "fastq"):
                qscores = record.letter_annotations["phred_quality"]
                for qscore in qscores:
                    total += 1
                    if qscore in qscore_count:
                        qscore_count[qscore] += 1
                    else:
                        qscore_count[qscore] = 1
    else:
        with open(path, "rt") as input_path:
            for record in SeqIO.parse(input_path, "fastq"):
                qscores = record.letter_annotations["phred_quality"]
                for qscore in qscores:
                    total += 1
                    if qscore in qscore_count:
                        qscore_count[qscore] += 1
                    else:
                        qscore_count[qscore] = 1
    for i in range(43):
        if i in qscore_count:
            print("Q%s\t%.2f" % (i, qscore_count[i]/total))

    return 0


if __name__== "__main__":
    main()
