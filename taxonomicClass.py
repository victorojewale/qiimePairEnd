import sys
import os
import io
import qiime2.plugins
import pandas as pd

from qiime2.plugins import metadata, taxa, composition, feature_classifier
    
workdir='./'

def taxaClass( reads):
    
    

    gg_classifier = qiime2.Artifact.import_data('TaxonomicClassifier', workdir+'/classifier/')

    taxonomy = feature_classifier.methods.classify_sklearn(reads = qiime2.Artifact.load(reads),
                                                       classifier = gg_classifier)
    taxa_class=taxonomy.classification.save("taxa_class.qza")



    taxonomy_artifact = qiime2.Artifact.load('taxa_class.qza')

    taxonomy_df = taxonomy_artifact.view(pd.DataFrame)
    taxonomy_df.to_csv("taxaClass.csv",index= False)
    



    return taxonomy

    #taxonomy_classification = metadata.visualizers.tabulate(taxa_class.view(qiime2.Metadata))
    #taxonomy_classification.visualization

    taxa_bar_plot = taxa.visualizers.barplot(qiime2.Artifact.load(table_seq.qza), taxa_class, sample_metadata)
    taxa_bar_plot.visualization
    

def main():
    "Input is denoised representative sequence"
    taxaClass(sys.argv[1])


main()
