import pandas as pd
import sys
import os
import re
import shutil
import subprocess

inputs=sys.argv[1]
output=sys.argv[2]
#names=["Username", "IP", "Terminal 1", "Terminal 2", "RStudio", "Jupyter", "Download Files"]
df = pd.read_csv(inputs, sep=",", header=None, names=["Username", "IP"])
df['Terminal 1'] = df["IP"].map(lambda beta_value: "<a href='http://{}:8080' target='_blank'>terminal 1</a>".format(beta_value))
df['Terminal 2'] = df["IP"].map(lambda beta_value: "<a href='http://{}:8080' target='_blank'>terminal 2</a>".format(beta_value))
df['RStudio'] = df["IP"].map(lambda beta_value: "<a href='http://{}:8787' target='_blank'>rstudio</a>".format(beta_value))
df['Jupyter'] = df["IP"].map(lambda beta_value: "<a href='http://{}:8888' target='_blank'>jupyter</a>".format(beta_value))
df['Download Files'] = df["IP"].map(lambda beta_value: "<a href='http://{}' target='_blank'>download files</a>".format(beta_value))

df.to_csv("csv-intermediate-file-csv", index=False, header=["Username", "IP", "Terminal 1", "Terminal 2", "RStudio", "Jupyter", "Download Files"])

def csvtomd(output):
    return subprocess.Popen(
        'csvtomd csv-intermediate-file-csv > {}; rm csv-intermediate-file-csv'.format(output),
         stdout=subprocess.PIPE, shell=True)
csvtomd(output)
