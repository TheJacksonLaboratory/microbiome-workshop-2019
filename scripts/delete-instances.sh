#!/bin/bash

aws ec2 describe-instances --query 'Reservations[?Instances[?Tags[?Key==`sv-calling`]]].Instances[].InstanceId' --profile microbiome | grep i- \
 | awk '{print $1}' \
 | sed 's/\"//g' \
 | sed 's/,//' | xargs -L1 -I% aws ec2 terminate-instances --instance-ids % --profile microbiome 
