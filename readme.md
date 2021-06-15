#  Pair End Qiime Analysis Pipeline

![overview of qiime](https://user-images.githubusercontent.com/39276857/101550906-6830fb80-39b0-11eb-90d6-62a69447ced1.png)


## About Analysis
An analysis of soil samples from the Atacama Desert in northern Chile. The Atacama Desert is one of the most arid locations on Earth, with some areas receiving less than a millimeter of rain per decade. Despite this extreme aridity, there are microbes living in the soil. The soil microbiomes profiled in this study follow two east-west transects, Baquedano and Yungay, across which average soil relative humidity is positively correlated with elevation (higher elevations are less arid and thus have higher average soil relative humidity). Along these transects, pits were dug at each site and soil samples were collected from three depths in each pit.
https://microbiomejournal.biomedcentral.com/articles/10.1186/2049-2618-1-28
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6990129/
P.S. There are links to the dataset used for this pipeline in the ATACAMA end to end Notebook.   

## dataProcess.py
This script converts the fastq raw files into artifacts(qiime analysis are done in this format).

It is run with {python dataProcess.py pairedSequencesDirectory}

The output is an artifact file(.qza)

## demultiplex.py
This script does the demultiplexing of the processed artifact gotten from the dataProcess stage.

"Imagine we have just received some FASTQ data, hot off the sequencing instrument. Most next-gen sequencing instruments have the capacity to analyze hundreds or even thousands of samples in a single lane/run; we do so by multiplexing these samples, which is just a fancy word for mixing a whole bunch of stuff together. How do we know which sample each read came from? This is typically done by appending a unique barcode (a.k.a. index or tag) sequence to one or both ends of each sequence. Detecting these barcode sequences and mapping them back to the samples they belong to allows us to demultiplex our sequences."

It is run with {python demultiplex.py artifactFromRawRead.qza}

The output is per_sample_sequences(.qza)

## denoise.py
Denoising and clustering

We denoise our sequences to remove and/or correct noisy reads. 

We dereplicate our sequences to reduce repetition and file size/memory requirements in downstream steps (don’t worry! we keep count of each replicate). 

We cluster sequences to collapse similar sequences (e.g., those that are ≥ 97% similar to each other) into single replicate sequences. This process, also known as OTU picking, was once a common procedure, used to simultaneously dereplicate but also perform a sort of quick-and-dirty denoising procedure (to capture stochastic sequencing and PCR errors, which should be rare and similar to more abundant centroid sequences). 

It is run with {python denoise.py perSampleSequence.qza}

The output is table : 

FeatureTable[Frequency]
    The resulting feature table.

representative_sequences : FeatureData[Sequence]
    The resulting feature sequences. Each feature in the feature table will
    be represented by exactly one sequence, and these sequences will be the
    joined paired-end sequences.

denoising_stats : SampleData[DADA2Stats]


## fullPipeline.py
This script is a combination of the 3 scripts above(dataprocess, demultiplex, denoise) 
The result of the fullPipeline.py can be used downstream for other analysis e.g taxanomic classification

It is run with {python fullPipeline.py (The directory of our pairend sequence reads) }

The final output(s) is the output(s) gotten from the denoise script  


## taxonomicClass.py
This script does the identification of the organisms that are present in a sample

https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-018-0470-z
"We can do this by comparing our query sequences (i.e., our features, be they ASVs or OTUs) to a reference database of sequences with known taxonomic composition. Simply finding the closest alignment is not really good enough — because other sequences that are equally close matches or nearly as close may have different taxonomic annotations. So we use taxonomy classifiers to determine the closest taxonomic affiliation with some degree of confidence or consensus (which may not be a species name if one cannot be predicted with certainty!), based on alignment, k-mer frequencies, etc"

It is run with {python taxonomicClass.py rep_seq.qza }

The output is taxa_class(.qza) which can be converted into a csv file(taxa_class.csv)
