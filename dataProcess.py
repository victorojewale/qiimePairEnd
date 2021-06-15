import sys
import os
import io
import qiime2

workdir='./'


# Function to perform raw sequence processing(import to artifact)
def import_data_format(seq_path):
    pair_end_sequences = qiime2.Artifact.import_data(
        'EMPPairedEndSequences', workdir+ seq_path)
 
    pair_end=pair_end_sequences.save("pair_end.qza")

    return pair_end_sequences



def main():
    "Our input here is the raw sequence reads(fastq) "
    import_data_format(sys.argv[1])


main()
