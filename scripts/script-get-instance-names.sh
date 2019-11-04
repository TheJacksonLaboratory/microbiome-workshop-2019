#!/bin/bash

aws ec2 describe-instances --query 'Reservations[?Instances[?Tags[?Key==`microbiome-prod`]]].Instances[].InstanceId' --profile microbiome | grep i- \
 | awk '{print $1}' \
 | sed 's/\"//g' \
 | sed 's/,//' #\
#| xargs -L1 -I%  sh -c 'alloc="aws ec2 allocate-address --domain vpc  --output text | awk \'{print $1}\'"; aws ec2 associate-address --instance-id i-0dc972fb678606cbb --allocation-id $alloc --profile microbiome
