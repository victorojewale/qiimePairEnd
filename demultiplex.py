import sys
import os
import io
import qiime2.plugins


workdir='./'

	

from qiime2.plugins import demux, metadata




sample_metadata = qiime2.Metadata.load(workdir+'/sample-metadata.tsv')


# Demultiplexing sequences
def demultiplex(pair_end_sequences):

    
    demux_sequences = qiime2.plugins.demux.methods.emp_paired(qiime2.Artifact.load(pair_end_sequences),
                                               sample_metadata.get_column(
                                                   'barcode-sequence'),
                                               golay_error_correction=False,
                                               rev_comp_mapping_barcodes=True)

    demux_per_sample=demux_sequences.per_sample_sequences.save("per_sample.qza")

    demux_summary = demux.visualizers.summarize(demux_sequences.per_sample_sequences)

    print(demux_summary.visualization)


    return demux_per_sample




def main():
    "Our input here is the artifact form of our raw reads"

    demultiplex(sys.argv[1])


main()
