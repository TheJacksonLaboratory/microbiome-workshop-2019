---
layout: post
title: "Working at the command line with Bash" 
date:   2018-11-06 12:00:00
categories: jekyll update
---

## Session Overview

The purpose of this session is to provide familiarity and comfort with the Unix shell for the purposes of working with the course material. It is not meant to be a comprehensive lesson. For more in-depth instruction of using Bash, the default Unix shell, please see the Software Carpentry lesson, ["The Unix Shell"][sc-url] <br>

You may see advanced commands in the workshop that are not covered here because of time. If you are curious about what they do, ask one of the instructors or helpers, use the `man` command (covered in [Section 1](#header1)), or try an online resource such as [Stack Overflow][so-url] (or [Google][google-url]!).<br>

Details of the individual session components are included below:

&nbsp;&nbsp;[1. Getting started with the shell](#header1) <br>
&nbsp;&nbsp;[2. Creating and editing text files](#header2) <br>
&nbsp;&nbsp;[3. Running commands and managing output](#header3) <br>
&nbsp;&nbsp;[4. Variables and wildcards](#header4) <br>
&nbsp;&nbsp;[5. Loops and scripts](#header5) <br>
&nbsp;&nbsp;[6. Miscellaneous](#header6) <br>


<br>
<br>
<br>


----------------------------------
# 1. Getting started with the shell<a name="header1"></a>

The job of a shell program is to provide a text-based environment for viewing files and directories, running programs and pipelines, and monitoring program status and output. The shell that we will be using in this workshop is called Bash. <br>

After logging in to your instance for this workshop, you should see a Bash prompt, where you can input commands:

{% highlight bash %}

{% endhighlight %}

In the example above, you'll see that a few commands have been entered at the prompt. The first line is empty and just shows the prompt. The second line 

"""The first line shows only a prompt, indicating that the shell is waiting for input. Your shell may use different text for the prompt. Most importantly: when typing commands, either from these lessons or from other sources, do not type the prompt, only the commands that follow it.
"""


ls
<options, including -h -a -l -p>
pwd
cd
man
mkdir
cp/mv
rm

----------------------------------
# 2. Creating and editing text files<a name="header2"></a>

echo
nano
cat

The Bash shell gives us access to several useful Unix utilites for working with text and text files. We'll start with a very simple command called `echo`, which simply repeats text back that is given as an argument. For example:

 
{% highlight bash %}

{% endhighlight %}

Here, the `echo` command has taken the input text and directed it to our screen as **Standard Output**, or **stdout**. We can **redirect** stdout to a file using the `>` character. For example:

 
{% highlight bash %}

{% endhighlight %}

> Challenge 2.1: Create a text file called 'text_file1' that contains the line "Roses are red"<br>
> Challenge 2.2: Try viewing the content of your file with the `cat` command: `cat text_file1`.

Now what if you want to edit the file you just created? For this, we will use a basic [text editor][texteditor-wikipedia] called Nano. For details on how to use Nano, see the [online documentation][nano-homepage]. 

{% highlight bash %}

{% endhighlight %}

![Nano]({{ site.baseurl }}/images/NanoExample.png)
 
> Challenge 2.3: Add a new line to your document: "Violets are blue"<br> 
> Challenge 2.4: Try saving the document, closing it, and re-opening it.<br>
> Challenge 2.5: Using any method you'd like, create a second file called 'text_file2' that contains the rest of our poem:<br>
>> There are trillions of bacteria<br>
>> Living on you!<br>

<br>
<br>


----------------------------------
# 3. Running commands and managing output<a name="header3"></a> 

As mentioned above, Bash gives you access to dozens of small programs that are very useful for dealing with text files. A few examples are:

`grep`
grep lets you perform searches on your text files. For example:

{% highlight bash %}

{% endhighlight %}

stderr
stdout
head -4
wc -l
less
grep -v (exclude)
running a command with inputs with redirection
|
> - “redirect"
&>
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
# 4. Variables and wildcards<a name="header4"></a>

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

> How many unique sequences remain after removing duplicate copies?
> Have a look at the first four lines of `all_unique_seqs.fasta` to see where sizeout is recorded.

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
# 5. Loops and scripts<a name="header5"></a>

variable
${VARNAME}
backticks ` `
date
 
\ — continuous character
 
comments #
wildcards *
 
for
do
 
 
execution of program
./
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
# 6. Miscellaneous<a name="header6"></a>


 
chmod 
which
awk

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

# call this script from it's installed location using python
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



[texteditor-wikipedia]: https://en.wikipedia.org/wiki/Text_editor
[sc-url]: http://swcarpentry.github.io/shell-novice/
[so-url]: https://stackoverflow.com
[google-url]: https://www.google.com

