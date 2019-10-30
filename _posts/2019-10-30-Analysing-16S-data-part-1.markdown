---
layout: post
title:  "Analysing 16S data: Part 1"
date:   2019-10-30 13:00:00
categories: jekyll update
---

## Session Overview

During this session we will cover the fundamentals of amplicon-based microbiome analysis.<br>
Details of the individual session components are included below:

&nbsp;&nbsp;[1. Using a text editor to document your actions](#header1) <br>
&nbsp;&nbsp;[2. An introduction to sequence data](#header2) <br>
&nbsp;&nbsp;[3. Combining paired-end reads into contiguous sequences](#header3) <br>
&nbsp;&nbsp;[4. Generating a unique set of 16S gene sequences](#header4) <br>
&nbsp;&nbsp;[5. Clustering unique sequences into operational taxonomic units](#header5) <br>
&nbsp;&nbsp;[6. Creating a table of OTU abundance](#header6) <br>
&nbsp;&nbsp;[7. Assigning taxonomy to OTU sequences](#header7) <br>
&nbsp;&nbsp;[8. Amalgamating code into a pipeline script](#header8) <br>

&nbsp;&nbsp;[Conclusions](#header9) <br>
&nbsp;&nbsp;[OTUs versus exact sequence variants](#header10) <br>



<br>
<br>
<br>


## Session One
----------------------------------
# 1. Using a text editor to document your actions<a name="header1"></a>

During this session you may wish to keep a record of the commands used to analyse your 16S data. 
One way to do this is to write each command to a file. From the command line, this can be 
acheived using a [text editor][texteditor-wikipedia]. There are many to choose from, but this 
session will use Nano.

{% highlight bash %}
# Navigate to the working directory for this session
cd ~/MCA/16s/Session1

# Open a new file
nano 16s_pipeline.sh
{% endhighlight %}
 
Opening a new text file you should see something similar to this: 

![Nano]({{ site.baseurl }}/images/NanoExample.png)
 
> Try writing some text to the document 16s_pipeline.sh<br>
> Try saving the document, closing it, and re-opening it.

Because the saved document is a shell script, it is also possible to run the entire 
script from the command line.

{% highlight bash %}
# Make the file 16s_pipeline.sh executable from the command line.
chmod u+x 16s_pipeline.sh

# run the code in 16s_pipeline.sh
./16s_pipeline.sh
{% endhighlight %}


For more information on using nano, see the Nano [online documentation][nano-homepage]. 
<br>
<br>

----------------------------------
# 2. An introduction to 16S sequence data<a name="header2"></a>

The ubiquitous format for the storage of sequence data are fastq files.
To begin, navigate to the location of the sequence data that will be used for today's session.

{% highlight bash %}
cd ~/MCA/16s/Session1/fastqs/             # change directory
ls                                        # list contents of directory
{% endhighlight %}
 
These data are from an Illumina paired-end sequencing run. There should be two files per sample,
with the files *.R1_sub.fastq and *.R2_sub.fastq containing the first and second reads in each 
pair, respectively. Have a look at the first four lines in one of the fastqs.

{% highlight bash %}
head -4 A_control.R1_sub.fastq            # view the first n lines of a file

@M03204:217:000000000-B8W8J:1:2108:24791:7353
AGAGTTTGATCCTGGCTCAGGATGAACGCTGGCGGCATGCCTTACACATGCAAGTCGGACGGGAAGTGGTGTTTCCAGTGGCGGACGGGTGAGTAACGCGTAAGAACCTACCCTTGGGAGGGGAACAACAGCTGGAAACGGCTGCTAATACCCCGTAGGCTGAGGAGCAAAAGGAGGAATCCGCCCGAGGAGGGGTTCGCGTCTGATTAGCTAGTTGGTGAGGCAATAGCTTACCAAGGCGATGATCAGTAGCTGGTCCGAGAGGATGATCAGCCACACTGGGACTGAGACACGGCCCAGA
+
CCCCCGFGGGGGGFCFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDFGGGGGGGGGGGGGGGGGGGFGGGGDGGGGGGGGGFGGGGGGEGB:FEFGGGFGGECGGGGFFGFGFGGGGGGGGFGFEGGGGGGFFFGGGGGGFECGGGFGGGGGGGGGGGGGGGGGGGGF6CFFGGGGDGGEFFCF:5*)5>29*5<)5>GF4)
{% endhighlight %}

> What information is contained in each line of the fastq? 
> How are the reads in *_R1_sub.fastq files matched to their corresponding pair in *_R2_sub.fastq?

For further detail on the contents of fastq files, see [`here`][fastq-wikipedia].
<br>
<br>
<br>

----------------------------------
# 3. Combining paired-end reads into contiguous sequences<a name="header3"></a> 

In order to generate a single, contiguous sequence spanning the target region of the 16S gene, it's
necessary the paired reads in each fastq file. To do this we will use a tool called FLASh. Start by
combining two fastq files for a single sample.

{% highlight bash %}
# Check that you have returned to the main session directory
# This should be ~/MCA/16s/Session1
pwd

# Run FLASh for a single sample
flash ./fastqs/A_control.R1_sub.fastq ./fastqs/A_control.R2_sub.fastq

# The files created by FLASh should be in the current directory
ls
{% endhighlight %}

> Have a look at the files created by FLASh, in particular the file out.extendedFrags.fastq<br>
> Are all sequences the same length?
> How many sequences were successfully assembled and how many failed to assemble? 

For information on options for running FLASh and the files it creates visit the
[website][flash-website], or access the help documentation on the command line.

{% highlight bash %}
flash --help
{% endhighlight %}

<br>

#### 3.b. Running FLASh using a for loop<a name="header3b"></a>

While it's possible to run FLASh individually for each sample. It's also possible to use a 
[for loop][go2linux-forloop] to iteratively combine fastqs for all the samples in the fastq directory.

{% highlight bash %}
# make a directory in which to store the combined fastq files
mkdir fastqs_combined

ls 
ls fastqs_combined

# Run FLASh for all samples in the working directory
for FASTQ1 in fastqs/*.R1_sub.fastq
do
  # capture the file prefix, which corresponds to the sample name
  SAMPLEID="$(basename ${FASTQ1%.R1_sub.fastq})"
  # assign the second fastq file to the variable FASTQ2
  FASTQ2="fastqs/${SAMPLEID}.R2_sub.fastq"
  # run FLASh 
  flash $FASTQ1 $FASTQ2 --output-prefix=$SAMPLEID --output-directory=fastqs_combined
done

ls fastqs_combined
{% endhighlight %}

> Using your text editor, copy the for loop into your pipeline script. <br>
> Remember to annotate your code so that you can return to it later.

<br>

#### 3.c. Converting fastq files to fasta format

From here on, it's necessary to work with fasta files, rather than fastq.
It's possible to convert our data from fastq to fasta format using the 
[FASTX-toolkit][fastx-homepage].

{% highlight bash %}
# Run fastq_to_fasta for the combined fastq files created by FLASh
for FASTQ in fastqs_combined/*.extendedFrags.fastq
do
  # capture the file prefix, which corresponds to the sample name
  SAMPLEID="${FASTQ%.extendedFrags.fastq}"
  # run fastq_to_fasta
  fastq_to_fasta -i $FASTQ -o $SAMPLEID.fasta
done

# The fasta files should now be in the same directory as the combined fastqs
ls fastqs_combined
{% endhighlight %}

> Enter the combined_fastq directory and look at the first four lines of a fasta file. 
> How do they differ from the fastq format? 

<br>

----------------------------------
# 4. Generating a unique set of 16S gene sequences<a name="header4"></a>

Having successfully processed our sequence data, the goals now are to:
1. Identify distinct biological taxa
2. Quantify the relative abundance of each distinct taxon

These goals are predicated on the assumption that the extent to which two distinct bacterial
taxa are related correlates with the similarity of their 16S rRNA gene sequences. Different
taxa can therefore be identified by resolving unique 16S gene sequences and counting their 
abundance. 

There are many ways to acheive these goals. However, in this session we will make use of the widely
used tool [USEARCH][usearch-homepage], which can accomplish all of these steps.

The first step in processing data for use with USEARCH is to pool 16S gene sequences from
different samples into one file. In order to keep track of which sequence originated from which 
sample, it is also necessary to add the sample name to the header line for each fasta sequence. 
For simplicity, this step will be carried out using a custom script. 

{% highlight bash %}
# The location of the script for combining fasta files
which samples2fasta

# Combine samples into a single file located in the run directory
samples2fasta fastqs_combined all_samples.fasta
{% endhighlight %}

The second step is to create a file containing a single copy of each unique sequence in the
dataset, as each unique sequence potentially represents a unique bacterial taxon. When the
`-sizeout` argument is provided USEARCH keeps a record of the number of times each unique
sequence appears in the data set. 

{% highlight bash %}
# How many sequences are in the combined fasta file?
cat all_samples.fasta | grep ">" | wc -l

# Run USEARCH to generate a file of unique sequences
usearch -fastx_uniques all_samples.fasta -fastaout all_unique_seqs.fasta -sizeout
{% endhighlight %}

> How many unique sequences remain after removing duplicate copies?<br>
> Have a look at the first four lines of `all_unique_seqs.fasta` to see where sizeout is recorded.<br>
> What is different about the first four lines of `all_unique_seqs.fasta` compared to previous fasta
> files we've looked at?

<br>

Sequence variation may be a result of divergent evolution, but it may also be caused by errors
during sequencing. If a bacterial taxon is present at a detectable abundance in these samples, then
its 16S gene sequence is likely to be represented multiple times in the data set. By contrast,
sequencing error is assumed to be (more-or-less) random, meaning that errors due to sequencing have
only a small likelihood of occurring more than once. For this reason it is common practice to 
discard unique sequences that occur one, or a few times. The next step is to sort unique sequences
based on their frequency of occurrence, and to discard those that occur only once. 

{% highlight bash %}
# Sort unique sequences based on the number of times they occur, discarding singletons
usearch -sortbysize all_unique_seqs.fasta -fastaout all_unique_seqs_sorted.fasta -minsize 2
{% endhighlight %}

> How many unique sequences remain after removing singletons? <br>
> How many unique sequences remain if you discard sequences occurring less than five times?

<br>
<br>


----------------------------------
# 5. Clustering unique sequences into operational taxonomic units<a name="header5"></a>

As discussed in Section 4, sequence-based analysis assumes that taxonomic (or biologically
relevant?) differences between bacteria are reflected by differences in their 16S gene sequence. 
But how much do two 16S gene sequences have to differ before they represent two distinct bacterial
strains, species, or even genera? There is a discussion of this issue on the USEARCH
[website][usearch-definingotus].

In this practical session the goal is to identify and quantify distinct bacterial species.
Assuming that a certain amount of 16S gene sequence variation exists within species (different
bacterial strains?) we will generate operational taxonomic units (OTUs) based on the assumption 
that two sequences which are more than 97% similar belong to the same species.

![Uparse]({{ site.baseurl }}/images/uparseotu_algo.jpeg)


The UPARSE-OTU algorithm, implemented in USEARCH, can be used to generate OTUs based on this 97%
similarity threshold. It selects a single representative sequence for each generated OTU.

{% highlight bash %}
# Cluster OTUs using a 97% similarity threshold
usearch -cluster_otus all_unique_seqs_sorted.fasta -otus otus.fasta
{% endhighlight %}

> How many OTUs have been generated? <br>
> How many chimeras were detected? <br>
> How does the number of OTUs compare to the number of sequences in the combined fasta file produced
> in Section 3c?

Note that [chimeras][usearch-chimera] can be a significant problem in amplicon-based sequence analysis.
There are dedicated tools for chimera detection and removal (e.g. [ChimeraSlayer][chimeraslayer-home]);
however the UPARSE-OTU algorithm implicitly filters chimeras.

 
<br>
<br>

----------------------------------
# 6. Creating a table of OTU abundance<a name="header6"></a>

Having generated a set of sequences representing distinct bacterial taxa (OTUs). The next step is to
quantify OTU abundance. This can be acheived by counting the number of sequences in each sample that
match each OTU. For a sequence to "match" an OTU it must be more than 97% similar to the 
representative sequence for that OTU.

The first step is to relabel each of our OTUs with a unique identifier. We will do this using a 
python script fasta_number.py

{% highlight bash %}
# location of the fasta_number.py python script
which fasta_number.py

# call python script to rename the OTUs in the format OTU_*
fasta_number.py otus.fasta OTU_ > otus_renamed.fasta
{% endhighlight %}


The next step is to use the pooled fasta file (`all_samples.fasta`) generated in
[Section 4](#header4) to map the sequences originating from each sample file back their closest
matching OTUs. Sample sequences that do not match any OTU sequenced at >97% similarity are assumed
to be sequencing errors and are discarded.

{% highlight bash %}
# Match all sample sequences back to OTU sequences at a 97% similarity threshold
# Sample sequnences are present in the file all_samples.fasta
# The reference (-db) is the file containing representative OTU sequences
usearch -usearch_global \
            all_samples.fasta \
        -db otus_renamed.fasta \
        -strand plus \
        -id 0.97 \
        -uc otu_map.uc
{% endhighlight %}

> Have a look at the format of the output file `otu_map.uc`. Can you identify the information in
> each column? <br>
> Can you fine a line in this file that begins with "N"?

The output file generated when matching sample sequences to OTUs is in 
[USEARCH cluster format][usearch-clusterformat]. It contains the best OTU match (if any) for each 
sample sequence. From this file it is possible to generate a count table summarizing the number of
sequences in each sample that match each OTU.

{% highlight bash %}
# find the location of the python script usearch2otutab.py
which uc2otutab.py

# As this is a script, not an executable progam we will run it
# from it's installed location using python
python ~/local/bin/uc2otutab.py otu_map.uc > otu_matrix.tsv
{% endhighlight %}

The resulting file `otu_matrix.tsv` is a count matrix in which columns are samples, rows are OTUs
and each cell represents the number of sequences assigned to each OTU in each sample. 

<br>
<br>

----------------------------------
# 7. Assigning taxonomy to OTU sequences<a name="header7"></a>

Having generated a matrix of OTU abundance in different samples it is often useful to compare OTU
sequences against a reference database in order to identify their likely taxonomy. One simple way to
do this would be to copy each sequence into  NCBI's [BLAST][ncbi-ntblast] tool, which will compare
it to the NCBI nucleotide database. 

{% highlight bash %}
# Select the first OTU sequence in your renamed fasta
head -2 otus_renamed.fasta
{% endhighlight %}

> Try copying the entire OTU sequence into the "Enter Query Sequence" box on the NCBI blast <br>
> website. Then hit "BLAST".
> How informative is the closest BLAST match in the NCBI nucleotide reference database? 

An alternative method for classifying 16S gene sequences is to use the Ribosomal Database Project
(RDP) classifier tool, which compares sequences to the [RDP reference database][rdp-database].
The RDP classifier can be run from the command line without the need to download the entire
reference database. 

{% highlight bash %}
# Run the RDP classifer. As this tool is written in java, it's necessary to first run
# java then pass the location of the installed classifier
java -Xmx1g -jar ~/local/src/rdp_classifier_2.12/dist/classifier.jar classify \
  -f filterbyconf \
  -c 0.8 \
  -o otu_taxonomy_rdp_0.8.tsv \
  -h otu_taxonomy.hierachy \
  otus_renamed.fasta
{% endhighlight %}

> Have a look at the two files (`otu_taxonomy_rdp_0.8.tsv` and `otu_taxonomy.hierachy`) produced by
> the RDP classifier.

The RDP classifier produces two files the first `otu_taxonomy_rdp_0.8.tsv` contains a taxonomic
classification from each OTU from Kingdom to Genus level. The second `otu_taxonomy.hierachy`
contains similar information in a commonly used hierachical format. Each taxonomic level encountered
in our dataset is listed in this file, with the final column showing the number of times it is 
encountered. 

For further information on the options available when running the RDP classifer have a look at the
help pages, as well as the `README` file that comes with the RDP installation.

{% highlight bash %}
# Running RDP without input arguments will cause it to print its help pages. 
java -Xmx1g -jar ~/local/src/rdp_classifier_2.12/dist/classifier.jar
java -Xmx1g -jar ~/local/src/rdp_classifier_2.12/dist/classifier.jar classify

# For more detailed information look at the README file
less ~/local/src/rdp_classifier_2.12/README
{% endhighlight %}

> What does the command `-c 0.8` mean?
 
<br>
<br>

----------------------------------
# 8. Amalgamating code into a pipeline script<a name="header8"></a>

Finally, having worked out how to  run each of the steps necssary to generate an OTU count table,
it should now be possible to take the code for each step and add it to the script
`16s_pipeline.sh`.

This effectively creates a simple computational pipeline. As the resulting script does not contain
any hardcoded sample names, it should be possible to run it on this and other datasets. In addition, 
a clear and well documented record of the code that has been run is essential for reproducible
computational analysis.

<br>
<br>

----------------------------------
## Conclusions<a name="header9"></a>

This session provides an overview of the fundamental steps taken to process 16S gene
sequence data from raw reads to a taxonomic abundance table that can be used for downstream
analysis. It makes use of the freely available tools FLASh and USEARCH. However, there are many 
other excellent tools/SOPs available online. See for example 
[Mothur][mothur-sop] and
[Qiime][qiime-tutorials],
for further discussion of the issues surrounding 16S sequence analysis.

If you have managed to maintain your script `16s_pipeline.sh` throughout this session, then you will
have a record of all the steps taken during 16S sequence processing. It should now  be 
possible to rerun this pipeline on this and other datasets to automatically go from 
[merging fastq files](#header3b) to [generating a count matrix](#header6). Pipelines are an
essential part of high-throughput sequence analysis. For an interesting discussion of the importance
of reproducibility in modern biological research see [here][nbiotech-article].

# OTUs versus exact sequence variants<a name="header10"></a>

In this session we have focussed on the fundamental steps that are common to most 16S analysis
methodologies. In an effort to make these steps as transparent as possible, we've also avoided
being tied to a single user environment.

One recent advance in 16S sequence analysis is the move from OTU-based analysis towards the use
of denoising algorithms designed to correct for sequencing error. As time is limited, we have not 
gone into this in the main session; however, you can find a bonus session on the use of DADA2 for
denoising 16S sequence data [here](https://thejacksonlaboratory.github.io/microbiome-workshop-2019/amplicon_sequence_variants.html).





[texteditor-wikipedia]: https://en.wikipedia.org/wiki/Text_editor
[nano-homepage]: https://www.nano-editor.org/docs.php
[fastq-wikipedia]: https://en.wikipedia.org/wiki/FASTQ_format
[flash-website]: https://ccb.jhu.edu/software/FLASH/
[go2linux-forloop]: http://go2linux.garron.me/bash-for-loop/
[fastx-homepage]: http://hannonlab.cshl.edu/fastx_toolkit/
[usearch-homepage]: https://www.drive5.com/usearch/
[usearch-definingotus]: https://www.drive5.com/usearch/manual/otus.html
[usearch-chimera]: https://www.drive5.com/usearch/manual/chimera_formation.html
[chimeraslayer-home]: http://microbiomeutil.sourceforge.net/#A_CS
[usearch-clusterformat]: https://www.drive5.com/usearch/manual/opt_uc.html
[mothur-sop]: https://www.mothur.org/wiki/MiSeq_SOP
[qiime-tutorials]: http://qiime.org/tutorials/
[tornado-tutorial]: http://acai.igb.uiuc.edu/bio/tutorial.html
[nbiotech-article]: https://www.nature.com/articles/nbt.2740
[ncbi-blast]: https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch
[rdp-database]: http://rdp.cme.msu.edu/misc/resources.jsp
