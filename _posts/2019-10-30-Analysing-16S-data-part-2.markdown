---
layout: post
title:  "Analysing 16S data: Part 2"
date:   2019-10-30 14:00:00
categories: jekyll update
---

## Session Overview

During this session we will cover the fundamentals of amplicon-based microbiome analysis.<br>
Details of the individual session components are included below:

&nbsp;&nbsp;[1. Using RStudio](#header1) <br>
&nbsp;&nbsp;[2. Loading microbiome data into R](#header2) <br>
&nbsp;&nbsp;[3. Normalizing count data](#header3) <br>
&nbsp;&nbsp;[4. Loading data into phyloseq](#header4) <br>
&nbsp;&nbsp;[5. Plotting figures](#header5) <br>
&nbsp;&nbsp;[6. Analysis of alpha diversity](#header6) <br>
&nbsp;&nbsp;[7. Analysis of beta diversity](#header7) <br>

&nbsp;&nbsp;[Conclusions](#header8) <br>

<br>
<br>
<br>


## Session One: Part 2
----------------------------------
# 1. Using RStudio<a name="header1"></a>

In the first part of this session we used the Linux command line to process our 16S data and we used
the text editor Nano to document each step in this process. Having generated an OTU count matrix and
an associated taxonomy, we will now use the statistical programming language R to further analyse
these data. 

R can also be run from the command line (try typing 'R' on the Linux command line). However, for
this session we will use RStudio, which is a freely available
[Integrated Development Environment][wikipedia-ide] (IDE) for R. 

First, from the Linux command line create a new working directory called Session1.2, then link the
output from the first part of Session 1 to this directory.

{% highlight bash %}
cd ~/MCA/16s/       # the parent directory
mkdir Session1.2    # the working directory for the second part of this session
cd Session1.2

# create a link for the files that will be used from here on
ln -s ../Session1/otu_matrix.tsv .
ln -s ../Session1/otu_taxonomy_rdp_0.8.tsv .
{% endhighlight %}

Once you have set up your working directory, return to the homepage for these practical sessions
and click on the link to open RStudio. 
This will open a [Graphical User Interface][wikipedia-gui] (GUI) in your browser, which will look
something like the image below. If you do not see the panel on the top left, on the control bar
select "File" > "New File" > "RScript". Brielfy, there should now be four open tabs: the top left is
an R script, which is analagous to the Nano script we created during the first part of this session;
the bottom left is the R console, which contains a command prompt similar to the one on the Linux 
command line; the tab on the top right provide information on your current R session; and the tab on
the bottom right provides additional useful information, such as help pages, or a window for viewing
graphical plots. <br>

![RStudio]({{ site.baseurl }}/images/rstudio.png)

We will be writing most of our code in the script window (top left), and running it in the R console.

Start by typing an R command in the script window, then pressing `Ctrl + Return` to execute it in
the console.

{% highlight R %}
# Type a print command in the R script window
print("Hello R")
# With the cursor on the same line as the print command, press Ctrl + Return
{% endhighlight %}

In the first half of this session, we were running tools (e.g. USEARCH) from within the working
directory: `~/MCA/16s/Session1`. We have just created a new working directory for the second half
of the session: `~/MCA/16s/Session1.2`. We now need to make sure that RStudio is running within
our current working directory. 

{% highlight R %}
# Find out which working directory R is running in? 
getwd()

# See which files are present in this working directory
list.files('.')

# Change the directory to the working directory for the current session
setwd('~/MCA/16s/Session1.2')

# Make sure that the otu count matrix and taxonomy file are present in the working directory
list.files('.')
{% endhighlight %}

 
> Please ask if you have any further questions about working in RStudio.

<br>
<br>

----------------------------------
# 2. Loading microbiome data into R<a name="header2"></a>

The first step is to load data into the R session. In addition to the OTU count matrix and taxonomy
table we will also load an example file containing metadata for each sample. These tables will
appear as [data frames][rtutor-dataframe]. 

{% highlight R %}
# Read in the otu count table, specify whether row/column names are present
# and what separator is used
df_count <- read.table('otu_matrix.tsv', row.names=1, header=TRUE, sep='\t')
# Look at the first six lines of the count table
head(df_count)

# Read in the taxonomy information for each OTU
df_tax <- read.table('otu_taxonomy_rdp_0.8.tsv', row.names=1,
	             header=TRUE, sep='\t')
# Look at the first six lines of the taxonomy table
head(df_tax)

# Read in the metadata for each sample. Note this is a comma-separated file
# Note this file is not in the working directory
df_meta <-  read.table('~/MCA/data/16S/Metadata.csv', 
                       header=TRUE, sep=',', row.names=1)
head(df_meta)

# It is important that the sample names are the same across data frames
# Remove the fasta suffix from the sample names in the data frame of OTU counts
names(df_count) <- gsub('.fasta', '', names(df_count))
head(df_count)
{% endhighlight %}

<br>
<br>

----------------------------------
# 3. Normalizing count data<a name="header3"></a>

There are many reasons why sampling of 16S rDNA may not be consistent across samples. For example,
the amount of material used for genomic DNA extraction may be variable. The exact number of reads
generated by sequencing platforms is also variable between runs. Furthermore, when samples are
multiplexed, technical error during pooling may mean that different volumes of each sample are 
loaded onto the flow cell.
 
{% highlight bash %}
# The total number of sequences for each sample
colSums(df_count)

# Plot a histogram of the number of sequences for each sample
hist(colSums(df_count), breaks=20)

{% endhighlight %}

> Try plotting a histogram of the number of sequences per OTU.

Together, these factors mean that i) the number of sequence reads generated per sample is likely
to be highly variable, and ii) that estimating the exact number of 16S gene sequences in the 
original sample is generally not possible. Estimates of the abundance of different taxa within a
sample are therefore relative, and it is necessary to normalize counts before comparing a single
taxon between samples.

Data normalization (adjusting for differences in sequencing depth) can be performed on the count
matrix once it has been loaded into R. There are several different normalization methods one of 
which is to rarefy (i.e. randomly sample without replacement) data so that an equal number of
sequence counts are present for each sample. Rarefying requires loading an R package called
`metseqR`.

{% highlight R %}
# Load the metaseqR package
library('metaseqR')

# The sample with the smallest number of sequences
min(colSums(df_count))

# Downsample the number of counts so there's an even number across samples.
df_rare <- downsample.counts(df_count, seed=42)
colSums(df_rare)

# It is also possible to convert taxon read counts to proportions.
# First, it's necessary to convert the count data frame to a matrix
m_count <- as.matrix(df_count)
# Use the prop.table() function to fetch proportions
m_prop <- prop.table(m_count, margin=2)
df_count_prop <- as.data.frame(m_prop)
head(df_count_prop)

colSums(df_count_prop)

{% endhighlight %}

For discussion of the issues surrounding rarefying data (including disambiguation of the terms
rarefying and rarefaction) see this [PLoS article][mcmurdie-rarefaction].

<br>
<br>


----------------------------------
# 4. Loading data into phyloseq <a name="header4"></a>
The package `metaseqR` contains functions specifically developed for the analysis of sequence data.
A similar package is `phyloseq`, which has been developed exclusively for 16S analysis. It provides
many convenient functions for data visualization and exploration.

To use `phyloseq` it's necessary to combine our count, taxonomy, and metadata data frames into a 
single `phyloseq` object.

{% highlight R %}
# load the phyloseq package
library('phyloseq')

# First, it's necessary to convert our data frames to matrices
m_count <- as.matrix(df_count)
m_tax <- as.matrix(df_tax)

# Next, it's necessary to convert these data into the format required by phyloseq
OTU <- otu_table(m_count, taxa_are_rows=TRUE)
TAX <- tax_table(m_tax)
# The metadata contains mixed data
MD <- sample_data(df_meta)

# Next, it's necessary to convert these data into the format required by phyloseq
OTU <- otu_table(m_count, taxa_are_rows=TRUE)
TAX <- tax_table(m_tax)
# The metadata contains mixed data
MD <- sample_data(df_meta)

# Generate the phyloseq object
physeq <- phyloseq(OTU, TAX, MD)

# The result is a data structure specifically designed for handling 16S data
class(physeq)
str(physeq)
{% endhighlight %}

For further information on using `phyloseq` have a look at the 
[online documentation][phyloseq-docs].

#### 3.b. Normalizing data within phyloseq<a name="header4b"></a>

In addition to storing data, phyloseq provides convenient functions that allow you to manipulate
in a flexible manner. For example, it is possible to normalize data. We will normalize the count
data so that the columns for each sample sum the median number of counts in the un-normalized
count matrix.

{% highlight R %}

# get the median number of counts per sample
total = median(colSums(df_count))

# create a custom R function to normalize data
myFunction = function(x, t=total) round(t * (x / sum(x)))

# use transform_sample_counts() to apply your custom function to the count data
physeq_norm = transform_sample_counts(physeq, myFunction)

# The sample counts stored within the phyloseq object
colSums(otu_table(physeq_norm))
{% endhighlight %}

> Have a look at other data normalization methods available within the `phyloseq` package.
> For example see the function `normalize.deseq()`

----------------------------------
# 5. Plotting figures<a name="header5"></a>

Phyloseq also provides convenient functions for generating summary plot of your data.<br>
Once your data are contained within a `phyloseq` object, it is easy to genreate sophisticated plots
with relatively little effort.

{% highlight R %}
# phyloseq holds all information within one R object
str(physeq_norm)

# Plotting a stacked bar chart of taxon abundance
plot_bar(physeq, fill="phylum")
plot_bar(physeq_norm, fill="phylum")

# Plotting a heatmap of taxon abundance
plot_heatmap(physeq_norm)
plot_heatmap(physeq_norm, taxa.label='family')
{% endhighlight %}

For further information on plotting with phyloseq try looking at the help documentation for each 
plot function. Additionally, have a look at some of the online
[phyloseq tutorials][phyloseq-tutorials]

> Try plotting a stacked bar chart in which counts are coloured by genus. <br>
> What data transformations are implicitly made when plotting a heatmap?

<br>
<br>

----------------------------------
# 6. Analysis of alpha diversity<a name="header6"></a>

While individual taxa are of interest, many biologically relevant changes in the microbiome (for
example dysbiosis) are reported at the community level. Statistics that summarize changes in
microbiome community composition are therefore of interest.

Alpha diversity metrics represent measurements of microbiome diversity within an individual. For
comparative purposes, it is possible to compare the alpha diversity of individual A with that of
individual B. 

There are multiple different statistical methods for measuring alpha diversity (although, 
see [here][wikipedia-richness] for disambiguation of the terms 'richness' and 'diversity', both
of which are considered measurements of 'alpha diversity'). Phyloseq provides convenient access
to many of these methods.

{% highlight R %}
# Plot multiple measures of alpha diversity with phyloseq
plot_richness(physeq)

# Pass a variable in df_meta as a colour
plot_richness(physeq, color='Condition')

# Plot alpha diversity for normalized dataset
plot_richness(physeq_norm, color='Condition')

# Note, it's also possible to extract the alpha diversity estimates for further analysis
estimate_richness(physeq, measures=c("Chao1", "Shannon"))
{% endhighlight %}

> Which alpha diversity measures alter between the normalized and un-normalized data sets?<br>
> Which data set returns the correct alpha diversity metrics? 



<br>
<br>

----------------------------------
# 7. Analysis of beta diversity<a name="header7"></a>

In contrast to alpha diversity, beta diversity metrics represent measurments of the extent to 
which the microbiome changes across individuals. For a discussion of the differences between
alpha and beta diversity see [Jost 2007][ecology-jost2007].

To plot beta diversity, it is first necessary to generate a metric that summarizes how much
the microbiome varies between every pair of individuals in a study. There are many such measures
of similarity/dissimilarity. (For a more-or-less comprehensive summary see Chapter 7 of
[Legendre & Legendre 2012][elsevier-numericalecology]).

Pairwise comparison of similarity/dissimilarity between all sampels in a study can be used to
generaet resemblance matrices, which can in turn, be used to plot visual summaries of beta
diversity.

{% highlight R %}
# It is possible to generate a distance matrix in phyloseq
dist_norm <- phyloseq::distance(physeq_norm, method='bray')
dist_norm


# Plot beta diversity in phyloseq (DM generated implicitly)
# First it's necessary to perform the ordination
physeq_norm_ord <- ordinate(physeq_norm, method="PCoA", distance="bray")
# Then run the plot function
plot_ordination(physeq_norm, physeq_norm_ord, color="Condition")
{% endhighlight %}

> What does each cell in the distance matrix `dist_norm` represent?<br>
> Try colouring your beta diversity plot by one of the other variables in the medata.<br>

For a summary of all the dissimilarity measures offered by `phyloseq`, try typing 
`?distanceMethodList` into your R console.

<br>
<br>

----------------------------------
# Conclusions<a name="header8"></a>

Reading data into R provides access to a wide variety of R libraries that are written specifically
for the analysis of 16S sequence data. Using packages provides 
[high-level][wikipedia-highlevel] 
access to the power of R as a statistical programming language, thereby dramatically increasing
the ease of analysis. However, this comes at an increased risk of making invalid statistical
assumptions about your data. 

Fortunately, a central tenet of the R language is that it should be robust as well as convenient.
The [BioConductor][bioconductor-home] initiative extends these principles to genomic analysis;
it contains several packages that are useful for microbiome analysis. This session has introduced
[`phyloseq`][bioc-phyloseq]
and [`metaseqR`][bioc-metaseqr], 
but see also [`metagenomeSeq`][bioc-metagenomeseq]
and [`Metagenome`][bioc-metagenome].


[wikipedia-ide]: https://en.wikipedia.org/wiki/Integrated_development_environment
[wikipedia-gui]: https://en.wikipedia.org/wiki/Graphical_user_interface
[rtutor-dataframe]: http://www.r-tutor.com/r-introduction/data-frame
[mcmurdie-rarefaction]: http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003531
[phyloseq-docs]: https://joey711.github.io/phyloseq/
[phyloseq-tutorials]: https://joey711.github.io/phyloseq/tutorials-index.html
[wikipedia-richness]: https://en.wikipedia.org/wiki/Species_richness
[ecology-jost2007]: http://onlinelibrary.wiley.com/doi/10.1890/06-1736.1/abstract
[elsevier-numericalecology]: https://www.elsevier.com/books/numerical-ecology/legendre/978-0-444-53868-0
[wikipedia-highlevel]: https://en.wikipedia.org/wiki/High-level_programming_language
[bioconductor-home]: http://bioconductor.org/
[bioc-phyloseq]: http://bioconductor.org/packages/release/bioc/html/phyloseq.html
[bioc-metaseqr]: http://bioconductor.org/packages/release/bioc/html/metaseqR.html
[bioc-metagenomeseq]: http://bioconductor.org/packages/release/bioc/html/metagenomeSeq.html
[bioc-metagenome]: http://bioconductor.org/packages/release/bioc/html/metagene.html
