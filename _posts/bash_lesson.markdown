---
layout: post
title: "Working at the command line with Bash" 
date:   2018-11-06 12:00:00
categories: jekyll update
---

## Session Overview

TEST The purpose of this session is to provide familiarity and comfort with the Unix shell for the purposes of working with the course material. It is not meant to be a comprehensive lesson. For more in-depth instruction of using Bash, the default Unix shell, please see the Software Carpentry lesson, ["The Unix Shell"][sc-url] <br>

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

<br>
<br>
<br>

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

# 4. Variables and wildcards<a name="header4"></a>

variable
${VARNAME}
backticks ` `
date
wildcards *


<br>
<br>
<br>

----------------------------------
# 5. Loops and scripts<a name="header5"></a>

 
\ — continuous character
 
comments #
 
for
do
 
 
execution of program
./

 
<br>
<br>
<br>

----------------------------------
# 6. Miscellaneous<a name="header6"></a>


 
chmod 
which
awk

 
<br>
<br>
<br>


[texteditor-wikipedia]: https://en.wikipedia.org/wiki/Text_editor
[sc-url]: http://swcarpentry.github.io/shell-novice/
[so-url]: https://stackoverflow.com
[google-url]: https://www.google.com

