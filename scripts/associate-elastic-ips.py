
import csv
import pandas as pd
import sys
import os
import re
import shutil
import subprocess

f = open('allocate.csv')
csv_f = csv.reader(f)

def associate(instance_name, ip):
    return subprocess.Popen(
        'aws ec2 associate-address  --instance-id {} --allocation-id {} --profile microbiome'.format(instance_name, ip),
         stdout=subprocess.PIPE, shell=True)

for row in csv_f:
  associate(row[0], row[1])
