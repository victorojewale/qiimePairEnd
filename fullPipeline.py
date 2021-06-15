import sys
import os
import io
import qiime2
import qiime2.plugins
import pandas as pd




from qiime2.plugins.dada2.methods import denoise_paired
from qiime2.plugins import feature_table, metadata
from qiime2.plugins import demux


workdir='./'

sample_metadata = qiime2.Metadata.load(workdir+'/sample-metadata.tsv')




# Function to perform raw sequence processing(import to artifact)
def import_data_format(seq_path):
    pair_end_sequences = qiime2.Artifact.import_data(
        'EMPPairedEndSequences', workdir+ seq_path)
 
    pair_end=pair_end_sequences.save("pair_end.qza")

    return pair_end_sequences



# Demultiplexing sequences
def demultiplex(pair_end_sequences):

    
    demux_sequences = qiime2.plugins.demux.methods.emp_paired((pair_end_sequences),
                                               sample_metadata.get_column(
                                                   'barcode-sequence'),
                                               golay_error_correction=False,
                                               rev_comp_mapping_barcodes=True)

    demux_per_sample=demux_sequences.per_sample_sequences.save("per_sample.qza")

    demux_summary = demux.visualizers.summarize(demux_sequences.per_sample_sequences)
    #viz = feature_table.visualizers.tabulate_seqs(rep_seqs)
    #demux_per_sample.visualization.save('foo.qzv')
    #!qiime tools view foo.qzv

    print(demux_summary.visualization)


    return demux_per_sample

# denoising
def denoise(demux_per_sample):
    clean_seq = denoise_paired(qiime2.Artifact.load(demux_per_sample),
                               trunc_len_f=150, trunc_len_r=150,
                               trim_left_f=13, trim_left_r=13, n_threads=4)


    #rep sequences csv(representative sequences)
    rep_seq=clean_seq.representative_sequences.save("rep_seq.qza")
    

    #table sequences csv(feature table)
    table_seq=clean_seq.table.save("table_seq.qza")
    table_seq_artifact = qiime2.Artifact.load('table_seq.qza')


    table_seq_md = table_seq_artifact.view(qiime2.Metadata)
    table_seq_tab, = metadata.visualizers.tabulate(input=table_seq_md)
    print(table_seq_tab)

    denoiseStats_seq=clean_seq.denoising_stats.save("denoiseStats_seq.qza") 
    return clean_seq
  


def main():
    "Our input here is the raw sequence reads(fastq) "
    pair_end_sequences =import_data_format(sys.argv[1])
    demux_per_sample=demultiplex(pair_end_sequences)
    denoise(demux_per_sample)



if __name__ == "__main__":
    main()
