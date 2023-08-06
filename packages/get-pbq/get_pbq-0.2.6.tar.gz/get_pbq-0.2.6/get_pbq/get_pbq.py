from Bio import SeqIO
import os
import gzip
import argparse

def main(input_path=None):
    if not input_path:
        parser = argparse.ArgumentParser(
            description='Get per-base quality scores as percentage and count.',
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
        with gzip.open(input_path, "rt") as input_path:
            for record in SeqIO.parse(input_path, "fastq"):
                qscores = record.letter_annotations["phred_quality"]
                for qscore in qscores:
                    total += 1
                    if qscore in qscore_count:
                        qscore_count[qscore] += 1
                    else:
                        qscore_count[qscore] = 1
    else:
        with open(input_path, "rt") as input_path:
            for record in SeqIO.parse(input_path, "fastq"):
                qscores = record.letter_annotations["phred_quality"]
                for qscore in qscores:
                    total += 1
                    if qscore in qscore_count:
                        qscore_count[qscore] += 1
                    else:
                        qscore_count[qscore] = 1
    print("Phred Score\tBases(%)\tBases(#)")
    for i in range(43):
        if i in qscore_count:
            print("Q%s\t%.1f\t" % (i, qscore_count[i]/total*100, qscore_count))

    return 0


if __name__== "__main__":
    main()
