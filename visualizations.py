import sys
import os
import io
import qiime2.plugins
import pandas as pd



from qiime2.plugins.demux.visualizers import summarize
from qiime2.plugins import feature_table, metadata

workdir='./'

sample_metadata = qiime2.Metadata.load(workdir+'/sample-metadata.tsv')


def demuxVisual(per_sample_seq):
 
    demux_summary = summarize(qiime2.Artifact.load(per_sample_seq))

    demux_summary.visualization
    return demux_summary.visualization

def visualRepSeq(repSeq):
    #Visualize representative sequences
    out_dir = "/tmp/deblur_sqs_vis"
    dada_seq_viz = feature_table.visualizers.tabulate_seqs(qiime2.Artifact.load(repSeq)).export_data(out_dir)

    
    from IPython.core.display import  HTML
    HTML('<iframe height = 1000, width = 1000, src = "{}/data/index.html"> </iframe>'.format(out_dir))
    
    
    return dada_seq_viz.visualization

def visualTabSeq(tabSeq):
    #Visualize feature table

    #feature_table_viz = feature_table.visualizers.summarize(qiime2.Artifact.load(tabSeq),
    #                                                   sample_metadata)
    #feature_table_viz.visualization
    unrarefied_table=qiime2.Artifact.load(tabSeq)
    rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
    rarefied_table = rarefy_result.rarefied_table

    
    df = rarefied_table.view((pd.DataFrame))
    df.to_csv("featureTable.csv",index= False)
    

    return df

def main():

    visualTabSeq(sys.argv[1])


main()
