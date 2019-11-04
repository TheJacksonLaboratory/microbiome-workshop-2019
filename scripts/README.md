# production
sh create-image.sh i-0748ba10fd728986b "lrs-pacbio-v1-pre-release" "pacbio genomics instance image for testing pre release"
sh create-image.sh i-0748ba10fd728986b "lrs-pacbio-v1beta-practice2" "Pacbio instance image for testing2"
sh create-instances.sh ami-0067ad49c9972ee8e 6 m5a.xlarge lrs-workshop-2019 fritz-workshop
sh script-get-ips.sh 
pandoc -s 2 -o example2.html
python create_table.py users.csv users.md


sh script-get-instance-names.sh > allocate.csv


# Shutdown instances
sh script-get-instance-names.sh  | xargs -L1 -I% aws ec2 stop-instances --instance-ids %

# Start instances
sh script-get-instance-names.sh  | xargs -L1 -I% aws ec2 start-instances --instance-ids %

